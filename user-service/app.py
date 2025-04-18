from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy data user dengan nomor telepon
users = [
    {"id": 1, "name": "Andi", "phone": "081234567890"},
    {"id": 2, "name": "Budi", "phone": "082345678901"}
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = {
        "id": len(users) + 1,
        "name": data.get("name"),
        "phone": data.get("phone")
    }
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(port=5001, debug=True)
