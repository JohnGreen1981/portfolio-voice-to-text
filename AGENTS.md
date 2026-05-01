# Voice To Text Bot

## Purpose

Sanitized portfolio repository for a Telegram bot that transcribes voice/audio messages and optionally cleans up the transcript with GPT.

This repo is intended for public review. It must stay free of private tokens, user data, audio files and transcripts.

## Stack

- Python 3.11
- aiogram 3
- AssemblyAI Speech-to-Text
- OpenAI API for optional transcript cleanup
- Docker

## Structure

```text
bot.py             Telegram handlers and inline-button workflow
config.py          env loading and editor prompt
openai_client.py   AssemblyAI + OpenAI API calls
requirements.txt   Python dependencies
Dockerfile         container image
.env.example       placeholder-only environment template
```

## AI-Assisted Development Note

This project is presented as an AI-assisted automation prototype. The portfolio emphasis is workflow design, prompt/control decisions, API integration, manual scenario checks and documentation.

Do not describe it as a hand-written production backend.

## Rules

- Do not commit `.env`, tokens, owner IDs, audio files, transcripts, local databases or logs.
- Keep `.env.example` placeholder-only.
- If changing runtime code, run `python3 -m py_compile bot.py config.py openai_client.py`.
- Keep `OWNER_ID` access control enabled in real deployments.

