
# lms/ui/video.py
import json
import gradio as gr

def video_tab(service, user_box: gr.Textbox):
    with gr.Tab("Video"):
        gr.Markdown("## Interactive YouTube Lesson")

        video_id = "V1"
        youtube_video_id = "dQw4w9WgXcQ"  # ← replace with your own ID
        markers = service.get_video_markers(video_id)  # [{'id','time','type',...}]

        # Hidden bridge components
        marker_event = gr.Textbox(label="Marker Event", visible=False)
        video_time = gr.Textbox(label="Video Time", visible=False)
        video_duration = gr.Textbox(label="Video Duration", visible=False)
        resume_signal = gr.Textbox(label="Resume Signal", visible=False)
        resume_time = gr.Textbox(label="Resume Time", visible=False)

        # Load last progress
        load_btn = gr.Button("Load Last Progress")
        load_msg = gr.Markdown()
        def _load_progress(user):
            t = service.get_last_progress(user, video_id)
            return str(t), f"Loaded: {t:.2f}s"
        load_btn.click(fn=_load_progress, inputs=[user_box], outputs=[resume_time, load_msg])

        # MCQ panel
        with gr.Group(visible=False) as mcq_panel:
            mcq_prompt = gr.Markdown("**MCQ Prompt**")
            mcq_choice = gr.Radio(choices=["A","B","C","D"], label="Select")
            mcq_submit = gr.Button("Submit MCQ")
            mcq_msg = gr.Markdown()
            def _submit_mcq(user, choice):
                return service.submit_video_quiz_mcq(user, video_id, "V1-M30", choice)
            mcq_submit.click(fn=_submit_mcq, inputs=[user_box, mcq_choice], outputs=mcq_msg).then(
                fn=lambda: "resume", inputs=None, outputs=resume_signal
            )

        # Short answer panel
        with gr.Group(visible=False) as short_panel:
            short_prompt = gr.Markdown("**Short Answer Prompt**")
            short_text = gr.Textbox(lines=4, label="Your answer")
            short_submit = gr.Button("Submit")
            short_msg = gr.Markdown()
            def _submit_short(user, text):
                return service.submit_video_quiz_short(user, video_id, "V1-M70", text)
            short_submit.click(fn=_submit_short, inputs=[user_box, short_text], outputs=short_msg).then(
                fn=lambda: "resume", inputs=None, outputs=resume_signal
            )

        # Show appropriate panel when a marker event fires
        def _open_marker(mid):
            if mid == "V1-M30":
                return (gr.update(visible=True), gr.update(value="**V1-M30:** What is the main idea?"),
                        gr.update(visible=False), gr.update(value=""))
            elif mid == "V1-M70":
                return (gr.update(visible=False), gr.update(value=""),
                        gr.update(visible=True), gr.update(value="**V1-M70:** Summarize in one sentence:"))
            else:
                return (gr.update(visible=False), gr.update(value=""),
                        gr.update(visible=False), gr.update(value=""))
        marker_event.change(fn=_open_marker, inputs=[marker_event], outputs=[mcq_panel, mcq_prompt, short_panel, short_prompt])

        # Save progress when time changes
        def _save_progress(user, cur_time, dur):
            try:
                t = float(cur_time) if cur_time else 0.0
                d = float(dur) if dur else 0.0
            except Exception:
                t, d = 0.0, 0.0
            return service.save_video_progress(user, video_id, t, d)
        video_time.change(fn=_save_progress, inputs=[user_box, video_time, video_duration], outputs=load_msg)

        # Notes & bookmarks
        gr.Markdown("### Notes & Bookmarks")
        note_box = gr.Textbox(lines=3, label="Note")
        note_btn = gr.Button("Save Note")
        note_msg = gr.Markdown()
        note_btn.click(fn=lambda u, n: service.save_video_note(u, video_id, n), inputs=[user_box, note_box], outputs=note_msg)

        bm_note = gr.Textbox(lines=2, label="Bookmark note")
        bm_btn = gr.Button("Save Bookmark (current time)")
        bm_msg = gr.Markdown()
        def _save_bm(user, cur_time, note):
            try:
                t = float(cur_time) if cur_time else 0.0
            except Exception:
                t = 0.0
            return service.save_video_bookmark(user, video_id, t, note or "")
        bm_btn.click(fn=_save_bm, inputs=[user_box, video_time, bm_note], outputs=bm_msg)

        # YouTube Player API bridge
        markers_json = json.dumps(markers)
        html = f"""
                <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;">
                <div id="yt-player" style="position:absolute;top:0;left:0;width:100%;height:100%;"></div>
                </div>

                <script>
                (function() {{
                // Avoid duplicate script loads
                const API_URL = "https://www.youtube.com/iframe_api";
                if (![...document.scripts].some(s => s.src === API_URL)) {{
                    const tag = document.createElement('script');
                    tag.src = API_URL;
                    document.head.appendChild(tag);
                }}

                const markers = {markers_json};
                const done = new Set();
                let player = null;
                let lastSent = -1;

                const findInput = (label) => [...document.querySelectorAll('input')].find(el => el.getAttribute('aria-label') === label);
                const markerEventBox = findInput('Marker Event');
                const videoTimeBox = findInput('Video Time');
                const videoDurationBox = findInput('Video Duration');
                const resumeSignalBox = findInput('Resume Signal');
                const resumeTimeBox = findInput('Resume Time');

                const dispatchInput = (el, value) => {{
                    if (!el) return;
                    el.value = value;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }};

                window.onYouTubeIframeAPIReady = function() {{
                    try {{
                    player = new YT.Player('yt-player', {{
                        videoId: '{youtube_video_id}',
                        playerVars: {{
                        'playsinline': 1,
                        'enablejsapi': 1,
                        'origin': window.location.origin
                        }},
                        events: {{
                        'onReady': onReady
                        }}
                    }});
                    }} catch (e) {{
                    console.error('YT init error:', e);
                    }}
                };

                function onReady() {{
                    try {{
                    const dur = player.getDuration() || 0;
                    dispatchInput(videoDurationBox, String(dur));
                    }} catch(e) {{}}

                    // Resume when resumeTime changes
                    if (resumeTimeBox) {{
                    resumeTimeBox.addEventListener('input', () => {{
                        const t = parseFloat(resumeTimeBox.value || '0');
                        if (!isNaN(t) && player) {{
                        player.seekTo(t, true);
                        player.playVideo();
                        }}
                    }});
                    }}

                    // Resume after quiz submit
                    if (resumeSignalBox) {{
                    resumeSignalBox.addEventListener('input', () => {{
                        const v = (resumeSignalBox.value || '').trim();
                        if (v === 'resume' && player) {{
                        player.playVideo();
                        dispatchInput(resumeSignalBox, '');
                        }}
                    }});
                    }}

                    // Poll current time for progress + markers
                    setInterval(() => {{
                    if (!player) return;
                    let t = 0;
                    try {{ t = player.getCurrentTime() || 0; }} catch(e) {{}}

                    // Throttle progress every 5 sec
                    const tInt = Math.floor(t);
                    if (tInt % 5 === 0 && tInt !== lastSent) {{
                        lastSent = tInt;
                        dispatchInput(videoTimeBox, String(t));
                    }}

                    // Trigger markers
                    for (const m of markers) {{
                        if (t >= m.time && !done.has(m.id)) {{
                        done.add(m.id);
                        try {{ player.pauseVideo(); }} catch(e) {{}}
                        dispatchInput(markerEventBox, m.id);
                        break;
                        }}
                    }}
                    }}, 500);
                }
                }})();
                </script>
                """
        gr.HTML(html)
        gr.Markdown("> Press **Play** if autoplay is blocked. If the player still doesn’t appear, disable ad‑blockers and check console errors (F12).")
