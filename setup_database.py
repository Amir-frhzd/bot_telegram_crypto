import sqlite3

# نام دیتابیس جدید
DATABASE_NAME = "bot_users.db"

# اتصال به دیتابیس (ایجاد فایل جدید در صورت عدم وجود)
conn = sqlite3.connect(DATABASE_NAME)

# ساخت Cursor برای اجرای دستورات SQL
cursor = conn.cursor()

# ساخت جدول users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    first_name TEXT,
    username TEXT,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    photo TEXT,
    visit_count INTEGER DEFAULT 1
)
''')

print(f"Database '{DATABASE_NAME}' and table 'users' created successfully.")

#ایجاد جدول هشدارهای قیمت
cursor.execute('''
CREATE TABLE IF NOT EXISTS
price_alerts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        threshold_price REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id))
''')

print(f"Database '{DATABASE_NAME}' and table 'price_alerts' created successfully.")

# ذخیره تغییرات و بستن اتصال
conn.commit()
conn.close()