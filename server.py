from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import threading
import requests
import time

app = Flask(__name__)
CORS(app)

USER_DATA_FILE = "users.json"
lock = threading.Lock()


# Функция загрузки пользователей из файла
def load_users():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("[ERROR] Ошибка чтения users.json. Используется пустой словарь.")
            return {}  # Если файл поврежден, возвращаем пустой словарь
    return {}


# Функция сохранения пользователей в файл
def save_users():
    with lock:  # Защита от одновременной записи
        try:
            with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(users, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Ошибка записи users.json: {e}")


# Загружаем пользователей при старте сервера
users = load_users()


@app.route("/save_user", methods=["POST"])
def save_user():
    data = request.json
    user_id = str(data.get("id"))
    user_name = data.get("name")

    if user_id and user_name:
        users[user_id] = users.get(user_id, {"crystals": 0, "keys": 0, "hlcoin": 0})
        users[user_id]["name"] = user_name
        save_users()
        return jsonify({"message": "User saved!"}), 200
    return jsonify({"error": "Invalid data"}), 400


@app.route("/get_user/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id, {"name": "Гость", "crystals": 0, "keys": 0, "hlcoin": 0})
    return jsonify(user)


@app.route("/save_progress", methods=["POST"])
def save_progress():
    data = request.json
    user_id = str(data.get("userId"))
    progress = data.get("progress")

    if not user_id or not isinstance(progress, dict):
        return jsonify({"error": "Invalid data"}), 400

    user = users.get(user_id, {})
    user["crystals"] = progress.get("crystals", user.get("crystals", 0))
    user["keys"] = progress.get("keys", user.get("keys", 0))
    user["hlcoin"] = progress.get("hlcoin", user.get("hlcoin", 0))
    users[user_id] = user

    save_users()
    return jsonify({"message": "Progress saved!"}), 200


@app.route("/get_progress/<string:user_id>", methods=["GET"])
def get_progress(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"crystals": 0, "keys": 0, "hlcoin": 0})
    return jsonify({
        "crystals": user.get("crystals", 0),
        "keys": user.get("keys", 0),
        "hlcoin": user.get("hlcoin", 0)
    })


@app.route("/", methods=["GET"])
def home():
    return "Bot server is running!", 200


# Функция пинга для предотвращения засыпания сервера
def ping_server():
    while True:
        try:
            requests.get("https://server-for-holi-111.onrender.com/")
            print("[INFO] Сервер пингуется для предотвращения засыпания.")
        except Exception as e:
            print(f"[ERROR] Ошибка при пинге: {e}")
        time.sleep(600)  # Пинг каждые 10 минут


if __name__ == "__main__":
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump({}, file)

    threading.Thread(target=ping_server, daemon=True).start()
    app.run(host="0.0.0.0", port=6000)
