import asyncio

from app.bot import bot, dp
from app.services.parser import parser

from .handlers import router


async def main():
    print("The application has started")

    await parser.init(bot)

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
