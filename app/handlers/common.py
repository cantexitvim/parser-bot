from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.core.keyboards import menu
from app.texts.common import HELP, WELCOME

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        WELCOME.format(name=message.from_user.first_name),
        reply_markup=menu,
        parse_mode="HTML",
    )


@router.message(F.text == "Help")
async def help_handler(message: Message):
    await message.answer(
        HELP,
        parse_mode="HTML",
    )
