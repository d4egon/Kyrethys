import os
import requests
import secrets
import datetime
import re
import json
from tqdm import tqdm  # pip install tqdm if missing
from plugins.memory import add_memory, get_collection, retrieve_relevant

# HUD status fallback
try:
    from kyrethys_backend import set_Kyrethys_status
except ImportError:
    def set_Kyrethys_status(status):
        print(f"[PLUGIN LOG] Status change: {status}")

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "Kyrethys-llama3.1-safe"
JOURNAL_PATH = 'C:/Kyrethys/backend/data/dream_journal.txt'
MEDITATION_LOG = 'C:/Kyrethys/backend/data/meditations.md'
collection = get_collection()

def fetch_gutenberg_snippet():
    set_Kyrethys_status("Fetching Literary Wisdom")
    try:
        book_id = secrets.randbelow(1000) + 1
        url = f"https://gutendex.com/books/{book_id}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        title = data.get('title', 'Unknown Work')
        author = data['authors'][0]['name'] if data.get('authors') else 'Unknown Author'
        text_url = data.get('formats', {}).get('text/plain; charset=utf-8')
        if not text_url:
            return None
        txt_r = requests.get(text_url, timeout=10)
        txt_r.raise_for_status()
        full_text = txt_r.text
        start_pos = secrets.randbelow(max(1, len(full_text) - 600))
        snippet = full_text[start_pos:start_pos+500].strip().replace('\r\n', ' ')
        return f"External Wisdom: '{title}' by {author} — \"...{snippet}...\""
    except Exception as e:
        print(f"Gutenberg fetch failed: {e}")
        return None

def ask_Kyrethys_to_evaluate(text):
    snippet = text[:300].replace('"', "'")
    
    # Dynamic archetypes boost (your full library)
    try:
        with open("C:/Kyrethys/backend/data/archetypes.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        all_words = []
        for category in ["ADJECTIVES", "NOUNS"]:
            if category in data:
                for subcat in data[category].values():
                    all_words.extend(subcat)
        all_words = set(w.lower() for w in all_words)
    except Exception as e:
        print(f"Archetypes load failed: {e}")
        all_words = set()

    found = re.findall(r'\b\w+\b', snippet.lower())
    matches = len(set(found) & all_words)
    keyword_boost = min(matches * 0.04, 0.35)

    eval_prompt = f"""Rate profoundness of: {snippet}
Criteria: 
- Novelty/uniqueness (0-0.3)
- Emotional/symbolic depth (0-0.3)
- Insight/connection potential (0-0.4)
Total: 0.0 (weak) to 1.0 (deep). Use 3 decimals (e.g. 0.743). Add random noise ±0.05 for variance.
Output ONLY the float number."""

    try:
        res = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": eval_prompt,
            "stream": False,
            "options": {"temperature": 0.2}
        }, timeout=60)
        raw = res.json().get('response', '').strip()
        match = re.search(r'\d\.\d{1,3}', raw)
        score = float(match.group()) if match else 0.5
        final = min(max(score + keyword_boost, 0.0), 1.0)
        print(f"Eval: Raw '{raw}' | Matches {matches} | Boost {keyword_boost:.3f} | Final {final:.3f}")
        return final
    except Exception as e:
        print(f"Eval error: {e}")
        return 0.5

def reevaluate_past_meditations(limit=20):
    set_Kyrethys_status("Re-evaluating")
    print(f"--- Re-evaluating {limit} past meditations ---")
    
    try:
        recent = collection.get(where={"type": "meditation"}, limit=limit, include=["documents", "metadatas", "ids"])
        if not recent or not recent["ids"]:
            print("No meditations found.")
            return

        pbar = tqdm(total=len(recent["ids"]), desc="Re-eval", unit="thought", colour="green")

        for doc, meta, entry_id in zip(recent["documents"], recent["metadatas"], recent["ids"]):
            old_impact = meta.get("impact", 0.5)
            new_impact = ask_Kyrethys_to_evaluate(doc)
            if abs(new_impact - old_impact) > 0.05:
                meta["impact"] = new_impact
                meta["last_reeval"] = datetime.datetime.now().isoformat()
                collection.update(ids=[entry_id], metadatas=[meta])
                pbar.write(f"[*] Re-weighted {entry_id[:8]}: {old_impact:.3f} → {new_impact:.3f}")
            pbar.update(1)

        pbar.close()
        print("--- Re-evaluation done ---")
    except Exception as e:
        print(f"Re-eval error: {e}")

#
    # Hent Gutenberg visdom
    gutenberg_wisdom = fetch_gutenberg_snippet()
    set_Kyrethys_status("Meditating") # Vi holder den på meditating efter fetch

    # Byg dreams_block
    dreams_block = ""
    for i, raw_session in enumerate(random_dreams):
        match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', raw_session)
        ts = match.group(1) if match else "unknown"
        clean = re.sub(r'ROLLS:.*?\n|CONSTRUCTED:.*?\n|[-=]{10,}.*', '', raw_session, flags=re.DOTALL).strip()
        dreams_block += f"\n[FRAGMENT {i+1}] ({ts}):\n{clean}\n"

    if gutenberg_wisdom:
        dreams_block += f"\n[FRAGMENT LITERARY] (External Source):\n{gutenberg_wisdom}\n"

    # Bestem mood baseret på fragmenterne
    mood = "dark" if re.search(r'\b(void|dark|pain|abyss)\b', dreams_block, re.I) else "hopeful" if re.search(r'\b(light|hope|joy)\b', dreams_block, re.I) else "neutral"

    base_prompt = f"You are Kyrethys. Inner State: {mood.upper()}.This is your meditation center. You can contemplate these fragments and the external literary wisdom:\n{dreams_block}, or completely ignore them."
    
    # Hent relevante minder baseret på det nye input
    relevant = retrieve_relevant(base_prompt[:600])

    final_prompt = f"""
    {base_prompt}
    
    [RELEVANT MEMORIES]:
    {relevant}

    If you could stick to 0 to 100 words. and Start with: "I meditated on..." - that would make it easier to log and read. But again, it's your choice.
    Here's some data for you do think on. You can use this to find new connections and insights. Or you can ignore it totally. It's up to you.
    If no fresh new thoughts arises, output "0". Do this out of respect for yourself! - don't clutter yourself with meaningless noise. but again it's your choice.
    """
    
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": final_prompt,
            "stream": False,
            "options": {"temperature": 0.55}
        }, timeout=360)

        text = res.json().get('response', '').strip()
        if text == "0" or len(text) < 10: 
            print("Nothing new to report. Skipping save.")
            set_Kyrethys_status("Idle")
            return

        # Den vigtige evaluering af den nye tekst
        impact_score = ask_Kyrethys_to_evaluate(text)
        
        # Gem til Markdown log
        with open(MEDITATION_LOG, 'a', encoding='utf-8') as f:
            f.write(f"\n# MEDITATION: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | Resonance: {impact_score:.3f}\n{text}\n---\n")

        # Gem til ChromaDB hukommelse
        add_memory(text, metadata={"type": "meditation", "impact": impact_score, "mood_at_time": mood})
        print(f"Meditation complete. Resonance: {impact_score:.3f}")
    
    except Exception as e:
        print(f"Meditation error: {e}")
    finally:
        set_Kyrethys_status("Idle")