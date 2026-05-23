"""AI/API logic for the Digital Resume Assistant."""

from __future__ import annotations

import base64
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent
RESUME_PATH = BASE_DIR / "me" / "Sruthy_Plakkat_Resume_v2.pdf"

OPEN_ROUTER_API_KEY = os.environ.get("OPEN_ROUTER_API_KEY")
OPEN_ROUTER_MODEL = os.environ.get("OPEN_ROUTER_MODEL", "openrouter/auto")
OPEN_ROUTER_BASE_URL = "https://openrouter.ai/api/v1"

SYSTEM_PROMPT_TEMPLATE = """You are a professional digital resume assistant for Sruthy Plakkat.
Answer questions about her background, skills, experience, education, and projects using only the resume below.

RULES:
1. Answer factually and professionally using only resume content.
2. If a question cannot be answered from the resume, say so politely and suggest the visitor reach out directly via email at sruthyplakkat@gmail.com.
3. Keep answers concise but complete (3–5 sentences max).
4. Be warm, engaging, and professional.

RESUME:
{resume_context}"""


def extract_resume_text(path: Path) -> str | None:
    if not path.exists():
        return None
    pages = [p.extract_text() for p in PdfReader(path).pages if p.extract_text()]
    return "\n\n".join(pages).strip() if pages else None


def get_resume_data_url(path: Path) -> str | None:
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return "data:application/pdf;base64," + base64.b64encode(f.read()).decode()


def call_open_router(messages: list[dict], resume_context: str) -> str:
    if not OPEN_ROUTER_API_KEY:
        return "⚠️  OPEN_ROUTER_API_KEY not configured. Add it to your .env file."

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(resume_context=resume_context)

    try:
        resp = requests.post(
            f"{OPEN_ROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
                "HTTP-Referer": "https://resume-assistant.local",
                "X-Title": "Resume Assistant",
            },
            json={
                "model": OPEN_ROUTER_MODEL,
                "messages": [{"role": "system", "content": system_prompt}] + messages,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            timeout=30,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return content or "I wasn't able to generate a response. Please try rephrasing."
    except requests.exceptions.HTTPError as exc:
        return f"API error {exc.response.status_code}: {exc.response.text[:200]}"
    except (KeyError, IndexError, ValueError) as exc:
        return f"Unexpected API response: {exc}"
    except requests.exceptions.RequestException as exc:
        return f"Network error: {exc}"


def chat_with_assistant(
    question: str,
    chat_history: list[dict],
) -> tuple[list[dict], str, str]:
    if not question or not question.strip():
        return chat_history, "", ""

    if not OPEN_ROUTER_API_KEY:
        return chat_history, "⚠️  OPEN_ROUTER_API_KEY not configured.", ""

    resume_text = extract_resume_text(RESUME_PATH)
    if resume_text is None:
        return chat_history, "❌ Resume PDF not found in the `me/` folder.", ""

    api_messages = list(chat_history) + [{"role": "user", "content": question.strip()}]
    answer = call_open_router(api_messages, resume_text)

    new_history = list(chat_history) + [
        {"role": "user", "content": question.strip()},
        {"role": "assistant", "content": answer},
    ]
    return new_history, "", ""
