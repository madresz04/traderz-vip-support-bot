import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import FastAPI, Request
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.webhook.base import BaseWebhookServer

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL", "") + WEBHOOK_PATH

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
app = FastAPI()

# --- PÁRBESZÉDEK LOGIKÁJA ---
@dp.message(F.text)
async def handle_start(msg: types.Message):
    if msg.text == "/start":
        builder = InlineKeyboardBuilder()
        builder.button(text="✅ Yes, I've traded before", callback_data="yes")
        builder.button(text="❌ No, I'm completely new", callback_data="no")
        await msg.answer("Hey there 👋\n\nHave you traded before?", reply_markup=builder.as_markup())
    elif msg.text == "/vip":
        await msg.answer("🚀 Our VIP includes:\n- Live signals\n- Risk management support\n- Trade setups\n\n💵 Price: $50/month\n\nIf you're ready, type /buy")
    elif msg.text == "/buy":
        await msg.answer("Please proceed to payment via this link:\nhttps://your-payment-link.com")

# --- CALLBACK KEZELÉS ---
@dp.callback_query(F.data == "yes")
async def handle_yes(call: types.CallbackQuery):
    await call.message.edit_text("Awesome! We'll tailor the experience to your trading level. 💪")

@dp.callback_query(F.data == "no")
async def handle_no(call: types.CallbackQuery):
    await call.message.edit_text("No worries! We'll guide you through everything from scratch. 👶")

# --- WEBHOOK SETUP ---
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    print("Webhook set:", WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

# --- FastAPI-hoz kötött handler ---
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
