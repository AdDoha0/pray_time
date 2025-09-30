import asyncio
from datetime import datetime
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv

from pray_time import wait_and_notify  

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Флаг для отслеживания активации
is_activated = False

async def send_prayer(chat_id: int, name: str, when_dt: datetime):
    text = f"⏰ Наступило время молитвы: {name.upper()} ({when_dt.strftime('%H:%M')} по Мск)"
    await bot.send_message(chat_id, text)

@dp.message()
async def activate(msg: Message):
    global is_activated
    
    if is_activated:
        await msg.answer("✅ Бот уже активирован и работает.")
        return
    
    is_activated = True
    asyncio.create_task(wait_and_notify(
        lambda name, when_dt: send_prayer(msg.chat.id, name, when_dt)
    ))
    await msg.answer("✅ Бот активирован. Буду присылать напоминания о молитвах сюда.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
