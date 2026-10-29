# Parser Bot

Асинхронный Telegram-бот для автоматизированного сбора изображений с веб-страниц и публикации их в заданном Telegram-канале.

Бот извлекает URL изображений из HTML, загружает файлы, проверяет их на дубликаты по исходному URL и SHA-256 хешу, сохраняет информацию об обработанных изображениях в SQLite и отправляет новые изображения в Telegram.

## Features

- Парсинг HTML-страниц с помощью BeautifulSoup.
- Настройка правил извлечения изображений для разных доменов.
- Асинхронные HTTP-запросы с повторными попытками.
- Проверка дубликатов по URL и SHA-256 хешу содержимого.
- Сохранение информации об обработанных изображениях в SQLite.
- Отправка изображений в Telegram группами до 10 файлов.
- Поддержка хештегов для публикаций.
- Ограничение доступа к запуску парсера по Telegram ID пользователей.
- Логирование URL, которые не удалось обработать.

## Tech Stack

- **Python 3.12+**
- **aiogram 3** — взаимодействие с Telegram Bot API
- **httpx** — асинхронные HTTP-запросы
- **BeautifulSoup4** — парсинг HTML
- **SQLite / aiosqlite** — хранение данных об изображениях
- **Pydantic Settings** — конфигурация через переменные окружения
- **Poetry** — управление зависимостями

## Architecture

- **Handlers** — обработка команд и взаимодействий с пользователем в Telegram.
- **Parser Service** — загрузка страниц, извлечение URL изображений и управление процессом парсинга.
- **Image Service** — загрузка изображений, проверка дубликатов и сохранение информации о файлах.
- **Repository** — SQL-запросы для поиска и сохранения обработанных изображений.
- **Utilities** — HTTP-запросы с повторными попытками, отправка изображений в Telegram и загрузка конфигурации.

## Configuration

### 1. Environment variables

Создайте файл `.env` на основе `.env.example`:

```dotenv
TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
PAGE_URLS_PATH=./page_urls
DOMAINS_PATH=./domains.json
SKIPPED_URLS_PATH=./skipped_urls
USERS=[<YOUR_TELEGRAM_USER_ID>]
TARGET_CHAT_ID=<YOUR_TARGET_CHAT_ID>
DEFAULT_HASHTAG=<YOUR_DEFAULT_HASHTAG>
```

| Переменная | Описание |
|---|---|
| `TOKEN` | Токен Telegram-бота, полученный у BotFather |
| `PAGE_URLS_PATH` | Путь к файлу со списком страниц для парсинга |
| `DOMAINS_PATH` | Путь к конфигурации правил извлечения изображений |
| `SKIPPED_URLS_PATH` | Путь к файлу с логом пропущенных URL |
| `USERS` | Список Telegram ID пользователей, которым разрешён запуск парсера |
| `TARGET_CHAT_ID` | ID чата или канала для публикации изображений |
| `DEFAULT_HASHTAG` | Хештег по умолчанию для публикаций |

### 2. Domains configuration

В `domains.json` задаются правила извлечения изображений для каждого домена.

Пример:

```json
{
  "example.com": {
    "tag": "img",
    "attribute": "src",
    "class": "thumbnail"
  }
}
```

- `tag` — HTML-тег, содержащий изображение.
- `attribute` — атрибут, из которого извлекается URL изображения.
- `class` — CSS-класс элементов, которые нужно обработать; необязателен.

### 3. Pages configuration

В файле `page_urls` укажите URL страниц, которые необходимо обработать, по одному на строку.

Можно указать индивидуальный хештег после URL через пробел:

```text
https://example.com/gallery #Gallery
https://example.com/news
```

Если хештег для страницы не указан, используется `DEFAULT_HASHTAG`.

## Installation

### Requirements

- Python 3.12–3.14
- Poetry
- Telegram-бот, созданный через BotFather
- Telegram-канал или чат, в который бот сможет отправлять сообщения

### Run locally

Клонируйте репозиторий:

```bash
git clone https://github.com/cantexitvim/parser-bot.git
cd parser-bot
```

Установите зависимости:

```bash
poetry install
```

Создайте `.env`, настройте переменные окружения и подготовьте файлы `page_urls` и `domains.json`.

Запустите приложение:

```bash
poetry run python -m app.main
```

## Usage

1. Откройте бота в Telegram.
2. Отправьте команду **Connect** и выберите чат, чтобы получить свой Telegram ID и ID выбранного чата.
3. Укажите необходимые ID в `.env` и настройте целевой канал для публикации.
4. Отправьте команду **Run**, чтобы запустить парсер.

После запуска бот обрабатывает настроенные страницы, пропускает уже известные или неподдерживаемые изображения и публикует новые в целевом Telegram-чате.

## Project Structure

```text
parser-bot/
├── app/
│   ├── core/
│   │   ├── exceptions.py
│   │   ├── keyboards.py
│   │   └── settings.py
│   ├── database/
│   │   ├── connection.py
│   │   └── repositories.py
│   ├── handlers/
│   │   ├── common.py
│   │   ├── connection.py
│   │   └── parser.py
│   ├── services/
│   │   ├── images.py
│   │   └── parser.py
│   ├── texts/
│   ├── utils/
│   │   ├── load.py
│   │   ├── progress_bar.py
│   │   ├── request.py
│   │   └── telegram.py
│   ├── bot.py
│   └── main.py
├── .env.example
├── domains.json
├── page_urls
├── skipped_urls
├── pyproject.toml
└── poetry.lock
```

## Design Decisions

- **Асинхронная обработка:** `httpx` и `aiogram` позволяют выполнять сетевые операции без блокировки основного цикла приложения.
- **Разделение ответственности:** логика парсинга, обработки изображений, работы с базой данных и взаимодействия с Telegram вынесена в отдельные модули.
- **Дедупликация:** проверка исходного URL и SHA-256 хеша позволяет избегать повторной обработки одинаковых изображений, в том числе доступных по разным адресам.
- **Конфигурация без изменения кода:** список страниц, правила извлечения изображений и параметры запуска задаются через файлы конфигурации и переменные окружения.
