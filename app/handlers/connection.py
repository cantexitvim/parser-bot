from aiogram import F, Router
from aiogram.types import Message

from app.core.keyboards import connect, menu

router = Router()


@router.message(F.text == "Connect")
async def connect_handler(message: Message):
    await message.answer(
        text="Choose the channel you want to connect:",
        reply_markup=connect,
    )


@router.message(F.chat_shared)
async def chat_selected(message: Message):
    await message.answer(
        f"User: {message.from_user.id}\nSelected chat: {message.chat_shared.chat_id}",
        reply_markup=menu,
    )
