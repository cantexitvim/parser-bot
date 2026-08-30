import asyncio
from typing import Iterator

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import BufferedInputFile, InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder, MediaType

from app.core.settings import settings


async def send_images(
    *, bot: Bot, images: list[tuple[bytes, str]], hashtag: str
) -> None:
    print("Sending images...")

    media_gen = get_media(images)

    for media in media_gen:
        while True:
            try:
                await bot.send_media_group(
                    chat_id=settings.target_chat_id,
                    media=MediaGroupBuilder(media=media, caption=hashtag).build(),
                )

                break
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)

    print("Images sended\n")


def get_media(images: list[tuple[bytes, str]]) -> Iterator[list[MediaType]]:
    ind = 0

    while ind < len(images):
        yield [
            InputMediaPhoto(
                media=BufferedInputFile(
                    img_bytes,
                    filename=f"image{ext}",
                )
            )
            for img_bytes, ext in images[ind : ind + 10]
        ]

        ind += 10
