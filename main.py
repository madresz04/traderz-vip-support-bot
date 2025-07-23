import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "7764705724:AAE_5U4kt5_iCe0B-m9Z_SRgYhMpS76mpgg"
ADMIN_USERNAME = "christtfxg"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Kapcsolatfelvétel 💬"))
    bot.send_message(message.chat.id,
                     "Szia! 👋 Ez a Traderz VIP Support bot.

Ha kérdésed van, kattints a gombra, és felvesszük veled a kapcsolatot!",
                     reply_markup=markup)
    notify_admin(f"📥 Új felhasználó indította el a botot:

👤 @{message.from_user.username or 'Nincs username'}
🆔 {message.from_user.id}")

@bot.message_handler(func=lambda message: message.text == "Kapcsolatfelvétel 💬")
def contact_request(message):
    bot.send_message(message.chat.id, "Köszönjük! Hamarosan jelentkezünk. 🔔")
    notify_admin(f"📨 Kapcsolatfelvételi kérés érkezett:

👤 @{message.from_user.username or 'Nincs username'}
🆔 {message.from_user.id}")

def notify_admin(text):
    try:
        bot.send_message(f"@{ADMIN_USERNAME}", text)
    except Exception as e:
        print("Nem sikerült üzenni az adminnak:", e)

bot.polling()
