
# app.py
import gradio as gr
from lms.config import ensure_local_dirs
from lms.storage.local_csv import LocalCSVStorage
from lms.services.submissions import SubmissionService
from lms.ui.listening import listening_tab
from lms.ui.speaking import speaking_tab
from lms.ui.reading import reading_tab
from lms.ui.writing import writing_tab
from lms.ui.admin import admin_tab
from lms.ui.video import video_tab  # ← new

def build_app():
    ensure_local_dirs()

    storage = LocalCSVStorage()
    service = SubmissionService(storage)

    with gr.Blocks(title="Mini LMS (Local)") as demo:
        gr.Markdown("# Mini LMS – Listening / Speaking / Reading / Writing / Video")
        gr.Markdown("**Local demo:** data saved to CSV; mic audio to `data/audio/`; video in `samples/`.")

        user_box = gr.Textbox(label="User name", placeholder="e.g., tri.nguyen", value="demo_user")

        with gr.Tabs():
            listening_tab(service, user_box)
            speaking_tab(service, user_box)
            reading_tab(service, user_box)
            writing_tab(service, user_box)
            video_tab(service, user_box)   # ← interactive video
            admin_tab(service)

    return demo

if __name__ == "__main__":
    app = build_app()
    app.launch()
