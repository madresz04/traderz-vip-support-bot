import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Start gombos menü
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton("📈 Kapcsolat"), KeyboardButton("💸 Előfizetés"))

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "Üdv a Traderz VIP Support Botban! Válassz egy lehetőséget:",
        reply_markup=start_keyboard
    )

@dp.message_handler(lambda message: message.text == "📈 Kapcsolat")
async def contact_handler(message: types.Message):
    await message.answer("Írj az adminnak: @christtfxg")

@dp.message_handler(lambda message: message.text == "💸 Előfizetés")
async def subscription_handler(message: types.Message):
    await message.answer("Az előfizetéshez látogass el ide: https://traderzvip.hu")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
