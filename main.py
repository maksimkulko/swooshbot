import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import requests

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Токен вашего бота, который вы получили от BotFather
BOT_TOKEN = '7021832817:AAG6aE1YZx9Uj2AsDRwwoOpKARvCnHSDnFc'

# URL для получения курса юаня (можете использовать другой источник данных)
YUAN_EXCHANGE_RATE_URL = "https://api.exchangerate-api.com/v4/latest/CNY"
USD_EXCHANGE_RATE_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# Ваша комиссия
COMMISSION_RATE = 65

# Функция для получения текущего курса юаня
def get_yuan_exchange_rate():
    response = requests.get(YUAN_EXCHANGE_RATE_URL)
    data = response.json()
    return data["rates"]["USD"]
def get_byn_exchange_rate():
    response = requests.get(USD_EXCHANGE_RATE_URL)
    data = response.json()
    return data["rates"]["BYN"]

def get_rub_exchange_rate():
    response = requests.get(USD_EXCHANGE_RATE_URL)
    data = response.json()
    return data["rates"]["RUB"]

# Инициализируем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)

# Обработка введенных чисел
@dp.message()
async def process_number(message: types.Message):
    try:
        number = float(message.text)
        yuan_rate = get_yuan_exchange_rate()
        byn_rate = get_byn_exchange_rate()
        rub_rate = get_rub_exchange_rate()
        amount_in_rub = number * 14
        amount_in_usd = amount_in_rub / rub_rate
        final_amount = amount_in_usd + COMMISSION_RATE
        await message.reply(f"Сумма после конвертации и добавления комиссии: {final_amount:.0f} USD\nСумма в белорусских рублях: {round((final_amount*byn_rate),-1):.0f} BYN\nСумма в российских рублях: {round((final_amount*(rub_rate+7)),-2):.0f} RUB\nСумма в белорусских рублях + 10%: {round(((final_amount*byn_rate)*1.1),-1):.0f} BYN")
    except ValueError:
        await message.reply("Введите цену в юанях.")

# Запускаем бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
