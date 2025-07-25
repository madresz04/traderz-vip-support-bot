import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import os
from dotenv import load_dotenv

# Betöltjük a környezeti változókat
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Inicializáljuk a botot
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Naplózás
logging.basicConfig(level=logging.INFO)

# Üdvözlő üzenet gombokkal
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="✅ Yes, I’ve traded before", callback_data="yes"),
        InlineKeyboardButton(text="❌ No, I’m completely new", callback_data="no"),
        InlineKeyboardButton(text="🚀 VIP Info", callback_data="vip")
    )

    await message.answer(
        "👋 Hey, welcome to Traderz VIP Support!\n\n"
        "Have you ever traded before?", 
        reply_markup=keyboard
    )

# Callback-kezelő
@dp.callback_query_handler(lambda c: c.data in ["yes", "no", "vip"])
async def handle_callback(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "yes":
        response = "Nice! You're in the right place. Let me show you what we offer. 💼"
    elif data == "no":
        response = "No worries at all! We’ve got a full beginners’ guide ready for you. 📘"
    elif data == "vip":
        response = (
            "🚀 VIP Membership gives you:\n"
            "- Daily trade signals 📈\n"
            "- 1-on-1 mentorship 🧑‍🏫\n"
            "- Exclusive community access 👥\n\n"
            "Type /start again to return to the main menu."
        )

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, response)

    # Értesítés az adminnak
    await bot.send_message(
        ADMIN_ID,
        f"📩 {callback_query.from_user.full_name} ({callback_query.from_user.id}) "
        f"választott: {data.upper()}"
    )

# Futtatás
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
