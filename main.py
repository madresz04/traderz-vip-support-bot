import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # pl.: "123456789"

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# 📌 GOMBOS VÁLASZOK
start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="✅ Yes, I’ve traded before")],
    [KeyboardButton(text="❌ No, I’m completely new")],
    [KeyboardButton(text="💎 VIP Info")]
], resize_keyboard=True)

followup_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📚 I want signals & help")],
    [KeyboardButton(text="💬 I have questions")],
], resize_keyboard=True)


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 Hey there! Welcome to Traderz VIP Support.\n\n"
        "Have you traded before?",
        reply_markup=start_keyboard
    )
    if ADMIN_ID:
        await bot.send_message(chat_id=ADMIN_ID, text=f"👤 New user: @{message.from_user.username} ({message.from_user.id})")


@dp.message(F.text == "✅ Yes, I’ve traded before")
async def handle_yes(message: Message):
    await message.answer(
        "Great! 👌 Then you’ll love what we offer.\n"
        "Are you looking for signals and support?",
        reply_markup=followup_keyboard
    )


@dp.message(F.text == "❌ No, I’m completely new")
async def handle_no(message: Message):
    await message.answer(
        "No worries at all! 👶 We’ll help you get started step by step.\n"
        "What would you like help with first?",
        reply_markup=followup_keyboard
    )


@dp.message(F.text == "💎 VIP Info")
async def handle_vip(message: Message):
    await message.answer(
        "💎 <b>VIP Membership Includes:</b>\n"
        "- Daily accurate signals 📈\n"
        "- Personal mentorship 🧠\n"
        "- 24/7 support 💬\n\n"
        "Want to get started? Let us know!"
    )


@dp.message(F.text == "📚 I want signals & help")
async def handle_signals(message: Message):
    await message.answer(
        "Awesome! 🚀 One of our admins will reach out to get you started.\n"
        "Make sure your messages are open for replies!"
    )
    if ADMIN_ID:
        await bot.send_message(chat_id=ADMIN_ID, text=f"📚 Signals requested by @{message.from_user.username}")


@dp.message(F.text == "💬 I have questions")
async def handle_questions(message: Message):
    await message.answer(
        "Sure thing! Just type your question here and an admin will reply shortly. 💬"
    )
    if ADMIN_ID:
        await bot.send_message(chat_id=ADMIN_ID, text=f"❓ User @{message.from_user.username} has a question.")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
