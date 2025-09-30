import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class Config:
    """Класс для хранения конфигурации бота"""
    
    # Токен бота
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # Режим отладки
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # ID администратора
    ADMIN_ID = os.getenv("ADMIN_ID")
    
    # Проверка обязательных переменных
    @classmethod
    def validate(cls):
        """Проверяет наличие обязательных переменных окружения"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не найден в переменных окружения")
        
        if not cls.ADMIN_ID:
            print("Предупреждение: ADMIN_ID не установлен")
        
        return True 