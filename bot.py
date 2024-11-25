import telebot
from dotenv import load_dotenv
import os
import time
import threading
from MODULES.price_checker import check_price_alerts

# ایمپورت توابع
from MODULES.user_management import register_or_update_user
from MODULES.price_checker import get_price, save_price_alert, check_price_alerts

# بارگذاری توکن و شناسه کانال
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def check_membership(user_id):
    """بررسی عضویت کاربر در کانال"""
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "نامشخص"
    first_name = message.from_user.first_name or "نامشخص"

    # بررسی عضویت
    if not check_membership(user_id):
        bot.send_message(message.chat.id, f"{CHANNEL_ID}برای استفاده از ربات، لطفاً عضو کانال ما شوید.")
        return

    # ثبت یا بروزرسانی کاربر
    response = register_or_update_user(user_id, username, first_name)
    bot.send_message(message.chat.id, response)

    # ارسال منوی اصلی
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("استعلام قیمت", "آلارم قیمت")
    bot.send_message(message.chat.id, "یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "استعلام قیمت")
def handle_price_check(message):
    bot.send_message(message.chat.id, "لطفاً نماد موردنظر خود را وارد کنید (مثال: BTC-USDT):")

@bot.message_handler(func=lambda message: message.text == "آلارم قیمت")
def handle_price_alert(message):
    bot.send_message(message.chat.id, "لطفاً نماد و قیمت موردنظر را به صورت زیر وارد کنید:\n\nBTC-USDT 30000", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if " " in text:
        # آلارم قیمت
        try:
            symbol, threshold_price = text.split()
            threshold_price = float(threshold_price)
            response = save_price_alert(user_id, symbol.upper(), threshold_price)
            bot.send_message(message.chat.id, response)
        except:
            bot.send_message(message.chat.id, "فرمت پیام اشتباه است!")
    else:
        # استعلام قیمت
        try:
            price = get_price(text.upper())
            bot.send_message(message.chat.id, f"قیمت {text.upper()} در حال حاضر: {price}")
        except:
            bot.send_message(message.chat.id, "نماد اشتباه است!")

# بررسی آلارم‌ها هر 2 دقیقه
def price_alert_checker():
    while True:
        check_price_alerts(bot)

if __name__ == "__main__":
    alert_thread =threading.Thread(target=price_alert_checker)
    alert_thread.start()
    print("BOT IS WORKING...")
    bot.polling()