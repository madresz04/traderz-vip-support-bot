import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
import os

# Token és admin ID
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # Számként add meg Render Secretben pl. 123456789

# Gombok
yes_button = InlineKeyboardButton(text="✅ Yes, I’ve traded before", callback_data="yes")
no_button = InlineKeyboardButton(text="❌ No, I’m a beginner", callback_data="no")
vip_button = InlineKeyboardButton(text="💎 VIP Description", callback_data="vip")

keyboard = InlineKeyboardMarkup(inline_keyboard=[[yes_button], [no_button], [vip_button]])

# Logger
logging.basicConfig(level=logging.INFO)

# Bot és Dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# START parancs
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Welcome to Traderz VIP Support!\nChoose an option below:",
        reply_markup=keyboard
    )

# YES
@dp.message(Command("yes"))
async def yes_command(message: Message):
    await message.answer("Great! You're an experienced trader. 🔥")
    await notify_admin(f"✅ User @{message.from_user.username} ({message.from_user.id}) has traded before.")

# NO
@dp.message(Command("no"))
async def no_command(message: Message):
    await message.answer("No worries! We'll guide you step by step. 🧠")
    await notify_admin(f"❌ User @{message.from_user.username} ({message.from_user.id}) is a beginner.")

# VIP
@dp.message(Command("vip"))
async def vip_command(message: Message):
    await message.answer("💎 Our VIP gives you:\n\n✅ Daily Signals\n📊 Market Analysis\n🧠 Trader Support")
    await notify_admin(f"💎 VIP info was requested by @{message.from_user.username} ({message.from_user.id})")

# CALLBACK KEZELŐ
@dp.callback_query()
async def handle_callback(callback: CallbackQuery):
    data = callback.data
    user = callback.from_user

    if data == "yes":
        await callback.message.answer("Great! You're an experienced trader. 🔥")
        await notify_admin(f"✅ User @{user.username} ({user.id}) has traded before.")
    elif data == "no":
        await callback.message.answer("No worries! We'll guide you step by step. 🧠")
        await notify_admin(f"❌ User @{user.username} ({user.id}) is a beginner.")
    elif data == "vip":
        await callback.message.answer("💎 Our VIP gives you:\n\n✅ Daily Signals\n📊 Market Analysis\n🧠 Trader Support")
        await notify_admin(f"💎 VIP info was requested by @{user.username} ({user.id})")

    await callback.answer()

# Admin értesítés
async def notify_admin(text: str):
    if ADMIN_ID:
        try:
            await bot.send_message(chat_id=int(ADMIN_ID), text=text)
        except Exception as e:
            logging.error(f"Failed to send admin message: {e}")

# Fő függvény
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
