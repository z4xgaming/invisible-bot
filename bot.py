import telebot
import random
import time
from datetime import datetime

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# ====== STORAGE ======
user_daily_count = {}
global_daily_count = 0
last_reset_day = datetime.now().day

DAILY_USER_LIMIT = 2
GLOBAL_LIMIT = 1000

# invisible characters (Free Fire style)
invisible_chars = ["\u200b", "\u200c", "\u200d", "\u2060"]

def generate_invisible_name():
    length = random.randint(6, 12)
    return "".join(random.choice(invisible_chars) for _ in range(length))

def reset_limits():
    global user_daily_count, global_daily_count, last_reset_day
    today = datetime.now().day
    if today != last_reset_day:
        user_daily_count = {}
        global_daily_count = 0
        last_reset_day = today

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id,
        "🔥 Invisible Name Bot Ready!\n\n"
        "Command: /name")

@bot.message_handler(commands=['name'])
def give_name(msg):
    global global_daily_count
    reset_limits()

    user_id = msg.from_user.id

    if global_daily_count >= GLOBAL_LIMIT:
        bot.send_message(msg.chat.id, "❌ Aaj ka 1000 limit khatam ho gaya")
        return

    if user_daily_count.get(user_id, 0) >= DAILY_USER_LIMIT:
        bot.send_message(msg.chat.id, "❌ Tumhari daily limit 2 names khatam ho gayi")
        return

    name1 = generate_invisible_name()
    name2 = generate_invisible_name()

    user_daily_count[user_id] = user_daily_count.get(user_id, 0) + 2
    global_daily_count += 2

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("📋 Copy Name 1", callback_data=name1),
        telebot.types.InlineKeyboardButton("📋 Copy Name 2", callback_data=name2)
    )

    bot.send_message(
        msg.chat.id,
        f"🎮 Your Invisible Names:\n\n`{name1}`\n`{name2}`",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.answer_callback_query(call.id, "Copied ✔️ (manually long press karke copy karo)")

bot.polling()
