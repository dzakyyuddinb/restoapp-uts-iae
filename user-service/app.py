from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Model User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    payment_status = db.Column(db.String(20), nullable=False, default='unpaid')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "payment_status": self.payment_status
        }

# Initialize database
with app.app_context():
    db.create_all()

# GET semua user
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# GET user by id
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "Pengguna tidak ditemukan"}), 404

# POST user baru
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data.get("name"),
        phone=data.get("phone"),
        payment_status="unpaid"
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# PUT update payment status user
@app.route('/users/<int:user_id>/payment-status', methods=['PUT'])
def update_payment_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Pengguna tidak ditemukan"}), 404

    data = request.get_json()
    status = data.get("status")
    if status not in ["pending", "paid", "failed"]:
        return jsonify({"error": "Status tidak valid"}), 400

    user.payment_status = status
    db.session.commit()
    return jsonify(user.to_dict()), 200

# DELETE user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Pengguna tidak ditemukan."}), 404

    data = request.get_json()
    confirm = data.get("confirm") if data else False
    if not confirm:
        return jsonify({"message": "Konfirmasi diperlukan untuk menghapus pengguna. Kirim 'confirm: true' di body."}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Pengguna dengan ID {user_id} berhasil dihapus."}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)
