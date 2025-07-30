import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# ⛔ Itt írd be a tokenedet
TOKEN = "7764705724:AAE_5U4kt5_iCe0B-m9Z_SRgYhMpS76mpgg"

# Gombok
start_buttons = [["✅ Yes, I’ve traded before"], ["❌ No, I’m completely new"]]
vip_buttons = [["🔗 Join the VIP Group"], ["🚀 I want to learn & earn"]]

# Üdvözlő üzenet
WELCOME_TEXT = (
    "Hey! 👋 Welcome to the official Traderz Group bot – glad to have you here! I’m Chris, founder of the group. 🚀\n\n"
    "Before we go any further, just a quick question:\n\n"
    "📊 Have you ever traded on the forex/financial markets?\n👇 Choose one:"
)

# Válasz szövegek
YES_TEXT = (
    "Nice one! 💪 As an experienced trader, you know how much a high-quality entry and a clear plan matter. "
    "That’s exactly what you’ll get in our *VIP group*:\n\n"
    "✅ 2–5 premium signals daily\n✅ Full entries with SL & TP\n✅ XAUUSD and FX PAIRS\n"
    "✅ Live market updates & analysis\n✅ Clean, consistent system\n✅ Active, trader-focused community\n\n"
    "👇 If you’re ready to take it to the next level, start here: /vip"
)

NO_TEXT = (
    "No worries at all – everyone starts somewhere. 🙏 Our VIP group is *not just signals* – it actually teaches you while you earn.\n\n"
    "Here’s what you’ll get:\n✅ Easy-to-follow signals with SL & TP\n✅ Simple breakdowns of why we enter\n"
    "✅ Weekly summaries to track your learning\n✅ Supportive community – we’ve got your back\n\n"
    "👇 If that sounds good, let’s get started: /vip"
)

VIP_TEXT = (
    "🔥 Ready to level up? The Traderz VIP isn’t just a signal group – it’s a full *trading ecosystem*.\n\n"
    "🎯 Here’s what’s included:\n✅ 2–5 premium signals daily\n✅ XAUUSD and FX pairs\n"
    "✅ Risk management, psychology tips, education\n✅ Weekly breakdowns\n✅ Direct mentor access\n\n"
    "💼 How to join:\n"
    "1️⃣ Register with our trusted broker: 🔗 https://puvip.co/zqeM7r\n"
    "2️⃣ Make a minimum deposit of *350 USD* 💰\n"
    "3️⃣ ✅ *Claim your 50% deposit bonus* – available through this link only\n"
    "4️⃣ Send us your deposit screenshot or account number 📥\n\n"
    "Let’s stop watching others win – 👉 *Start winning yourself. Join VIP today.*"
)

# Start parancs
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=ReplyKeyboardMarkup(start_buttons, one_time_keyboard=True, resize_keyboard=True)
    )

# /vip parancs
async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        VIP_TEXT,
        parse_mode="Markdown"
    )

# Válaszüzenetek
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Yes" in text:
        await update.message.reply_text(
            YES_TEXT,
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(vip_buttons, one_time_keyboard=True, resize_keyboard=True)
        )
    elif "No" in text:
        await update.message.reply_text(
            NO_TEXT,
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(vip_buttons, one_time_keyboard=True, resize_keyboard=True)
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
