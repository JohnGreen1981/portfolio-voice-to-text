# Voice To Text Bot

Telegram bot for transcribing voice/audio messages and optionally cleaning up the transcript with GPT.

This is a sanitized portfolio version. It does not include production `.env` files, user data, audio files, private transcripts, local databases, or deployment notes.

## What It Demonstrates

- Speech-to-text workflow in Telegram.
- AssemblyAI integration.
- One-click GPT text cleanup after transcription.
- Inline-button UX for editing and copying results.
- Docker-based deployment path.
- AI-assisted development workflow: requirements, implementation via coding assistants, manual scenario checks, cleanup and documentation.

## User Workflow

1. User sends a voice message or audio file to the bot.
2. Bot downloads the file and sends it to AssemblyAI.
3. Bot returns the raw transcript.
4. User can press `Edit` to run GPT cleanup for that specific transcript.
5. User can press `Copy` to convert the text to a copy-friendly monospace message.

The editor is intentionally not a global mode: the raw transcript is always available first, and GPT cleanup is applied only by explicit user action.

## Stack

- Python 3.11
- aiogram 3
- AssemblyAI
- OpenAI API
- Docker

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python bot.py
```

Required environment variables:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
OPENAI_API_KEY=your_openai_api_key
OWNER_ID=your_telegram_user_id
```

Set `OWNER_ID=0` only for local experiments where access control is not needed.

## Docker

```bash
docker build -t voice-to-text-bot .
docker run -d \
  --name voice-to-text-bot \
  --restart unless-stopped \
  --env-file .env \
  voice-to-text-bot
```

## Project Structure

```text
bot.py             Telegram handlers and inline-button workflow
config.py          environment variables and editor prompt
openai_client.py   AssemblyAI transcription and GPT cleanup calls
Dockerfile         container image
requirements.txt   Python dependencies
```

## Safety Notes

- Do not commit `.env`.
- Do not commit audio files or transcripts from real users.
- Keep `OWNER_ID` enabled in real deployments.
- GPT cleanup can change style; keep raw transcripts available when exact wording matters.

## Portfolio Note

This project is presented as an AI-assisted automation prototype. The focus is workflow design, prompt/control decisions, API integration and practical UX, not a claim of hand-written production backend engineering.
