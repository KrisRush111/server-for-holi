from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

USER_DATA_FILE = "users.json"

# Функция загрузки пользователей из файла
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Функция сохранения пользователей в файл
def save_users():
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Загружаем пользователей при старте сервера
users = load_users()

@app.route("/save_user", methods=["POST"])
def save_user():
    """Сохраняет нового пользователя"""
    data = request.json
    user_id = str(data.get("id"))  # Приводим ID к строке
    user_name = data.get("name")

    if user_id and user_name:
        if user_id not in users:  # Не изменяем имя, если уже есть
            users[user_id] = {"name": user_name, "crystals": 0, "keys": 0}
            save_users()
        return jsonify({"message": "User saved!"}), 200
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
    app.run(host="0.0.0.0", port=5000)
