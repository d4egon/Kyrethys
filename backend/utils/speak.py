import asyncio
import edge_tts
import os
import time
import threading
import queue
from pygame import mixer

# 1. Initialize once and KEEP OPEN
mixer.init()
speech_queue = queue.Queue()

def speech_worker():
    """Background thread that processes sentences one by one."""
    while True:
        text = speech_queue.get()
        if text is None: break # Shutdown signal
        
        try:
            # Create a new event loop for this thread to handle the async TTS
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_execute_speak(text))
            loop.close()
        except Exception as e:
            print(f"Speech Worker Error: {e}")
        
        speech_queue.task_done()

async def _execute_speak(text):
    voice = "en-US-GuyNeural"
    # Unique filename per chunk to prevent 'File in use' errors
    temp_file = f"speech_{int(time.time()*1000)}.mp3"
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_file)
        
        mixer.music.load(temp_file)
        mixer.music.play()
        
        # Wait for the audio to finish
        while mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
        mixer.music.unload() # Unlock the file
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except: pass # Ignore if file is briefly locked
            
    except Exception as e:
        print(f"TTS Execution Error: {e}")

# 2. Start the background thread immediately on import
threading.Thread(target=speech_worker, daemon=True).start()

def speak(text):
    """The main entry point called by your API."""
    if not text or not text.strip():
        return
    
    print(f"Queuing for vocalization: {text[:50]}...")
    speech_queue.put(text)