from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import os

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = f"https://traderz-bot.onrender.com/webhook"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("✅ Yes, I’ve traded before")],
        [KeyboardButton("❌ No, I’m completely new")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Hey! 👋 Welcome to the official Traderz Group bot – glad to have you here! "
        "I’m Chris, founder of the group. 🚀\n\n"
        "📊 Have you ever traded on the forex/financial markets?\n👇 Choose one:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Yes" in text:
        await update.message.reply_text(
            "Nice one! 💪 As an experienced trader, you know how much a high-quality entry and a clear plan matter. "
            "That’s exactly what you’ll get in our **VIP group**:\n"
            "✅ 2–5 premium signals daily\n"
            "✅ Full entries with SL & TP\n"
            "✅ XAUUSD and FX PAIRS\n"
            "✅ Live market updates & analysis\n"
            "✅ Clean, consistent system\n"
            "✅ Active, trader-focused community\n\n"
            "👇 If you’re ready to take it to the next level, start here: /vip"
        )
    elif "No" in text:
        await update.message.reply_text(
            "No worries at all – everyone starts somewhere. 🙏\n"
            "Our VIP group is **not just signals** – it actually teaches you while you earn. Here’s what you’ll get:\n"
            "✅ Easy-to-follow signals with SL & TP\n"
            "✅ Simple breakdowns of why we enter\n"
            "✅ Weekly summaries to track your learning\n"
            "✅ Supportive community – we’ve got your back\n\n"
            "👇 If that sounds good, let’s get started: /vip"
        )
    elif "/vip" in text or "vip" in text.lower():
        await update.message.reply_text(
            "🔥 Ready to level up? The Traderz VIP isn’t just a signal group – it’s a full **trading ecosystem**. "
            "Daily entries, smart analysis, and a community that grows with you.\n\n"
            "🎯 Here’s what’s included:\n"
            "✅ 2–5 premium signals daily\n"
            "✅ XAUUSD and FX pairs\n"
            "✅ Risk management, psychology tips, education\n"
            "✅ Weekly breakdowns\n"
            "✅ Direct mentor access\n\n"
            "💼 How to join:\n"
            "1️⃣ Register with our trusted broker: 🔗 https://puvip.co/zqeM7r\n"
            "2️⃣ Make a minimum deposit of **350 USD** 💰\n"
            "3️⃣ ✅ **Claim your 50% deposit bonus** – available through this link only\n"
            "4️⃣ Send us your deposit screenshot or account number 📥\n\n"
            "👉 **Start winning yourself. Join VIP today.**"
        )
    else:
        await update.message.reply_text("Please select an option from the menu.")

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Root route just for testing Render uptime
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

# Webhook setup when server starts
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
