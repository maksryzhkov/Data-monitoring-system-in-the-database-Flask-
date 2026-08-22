import sqlite3
import os

os.makedirs('instance', exist_ok=True)
db_path = os.path.join('instance', 'test_data.db')

# Удаляем старую БД, если она есть
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. ИДЕАЛЬНАЯ ТАБЛИЦА (без пропусков)
cursor.execute('''
CREATE TABLE clean_products (
    id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL
)
''')
cursor.executemany('INSERT INTO clean_products VALUES (?, ?, ?, ?)', [
    (1, 'Ноутбук', 85000.0, 'Электроника'),
    (2, 'Мышь', 1500.0, 'Электроника'),
    (3, 'Клавиатура', 3000.0, 'Электроника'),
    (4, 'Монитор', 25000.0, 'Электроника')
])

# 2. ГРЯЗНАЯ ТАБЛИЦА (много NULL-значений)
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT,
    phone TEXT
)
''')
cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', [
    (1, 'alex_dev', 'alex@example.com', '+79990001122'),
    (2, 'vasiliy_analyst', None, '+79990003344'),
    (3, 'pavel_admin', 'pavel@example.com', None),
    (4, 'guest_user', None, None)
])

# 3. КРИТИЧЕСКАЯ ТАБЛИЦА (почти все данные битые)
cursor.execute('''
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    status TEXT
)
''')
cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?)', [
    (101, 1, 1500.0, 'COMPLETED'),
    (102, 2, None, 'PENDING'),
    (103, 3, None, None),
    (104, 4, None, None)
])

conn.commit()
conn.close()
print("Тестовая БД успешно пересоздана в instance/test_data.db!")