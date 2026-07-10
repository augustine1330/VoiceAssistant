# debug_mic.py
import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 16000
CHUNK_SIZE  = 1280

print("Monitoring mic levels for 10 seconds...")
print("Stay silent for 3s, then speak, then go silent again")
print("-" * 40)

levels = []

def callback(indata, frames, time_info, status):
    chunk  = np.frombuffer(indata, dtype=np.int16)
    energy = np.abs(chunk).mean()
    levels.append(energy)
    bar    = "█" * int(energy / 2)
    label  = "SPEECH" if energy > 15 else "silence"
    print(f"  Energy: {energy:6.1f}  {label:8s}  {bar[:40]}")

with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=CHUNK_SIZE,
                       dtype="int16", channels=1, callback=callback):
    time.sleep(10)

print("-" * 40)
print(f"Min: {min(levels):.1f} | Max: {max(levels):.1f} | Mean: {np.mean(levels):.1f}")