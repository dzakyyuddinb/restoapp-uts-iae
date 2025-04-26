from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
db = SQLAlchemy(app)

# Model Payment
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "status": self.status
        }

# Initialize database
with app.app_context():
    db.create_all()

# POST untuk memproses pembayaran
@app.route('/payments', methods=['POST'])
def process_payment():
    data = request.get_json()
    order_id = data.get("order_id")
    user_id = data.get("user_id")
    amount = data.get("amount")

    if not order_id or not user_id or not amount:
        return jsonify({"error": "order_id, user_id, dan amount wajib diisi"}), 400

    payment = Payment(
        order_id=order_id,
        user_id=user_id,
        amount=amount,
        status="paid"
    )
    db.session.add(payment)
    db.session.commit()

    try:
        order_response = requests.put(f"http://localhost:5003/orders/{order_id}/payment", json={"payment_status": "paid"})
        order_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Kesalahan memperbaharui pemesanan: {e}")

    try:
        user_response = requests.put(f"http://localhost:5001/users/{user_id}/payment-status", json={"status": "paid"})
        user_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Kesalahan memperbaharui pengguna: {e}")

    return jsonify({"message": "Pembayaran diproses", "payment_id": payment.id}), 201

# GET status pembayaran
@app.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment_by_id(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({"error": "Pembayaran tidak ditemukan"}), 404
    return jsonify(payment.to_dict()), 200

if __name__ == '__main__':
    app.run(port=5004, debug=True)
