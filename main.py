import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import os
from dotenv import load_dotenv

# .env betöltése
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("✅ Yes, I’ve traded before", callback_data="yes"),
        InlineKeyboardButton("❌ No, I’m completely new", callback_data="no")
    )
    await message.answer(
        "Hey! 👋\n\nWelcome to the official Traderz Group bot – glad to have you here!\n\n"
        "📊 Have you ever traded on the forex/financial markets?\n\n👇 Choose one:",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "yes":
        await bot.send_message(callback_query.from_user.id,
            "Nice one! 💪\nAs an experienced trader, you know how much a high-quality entry and a clear plan matter.\n\n"
            "That’s exactly what you’ll get in our **VIP group**:\n\n"
            "✅ 2–5 premium signals daily\n✅ Full entries with SL & TP\n✅ XAUUSD and FX PAIRS\n"
            "✅ Live market updates & analysis\n✅ Clean, consistent system\n✅ Active, trader-focused community\n\n"
            "👇 If you’re ready to take it to the next level, start here:",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("🔗 Join the VIP Group", callback_data="vip")
            )
        )
    elif data == "no":
        await bot.send_message(callback_query.from_user.id,
            "No worries at all – everyone starts somewhere. 🙏\n\nOur VIP group is **not just signals** – it actually teache
