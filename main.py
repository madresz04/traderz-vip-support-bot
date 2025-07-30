import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Render-en állítsd be ENV-ben

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# ----- GOMBSOROK -----
start_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Yes, I’ve traded before", callback_data="yes")],
    [InlineKeyboardButton(text="❌ No, I’m completely new", callback_data="no")]
])

vip_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔗 Join the VIP Group", callback_data="vip")],
])

learn_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚀 I want to learn & earn", callback_data="vip")],
])

# ----- PARANCSOK -----
@dp.message(F.text, F.text.in_("/start"))
async def cmd_start(message: Message):
    await message.answer(
        "Hey! 👋\n\n"
        "Welcome to the official Traderz Group bot – glad to have you here!\n"
        "I’m Chris, founder of the group. 🚀\n\n"
        "Before we go any further, just a quick question:\n\n"
        "📊 Have you ever traded on the forex/financial markets?\n\n"
        "👇 Choose one:",
        reply_markup=start_buttons
    )

@dp.callback_query(F.data == "yes")
async def handle_yes(callback_query):
    await bot.send_message(
        callback_query.from_user.id,
        "Nice one! 💪\n"
        "As an experienced trader, you know how much a high-quality entry and a clear plan matter.\n\n"
        "That’s exactly what you’ll get in our <b>VIP group</b>:\n\n"
        "✅ 2–5 premium signals daily\n"
        "✅ Full entries with SL & TP\n"
        "✅ XAUUSD and FX PAIRS\n"
        "✅ Live market updates & analysis\n"
        "✅ Clean, consistent system\n"
        "✅ Active, trader-focused community\n\n"
        "👇 If you’re ready to take it to the next level, start here:",
        reply_markup=vip_button
    )

@dp.callback_query(F.data == "no")
async def handle_no(callback_query):
    await bot.send_message(
        callback_query.from_user.id,
        "No worries at all – everyone starts somewhere. 🙏\n"
        "Our VIP group is <b>not just signals</b> – it actually teaches you while you earn.\n\n"
        "Here’s what you’ll get:\n\n"
        "✅ Easy-to-follow signals with SL & TP\n"
        "✅ Simple breakdowns of why we enter\n"
        "✅ Weekly summaries to track your learning\n"
        "✅ Supportive community – we’ve got your back\n\n"
        "👇 If that sounds good, let’s get started:",
        reply_markup=learn_button
    )

@dp.callback_query(F.data == "vip")
async def handle_vip(callback_query):
    await bot.send_message(
        callback_query.from_user.id,
        "🔥 Ready to level up?\n\n"
        "The Traderz VIP isn’t just a signal group – it’s a full <b>trading ecosystem</b>.\n"
        "Daily entries, smart analysis, and a community that grows with you.\n\n"
        "🎯 Here’s what’s included:\n\n"
        "✅ 2–5 premium signals daily\n"
        "✅ XAUUSD and FX pairs\n"
        "✅ Risk management, psychology tips, education\n"
        "✅ Weekly breakdowns\n"
        "✅ Direct mentor access\n\n"
        "💼 How to join:\n\n"
        "1️⃣ Register with our trusted broker:\n"
        "<a href='https://puvip.co/zqeM7r'>https://puvip.co/zqeM7r</a>\n\n"
        "2️⃣ Make a minimum deposit of <b>350 USD</b>\n"
        "💰 You keep full control of your funds – we don’t touch a cent\n\n"
        "3️⃣ ✅ <b>Claim your 50% deposit bonus</b> – available through this link only\n"
        "(Only valid for new accounts using our partner link)\n\n"
        "4️⃣ Send us your deposit screenshot or account number\n"
        "📥 We’ll activate your VIP access within minutes!\n\n"
        "Let’s stop watching others win –\n"
        "👉 <b>Start winning yourself. Join VIP today.</b>"
    )


# ----- WEBHOOK SETUP -----
async def on_startup(app):
    webhook_url = os.getenv("WEBHOOK_URL")
    await bot.set_webhook(webhook_url)

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
app.on_startup.append(on_startup)

if __name__ == "__main__":
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
