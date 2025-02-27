from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Разрешаем запросы с фронтенда

USER_DATA_FILE = "users.json"

# Функция загрузки пользователей из файла
def load_users():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}  # Если файл повреждён, возвращаем пустой словарь
    return {}

# Функция сохранения пользователей в файл
def save_users():
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)  # Поддержка кириллицы

# Загружаем пользователей при старте сервера
users = load_users()

@app.route("/set_user", methods=["POST"])
def set_user():
    """Сохраняет или обновляет данные пользователя"""
    data = request.json
    user_id = str(data.get("user_id"))  # ID всегда строкой
    user_name = data.get("user_name")

    if user_id and user_name:
        # Если пользователя нет, создаём запись
        if user_id not in users:
            users[user_id] = {"name": user_name, "crystals": 0, "keys": 0}
        else:
            users[user_id]["name"] = user_name  # Обновляем имя без перезаписи ресурсов

        save_users()
        return jsonify({"message": "User data saved!"}), 200
    return jsonify({"error": "Invalid data"}), 400

@app.route("/get_user/<string:user_id>", methods=["GET"])
def get_user(user_id):
    """Возвращает данные пользователя"""
    user = users.get(user_id, {"name": "Гость", "crystals": 0, "keys": 0})
    return jsonify(user)

@app.route("/", methods=["GET"])
def home():
    """Проверка работы сервера"""
    return "Bot server is running!", 200

if __name__ == "__main__":
    # Если users.json не существует, создаём пустой файл
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump({}, file)

    app.run(host="0.0.0.0", port=5050, debug=True)
