
# lms/ui/video.py
import gradio as gr

def video_tab(service, user_box: gr.Textbox):
    with gr.Tab("Video"):
        gr.Markdown("## YouTube Video")

        # Thay bằng video ID của bạn (ví dụ: https://www.youtube.com/watch?v=dQw4w9WgXcQ)
        youtube_video_id = "8ppddE4s4Y"

        # Dùng dạng embed chuẩn
        embed_url = f"https://www.youtube.com/embed/{youtube_video_id}?rel=0"

        # HTML iframe hiển thị video, tỷ lệ 16:9
        html = """
<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;">
  <iframe
    src="{EMBED_URL}"
    title="YouTube video player"
    frameborder="0"
   html)
"""