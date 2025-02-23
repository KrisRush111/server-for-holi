from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Разрешаем запросы с любого домена

# Инициализация БД
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER UNIQUE,
                        user_name TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/set_username", methods=["POST"])
def set_username():
    data = request.json
    user_id = data.get("user_id")
    user_name = data.get("user_name")

    if not user_id or not user_name:
        return jsonify({"error": "Missing data"}), 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET user_name=?", (user_id, user_name, user_name))
    conn.commit()
    conn.close()

    return jsonify({"message": "Username saved"})

@app.route("/get_username/<int:user_id>")
def get_username(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"user_name": user[0]})
    else:
        return jsonify({"user_name": "Гость"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
