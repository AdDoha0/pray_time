from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

# Создаем роутер для базовых команд
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    user_name = message.from_user.first_name
    welcome_text = (
        f"Привет, {user_name}! 👋\n\n"
        "Я бот для расчета времени намаза.\n"
        "Используйте /help для получения списка команд."
    )
    await message.answer(welcome_text)

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "📋 <b>Доступные команды:</b>\n\n"
        "/start - Запуск бота\n"
        "/help - Список команд\n"
        "/about - О боте\n"
    )
    await message.answer(help_text, parse_mode="HTML")

@router.message(Command("about"))
async def cmd_about(message: Message):
    """Обработчик команды /about"""
    about_text = (
        "🤖 <b>О боте</b>\n\n"
        "Этот бот помогает узнать время намаза.\n"
        "Версия: 1.0\n"
        "Разработчик: @your_username"
    )
    await message.answer(about_text, parse_mode="HTML")

@router.message()
async def echo_handler(message: Message):
    """Обработчик всех остальных сообщений"""
    await message.answer(
        f"Получено сообщение: {message.text}\n"
        "Используйте /help для списка команд."
    ) 