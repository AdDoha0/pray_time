import asyncio
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

TZ = ZoneInfo("Europe/Moscow")
DATA_PATH = Path("data/pray_time.json")

def now_tz() -> datetime:
    return datetime.now(TZ)

def load_prayers_for_today() -> dict[str, str]:
    """Читает JSON и возвращает словарь prayer->'HH:MM' для сегодняшнего дня."""
    with DATA_PATH.open("r", encoding="utf-8") as f:
        obj = json.load(f)

    today = now_tz().date()
    if obj.get("month") != today.month:
        raise ValueError("Не найден месяц в pray_time.json")

    for day in obj["data"]:
        if day["day"] == today.day:
            return day["prayer"]

    raise ValueError("Не найден текущий день в pray_time.json")

def next_prayer_dt() -> tuple[str, datetime]:
    """
    Возвращает (название_молитвы, datetime её наступления в TZ).
    Если время молитвы уже прошло — пропускаем её и берём следующую.
    """
    prayers = load_prayers_for_today()  # {'fajr': '04:46', ...}
    today = now_tz().date()

    # превращаем в [(name, target_dt)], сортируем по времени
    schedule: list[tuple[str, datetime]] = []
    for name, hhmm in prayers.items():
        t = datetime.strptime(hhmm, "%H:%M").time()
        schedule.append((name, datetime.combine(today, t, tzinfo=TZ)))
    schedule.sort(key=lambda x: x[1])

    now = now_tz()
    for name, dt_target in schedule:
        if dt_target > now:
            return name, dt_target

    # Все молитвы на сегодня прошли — вернём первую молитву завтрашнего дня (ждём до завтра)
    first_name, first_time = sorted(prayers.items(), key=lambda x: x[1])[0]
    t = datetime.strptime(first_time, "%H:%M").time()
    tomorrow = today + timedelta(days=1)
    return first_name, datetime.combine(tomorrow, t, tzinfo=TZ)

async def wait_and_notify(send_coro):
    """
    Главный цикл: ждёт ближайшую молитву и вызывает send_coro(name, when_dt).
    send_coro — это ВАША асинхронная функция отправки (например, bot.send_message).
    """
    while True:
        name, when_dt = next_prayer_dt()
        delta = (when_dt - now_tz()).total_seconds()
        # Подстраховка от отрицательных/слишком маленьких значений
        await asyncio.sleep(max(0, delta))
        await send_coro(name, when_dt)
        # Подождём минуту, чтобы не сработать дважды, и пересчитаем расписание
        await asyncio.sleep(60)
