import os
import random
from datetime import datetime

import requests
import telebot
from dotenv import load_dotenv

from constants import DAY, MONTH, KEYWORD_WHEN, KEYWORD_WEATHER, CITY

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

ILIA_ID = os.environ.get("ILIA_ID")
MY_ID = os.environ.get("MY_ID")
IRA_ID = os.environ.get("IRA_ID")
NASTYA = os.environ.get("NASTYA")


def calculate_time_until(target_date):
    now = datetime.now()
    remaining_time = target_date - now
    return remaining_time


def get_weather_in_city():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units="
        f"metric&lang=ru&appid={WEATHER_API_KEY}"
    )
    weather_data = requests.get(url).json()
    temperature = round(weather_data["main"]["temp"])
    weather_description = weather_data["weather"][0]["description"]

    update_time = datetime.fromtimestamp(weather_data["dt"])

    return (
        f"Погода в городе {CITY}:\nТемпература: {temperature}°C\nСостояние: "
        f"{weather_description}\nОбновлено: {update_time}"
    )


def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather_button = telebot.types.InlineKeyboardButton(KEYWORD_WEATHER)
    time_button = telebot.types.InlineKeyboardButton(KEYWORD_WHEN)
    keyboard.add(weather_button, time_button)
    return keyboard


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Приветствую! Используй кнопки ниже:",
                     reply_markup=create_keyboard())


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_full_name = message.from_user.first_name
    if message.from_user.last_name:
        user_full_name += f" {message.from_user.last_name}"
    if message.text == KEYWORD_WHEN:
        target_date = datetime(datetime.now().year, MONTH, DAY)
        if target_date < datetime.now():
            target_date = datetime(datetime.now().year + 1, MONTH, DAY)

        remaining_time = calculate_time_until(target_date)
        days, seconds = remaining_time.days, remaining_time.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        responses = (
            (
                f"До Геша осталось: {days} дней, {hours} часов и {minutes} "
                "минут. Берегите печень, она вам еще пригодится!"
            ),
            (
                f"До вашего Шерегеша осталось: {days} дней, {hours} часов и"
                f"{minutes} минут. Не убейтесь там, кожанные ублюдки."
            ),
            (
                f"Так, осталось: {days} дней, {hours} часов и {minutes} минут"
                "до Шерегеша! По желтому снегу не катать."
            ),
            (
                f"Надоели, осталось: {days} дней, {hours} часов и {minutes}"
                "минут."
            ),
            "А, не скажу",
            f"Осталось: {days} дней, {hours} часов и {minutes} минут.",
        )

        if message.from_user.id == int(ILIA_ID):
            response_message = (
                f"{message.from_user.first_name}, ты куда собрался,"
                "тебя жена отпустила?"
            )
        elif message.from_user.id == int(IRA_ID):
            response_message = (
                f"Моя королева, ты будешь пархать на склоне через: {days}"
                "дней, {hours} часов и {minutes} минут."
            )
        elif message.from_user.id == int(MY_ID):
            response_message = (
                f"Хозяин, вы поедите в Шерегеш через:"
                f"{days} дней, {hours} часов и {minutes} минут."
            )
        elif message.from_user.id == int(NASTYA):
            response_message = (
                f"В Геш через: {days} дней, {hours} часов и {minutes} минут,"
                f"{message.from_user.first_name}, учебные склоны ждут тебя,"
                "не забудь защиту."
            )
        else:
            response_message = random.choice(responses)

        bot.send_message(
            message.chat.id,
            response_message,
            reply_markup=create_keyboard()
        )

    elif message.text == KEYWORD_WEATHER:
        weather_info = get_weather_in_city()
        bot.send_message(
            message.chat.id,
            weather_info,
            reply_markup=create_keyboard()
        )
    # Раскоментируйте строку 137 для получения ID пользователей.
    # Необходимо для тех случаев когда ID пользователя скрыт и
    # ботом @userinfobot невозможно его определить
    # bot.send_message(MY_ID, f'ID пользователя: {message.from_user.id}')


bot.polling()
