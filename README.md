# 📄 Sruthy Plakkat - Digital Resume Assistant

A modern, interactive resume assistant powered by **Open Router API** and **SendGrid**. Uses **UV** for fast, reliable Python package management.

## Features

✨ **Interactive Resume Q&A** - Ask questions about skills, experience, projects, and education  
🤖 **AI-Powered Responses** - Uses Open Router API for intelligent, context-aware answers  
📧 **Smart Email Integration** - Automatically sends user contact details via SendGrid for unanswered questions  
📱 **Beautiful Web Interface** - Built with Gradio for a modern, responsive design  
⚡ **Fast Setup** - Uses UV for quick dependency resolution and installation  

## Prerequisites

- Python 3.10 or higher
- [UV](https://docs.astral.sh/uv/) (fast Python package manager)
- [Open Router API Key](https://openrouter.ai)
- [SendGrid API Key](https://sendgrid.com)

## Quick Start

### 1. Install UV

On **Windows** (using PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

On **macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:
```bash
uv --version
```

### 2. Setup Project

```bash
cd c:\Users\SruthyPlakkat\Projects\agents\resume_agent
```

### 3. Create Virtual Environment

Using UV:
```bash
uv venv .venv
```

Activate virtual environment:
- **Windows (PowerShell)**: `.venv\Scripts\Activate.ps1`
- **Windows (CMD)**: `.venv\Scripts\activate.bat`
- **macOS/Linux**: `source .venv/bin/activate`

### 4. Install Dependencies

Using UV (fast!):
```bash
uv pip install -r requirements.txt
```

### 5. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPEN_ROUTER_API_KEY=sk-your-key-here
SENDGRID_API_KEY=SG.your-key-here
SENDGRID_FROM_EMAIL=noreply@example.com
SENDGRID_TO_EMAIL=your-email@example.com
```

### 6. Run the Assistant

```bash
python app.py
```

The application will open in your browser at `http://localhost:7860`

## UV Commands Reference

```bash
# Create virtual environment
uv venv .venv

# Install dependencies from requirements.txt
uv pip install -r requirements.txt

# Install a specific package
uv pip install gradio

# Show installed packages
uv pip list
```

## Configuration

### Open Router API

1. Sign up at [openrouter.ai](https://openrouter.ai)
2. Generate an API key from your account settings
3. Add to `.env`: `OPEN_ROUTER_API_KEY=your-key`

### SendGrid Setup

1. Create account at [sendgrid.com](https://sendgrid.com)
2. Verify a sender email address
3. Generate API key from Settings → API Keys
4. Add to `.env`:
   ```
   SENDGRID_API_KEY=your-key
   SENDGRID_FROM_EMAIL=verified@example.com
   SENDGRID_TO_EMAIL=your-email@example.com
   ```

## Project Structure

```
resume_agent/
├── app.py                 # Main application
├── pyproject.toml         # UV/Project configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
└── me/
    └── Sruthy_Plakkat_Resume_v2.pdf  # Your resume
```

## How It Works

1. **Resume Extraction** - PDF is parsed and stored as context
2. **User Question** - User asks a question about the resume
3. **AI Processing** - Open Router API generates an answer using resume context
4. **Smart Fallback** - If the answer isn't in the resume, the assistant suggests the user provide contact info
5. **Email Notification** - If user provides email, SendGrid sends you their details automatically

## Troubleshooting

### "OPEN_ROUTER_API_KEY not configured"
- Ensure `.env` file exists and contains your key
- Verify key is valid at [openrouter.ai](https://openrouter.ai)

### "Resume file not found"
- Make sure `Sruthy_Plakkat_Resume_v2.pdf` is in the `me/` folder
- Check file permissions

### SendGrid not sending emails
- Verify `SENDGRID_FROM_EMAIL` is a verified sender in SendGrid account
- Check API key is active (not expired)

### UV command not found
- Ensure UV is installed: `uv --version`
- May need to restart terminal or add to PATH

## Performance Tips

- UV resolves dependencies ~10x faster than pip
- Use `openrouter/auto` model for cost optimization

## License

Personal project - for resume inquiries only

## Contact

For questions about this project, use the resume assistant! 🤖
