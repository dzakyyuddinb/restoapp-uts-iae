from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL untuk User Service dan Menu Service
USER_SERVICE_URL = "http://localhost:5001/users"
MENU_SERVICE_URL = "http://localhost:5002/menus"

# Data pemesanan (sebagai placeholder)
orders = []

# Membuat pemesanan baru
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    user_id = data.get('user_id')
    menu_ids = data.get('menu_ids')

    if not user_id or not menu_ids:
        return jsonify({"error": "User ID dan Menu IDs diperlukan"}), 400
    
    # Validasi Pengguna
    user_response = requests.get(f"{USER_SERVICE_URL}/{user_id}")
    if user_response.status_code != 200:
        return jsonify({"error": "Pengguna tidak ditemukan"}), 404
    user = user_response.json()

    # Validasi Menu dan Cek Stok
    menu_items = []
    total_price = 0.0
    for menu_id in menu_ids:
        menu_response = requests.get(f"{MENU_SERVICE_URL}/{menu_id}")
        if menu_response.status_code != 200:
            return jsonify({"error": f"Menu item {menu_id} tidak ditemukan"}), 404
        menu_item = menu_response.json()

        if menu_item["stock"] > 0:
            menu_items.append(menu_item)
            total_price += menu_item["price"]
            # Kurangi stok sebanyak 1 (simulasi pengurangan stok setelah pemesanan)
            menu_item["stock"] -= 1
            # Update stok di Menu Service
            requests.put(f"{MENU_SERVICE_URL}/{menu_id}/update-stock", json={"sold_quantity": 1})
        else:
            return jsonify({"error": f"Menu item {menu_id} kehabisan stok"}), 400

    # Membuat pemesanan
    order = {
        "id": len(orders) + 1,
        "user_id": user_id,
        "items": menu_items,
        "total_price": total_price,
        "status": "pending",  # Status awal adalah pending
        "created_at": "now"  # Bisa diganti dengan timestamp waktu pembuatan
    }
    orders.append(order)

    return jsonify(order), 201

# Mendapatkan detail pemesanan berdasarkan ID
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return jsonify({"error": "Pemesanan tidak ditemukan"}), 404
    return jsonify(order)

# Memperbarui status pembayaran pemesanan
@app.route('/orders/<int:order_id>/payment', methods=['PUT'])
def update_payment_status(order_id):
    data = request.get_json()
    payment_status = data.get('payment_status')

    if payment_status not in ["pending", "paid", "failed"]:
        return jsonify({"error": "Status pembayaran tidak valid"}), 400

    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return jsonify({"error": "Pemesanan tidak ditemukan"}), 404

    order['status'] = payment_status
    return jsonify(order)

if __name__ == '__main__':
    app.run(port=5003, debug=True)