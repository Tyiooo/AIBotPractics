import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.settings import settings
from app.handlers import router

async def main():
    bot = Bot(token=settings.TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit!')