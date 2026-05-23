"""Gradio UI builder for the Digital Resume Assistant."""

from __future__ import annotations

from pathlib import Path

import gradio as gr

from agent import (
    RESUME_PATH,
    chat_with_assistant,
    extract_resume_text,
    get_resume_data_url,
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


def _tpl(name: str, **kwargs: str) -> str:
    """Load a template file and optionally format it with keyword arguments."""
    text = (TEMPLATES_DIR / name).read_text(encoding="utf-8")
    return text.format(**kwargs) if kwargs else text


def build_interface() -> gr.Blocks:
    css = (STATIC_DIR / "style.css").read_text(encoding="utf-8")
    js_code = (STATIC_DIR / "script.js").read_text(encoding="utf-8")

    resume_text = extract_resume_text(RESUME_PATH)
    resume_data_url = get_resume_data_url(RESUME_PATH)

    badge_cls = "sp-badge badge-ok" if resume_text else "sp-badge badge-err"
    badge_txt = "✓ Resume Loaded" if resume_text else "⚠ Resume Not Found"
    resume_pill = (
        f'<a href="{resume_data_url}" download="Sruthy_Plakkat_Resume_v2.pdf">📄 Resume</a>'
        if resume_data_url else ""
    )

    with gr.Blocks(
        title="Sruthy Portfolio",
        theme=gr.themes.Base(),
        css=css,
    ) as interface:

        gr.HTML(_tpl("hero.html", badge_cls=badge_cls, badge_txt=badge_txt, resume_pill=resume_pill))

        with gr.Row(elem_id="main-layout"):

            # LEFT: Resume content
            with gr.Column(scale=6, elem_id="resume-col"):
                gr.HTML(_tpl("about.html"))
                gr.HTML(_tpl("skills.html"))
                gr.HTML(_tpl("experience.html"))
                gr.HTML(_tpl("projects.html"))
                gr.HTML(_tpl("future.html"))
                gr.HTML(_tpl("certifications.html"))

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.HTML(_tpl("education.html"))
                    with gr.Column(scale=1):
                        gr.HTML(_tpl("awards.html"))

                gr.HTML(_tpl("how_it_works.html"))

            # RIGHT: Sticky chat sidebar
            with gr.Column(scale=4, elem_id="chat-col"):
                gr.HTML(_tpl("chat_header.html"))

                chatbot = gr.Chatbot(
                    label="",
                    height=380,
                    show_label=False,
                    avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=sruthy"),
                    elem_id="chat-window",
                )
                with gr.Row(elem_id="chat-input-row"):
                    question_input = gr.Textbox(
                        label="",
                        placeholder="Ask me anything about Sruthy…",
                        lines=1,
                        scale=9,
                        container=False,
                        show_label=False,
                        elem_id="chat-input",
                    )
                    submit_btn = gr.Button("↑", variant="primary", scale=1, min_width=46, elem_id="send-btn")
                with gr.Row():
                    clear_btn = gr.Button("✕ Clear chat", variant="secondary", scale=1, size="sm", elem_id="clear-btn")
                error_output = gr.Markdown(visible=False)

        gr.HTML(f"<script>\n{js_code}\n</script>")

        def handle(question: str, history: list[dict]):
            new_history, error, cleared_q = chat_with_assistant(question, history)
            if error:
                return new_history, gr.update(value=error, visible=True), cleared_q
            return new_history, gr.update(value="", visible=False), cleared_q

        submit_btn.click(
            fn=handle,
            inputs=[question_input, chatbot],
            outputs=[chatbot, error_output, question_input],
        )
        question_input.submit(
            fn=handle,
            inputs=[question_input, chatbot],
            outputs=[chatbot, error_output, question_input],
        )
        clear_btn.click(
            fn=lambda: ([], gr.update(value=""), gr.update(value="", visible=False)),
            outputs=[chatbot, question_input, error_output],
        )

    return interface
