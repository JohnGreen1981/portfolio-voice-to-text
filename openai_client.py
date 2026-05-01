import asyncio

import assemblyai as aai
from openai import AsyncOpenAI
from pathlib import Path

from config import OPENAI_API_KEY, ASSEMBLYAI_API_KEY, EDITOR_SYSTEM_PROMPT

aai.settings.api_key = ASSEMBLYAI_API_KEY
_transcriber = aai.Transcriber(config=aai.TranscriptionConfig(
    speech_model=aai.SpeechModel.universal,
    language_code="ru",
))

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def transcribe_audio(file_path: Path) -> str:
    """Transcribe audio file using AssemblyAI."""
    transcript = await asyncio.to_thread(_transcriber.transcribe, str(file_path))
    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")
    return transcript.text or ""


async def edit_text(text: str) -> str:
    """Edit text using GPT-4o-mini to remove filler words and fix grammar."""
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EDITOR_SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content or text
