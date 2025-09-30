import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import Config
from utils.logger import setup_logger
from handlers import basic

async def main():
    """Основная функция запуска бота"""
    
    # Проверяем конфигурацию
    Config.validate()
    
    # Настраиваем логирование
    logger = setup_logger()
    logger.info("Запуск бота...")
    
    # Создаем бота с настройками по умолчанию
    bot = Bot(
        token=Config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Создаем диспетчер
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(basic.router)
    
    try:
        # Удаляем вебхуки (если есть) и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Бот успешно запущен!")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем") 