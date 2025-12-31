
# lms/ui/listening.py
import gradio as gr
from lms.services.submissions import SubmissionService

def listening_tab(service: SubmissionService, user_box: gr.Textbox):
    with gr.Tab("Listening"):
        gr.Markdown("## Listening: play audio & answer MCQ")
        audio_path = service.sample_audio_path()
        if audio_path:
            gr.Audio(value=audio_path, label="Audio L1", interactive=False)
        else:
            gr.Markdown("⚠️ Put a sample file at `samples/audio_l1.mp3` to enable audio playback.")

        gr.Markdown("**Question L1-Q1 (demo):** Choose the correct answer.")
        choice = gr.Radio(choices=["A", "B", "C", "D"], label="Select an option")
        submit = gr.Button("Submit L1-Q1")
        out = gr.Markdown()

        submit.click(
            fn=lambda u, c: service.submit_mcq(u, "L1-Q1", c),
            inputs=[user_box, choice],
            outputs=out
        )