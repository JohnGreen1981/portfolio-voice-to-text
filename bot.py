import asyncio
import logging
import tempfile
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove
from aiogram.filters import Command

from config import TELEGRAM_BOT_TOKEN, OWNER_ID
from openai_client import transcribe_audio, edit_text

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

COPY_CALLBACK = "copy_text"
EDIT_CALLBACK = "edit_transcript"


def get_inline_keyboard(can_edit: bool = True) -> InlineKeyboardMarkup:
    """Generate inline keyboard for a transcription result."""
    keyboard = []
    if can_edit:
        keyboard.append([InlineKeyboardButton(text="✏️ Отредактировать", callback_data=EDIT_CALLBACK)])
    keyboard.append([InlineKeyboardButton(text="📋 Скопировать", callback_data=COPY_CALLBACK)])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def has_edit_button(markup: InlineKeyboardMarkup | None) -> bool:
    """Check whether the current inline keyboard still allows editing."""
    if not markup:
        return False

    return any(
        button.callback_data == EDIT_CALLBACK
        for row in markup.inline_keyboard
        for button in row
    )


def is_owner(user_id: int) -> bool:
    """Check if user is the owner."""
    return OWNER_ID == 0 or user_id == OWNER_ID


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command."""
    if not is_owner(message.from_user.id):
        return

    await message.answer(
        "👋 Привет! Отправь мне голосовое сообщение — я его транскрибирую.\n\n"
        "✏️ Если нужен литературный редактор, нажми кнопку под готовой расшифровкой.",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.callback_query(F.data == EDIT_CALLBACK)
async def edit_transcript_callback(callback: CallbackQuery):
    """Handle one-click editing for a completed transcription."""
    if not is_owner(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён")
        return

    original_text = callback.message.text or callback.message.caption
    if not original_text:
        await callback.answer("Нет текста для редактирования")
        return

    await callback.answer("Редактирую...")

    try:
        if callback.message.text:
            await callback.message.edit_text("✏️ Редактирую текст...")
            edited_text = await edit_text(original_text)
            await callback.message.edit_text(
                edited_text,
                reply_markup=get_inline_keyboard(can_edit=False)
            )
        else:
            await callback.message.edit_caption("✏️ Редактирую текст...")
            edited_text = await edit_text(original_text)
            await callback.message.edit_caption(
                caption=edited_text,
                reply_markup=get_inline_keyboard(can_edit=False)
            )
    except Exception as e:
        logger.error(f"Editor error: {e}")
        try:
            if callback.message.text:
                await callback.message.edit_text(
                    original_text,
                    reply_markup=get_inline_keyboard(can_edit=True)
                )
            else:
                await callback.message.edit_caption(
                    caption=original_text,
                    reply_markup=get_inline_keyboard(can_edit=True)
                )
        except Exception as restore_error:
            logger.error(f"Restore after editor error failed: {restore_error}")
        await callback.message.answer("❌ Ошибка при редактировании. Исходная расшифровка восстановлена.")


@dp.message(F.text.in_({"✏️ Включить редактор", "🖊 Выключить редактор"}))
async def legacy_toggle_editor_message(message: Message):
    """Handle old persistent keyboard buttons from previous bot versions."""
    if not is_owner(message.from_user.id):
        return

    await message.answer(
        "Редактор теперь применяется кнопкой под готовой расшифровкой.",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.callback_query(F.data == COPY_CALLBACK)
async def copy_text_callback(callback: CallbackQuery):
    """Handle copy button click."""
    if not is_owner(callback.from_user.id):
        await callback.answer("⛔️ Доступ запрещён")
        return

    text = callback.message.text or callback.message.caption
    if not text:
        await callback.answer("Нет текста для копирования")
        return
    
    # Escape HTML special characters manually to avoid extra dependencies
    safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    can_edit = has_edit_button(callback.message.reply_markup)
    
    try:
        await callback.message.edit_text(
            f"<code>{safe_text}</code>",
            parse_mode="HTML",
            reply_markup=get_inline_keyboard(can_edit=can_edit)
        )
        await callback.answer("Теперь нажми на текст сообщения, чтобы скопировать!")
    except Exception as e:
        await callback.answer("Ошибка при изменении сообщения")
        logger.error(f"Edit error: {e}")


@dp.message(F.voice | F.audio | F.document)
async def handle_voice(message: Message):
    """Handle voice messages, audio files, and audio documents."""
    if not is_owner(message.from_user.id):
        return
    
    # Determine file_id based on message type
    if message.voice:
        file_id = message.voice.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.document:
        # Check if it's an audio file
        mime = message.document.mime_type or ""
        name = (message.document.file_name or "").lower()
        if not (mime.startswith("audio/") or name.endswith(".m4a") or name.endswith(".ogg")):
            await message.answer(
                "Пожалуйста, отправьте голосовое сообщение или аудиофайл.",
                reply_markup=ReplyKeyboardRemove()
            )
            return
        file_id = message.document.file_id
    else:
        return

    # Send processing indicator and clear the old persistent keyboard.
    processing_msg = await message.answer(
        "🎧 Обрабатываю...",
        reply_markup=ReplyKeyboardRemove()
    )
    
    try:
        # Download file
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        # Create temp file and download
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        await bot.download_file(file_path, tmp_path)
        
        # Transcribe
        text = await transcribe_audio(tmp_path)

        # Cleanup temp file
        tmp_path.unlink(missing_ok=True)
        
        # Delete processing message
        await processing_msg.delete()
        
        # Send result
        await message.answer(text, reply_markup=get_inline_keyboard())
        
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        await processing_msg.edit_text(f"❌ Ошибка: {e}")


@dp.message()
async def handle_other(message: Message):
    """Handle non-voice messages."""
    if not is_owner(message.from_user.id):
        return

    await message.answer(
        "Пожалуйста, отправьте голосовое сообщение или аудиофайл.",
        reply_markup=ReplyKeyboardRemove()
    )


async def main():
    """Main function to start the bot."""
    logger.info("Starting bot...")
    
    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
