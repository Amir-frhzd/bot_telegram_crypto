import telebot
import requests
import os
import sqlite3
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

#بارگذاری مقادیر .env

load_dotenv()
Telegram_bot_token=os.getenv("Telegram_bot_token")

#اطلاعات کانال ها

CHANNEL_1='@arzmannn'

# تنظیمات بات 

bot = telebot.TeleBot(Telegram_bot_token)