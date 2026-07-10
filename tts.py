# tts.py
import threading
import pyttsx3
import win32com.client
import pythoncom
from config import TTS_RATE, TTS_VOLUME

class TTS:
    def __init__(self):
        self.engine = None
        self._lock = threading.Lock()
        self._init_engine()

    def _init_engine(self):
        try:
            if self.engine is not None:
                self.engine.stop()
            self.engine = pyttsx3.init("sapi5")
        except Exception:
            try:
                if self.engine is not None:
                    self.engine.stop()
                self.engine = pyttsx3.init()
            except Exception as e:
                print(f"[TTS] Could not initialize speech engine: {e}")
                self.engine = None
                return

        self.engine.setProperty("rate", TTS_RATE)
        self.engine.setProperty("volume", TTS_VOLUME)

        voices = self.engine.getProperty("voices") or []
        preferred = ["zira", "david", "english", "us"]
        selected_voice = None

        for voice in voices:
            name = voice.name.lower()
            if any(token in name for token in preferred):
                selected_voice = voice.id
                break

        if selected_voice:
            self.engine.setProperty("voice", selected_voice)
        elif voices:
            self.engine.setProperty("voice", voices[0].id)

    def speak(self, text: str):
        """Speak text out loud, blocking until done."""
        if not text:
            return

        with self._lock:
            print(f"[TTS] {text}")
            try:
                self._init_engine()
            except Exception as e:
                print(f"[TTS] Reinitialize error: {e}")
                return

            try:
                if self.engine is not None:
                    self.engine.say(text)
                    self.engine.runAndWait()
                else:
                    pythoncom.CoInitialize()
                    voice = win32com.client.Dispatch("SAPI.SpVoice")
                    voice.Speak(text)
                    pythoncom.CoUninitialize()
            except Exception as e:
                print(f"[TTS] Speech error: {e}")

    def speak_async(self, text: str):
        """Speak without blocking the main thread."""
        t = threading.Thread(target=self.speak, args=(text,), daemon=True)
        t.start()

        # Add this method to the TTS class
def shutdown(self):
    """Cleanly stop the TTS engine."""
    try:
        self.engine.stop()
    except:
        pass