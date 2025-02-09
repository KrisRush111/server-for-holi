from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Хранение данных пользователей (в реальном приложении лучше использовать базу данных)
users = {}


@app.route("/save_user", methods=["POST"])
def save_user():
    data = request.json
    user_id = str(data.get("id"))  # Приводим ID к строке
    user_name = data.get("name")

    if user_id and user_name:
        users[user_id] = {"name": user_name, "crystals": 0, "keys": 0}
        return jsonify({"message": "User saved!"}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400


@app.route("/get_user/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id, {"name": "Гость", "crystals": 0, "keys": 0})
    return jsonify(user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
