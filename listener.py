# listener.py
import os
import warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore")

import sounddevice as sd
import numpy as np
import queue
from faster_whisper import WhisperModel
from config import (
    SAMPLE_RATE,
    CHUNK_SIZE,
    COMMAND_SILENCE_TIMEOUT,
    WHISPER_MODEL_SIZE,
    NOISE_THRESHOLD,
)

class SpeechListener:

    def __init__(self):
        print("[STT] Loading faster-whisper model...")
        try:
            self.model = WhisperModel(
                WHISPER_MODEL_SIZE,
                device="cpu",
                compute_type="int8",
                download_root="./models/whisper",
                num_workers=1,
            )
            print(f"[STT] faster-whisper ready.")
        except Exception as e:
            print(f"[STT] CRITICAL: {e}")
            raise SystemExit(1)
        self._audio_queue = queue.Queue()

    def _has_speech(self, chunk):
        return np.abs(chunk).mean() > NOISE_THRESHOLD

    def _record_until_silence(self):
        speech_chunks = []
        silence_count = 0
        speech_detected = False
        silence_limit = int((SAMPLE_RATE / CHUNK_SIZE) * COMMAND_SILENCE_TIMEOUT)
        max_chunks = int((SAMPLE_RATE / CHUNK_SIZE) * 15)
        total_chunks = 0

        def audio_callback(indata, frames, time_info, status):
            self._audio_queue.put(
                np.frombuffer(indata, dtype=np.int16).copy()
            )

        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=CHUNK_SIZE,
            dtype="int16",
            channels=1,
            callback=audio_callback
        ):
            while True:
                try:
                    chunk = self._audio_queue.get(timeout=3.0)
                except queue.Empty:
                    print("[STT] Mic timeout.")
                    break
                total_chunks += 1
                if self._has_speech(chunk):
                    speech_detected = True
                    silence_count = 0
                    speech_chunks.append(chunk)
                else:
                    silence_count += 1
                    if speech_detected:
                        speech_chunks.append(chunk)
                if speech_detected and silence_count >= silence_limit:
                    print("[STT] End of speech detected.")
                    break
                if total_chunks >= max_chunks:
                    if not speech_detected:
                        print("[STT] No speech detected.")
                    break

        while not self._audio_queue.empty():
            try:
                self._audio_queue.get_nowait()
            except queue.Empty:
                break

        if not speech_chunks:
            return np.array([], dtype=np.float32)

        combined = np.concatenate(speech_chunks).astype(np.float32) / 32768.0
        print(f"[STT] Recorded {len(combined)/SAMPLE_RATE:.1f}s of audio.")
        return combined

    def listen_for_command(self):
        print("[STT] Listening for command...")
        try:
            audio = self._record_until_silence()

            if len(audio) == 0:
                return ""

            if len(audio) < int(SAMPLE_RATE * 0.3):
                print("[STT] Too short.")
                return ""

            print(f"[STT] Transcribing {len(audio)/SAMPLE_RATE:.1f}s...")

            segments, info = self.model.transcribe(
                audio,
                language="en",
                beam_size=5,
                best_of=5,
                temperature=0.0,
                condition_on_previous_text=False,
                vad_filter=True,
                vad_parameters=dict(
                    threshold=0.3,
                    min_speech_duration_ms=200,
                    min_silence_duration_ms=300,
                    speech_pad_ms=300,
                ),
                word_timestamps=False,
            )

            hallucinations = {
                "thank you", "thanks for watching", "you", ".",
                "...", "the", "bye", "goodbye", "a", "i", "oh",
                "um", "uh", "hmm", "us to be in these.",
                "us to be in these", "in the", "subscribe",
                "subtitles by", "transcribed by",
            }

            valid_single = {
                "yes", "no", "ok", "okay", "copy", "paste",
                "undo", "redo", "back", "stop", "cancel",
                "mute", "save", "quit", "exit", "scroll",
            }

            parts = []
            for seg in segments:
                text = seg.text.strip()
                if not text:
                    continue
                if text.lower() in hallucinations:
                    print(f"[STT] Filtered: {text}")
                    continue
                if len(text.split()) == 1 and text.lower() not in valid_single:
                    print(f"[STT] Filtered short: {text}")
                    continue
                parts.append(text)

            transcript = " ".join(parts).strip()

            if transcript:
                print(f"[STT] Heard: {transcript}")
            else:
                print("[STT] Nothing valid.")

            return transcript

        except sd.PortAudioError as e:
            print(f"[STT] Mic error: {e}")
            return ""
        except Exception as e:
            print(f"[STT] Error: {e}")
            return ""
