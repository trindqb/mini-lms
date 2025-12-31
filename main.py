
import gradio as gr

def build_app():
    youtube_url = """
    <iframe width="1006" height="673" src="https://www.youtube.com/embed/f8ppddE4s4Y" title="Flowers over the years in Kyung Hee University Korea" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    """
    with gr.Blocks() as demo:
        gr.HTML(youtube_url)
    return demo

if __name__ == "__main__":
    app = build_app()
    # Use share=False to keep local; HTTPS is not needed for local
    app.launch()

