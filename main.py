import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 Napi Szignálok", callback_data="signals")],
        [InlineKeyboardButton("💬 Ügyfélszolgálat", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Szia! Válassz egy lehetőséget:", reply_markup=reply_markup)

# Gombnyomás kezelő
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "signals":
        await query.edit_message_text("📈 Itt kapod majd a legfrissebb Traderz VIP szignálokat!")
    elif query.data == "support":
        await query.edit_message_text("💬 Írd le az üzenetedet, és továbbítjuk az adminnak!")

# Üzenetkezelő (továbbítás adminnak)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != ADMIN_CHAT_ID:
        msg = f"📩 Új üzenet:\n\n👤 Felhasználó: @{update.effective_user.username or 'Nincs username'}\n🆔 ID: {update.effective_user.id}\n\n💬 Üzenet:\n{update.message.text}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)
        await update.message.reply_text("✅ Köszönjük! Az üzenetedet továbbítottuk az adminnak.")
    else:
        await update.message.reply_text("⛔ Ez a bot az ügyfelek kiszolgálására készült.")

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()
