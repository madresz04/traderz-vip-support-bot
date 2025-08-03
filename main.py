from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, request
import os
import asyncio

# ─────────── BOT TOKEN ───────────
TOKEN = os.environ.get("BOT_TOKEN")

# ─────────── TELEGRAM HANDLEREK ───────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Yes, I’ve traded before", callback_data="yes")],
        [InlineKeyboardButton("❌ No, I’m completely new", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hey! 👋 Welcome to the official Traderz Group bot – glad to have you here!\n"
        "I’m Chris, founder of the group. 🚀\n\n"
        "Before we go any further, just a quick question:\n\n"
        "📊 Have you ever traded on the forex/financial markets?\n👇 Choose one:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "yes":
        keyboard = [[InlineKeyboardButton("🔗 Join the VIP Group", callback_data="vip")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=(
                "Nice one! 💪 As an experienced trader, you know how much a high-quality entry and a clear plan matter.\n\n"
                "That’s exactly what you’ll get in our **VIP group**:\n"
                "✅ 2–5 premium signals daily\n"
                "✅ Full entries with SL & TP\n"
                "✅ XAUUSD and FX PAIRS\n"
                "✅ Live market updates & analysis\n"
                "✅ Clean, consistent system\n"
                "✅ Active, trader-focused community\n\n"
                "👇 If you’re ready to take it to the next level, start here:"
            ),
            reply_markup=reply_markup
        )
    elif query.data == "no":
        keyboard = [[InlineKeyboardButton("🚀 I want to learn & earn", callback_data="vip")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=(
                "No worries at all – everyone starts somewhere. 🙏\n\n"
                "Our VIP group is **not just signals** – it actually teaches you while you earn. Here’s what you’ll get:\n"
                "✅ Easy-to-follow signals with SL & TP\n"
                "✅ Simple breakdowns of why we enter\n"
                "✅ Weekly summaries to track your learning\n"
                "✅ Supportive community – we’ve got your back\n\n"
                "👇 If that sounds good, let’s get started:"
            ),
            reply_markup=reply_markup
        )
    elif query.data == "vip":
        await query.edit_message_text(
            text=(
                "🔥 Ready to level up? The Traderz VIP isn’t just a signal group – it’s a full **trading ecosystem**.\n"
                "Daily entries, smart analysis, and a community that grows with you.\n\n"
                "🎯 Here’s what’s included:\n"
                "✅ 2–5 premium signals daily\n"
                "✅ XAUUSD and FX pairs\n"
                "✅ Risk management, psychology tips, education\n"
                "✅ Weekly breakdowns\n"
                "✅ Direct mentor access\n\n"
                "💼 How to join:\n"
                "1️⃣ Register with our trusted broker:\n"
                "🔗 [https://puvip.co/zqeM7r](https://puvip.co/zqeM7r)\n"
                "2️⃣ Make a minimum deposit of **350 USD** 💰\n"
                "👉 You keep full control of your funds – we don’t touch a cent\n"
                "3️⃣ ✅ **Claim your 50% deposit bonus** – available through this link only\n"
                "4️⃣ Send us your deposit screenshot or account number 📥\n"
                "We’ll activate your VIP access within minutes!\n\n"
                "Let’s stop watching others win – 👉 **Start winning yourself. Join VIP today.**"
            ),
            disable_web_page_preview=True
        )

# ─────────── FLASK + TELEGRAM ───────────
app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))

@app.route("/")
def index():
    return "✅ Bot is live on Render!"

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# ─────────── RENDER START ───────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    webhook_url = os.environ.get("RENDER_EXTERNAL_URL") + f"/{TOKEN}"
    asyncio.run(application.bot.set_webhook(webhook_url))
    app.run(host="0.0.0.0", port=port)
