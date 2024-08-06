import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.path.join(os.getcwd(), 'database', 'users.db')

# Завантаження списку адміністраторів з .env
ADMIN_IDS = set(map(int, os.getenv("ADMIN_IDS").split(',')))

def init_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            date_added TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name, last_name=None):
    # Перевірка, чи користувач є адміністратором
    if user_id in ADMIN_IDS:
        return  # Не додавати адміністратора в базу даних

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Отримання поточного часу у форматі без мікросекунд
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO users (user_id, username, first_name, last_name, date_added)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, current_time))
    
    conn.commit()
    conn.close()

def user_exists(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def get_all_users():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    conn.close()
    return [user[0] for user in users]
