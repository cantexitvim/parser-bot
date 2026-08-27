from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import BufferedInputFile, InputMediaPhoto, Message

from app.core.settings import settings
from app.parser import Parser

bot = Bot(settings.token)
dp = Dispatcher()

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    print("Command /start")

    parser = Parser()

    img_lists = parser.run_parser()

    for imgs in img_lists:
        if not imgs:
            print("Nothing to send\n")
            continue

        print("Sending images...")

        media = [
            InputMediaPhoto(media=BufferedInputFile(img_bytes, filename="image.jpg"))
            for img_bytes in imgs
        ]

        await bot.send_media_group(chat_id=message.chat.id, media=media)

        print("Images sended\n")
