import os
import random
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot

# 🔧 Настройки
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@yourchannel")  # заменишь на свой
POSTS_FILE = "posts.txt"

bot = Bot(token=BOT_TOKEN)

# 📦 Flask-приложение для Render
app = Flask(__name__)

# 📚 Чтение постов из файла
def get_random_post():
    try:
        with open(POSTS_FILE, "r", encoding="utf-8") as f:
            posts = [line.strip() for line in f if line.strip()]
            return random.choice(posts) if posts else None
    except Exception as e:
        print(f"Ошибка чтения постов: {e}")
        return None

# 🚀 Отправка поста в канал
def post_to_channel():
    message = get_random_post()
    if message:
        try:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
            print(f"✅ Отправлено: {message}")
        except Exception as e:
            print(f"❌ Ошибка отправки: {e}")

# ⏰ Планировщик
scheduler = BackgroundScheduler()
scheduler.add_job(post_to_channel, "interval", minutes=60)  # раз в час
scheduler.start()

# 🌐 Заглушка для Render
@app.route('/')
def index():
    return "Philosophical bot is running."

# 🔁 Старт Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
