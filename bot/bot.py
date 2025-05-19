from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("8103404493:AAFhKLIlBMeujxkTEporZWMjP36MgvpSWH0")  # безопасно через переменные окружения

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url="https://telegram-wheel-prize.vercel.app"))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Нажми кнопку ниже, чтобы запустить игру:", reply_markup=reply_markup)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
print("Bot started")
app.run_polling()
