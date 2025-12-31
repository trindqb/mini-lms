
# lms/config.py
import os
import pandas as pd

DATA_DIR = "data"
AUDIO_DIR = os.path.join(DATA_DIR, "audio")
CSV_LOCAL = os.path.join(DATA_DIR, "submissions_local.csv")
SAMPLES_DIR = "samples"

def ensure_local_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(SAMPLES_DIR, exist_ok=True)
    if not os.path.exists(CSV_LOCAL):
        pd.DataFrame(columns=[
            "ts","user","section","item_id","text","mcq_score","audio_path","choice"
        ]).to_csv(CSV_LOCAL, index=False)