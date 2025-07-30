import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# --- Állítsd be a TOKEN-t ---
TOKEN = "7764705724:AAE_5U4kt5_iCe0B-m9ZSRgYhMpS76mpgg"

# --- Admin értesítéshez Telegram ID ---
ADMIN_ID = "christtfxg"  # <- ezt írd át a saját vagy az ügyfél Telegram user ID-jére

# --- Gombok ---
def start_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, I’ve traded before", callback_data="yes"),
            InlineKeyboardButton("❌ No, I’m completely new", callback_data="no")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def vip_keyboard(from_callback=False):
    text = "🔗 Join the VIP Group" if from_callback else "🚀 I want to learn & earn"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data="vip")]
    ])

# --- Üzenetek ---
WELCOME_MESSAGE = (
    "Hey! 👋 Welcome to the official Traderz Group bot – glad to have you here! I’m Chris, founder of the group. 🚀\n\n"
    "Before we go any further, just a quick question:\n\n"
    "📊 Have you ever traded on the forex/financial markets?\n👇 Choose one:"
)

YES_MESSAGE = (
    "Nice one! 💪 As an experienced trader, you know how much a high-quality entry and a clear plan matter. "
    "That’s exactly what you’ll get in our *VIP group*:\n\n"
    "✅ 2–5 premium signals daily\n"
    "✅ Full entries with SL & TP\n"
    "✅ XAUUSD and FX PAIRS\n"
    "✅ Live market updates & analysis\n"
    "✅ Clean, consistent system\n"
    "✅ Active, trader-focused community\n\n"
    "👇 If you’re ready to take it to the next level, start here:"
)

NO_MESSAGE = (
    "No worries at all – everyone starts somewhere. 🙏\n\n"
    "Our *VIP group is not just signals* – it actually teaches you while you earn. Here’s what you’ll get:\n\n"
    "✅ Easy-to-follow signals with SL & TP\n"
    "✅ Simple breakdowns of why we enter\n"
    "✅ Weekly summaries to track your learning\n"
    "✅ Supportive community – we’ve got your back\n\n"
    "👇 If that sounds good, let’s get started:"
)

VIP_MESSAGE = (
    "🔥 Ready to level up? The Traderz VIP isn’t just a signal group – it’s a full *trading ecosystem*.\n\n"
    "🎯 Here’s what’s included:\n"
    "✅ 2–5 premium signals daily\n"
    "✅ XAUUSD and FX pairs\n"
    "✅ Risk management, psychology tips, education\n"
    "✅ Weekly breakdowns\n"
    "✅ Direct mentor access\n\n"
    "💼 How to join:\n"
    "1️⃣ Register with our trusted broker:\n"
    "🔗 [https://puvip.co/zqeM7r](https://puvip.co/zqeM7r)\n"
    "2️⃣ Make a minimum deposit of *350 USD* 💰\n"
    "You keep full control of your funds – we don’t touch a cent\n"
    "3️⃣ ✅ *Claim your 50% deposit bonus* – available through this link only\n"
    "(Only valid for new accounts using our partner link)\n"
    "4️⃣ Send us your deposit screenshot or account number 📥\n"
    "We’ll activate your VIP access within minutes!\n\n"
    "👉 *Start winning yourself. Join VIP today.*"
)

# --- Kezelők ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=start_keyboard())

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = query.from_user
    await query.answer()

    # Admin értesítés minden gombra
    msg = f"👤 @{user.username or user.full_name} ({user.id}) kattintott: /{data}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

    if data == "yes":
        await query.edit_message_text(YES_MESSAGE, reply_markup=vip_keyboard(True), parse_mode="Markdown")
    elif data == "no":
        await query.edit_message_text(NO_MESSAGE, reply_markup=vip_keyboard(), parse_mode="Markdown")
    elif data == "vip":
        await query.edit_message_text(VIP_MESSAGE, parse_mode="Markdown")

# --- Hibakezelés ---
async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please use the menu buttons. If you need help, type /start.")

# --- Főfüggvény ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))

    app.run_polling()
