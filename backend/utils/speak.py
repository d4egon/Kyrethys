import pyttsx3
import threading

engine = pyttsx3.init()
engine_busy = False

# Try to set Danish voice
voices = engine.getProperty('voices')
for voice in voices:
    if "Danish" in voice.name or "Dansk" in voice.name:
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    def speak_thread():
        global engine_busy
        if engine_busy or not text.strip():
            return
        engine_busy = True
        try:
            print(f"Marvix taler: {text[:60]}...")
            engine.say(text)
            engine.runAndWait()
            print("Speak færdig.")
        except Exception as e:
            print(f"TTS fejl: {e}")
        finally:
            engine_busy = False

    threading.Thread(target=speak_thread, daemon=True).start()