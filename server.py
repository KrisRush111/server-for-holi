from flask import Flask, request, jsonify

app = Flask(__name__)

# Временное хранилище пользователей
users = {}

@app.route("/update_user", methods=["POST"])
def update_user():
    """Обновляет данные пользователя."""
    data = request.json
    user_id = data.get("user_id")
    user_name = data.get("user_name")

    if not user_id or not user_name:
        return jsonify({"error": "Missing user_id or user_name"}), 400

    users[user_id] = user_name
    print(f"✅ Данные обновлены: {user_id} - {user_name}")

    return jsonify({"status": "success", "user_id": user_id, "user_name": user_name})

@app.route("/get_user", methods=["GET"])
def get_user():
    """Возвращает данные о пользователе."""
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    user_name = users.get(int(user_id))

    if not user_name:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user_id": user_id, "user_name": user_name})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
