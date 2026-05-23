#!/usr/bin/env python3
"""
Digital Resume Assistant — OpenRouter API.
Run: uv run python app.py
"""

from agent import RESUME_PATH
from ui import build_interface

if __name__ == "__main__":
    interface = build_interface()
    interface.launch(
        inbrowser=True,
        share=False,
        allowed_paths=[str(RESUME_PATH.parent)],
    )
