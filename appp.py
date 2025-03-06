import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Подключение к БД
conn = sqlite3.connect("subscriptions.db", check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы для подписок
cursor.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  name TEXT,
                  price REAL)''')
conn.commit()

# Добавление подписки
@app.route('/add', methods=['POST'])
def add_subscription():
    data = request.json
    user_id = data.get("user_id")
    name = data.get("name")
    price = data.get("price")
    if not user_id or not name or not price:
        return jsonify({"error": "Invalid data"}), 400
    cursor.execute("INSERT INTO subscriptions (user_id, name, price) VALUES (?, ?, ?)",
                   (user_id, name, price))
    conn.commit()
    return jsonify({"message": "Subscription added!"})

# Просмотр подписок
@app.route('/list', methods=['GET'])
def list_subscriptions():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    cursor.execute("SELECT name, price FROM subscriptions WHERE user_id = ?", (user_id,))
    subs = cursor.fetchall()
    return jsonify({"subscriptions": [{"name": name, "price": price} for name, price in subs]})

# Удаление подписки
@app.route('/delete', methods=['POST'])
def delete_subscription():
    data = request.json
    user_id = data.get("user_id")
    name = data.get("name")
    if not user_id or not name:
        return jsonify({"error": "Invalid data"}), 400
    cursor.execute("DELETE FROM subscriptions WHERE user_id = ? AND name = ?",
                   (user_id, name))
    conn.commit()
    return jsonify({"message": "Subscription deleted!"})

if __name__ == "__main__":
    app.run(debug=True)
