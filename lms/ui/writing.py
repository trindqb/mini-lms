
# lms/ui/writing.py
import gradio as gr
from lms.services.submissions import SubmissionService

def writing_tab(service: SubmissionService, user_box: gr.Textbox):
    with gr.Tab("Writing"):
        gr.Markdown("## Writing: essay prompt")
        gr.Markdown("**W1:** Share your perspective on online learning (150–200 words).")
        essay = gr.Textbox(lines=12, label="Essay for W1")
        submit = gr.Button("Submit W1")
        out = gr.Markdown()

        submit.click(
            fn=lambda u, t: service.submit_writing(u, "W1", t),
            inputs=[user_box, essay],
            outputs=out
        )
