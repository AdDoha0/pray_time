import asyncio
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_date():
    now = datetime.now(ZoneInfo("Europe/Moscow")) 
    return now.date()


def get_current_time():
    now = datetime.now(ZoneInfo("Europe/Moscow")) 
    return now.time()


def get_pray_time():
    with open("data/pray_time.json", "r") as file:  
        pray_time = json.load(file)
        if get_current_date().month == pray_time["month"]:
            for day in pray_time["data"]:
                if day["day"] == get_current_date().day:
                    return day["prayer"]
        else:
            print("Не найден месяц")

def get_current_prayer_time():
    while True:
        current_time = get_current_time()
        pray_time = get_pray_time()
        for prayer, time in pray_time.items():
            if current_time < time:
                return prayer
        time.sleep(1)


def wait_for_prayer():
    prayers = get_pray_time()
    # преобразуем строки в объекты времени
    prayers = {name: datetime.strptime(t, "%H:%M").time() for name, t in prayers.items()}

    while True:
        now = get_current_time()
        for name, pray_time in prayers.items():
            if now.hour == pray_time.hour and now.minute == pray_time.minute:
                print(f"⏰ Наступило время молитвы: {name} ({pray_time})")
                return  
        time.sleep(30)  


wait_for_prayer()