# Voice To Text Bot

## Назначение

Репозиторий Telegram-бота, который транскрибирует голосовые/аудиосообщения и по кнопке применяет GPT-правку к готовой расшифровке.

В репозитории не хранить приватные токены, пользовательские данные, аудиофайлы и транскрипты.

## Стек

- Python 3.11
- aiogram 3
- AssemblyAI Speech-to-Text
- OpenAI API для опциональной правки текста
- Docker

## Структура

```text
bot.py             Telegram handlers и сценарий на inline-кнопках
config.py          загрузка env и промпт редактора
openai_client.py   вызовы AssemblyAI + OpenAI API
requirements.txt   Python-зависимости
Dockerfile         Docker-образ
.env.example       шаблон окружения только с placeholder-значениями
```

## AI-assisted development

Проект показывает прототип автоматизации, собранный с помощью AI-assisted development: проектирование пользовательского сценария, промптов и контрольных решений, интеграцию API, ручную проверку сценариев и документацию.

Не описывать проект как production backend, написанный вручную с нуля.

## Правила

- Не коммитить `.env`, токены, owner ID, аудиофайлы, транскрипты, локальные базы и логи.
- `.env.example` должен содержать только placeholder-значения.
- При изменении runtime-кода запускать `python3 -m py_compile bot.py config.py openai_client.py`.
- В реальных деплоях оставлять `OWNER_ID` включённым.
