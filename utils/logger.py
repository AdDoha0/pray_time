import logging
import sys
from config import Config

def setup_logger():
    """Настройка логирования для бота"""
    
    # Определяем уровень логирования
    level = logging.DEBUG if Config.DEBUG else logging.INFO
    
    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Настраиваем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Удаляем существующие обработчики
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Файловый обработчик (если не в режиме отладки)
    if not Config.DEBUG:
        file_handler = logging.FileHandler('bot.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Настраиваем логгер aiogram
    aiogram_logger = logging.getLogger('aiogram')
    aiogram_logger.setLevel(logging.WARNING)
    
    return root_logger 