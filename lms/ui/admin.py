
# lms/ui/admin.py
import gradio as gr
from lms.services.submissions import SubmissionService

def admin_tab(service: SubmissionService):
    with gr.Tab("Admin"):
        gr.Markdown("## Admin: view & export submissions")
        refresh = gr.Button("Refresh")
        table = gr.Dataframe(
            headers=["ts","user","section","item_id","text","mcq_score","audio_path","choice"],
            interactive=False
        )
        info = gr.Markdown()
        export_btn = gr.Button("Export CSV")
        export_file = gr.File(label="Download CSV")

        refresh.click(fn=service.fetch_table, inputs=None, outputs=[table, info])
        export_btn.click(fn=service.export_csv, inputs=None, outputs=export_file)
