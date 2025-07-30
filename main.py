import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

ADMIN_USERNAME = "@christtfxg"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("✅ Yes, I’ve traded before")],
        [KeyboardButton("❌ No, I’m completely new")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Hey! 👋 Welcome to the official Traderz Group bot – glad to have you here!
"
        "I’m Chris, founder of the group. 🚀

"
        "Before we go any further, just a quick question:

"
        "📊 Have you ever traded on the forex/financial markets?

👇 Choose one:",
        reply_markup=reply_markup
    )
    await notify_admin(f"👤 New user started the bot: @{update.effective_user.username}")

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    if "yes" in text.lower():
        await send_yes_response(update)
    elif "no" in text.lower():
        await send_no_response(update)
    elif "/vip" in text.lower():
        await send_vip_response(update)
    else:
        await update.message.reply_text("Please choose one of the options provided.")

async def send_yes_response(update: Update) -> None:
    keyboard = [[KeyboardButton("🔗 Join the VIP Group")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Nice one! 💪 As an experienced trader, you know how much a high-quality entry and a clear plan matter.
"
        "That’s exactly what you’ll get in our *VIP group*:

"
        "✅ 2–5 premium signals daily
"
        "✅ Full entries with SL & TP
"
        "✅ XAUUSD and FX PAIRS
"
        "✅ Live market updates & analysis
"
        "✅ Clean, consistent system
"
        "✅ Active, trader-focused community

"
        "👇 If you’re ready to take it to the next level, start here: /vip",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def send_no_response(update: Update) -> None:
    keyboard = [[KeyboardButton("🚀 I want to learn & earn")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "No worries at all – everyone starts somewhere. 🙏

"
        "Our VIP group is *not just signals* – it actually teaches you while you earn. Here’s what you’ll get:

"
        "✅ Easy-to-follow signals with SL & TP
"
        "✅ Simple breakdowns of why we enter
"
        "✅ Weekly summaries to track your learning
"
        "✅ Supportive community – we’ve got your back

"
        "👇 If that sounds good, let’s get started: /vip",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def send_vip_response(update: Update) -> None:
    await update.message.reply_text(
        "🔥 Ready to level up? The Traderz VIP isn’t just a signal group – it’s a full *trading ecosystem*.

"
        "Daily entries, smart analysis, and a community that grows with you.

"
        "🎯 Here’s what’s included:
"
        "✅ 2–5 premium signals daily
"
        "✅ XAUUSD and FX pairs
"
        "✅ Risk management, psychology tips, education
"
        "✅ Weekly breakdowns
"
        "✅ Direct mentor access

"
        "💼 How to join:
"
        "1️⃣ Register with our trusted broker: 🔗 [https://puvip.co/zqeM7r](https://puvip.co/zqeM7r)
"
        "2️⃣ Make a minimum deposit of *350 USD* 💰
"
        "3️⃣ ✅ *Claim your 50% deposit bonus* – available through this link only
"
        "4️⃣ Send us your deposit screenshot or account number 📥

"
        "Let’s stop watching others win – 👉 *Start winning yourself. Join VIP today.*",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def notify_admin(message: str) -> None:
    if ADMIN_USERNAME.startswith("@"):
        logger.info(f"ADMIN: {message}")
    else:
        logger.warning("Admin username not set properly.")

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable not set")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vip", send_vip_response))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    app.run_polling()

if __name__ == "__main__":
    main()