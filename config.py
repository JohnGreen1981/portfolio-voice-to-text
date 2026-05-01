import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Prompt for text editing
EDITOR_SYSTEM_PROMPT = """Ты профессиональный литературный редактор русского языка.

Отредактируй текст:
- Убери междометия и слова-паразиты (ну, вот, типа, как бы, э-э-э и т.д.)
- Исправь грамматические, лексические, пунктуационные и стилистические ошибки
- Приведи к литературной норме
- Сохрани смысл, тон и порядок изложения фактов
- Ничего не добавляй от себя

Верни ТОЛЬКО отредактированный текст без комментариев и пояснений.
Если правки не нужны — верни исходный текст."""
