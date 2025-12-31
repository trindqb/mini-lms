
# lms/ui/reading.py
import gradio as gr
from lms.services.submissions import SubmissionService

def reading_tab(service: SubmissionService, user_box: gr.Textbox):
    with gr.Tab("Reading"):
        gr.Markdown("## Reading: read the passage and answer briefly")
        gr.Markdown("**R1 (demo passage):** Lorem ipsum dolor sit amet...")
        answer = gr.Textbox(lines=6, label="Your short answer for R1")
        submit = gr.Button("Submit R1")
        out = gr.Markdown()

        submit.click(
            fn=lambda u, t: service.submit_reading(u, "R1", t),
            inputs=[user_box, answer],
            outputs=out
        )
