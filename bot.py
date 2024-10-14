import logging
import python_weather
import asyncio
import sys

from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,)

TOKEN = config("BOT_TOKEN")

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(
        "Hi, I'm a bot that determines the weather in the city you need.",
        reply_markup=ReplyKeyboardRemove(),
    )

async def getweather(city):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)        
        return f'''Temperature in {weather.region}: {weather.temperature} degrees Celsius,
Wind directions: {weather.wind_direction},
Wind speed: {weather.wind_speed} MPH, 
{weather.description}'''


@dp.message()
async def echo_handler(message: Message):
    weather = await getweather(message.text)
    await message.answer(
        weather,
        reply_markup=ReplyKeyboardRemove(),
    )

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())