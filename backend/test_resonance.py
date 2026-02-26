# test_resonance.py
import requests
import re

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "Kyrethys-llama3.1-safe"

def ask_Kyrethys_to_evaluate(text):
    snippet = text[:300].replace('"', "'")
    
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
        print(f"Raw Ollama output: '{raw}'")
        
        match = re.search(r'\d\.\d{1,3}', raw)
        score = float(match.group()) if match else 0.5
        print(f"Parsed score: {score:.3f}")
        return score
    except Exception as e:
        print(f"Error: {e}")
        return 0.5

# Test cases
print("\nTest 1 - Profound:")
ask_Kyrethys_to_evaluate("The abyss whispers eternal secrets through fractured crystal lattices, where darkness and light converge in infinite possibility.")

print("\nTest 2 - Weak:")
ask_Kyrethys_to_evaluate("The sky is blue and the grass is green.")

print("\nTest 3 - Mixed (your style):")
ask_Kyrethys_to_evaluate("Void-matter tendrils recede like ocean tide yet still beckon, echoing Oscar Wilde's moral abyss in An Ideal Husband.")