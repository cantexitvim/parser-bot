import asyncio

from app.bot import bot, dp, router


async def main():
    print("The application has started")

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
