
# lms/ui/speaking.py
import gradio as gr
from lms.services.submissions import SubmissionService

def speaking_tab(service: SubmissionService, user_box: gr.Textbox):
    with gr.Tab("Speaking"):
        gr.Markdown("## Speaking: record from microphone and submit")
        gr.Markdown("**S1:** Describe your study plan for 1 minute.")
        mic = gr.Audio(sources=["microphone"], type="filepath", label="Record your answer")
        submit = gr.Button("Submit S1")
        out = gr.Markdown()

        submit.click(
            fn=lambda u, a: service.submit_speaking(u, "S1", a),
            inputs=[user_box, mic],
            outputs=out
        )
