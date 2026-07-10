# mic_test.py
import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 16000
CHUNK_SIZE  = 1280

print("=" * 40)
print("MIC CALIBRATION TEST")
print("=" * 40)
print("\nPhase 1: Stay SILENT for 5 seconds...")
print("(measuring your background noise level)")

silence_levels = []

def callback(indata, frames, time_info, status):
    chunk = np.frombuffer(indata, dtype=np.int16)
    silence_levels.append(np.abs(chunk).mean())

with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=CHUNK_SIZE,
                       dtype="int16", channels=1, callback=callback):
    time.sleep(5)

ambient = np.mean(silence_levels)
print(f"\n  Ambient noise level: {ambient:.0f}")

print("\nPhase 2: SPEAK NORMALLY for 5 seconds...")
print("(say anything out loud)")

speech_levels = []

with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=CHUNK_SIZE,
                       dtype="int16", channels=1, callback=callback):
    time.sleep(5)

speech = np.mean(silence_levels[-50:])
recommended = int(ambient * 2.5)

print(f"\n  Speech level:        {speech:.0f}")
print(f"  Ambient level:       {ambient:.0f}")
print(f"\n  RECOMMENDED NOISE_THRESHOLD = {recommended}")
print(f"\n  Set this in config.py:")
print(f"  NOISE_THRESHOLD = {recommended}")