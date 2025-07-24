import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Start parancs kezelése
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or "Nincs felhasználónév"
    
    # Felhasználónak válasz küldése
    buttons = [[KeyboardButton("📩 Kérdés küldése")]]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Szia! 👋 Miben segíthetünk?", reply_markup=markup)
    
    # Admin értesítése
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📥 Új felhasználó indította a botot:\n👤 @{username}\n🆔 ID: {user_id}"
    )

# Gombnyomás (kérdésküldés) kezelése
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or "Nincs felhasználónév"
    text = update.message.text

    if text == "📩 Kérdés küldése":
        await update.message.reply_text("Írd be a kérdésed, és a csapatunk hamarosan válaszol! 📨")
    else:
        await update.message.reply_text("Köszönjük, továbbítottuk az üzeneted! ✅")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"💬 Új üzenet érkezett:\n👤 @{username}\n🆔 {user_id}\n📨 Üzenet: {text}"
        )

# Bot inicializálása
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot elindult...")
    app.run_polling()
