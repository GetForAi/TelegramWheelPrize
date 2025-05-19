from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import threading

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Flask backend
app = Flask(__name__)
CORS(app)

BALANCE_FILE = 'balances.json'

def load_balances():
    if not os.path.exists(BALANCE_FILE):
        return {}
    with open(BALANCE_FILE, 'r') as f:
        return json.load(f)

def save_balances(data):
    with open(BALANCE_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/balance/<user_id>', methods=['GET'])
def get_balance(user_id):
    data = load_balances()
    return jsonify({'balance': data.get(user_id, 100)})

@app.route('/balance/<user_id>', methods=['POST'])
def update_balance(user_id):
    data = load_balances()
    json_data = request.get_json()
    amount = json_data.get('balance')
    data[user_id] = amount
    save_balances(data)
    return jsonify({'status': 'ok', 'balance': amount})

# Telegram bot
TOKEN = "8103404493:AAEa4xQG1hYW2XzJLYLxINqd1X7xTBsF5Y8"  # <-- Вставь сюда свой токен

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton(text="🎰 Открыть рулетку", web_app=WebAppInfo(url="https://telegram-wheel-prize.vercel.app"))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Нажми кнопку ниже, чтобы открыть рулетку:", reply_markup=reply_markup)

def run_telegram_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

# Запуск Flask и бота
if __name__ == '__main__':
    # запускаем телеграм-бота в отдельном потоке
    threading.Thread(target=run_telegram_bot).start()

    # запускаем Flask-сервер
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
