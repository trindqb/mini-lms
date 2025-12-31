
# Mini-LMS (Local, Modular, No Login)

A minimal LMS demo with Gradio: Listening (audio + MCQ), Speaking (mic recording), Reading (short answer), Writing (essay), and Admin (view/export).  
Local-first storage (CSV), modular design ready to swap with other backends (e.g., Firebase).

## Run locally
1. `python -m venv .venv && source .venv/bin/activate` (or `.\.venv\Scripts\activate` on Windows)
2. `pip install -r requirements.txt`
3. Put a sample audio at `samples/audio_l1.mp3` (mp3 or wav)
4. `python app.py`

## Data
- Submissions saved to `data/submissions_local.csv`
- Speaking audio copied to `data/audio/`

## Extend
- Replace `LocalCSVStorage` with another implementation (e.g., `FirebaseStorage`) without changing UI code.
- Add more MCQs by extending `answer_key` in `SubmissionService` or loading from JSON.
- Add rubrics or auto-grading by introducing new methods in `SubmissionService`.
