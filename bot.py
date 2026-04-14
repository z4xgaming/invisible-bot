import os
import telebot
import random
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

user_limit = {}
global_count = 0
last_reset = datetime.now().day

DAILY_USER_LIMIT = 2
GLOBAL_LIMIT = 1000

invisible_chars = ["\u200b", "\u200c", "\u200d", "\u2060"]

def generate_name():
    return "".join(random.choice(invisible_chars) for _ in range(random.randint(6, 12)))

def reset():
    global user_limit, global_count, last_reset
    today = datetime.now().day
    if today != last_reset:
        user_limit = {}
        global_count = 0
        last_reset = today

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "🔥 Invisible Name Bot Ready!\nUse /name")

@bot.message_handler(commands=['name'])
def name(msg):
    global global_count
    reset()

    uid = msg.from_user.id

    if global_count >= GLOBAL_LIMIT:
        bot.send_message(msg.chat.id, "❌ Daily 1000 limit finished")
        return

    if user_limit.get(uid, 0) >= DAILY_USER_LIMIT:
        bot.send_message(msg.chat.id, "❌ Tumhari 2 names ki limit khatam")
        return

    n1 = generate_name()
    n2 = generate_name()

    user_limit[uid] = user_limit.get(uid, 0) + 2
    global_count += 2

    bot.send_message(msg.chat.id,
        f"🎮 Your Names:\n\n`{n1}`\n`{n2}`",
        parse_mode="Markdown"
    )

bot.polling()
