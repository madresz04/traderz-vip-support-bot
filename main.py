import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "supersecretkey"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Üdvözlő üzenet
@dp.message(commands=["start"])
async def start_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("✅ Yes, I’ve traded before"))
    keyboard.add(types.KeyboardButton("❌ No, I’m a beginner"))
    keyboard.add(types.KeyboardButton("💎 What’s in VIP?"))
    await message.answer("Welcome to Traderz VIP Bot! 👋", reply_markup=keyboard)

# YES válasz
@dp.message(lambda msg: msg.text == "✅ Yes, I’ve traded before")
async def yes_handler(message: types.Message):
    await message.answer("Awesome! You're one step ahead. 💪")

# NO válasz
@dp.message(lambda msg: msg.text == "❌ No, I’m a beginner")
async def no_handler(message: types.Message):
    await message.answer("No worries! We’ll help you from scratch. 🚀")

# VIP válasz
@dp.message(lambda msg: msg.text == "💎 What’s in VIP?")
async def vip_handler(message: types.Message):
    await message.answer("VIP gives you access to:\n- Daily signals 📈\n- Private support 💬\n- Strategy sessions 📊")

# Webhook handler
async def on_startup(app: web.Application):
    await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET).register(app, path=WEBHOOK_PATH)
app.on_startup.append(on_startup)
setup_application(app, dp, bot=bot)

if __name__ == "__main__":
    web.run_app(app, port=10000)
