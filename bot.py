import telebot
from telebot import types

TOKEN = "8613705529:AAEQnA8hy8wj9N-YFdvqpRDcH6Th1HX16AQ"
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Views", "❤️ Reactions", "👥 Members")

    bot.send_message(message.chat.id, "Service select karo:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["📊 Views", "❤️ Reactions", "👥 Members"])
def ask_link(message):
    user_data[message.chat.id] = message.text
    bot.send_message(message.chat.id, "🔗 Apna post / channel link bhejo:")

@bot.message_handler(func=lambda message: True)
def process_link(message):
    service = user_data.get(message.chat.id)

    if not service:
        bot.send_message(message.chat.id, "❌ Pehle /start karo")
        return

    link = message.text

    if service == "📊 Views":
        bot.send_message(message.chat.id, f"🔄 Processing...\n📊 1000 Views added on:\n{link}")
    
    elif service == "❤️ Reactions":
        bot.send_message(message.chat.id, f"🔄 Processing...\n❤️ 200 Reactions added on:\n{link}")
    
    elif service == "👥 Members":
        bot.send_message(message.chat.id, f"🔄 Processing...\n👥 50 Members added")

    user_data.pop(message.chat.id)

print("Bot Running...")
bot.infinity_polling()