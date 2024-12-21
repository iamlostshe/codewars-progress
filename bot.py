'Основной файл запуска бота'

from os import getenv

import asyncio
from loguru import logger
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from handlers import routers
from utils import db


async def main() -> None:
    'Запуск бота'
    # Инициализируем файл для логов
    logger.add('log.log')

    # Получаем токен для бота из .env
    load_dotenv()
    TOKEN = getenv('BOT_TOKEN')

    # Инициализируем диспетчер и бота
    dp = Dispatcher()
    bot = Bot(TOKEN)

    # Подключаем роутеры
    for r in routers:
        logger.info('Include router: {} ...', r.name)
        dp.include_router(r)

    # Проверяем наличае бд
    await db.check_db()

    # Запускаем бота
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
