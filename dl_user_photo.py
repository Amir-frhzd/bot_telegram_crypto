import sqlite3
import telebot
import os


# توکن بات تلگرام
TELEGRAM_BOT_TOKEN = "6538597472:AAHTi5cPJ9XMcnz3N4AWp6C4nV1K_kni1D0"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# اتصال به دیتابیس
db_path = "./bot_users.db"  # مسیر دیتابیس شما
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# گرفتن عکس از دیتابیس و ذخیره در سیستم
def download_photos():
    # خواندن تمام کاربران و عکس‌ها
    cursor.execute("SELECT user_id, photo FROM users WHERE photo IS NOT NULL")
    users = cursor.fetchall()

    if not users:
        print("هیچ عکسی در دیتابیس ثبت نشده است.")
        return

    for user_id, file_id in users:
        try:
            # دریافت اطلاعات فایل از تلگرام
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # ذخیره فایل عکس در سیستم
            photo_path = f"{user_id}_profile.jpg"  # نام فایل
            with open(photo_path, 'wb') as photo_file:
                photo_file.write(downloaded_file)

            print(f"عکس کاربر {user_id} ذخیره شد: {photo_path}")
        except Exception as e:
            print(f"خطا در دانلود عکس برای کاربر {user_id}: {e}")

# فراخوانی تابع برای دانلود عکس‌ها
download_photos()