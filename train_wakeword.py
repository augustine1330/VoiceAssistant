# train_wakeword.py
"""
Trains a custom wake word model for a target phrase such as 'kofi'.
Uses synthetic speech samples — no microphone recording needed.
"""

import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import scipy.special as sp

if not hasattr(sp, "sph_harm"):
    try:
        sp.sph_harm = sp.sph_harm_y
    except Exception:
        pass

TARGET_PHRASE = "kofi"
OUTPUT_DIR = Path("./models/custom")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

config_path = OUTPUT_DIR / "train_config.yaml"
config_path.write_text(textwrap.dedent(f"""
model_name: {TARGET_PHRASE.replace(' ', '_')}
target_phrase: [{TARGET_PHRASE}]
output_dir: {str(OUTPUT_DIR.resolve())}

n_samples: 5000
n_samples_val: 500
augmentation_rounds: 1
augmentation_batch_size: 16
tts_batch_size: 4

piper_sample_generator_path: ./piper
custom_negative_phrases: []

rir_paths:
  - ./models/rir
background_paths:
  - ./models/backgrounds
background_paths_duplication_rate:
  - 1
"""))

print(f"Training config written to {config_path}")
print("Running openWakeWord training pipeline...")

cmd = [
    sys.executable,
    "-m",
    "openwakeword.train",
    "--training_config",
    str(config_path),
    "--generate_clips",
    "--augment_clips",
    "--train_model",
    "--convert_to_tflite",
]

env = os.environ.copy()
env.setdefault("PYTHONPATH", os.getcwd())
result = subprocess.run(cmd, cwd=Path(__file__).resolve().parent, env=env)
if result.returncode != 0:
    raise SystemExit(result.returncode)

print(f"✅ Training finished. Check {OUTPUT_DIR} for the generated model files.")