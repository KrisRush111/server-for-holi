from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

USER_DATA_FILE = "users.json"


# Функция загрузки пользователей из файла
def load_users():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
                data = file.read().strip()
                return json.loads(data) if data else {}  # Проверка на пустой файл
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Ошибка загрузки users.json: {e}")
            return {}
    return {}


# Функция сохранения пользователей в файл
def save_users():
    try:
        with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)  # Поддержка кириллицы
    except IOError as e:
        logging.error(f"Ошибка сохранения users.json: {e}")


# Загружаем пользователей при старте сервера
users = load_users()


@app.route("/save_user", methods=["POST"])
def save_user():
    """Сохраняет нового пользователя"""
    data = request.json
    user_id = str(data.get("id"))  # ID всегда строкой
    user_name = data.get("name")

    if user_id and user_name:
        users[user_id] = users.get(user_id, {"crystals": 0, "keys": 0})  # Не перезаписываем
        users[user_id]["name"] = user_name  # Но обновляем имя
        save_users()
        logging.info(f"Пользователь {user_id} ({user_name}) сохранён.")
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
    # Если users.json не существует, создаём пустой файл
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump({}, file)

    logging.info("Сервер запущен на порту 5000")
    app.run(host="0.0.0.0", port=5000)