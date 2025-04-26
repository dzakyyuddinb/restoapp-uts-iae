from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Data pemesanan (sebagai placeholder)
payments = []

# URL untuk Order Service dan User Service
ORDER_SERVICE_URL = "http://localhost:5003/orders"
USER_SERVICE_URL = "http://localhost:5001/users"

# Membuat endpoint u/ memproses pembayaran baru
@app.route('/payments', methods=['POST'])
def process_payment():
    data = request.get_json()
    order_id = data.get("order_id")
    user_id = data.get("user_id")
    amount = data.get("amount")

     #Validasi input
    if order_id is None or user_id is None or amount is None:
        return jsonify({"error": "order_id, user_id, dan amount wajib diisi"}), 400
    
    payment = {
        "id": len(payments) + 1,
        "order_id": order_id,
        "user_id": user_id,
        "amount": amount,
        "status": "paid" # status pembayaran
    }
    payments.append(payment)
    
    # Update status pembayaran di order service
    try:
        order_response = requests.put(f"{ORDER_SERVICE_URL}/{order_id}/payment", json={"payment-status": "paid"})
        order_response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Kesalahan memperbaharui pemesanan: {e}")
    
    # Update status pembayaran di user service
    try:
        user_response = requests.put(f"{USER_SERVICE_URL}/{user_id}/payment-status", json={"status": "paid"})
        user_response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Kesalahan memperbaharui pengguna: {e}")

    return jsonify({"message":"Pembayaran diproses", "payment_id": payment["id"]}), 201
    
# Membuat endpoint GET u/ cek status pembayaran
@app.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment_by_id(payment_id):
    # Mengambil data pembayaran berdasarkan id pembayaran
    payment = next((p for p in payments if p["id"] == payment_id), None)
    if not payment:
        return jsonify({"error": "Pembayaran tidak ditemukan"}), 404
    return jsonify(payment), 200

if __name__ == '__main__':
    app.run(port=5004, debug=True)