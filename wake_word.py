# wake_word.py
import threading
import time
import numpy as np
import sounddevice as sd
from openwakeword.model import Model
from config import (
    WAKE_WORD_NAME,
    WAKE_WORD_MODEL_PATH,
    WAKE_WORD_THRESHOLD,
    WAKE_WORD_COOLDOWN,
    SAMPLE_RATE,
    CHUNK_SIZE,
)

class WakeWordDetector:
    def __init__(self, on_detected):
        self.on_detected = on_detected
        self._running = False
        self._thread = None
        self._last_triggered = 0       # cooldown tracker

        print("[WakeWord] Loading openWakeWord model...")

        if WAKE_WORD_MODEL_PATH:
            # Custom .tflite or .onnx model file
            self.model = Model(
                wakeword_models=[WAKE_WORD_MODEL_PATH],
                inference_framework="onnx"          # or "tflite"
            )
            # The key in predictions dict will be the filename without extension
            import os
            self._model_key = os.path.splitext(
                os.path.basename(WAKE_WORD_MODEL_PATH)
            )[0]
        else:
            # Built-in model (hey_jarvis, alexa, hey_mycroft, hey_rhasspy)
            self.model = Model(
                wakeword_models=[WAKE_WORD_NAME],
                inference_framework="onnx"
            )
            self._model_key = WAKE_WORD_NAME

        print(f"[WakeWord] Model loaded: '{self._model_key}'")
        print(f"[WakeWord] Threshold: {WAKE_WORD_THRESHOLD} | Cooldown: {WAKE_WORD_COOLDOWN}s")

    def start(self):
        """Start the always-on background listener thread."""
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        print(f"[WakeWord] Listening for '{self._model_key}' in background...")

    def stop(self):
        self._running = False

    def _listen_loop(self):
        """
        Continuously reads mic audio in CHUNK_SIZE frames,
        feeds into openWakeWord, checks prediction score.
        """
        def audio_callback(indata, frames, time_info, status):
            if not self._running:
                return

            # Convert raw audio to float32 numpy array
            audio_chunk = np.frombuffer(indata, dtype=np.int16).astype(np.float32)

            # Run inference
            predictions = self.model.predict(audio_chunk)

            # Get score for our wake word
            score = predictions.get(self._model_key, 0.0)

            if score >= WAKE_WORD_THRESHOLD:
                now = time.time()
                # Cooldown: don't re-trigger within N seconds
                if now - self._last_triggered >= WAKE_WORD_COOLDOWN:
                    self._last_triggered = now
                    print(f"[WakeWord] ✅ Detected! Score: {score:.3f}")
                    # Fire callback in a separate thread so audio stream isn't blocked
                    threading.Thread(
                        target=self.on_detected,
                        daemon=True
                    ).start()

        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=CHUNK_SIZE,
            dtype="int16",
            channels=1,
            callback=audio_callback
        ):
            while self._running:
                time.sleep(0.1)     # keep thread alive; audio handled by callback

    def cleanup(self):
        """Gracefully stop the listener."""
        print("[WakeWord] Stopping...")
        self.stop()
        if self._thread:
            self._thread.join(timeout=2)
        print("[WakeWord] Stopped.")