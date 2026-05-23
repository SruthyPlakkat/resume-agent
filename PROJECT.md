# Digital Resume Assistant — Project Reference

## What It Does

An AI-powered interactive portfolio for Sruthy Plakkat. Visitors land on a styled resume page and can chat with an AI assistant that answers questions about her background using the actual PDF resume as context. Built with Gradio, served locally or deployable to Hugging Face Spaces.

---

## Project Structure

```
resume_agent/
│
├── app.py                  ← Entry point. Run this to start the app.
├── agent.py                ← All AI/API logic (OpenRouter, PDF parsing)
├── ui.py                   ← Gradio UI builder (loads templates + static files)
├── tools.py                ← SendGrid email tool definition
│
├── static/
│   ├── style.css           ← All CSS (dark theme, layout, components)
│   └── script.js           ← Chat sidebar collapse + drag-resize behavior
│
├── templates/
│   ├── hero.html           ← Name, role, links, resume badge (dynamic)
│   ├── about.html          ← Professional summary
│   ├── skills.html         ← Chip-based skills grid
│   ├── experience.html     ← Timeline of 3 roles
│   ├── projects.html       ← Open source & side projects
│   ├── future.html         ← Pipeline / planned project cards
│   ├── certifications.html ← Cert badges grid
│   ├── education.html      ← Degree card
│   ├── awards.html         ← Recognition cards
│   ├── how_it_works.html   ← 4-step explainer
│   └── chat_header.html    ← Sticky chat panel header with toggle button
│
├── me/
│   └── Sruthy_Plakkat_Resume_v2.pdf   ← Source of truth for all AI answers
│
├── .env                    ← API keys (never commit this)
├── pyproject.toml          ← Dependencies
└── uv.lock                 ← Lockfile
```

---

## How to Run

```bash
uv run python app.py
```

The app opens in your browser automatically (`inbrowser=True`).

---

## Environment Variables (`.env`)

| Variable              | Required | Description                                  |
|-----------------------|----------|----------------------------------------------|
| `OPEN_ROUTER_API_KEY` | Yes      | Your OpenRouter API key                      |
| `OPEN_ROUTER_MODEL`   | No       | Model to use (default: `openrouter/auto`)    |
| `SENDGRID_API_KEY`    | No       | Enables contact email forwarding             |
| `SENDGRID_FROM_EMAIL` | No       | Sender address for contact emails            |
| `SENDGRID_TO_EMAIL`   | No       | Where contact emails are delivered           |

---

## Agent Framework

**No agent framework is used.** The "agent" is a direct REST API client built with Python's `requests` library calling OpenRouter's OpenAI-compatible chat completions endpoint.

### What this means in practice

| Concern | Approach |
|---|---|
| Model access | Raw HTTP POST to `openrouter.ai/api/v1/chat/completions` |
| Conversation memory | Full `chat_history` list passed on every request (no vector store, no retrieval) |
| Context injection | Resume text prepended as a `system` message on every call |
| Tool use | JSON schema defined in `tools.py` — OpenAI function-calling format — but **not currently active** in the chat loop |
| Orchestration | None — single API call per user message, no multi-step reasoning loop |
| Streaming | Not used — waits for full response before displaying |

### Why no framework?

This is intentionally simple. A full agent framework (LangChain, OpenAI Agents SDK, LlamaIndex) would add overhead with no benefit here — the task is always the same: inject the resume, answer the question, return the reply. There are no tools to call, no planning steps, no memory retrieval, and no branching logic.

### How it compares to real agent patterns

```
This app (simple chatbot):
  User → system prompt + history → LLM → reply

A real agent loop (e.g. ReAct / OpenAI Agents SDK):
  User → LLM → [tool_calls?] → execute tools → LLM → [more tools?] → reply
```

The code is structured so adding tool-calling is straightforward — `tools.py` already defines the SendGrid tool in OpenAI function-calling format. To upgrade to a real agent loop, pass `tools` to `call_open_router()` and handle `tool_calls` in the response before returning.

### OpenRouter's role

OpenRouter is a **model gateway**, not an agent framework. It:
- Accepts any OpenAI-compatible request
- Routes it to the underlying model (Claude, GPT-4, Mistral, etc.)
- Returns a standard `choices[0].message.content` response

Setting `OPEN_ROUTER_MODEL=openrouter/auto` lets OpenRouter pick the best available model. Pin to a specific model like `anthropic/claude-sonnet-4-5` or `openai/gpt-4o` via the `.env` file.

---

## How the Agent Works

### Request Flow

```
User types a question
        │
        ▼
  ui.py: handle()
        │
        ▼
  agent.py: chat_with_assistant()
        │
        ├─ extract_resume_text()   ← reads PDF on every request
        │       └─ PdfReader extracts text from each page
        │
        └─ call_open_router()
                │
                ├─ Builds system prompt:
                │   "You are Sruthy's assistant. Use only this resume: {text}"
                │
                ├─ Appends full chat history + new question
                │
                └─ POST → openrouter.ai/api/v1/chat/completions
                          │
                          ▼
                    AI response returned
                          │
                          ▼
              Appended to chat_history
                          │
                          ▼
              Displayed in Gradio Chatbot
```

### Key Design Choices

**Stateless per turn** — the resume PDF is re-read on every message. This is intentional: no in-memory state to manage, always reflects the latest PDF if you update it.

**Full history in every API call** — the entire conversation (`chat_history`) is sent with each request. The model can reference earlier messages, so follow-up questions work naturally ("tell me more about that", "what else?").

**System prompt guards** — the prompt instructs the model to answer only from resume content and to direct unanswerable questions to `sruthyplakkat@gmail.com`. This prevents hallucination about her background.

**OpenRouter as gateway** — `openrouter/auto` lets OpenRouter pick the best available model. You can pin a specific model (e.g. `anthropic/claude-3-5-sonnet`) via the `.env` variable.

---

## File Responsibilities

### `app.py` — Entry Point
```python
from agent import RESUME_PATH
from ui import build_interface

interface = build_interface()
interface.launch(inbrowser=True, allowed_paths=[str(RESUME_PATH.parent)])
```
Owns nothing except wiring `ui.py` to Gradio's `launch()`. All configuration lives in the files it imports.

---

### `agent.py` — AI & PDF Logic

| Function | What it does |
|---|---|
| `extract_resume_text(path)` | Reads PDF, extracts text from all pages via `PdfReader` |
| `get_resume_data_url(path)` | Base64-encodes the PDF for in-browser download link |
| `call_open_router(messages, resume_context)` | Sends chat + resume to OpenRouter, returns assistant reply |
| `chat_with_assistant(question, chat_history)` | Orchestrates the above; returns updated history |

Constants exported: `RESUME_PATH`, `BASE_DIR`

---

### `ui.py` — Gradio Interface Builder

Exports one function: `build_interface() → gr.Blocks`

Inside it:
1. Reads `static/style.css` and passes to `gr.Blocks(css=...)`
2. Reads `static/script.js` and injects as `<script>` at the bottom of the page
3. Loads each template with `_tpl("filename.html")` — a thin wrapper around `Path.read_text()`
4. The hero template uses `.format()` to inject `badge_cls`, `badge_txt`, and `resume_pill` dynamically
5. Wires Gradio events: `submit_btn.click`, `question_input.submit`, `clear_btn.click`

---

### `tools.py` — SendGrid Email Tool

Defines `send_contact_email(visitor_email, visitor_name, message)` and its JSON tool schema (`send_contact_email_json`). The schema is structured for OpenAI-compatible tool/function calling.

Currently not wired into the chat flow by default — the AI assistant directs visitors to email directly. To activate tool use, pass `tools` to the API call in `agent.py` and handle `tool_calls` in the response.

---

### `static/style.css` — All Visual Styling

Organized sections (search by comment):

| Section | What it controls |
|---|---|
| Body / container | Dark gradient background, max-width layout |
| `#hero` | Avatar pulse, name gradient, link pills |
| `.glass` | Frosted-glass card base with per-section accent colors |
| `.sec-*` | CSS custom property overrides per section (color, glow) |
| `.chip-*` | Skill tag color variants (AI, test, lang, devops) |
| `.exp-item` | Timeline dots and vertical connector lines |
| `#chat-col` | Sticky sidebar, collapse/expand, scrollbar |
| `.chat-panel-hdr` | Sticky chat header with live dot |
| `#chat-input-row` | Compound input + send button row |
| `#send-btn` | Circular gradient send button |
| Media queries | Responsive at 960px, 768px, 600px, 480px |

---

### `static/script.js` — Chat Sidebar Behavior

Two features, one IIFE:

1. **Collapse/expand** — reads/writes `localStorage.chatCollapsed`; toggles `.chat-collapsed` class on `#chat-col`; swaps `◀` / `▶` on the button
2. **Drag resize** — injects a `div.chat-resize-handle` into the DOM; tracks `mousedown` / `mousemove` / `mouseup` to resize the column between 260px and 700px

Initialization retries every 400ms until the Gradio DOM is ready (Gradio renders async).

---

### `templates/` — HTML Sections

All templates are plain HTML fragments (no templating engine needed). They are loaded with `Path.read_text()` and passed directly to `gr.HTML()`.

**Exception:** `hero.html` uses Python `str.format()` placeholders:

| Placeholder | Value |
|---|---|
| `{badge_cls}` | `"sp-badge badge-ok"` or `"sp-badge badge-err"` |
| `{badge_txt}` | `"✓ Resume Loaded"` or `"⚠ Resume Not Found"` |
| `{resume_pill}` | Download `<a>` tag with base64 PDF data URL, or empty string |

To add content to any section, edit the corresponding `.html` file directly — no Python knowledge required.

---

## Adding a New Pipeline Project Card

Edit `templates/future.html` and copy this block inside `.future-grid`:

```html
<div class="future-card">
  <div class="future-status planned">🔮 Planned</div>
  <div class="future-card-title">Your Project Title</div>
  <div class="future-card-desc">Short description of what it does.</div>
  <div class="future-card-tags">
    <span class="chip chip-ai">Tool A</span>
    <span class="chip chip-devops">Tool B</span>
  </div>
</div>
```

Change `planned` → `complete` and the icon to `✅ Live` when it ships.

---

## Updating the Resume

Replace `me/Sruthy_Plakkat_Resume_v2.pdf` with the new PDF. The agent reads it fresh on every chat message, so no restart is needed if the app is already running. The download link in the hero also updates automatically on next page load.

---

## Dependencies

| Package | Purpose |
|---|---|
| `gradio` | Web UI framework |
| `pypdf` | PDF text extraction |
| `requests` | HTTP calls to OpenRouter |
| `python-dotenv` | `.env` file loading |
| `sendgrid` | Contact email (optional) |
