import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("📝 Info", callback_data="info"),
        InlineKeyboardButton("💬 Support", callback_data="support")
    )
    await message.answer("Üdvözöllek a Traderz VIP Support botban! 👋\nVálassz egy lehetőséget:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "info":
        await bot.send_message(callback_query.from_user.id, "📌 Ez egy automatikus válaszüzenet a Traderz VIP szolgáltatásról. További részletekért fordulj az adminhoz.")
    elif data == "support":
        await bot.send_message(callback_query.from_user.id, "🛠 Az admin hamarosan felveszi veled a kapcsolatot.")

    await bot.answer_callback_query(callback_query.id)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
