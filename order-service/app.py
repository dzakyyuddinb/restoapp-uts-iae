from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

# Model Order
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    items = db.Column(db.PickleType, nullable=False)  # Menyimpan data item menu dalam format serializable
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": self.items,
            "total_price": self.total_price,
            "status": self.status,
            "created_at": self.created_at
        }

# Initialize database
with app.app_context():
    db.create_all()

# POST membuat pemesanan
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    menu_ids = data.get("menu_ids")

    if not user_id or not menu_ids:
        return jsonify({"error": "User ID dan Menu IDs diperlukan"}), 400

    user_response = requests.get(f"http://localhost:5001/users/{user_id}")
    if user_response.status_code != 200:
        return jsonify({"error": "Pengguna tidak ditemukan"}), 404
    user = user_response.json()

    menu_items = []
    total_price = 0.0
    for menu_id in menu_ids:
        menu_response = requests.get(f"http://localhost:5002/menus/{menu_id}")
        if menu_response.status_code != 200:
            return jsonify({"error": f"Menu item {menu_id} tidak ditemukan"}), 404
        menu_item = menu_response.json()

        if menu_item["stock"] > 0:
            menu_items.append(menu_item)
            total_price += menu_item["price"]
            menu_item["stock"] -= 1
            requests.put(f"http://localhost:5002/menus/{menu_id}/update-stock", json={"sold_quantity": 1})
        else:
            return jsonify({"error": f"Menu item {menu_id} kehabisan stok"}), 400

    order = Order(
        user_id=user_id,
        items=menu_items,
        total_price=total_price,
        created_at="now"
    )
    db.session.add(order)
    db.session.commit()

    return jsonify(order.to_dict()), 201

# GET pemesanan berdasarkan ID
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Pemesanan tidak ditemukan"}), 404
    return jsonify(order.to_dict()), 200

# PUT update status pembayaran
@app.route('/orders/<int:order_id>/payment', methods=['PUT'])
def update_payment_status(order_id):
    data = request.get_json()
    payment_status = data.get("payment_status")

    if payment_status not in ["pending", "paid", "failed"]:
        return jsonify({"error": "Status pembayaran tidak valid"}), 400

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Pemesanan tidak ditemukan"}), 404

    order.status = payment_status
    db.session.commit()
    return jsonify(order.to_dict()), 200

if __name__ == '__main__':
    app.run(port=5003, debug=True)
