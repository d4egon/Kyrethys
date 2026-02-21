import subprocess
import time

def speak_dream(rolls, vision, dream_text):
    print("\n[TTS] Initializing Windows Speech Engine...")
    
    # 1. Prepare the narration layers
    intro = f"New session initiated. The dice have fallen: {str(rolls)}."
    anchor = f"The anchor of this reality is: {vision}."
    body = f"Listen to the vision. {dream_text}"
    
    full_narration = f"{intro} {anchor} {body}"
    
    # 2. Console Feedback (So you can follow along)
    print(f"[TTS] Narrating Rolls: {str(rolls)}")
    print(f"[TTS] Narrating Anchor: {vision}")
    print(f"[TTS] Narrating Dream Body ({len(dream_text)} characters)...")

    # Clean up for PowerShell (important to avoid syntax errors)
    clean_text = full_narration.replace('"', "'").replace('\n', ' ').strip()

    # 3. The Execution
    # We use a slight delay to let the user prepare their ears
    time.sleep(1) 
    
    print("[SYSTEM] Voice active. Silence for playback...")
    
    # Windows PowerShell TTS Command
    cmd = f'PowerShell -Command "Add-Type –AssemblyName System.Speech; ' \
          f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; ' \
          f'$speak.Rate = -1; ' \
          f'$speak.Speak(\\"{clean_text}\\")"'
    
    try:
        # shell=True is used here to ensure the PowerShell environment is loaded
        subprocess.run(cmd, shell=True, check=True)
        print("[SUCCESS] Narration complete.")
    except Exception as e:
        print(f"[ERROR] TTS failed: {e}")