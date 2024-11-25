import requests
from .database import get_connection

KUCOIN_API_URL = "https://api.kucoin.com/api/v1/market/orderbook/level1"

def get_price(symbol):
    """دریافت قیمت از API کوکوین"""
    response = requests.get(KUCOIN_API_URL, params={"symbol": symbol})
    data = response.json()
    if data["code"] == "200000":
        return float(data["data"]["price"])
    else:
        raise ValueError("خطا در دریافت قیمت")

def save_price_alert(user_id, symbol, threshold_price):
    """ذخیره آلارم قیمت برای کاربر"""
    conn = get_connection()
    cursor = conn.cursor()

    # بررسی تعداد آلارم‌های کاربر
    cursor.execute("SELECT COUNT(*) FROM price_alerts WHERE user_id = ?", (user_id,))
    count = cursor.fetchone()[0]

    if count >= 3:
        return "شما حداکثر سه آلارم فعال دارید!"

    # ذخیره آلارم جدید
    cursor.execute("""
        INSERT INTO price_alerts (user_id, symbol, threshold_price)
        VALUES (?, ?, ?)
    """, (user_id, symbol, threshold_price))
    conn.commit()
    conn.close()
    return "آلارم شما ثبت شد."

def check_price_alerts(bot):
    """بررسی آلارم‌های قیمت"""
    conn = get_connection()
    cursor = conn.cursor()

    # دریافت تمام آلارم‌ها
    cursor.execute("SELECT id, user_id, symbol, threshold_price FROM price_alerts")
    alerts = cursor.fetchall()

    for alert_id, user_id, symbol, threshold_price in alerts:
        try:
            price = get_price(symbol)
            if price <= threshold_price:
                bot.send_message(user_id, f"قیمت {symbol} به {price} رسید!")
                cursor.execute("DELETE FROM price_alerts WHERE id = ?", (alert_id,))
                conn.commit()
        except Exception as e:
            print(f"خطا در بررسی آلارم: {e}")

    conn.close()