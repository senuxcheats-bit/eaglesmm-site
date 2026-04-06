import telebot
from telebot import types
import time
import random

TOKEN = "8613705529:AAEQnA8hy8wj9N-YFdvqpRDcH6Th1HX16AQ"
ADMIN_ID = 8163616038  # apna Telegram ID yahan dalo

bot = telebot.TeleBot(TOKEN)

user_step = {}
user_data = {}
orders = []

# START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Post Views", "❤️ Reactions", "👥 Members")
    
    bot.send_message(message.chat.id, "👋 Welcome!\nSelect service:", reply_markup=markup)
    user_step[message.chat.id] = "service"

# SERVICE SELECT
@bot.message_handler(func=lambda m: m.text in ["📊 Post Views", "❤️ Reactions", "👥 Members"])
def service_select(message):
    user_data[message.chat.id] = {"service": message.text}
    user_step[message.chat.id] = "link"
    
    bot.send_message(message.chat.id, "🔗 Apna Telegram post ya channel link bhejo:")

# HANDLE ALL
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    chat_id = message.chat.id
    
    if chat_id not in user_step:
        bot.send_message(chat_id, "❌ Pehle /start karo")
        return

    step = user_step[chat_id]

    # STEP 1: LINK
    if step == "link":
        if "t.me" not in message.text:
            bot.send_message(chat_id, "❌ Valid Telegram link bhejo")
            return
        
        user_data[chat_id]["link"] = message.text
        user_step[chat_id] = "quantity"
        
        bot.send_message(chat_id, "🔢 Quantity bhejo (e.g. 1000):")

    # STEP 2: QUANTITY
    elif step == "quantity":
        if not message.text.isdigit():
            bot.send_message(chat_id, "❌ Sirf number bhejo")
            return
        
        qty = int(message.text)
        user_data[chat_id]["quantity"] = qty
        
        service = user_data[chat_id]["service"]
        link = user_data[chat_id]["link"]

        order_id = random.randint(10000, 99999)

        bot.send_message(chat_id, f"🆔 Order ID: {order_id}\n🔄 Processing...")

        time.sleep(2)  # fake delay

        if service == "📊 Post Views":
            result = f"✅ {qty} Views Added (Fake)"
        elif service == "❤️ Reactions":
            result = f"❤️ {qty} Reactions Added (Fake)"
        elif service == "👥 Members":
            result = f"👥 {qty} Members Added (Fake)"

        bot.send_message(chat_id, f"{result}\n🔗 {link}")

        # SAVE ORDER
        orders.append({
            "id": order_id,
            "user": chat_id,
            "service": service,
            "qty": qty
        })

        # SEND TO ADMIN
        bot.send_message(ADMIN_ID, f"📥 New Order\nID: {order_id}\nUser: {chat_id}\nService: {service}\nQty: {qty}")

        user_step.pop(chat_id)
        user_data.pop(chat_id)

# ADMIN COMMAND
@bot.message_handler(commands=['orders'])
def show_orders(message):
    if message.chat.id != ADMIN_ID:
        return
    
    if not orders:
        bot.send_message(message.chat.id, "No orders yet")
        return
    
    text = "📊 Orders List:\n\n"
    for o in orders:
        text += f"ID: {o['id']} | {o['service']} | {o['qty']}\n"
    
    bot.send_message(message.chat.id, text)

print("Bot Running...")
bot.infinity_polling()