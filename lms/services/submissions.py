
# lms/services/submissions.py
import os
import shutil
from datetime import datetime
from typing import Optional
import pandas as pd
from lms.storage.base import StorageBackend
from lms.config import AUDIO_DIR, SAMPLES_DIR

class SubmissionService:
    def __init__(self, backend: StorageBackend):
        self.backend = backend
        # Simple answer key demo; you can load from JSON later
        self.answer_key = {
            "L1-Q1": "B",
            "L2-Q1": "D",
        }

        self.video_markers = {
            "V1": [
                {"id": "V1-M30", "time": 30, "type": "mcq", "prompt": "What is the main idea?", "choices": ["A","B","C","D"], "correct": "C"},
                {"id": "V1-M70", "time": 70, "type": "short", "prompt": "Summarize in one sentence:", "min_words": 5},
            ]
        }
    
    @staticmethod
    def now_ts_str():
        return datetime.utcnow().isoformat()

    @staticmethod
    def now_ts_int():
        return int(datetime.utcnow().timestamp())

    # Listening MCQ
    def submit_mcq(self, user: str, item_id: str, choice: Optional[str]) -> str:
        if not user.strip():
            return "Please enter a user name."
        if choice is None:
            return "Please select an option."

        correct = self.answer_key.get(item_id, "")
        score = 1 if choice == correct else 0

        row = {
            "ts": self.now_ts_str(),
            "user": user,
            "section": "listening_mcq",
            "item_id": item_id,
            "text": "",
            "mcq_score": score,
            "audio_path": "",
            "choice": choice
        }
        self.backend.save_mcq(row)
        return f"Saved. Score: {score}/1"

    # Reading short answer
    def submit_reading(self, user: str, item_id: str, text: str) -> str:
        if not user.strip():
            return "Please enter a user name."
        if not text.strip():
            return "Answer cannot be empty."

        row = {
            "ts": self.now_ts_str(),
            "user": user,
            "section": "reading",
            "item_id": item_id,
            "text": text.strip(),
            "mcq_score": "",
            "audio_path": "",
            "choice": ""
        }
        self.backend.save_text(row)
        return "Saved reading answer."

    # Writing essay
    def submit_writing(self, user: str, item_id: str, text: str) -> str:
        if not user.strip():
            return "Please enter a user name."
        if not text.strip():
            return "Essay cannot be empty."

        row = {
            "ts": self.now_ts_str(),
            "user": user,
            "section": "writing",
            "item_id": item_id,
            "text": text.strip(),
            "mcq_score": "",
            "audio_path": "",
            "choice": ""
        }
        self.backend.save_text(row)
        return "Saved essay."

    # Speaking audio (mic capture → filepath)
    def submit_speaking(self, user: str, item_id: str, audio_filepath: Optional[str]) -> str:
        if not user.strip():
            return "Please enter a user name."
        if audio_filepath is None:
            return "No recorded audio."

        ts_int = self.now_ts_int()
        fname = f"{user}_speaking_{item_id}_{ts_int}.wav"
        os.makedirs(AUDIO_DIR, exist_ok=True)
        target = os.path.join(AUDIO_DIR, fname)
        shutil.copy(audio_filepath, target)

        row = {
            "ts": self.now_ts_str(),
            "user": user,
            "section": "speaking",
            "item_id": item_id,
            "text": "",
            "mcq_score": "",
            "audio_path": target,
            "choice": ""
        }
        self.backend.save_audio(row)
        return f"Saved audio: `{target}`"

    # Admin helpers
    def fetch_table(self, limit: int = 50):
        df = self.backend.fetch_recent(limit=limit)
        if df.empty:
            return df, "No submissions yet."
        return df, f"Loaded {len(df)} rows."

    def export_csv(self):
        df = self.backend.export_all()
        out_path = os.path.join(os.getcwd(), f"submissions_export_{self.now_ts_int()}.csv")
        df.to_csv(out_path, index=False)
        return out_path

    # Utility for sample audio path
    @staticmethod
    def sample_audio_path():
        p = os.path.join(SAMPLES_DIR, "audio_l1.mp3")
        return p if os.path.exists(p) else None



# ---------- Video helper ----------
    @staticmethod
    def sample_video_path():
        p = os.path.join(SAMPLES_DIR, "video_l1.mp4")
        return p if os.path.exists(p) else None

    def get_video_markers(self, video_id: str):
        return self.video_markers.get(video_id, [])

    # Save video quiz interactions
    def submit_video_quiz_mcq(self, user: str, video_id: str, marker_id: str, choice: Optional[str]) -> str:
        if not user.strip():
            return "Please enter a user name."
        if choice is None:
            return "Please select an option."
        # find correct
        correct = None
        for m in self.get_video_markers(video_id):
            if m["id"] == marker_id and m["type"] == "mcq":
                correct = m.get("correct")
                break
        score = 1 if choice == correct else 0

        row = {
            "ts": self.now_ts_str(),
            "user": user,
            "section": "video_quiz",
            "item_id": marker_id,
            "text": "",
            "mcq_score": score,
            "audio_path": "",
            "choice": choice
        }
        self.backend.save_mcq(row)
        return f"Saved. Score: {score}/1"

    def submit_video_quiz_short(self, user: str, video_id: str, marker_id: str, text: str) -> str:
        if not user.strip():
            return "Please enter a user name."
        if not text.strip():
            return "Answer cannot be empty."
        row = {
            "ts": self.now_ts_str(),
            "user": user,
            "section": "video_quiz",
            "item_id": marker_id,
            "text": text.strip(),
            "mcq_score": "",
            "audio_path": "",
            "choice": ""
        }
        self.backend.save_text(row)
        return "Saved short answer."

    # Notes and bookmarks
    def save_video_note(self, user: str, video_id: str, note: str) -> str:
        if not user.strip():
            return "Please enter a user name."
        if not note.strip():
            return "Note cannot be empty."
        row = {
            "ts": self.now_ts_str(),
            "user": user,
            "section": "video_note",
            "item_id": video_id,
            "text": note.strip(),
            "mcq_score": "",
            "audio_path": "",
            "choice": ""
        }
        self.backend.save_text(row)
        return "Saved note."

    def save_video_bookmark(self, user: str, video_id: str, time_sec: float, note: str) -> str:
        if not user.strip():
            return "Please enter a user name."
        row = {
            "ts": self.now_ts_str(),
            "user": user,
            "section": "video_bookmark",
            "item_id": video_id,
            "text": f"{time_sec:.2f}s | {note.strip()}",
            "mcq_score": "",
            "audio_path": "",
            "choice": ""
        }
        self.backend.save_text(row)
        return f"Saved bookmark at {time_sec:.2f}s."

    # Progress tracking (resume)
    def save_video_progress(self, user: str, video_id: str, current_time: float, duration: float) -> str:
        if not user.strip():
            return "Please enter a user name."
        pct = (current_time / duration * 100.0) if duration > 0 else 0.0
        row = {
            "ts": self.now_ts_str(),
            "user": user,
            "section": "video_progress",
            "item_id": video_id,
            "text": f"time={current_time:.2f};duration={duration:.2f};pct={pct:.2f}",
            "mcq_score": "",
            "audio_path": "",
            "choice": ""
        }
        self.backend.save_text(row)
        return f"Progress saved at {current_time:.2f}s ({pct:.1f}%)."

    def get_last_progress(self, user: str, video_id: str) -> float:
        """Return last known time (seconds) from storage; 0 if none."""
        df = self.backend.export_all()
        if df.empty:
            return 0.0
        df = df[(df["user"] == user) & (df["section"] == "video_progress") & (df["item_id"] == video_id)]
        if df.empty:
            return 0.0
        # pick latest by ts
        df = df.sort_values("ts", ascending=False)
        text = str(df.iloc[0]["text"])
        # text like: time=12.34;duration=89.0;pct=14.0
        try:
            parts = dict([kv.split("=") for kv in text.split(";")])
            return float(parts.get("time", "0"))
        except Exception:
            return 0.0