from .database import get_connection

def register_or_update_user(user_id, username, first_name):
    """ثبت یا بروزرسانی اطلاعات کاربر"""
    conn = get_connection()
    cursor = conn.cursor()

    # بررسی کاربر
    cursor.execute("SELECT visit_count FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        # بروزرسانی تعداد مراجعات
        new_count = user[0] + 1
        cursor.execute("UPDATE users SET visit_count = ? WHERE user_id = ?", (new_count, user_id))
        conn.commit()
        conn.close()
        return f"خوش آمدید! شما {new_count} بار مراجعه کرده‌اید."
    else:
        # ثبت کاربر جدید
        cursor.execute("""
            INSERT INTO users (user_id, username, first_name, visit_count)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, first_name, 1))
        conn.commit()
        conn.close()
        return "اطلاعات شما ثبت شد."