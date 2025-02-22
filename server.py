from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

USER_DATA_FILE = "users.json"

# Загружаем список пользователей при старте сервера
def load_users():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

# Сохраняем пользователей в файл
def save_users():
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

users = load_users()

@app.route("/update_user", methods=["POST"])
def update_user():
    """Добавляет нового пользователя"""
    data = request.json
    user_name = data.get("user_name")

    if user_name and user_name not in users:
        users.append(user_name)
        save_users()
        return jsonify({"message": "User added!"}), 200

    return jsonify({"error": "Invalid data or user already exists"}), 400

@app.route("/users", methods=["GET"])
def list_users():
    """Отображает HTML-страницу со списком пользователей"""
    user_list_html = "<br>".join(users)
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Holiarus - Пользователи</title>
        <meta http-equiv="refresh" content="5">  <!-- Автообновление каждые 5 секунд -->
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #222; color: white; text-align: center; }}
            h1 {{ color: #ff9800; }}
            .container {{ margin-top: 50px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Список игроков</h1>
            <p>Обновляется автоматически</p>
            <div>{user_list_html}</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == "__main__":
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)

    app.run(host="0.0.0.0", port=5000)
