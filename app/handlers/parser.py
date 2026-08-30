from aiogram import F, Router
from aiogram.types import Message

from app.core.settings import settings
from app.services.parser import parser

router = Router()


@router.message(F.text == "Run")
async def run_handler(message: Message):
    user_id = message.from_user.id

    if user_id not in settings.users:
        print(f"Unknown user {user_id}")
        await message.answer(f"Unknown user {message.from_user.username}")
        return

    await parser.run_parser()
