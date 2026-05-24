---
title: Resume Agent
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 6.14.0
python_version: '3.10'
app_file: app.py
pinned: false
license: mit
---

# Sruthy Plakkat - Digital Resume Assistant

A modern, interactive resume assistant powered by **Open Router API** and **SendGrid**. Ask me anything about Sruthy's background, skills, experience, and projects.

## Features

- **Interactive Resume Q&A** - Ask questions about skills, experience, projects, and education
- **AI-Powered Responses** - Uses Open Router API for intelligent, context-aware answers
- **Smart Email Integration** - Automatically sends user contact details via SendGrid for unanswered questions
- **Beautiful Web Interface** - Built with Gradio

## Environment Variables

| Variable | Description |
|---|---|
| `OPEN_ROUTER_API_KEY` | Your OpenRouter API key |
| `SENDGRID_API_KEY` | Your SendGrid API key |
| `SENDGRID_FROM_EMAIL` | Verified sender email |
| `SENDGRID_TO_EMAIL` | Email to receive contact notifications |
