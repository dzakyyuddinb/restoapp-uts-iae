from flask import Flask, request, jsonify

app = Flask(__name__)

#dummy data menu
menus = [
    {"id": 1, "name": "Nasi Ayam Bakar", "price": 18000, "stock": 15},
    {"id": 2, "name": "Kwetiau Goreng", "price": 20000, "stock": 7}
]

@app.route('/menus', methods=['GET'])
def get_menus():
    return jsonify(menus), 200

@app.route('/menus/<int:menu_id>', methods=['GET'])
def get_menu_by_id(menu_id):
    menu = next((m for m in menus if m["id"] == menu_id), None)
    if menu:
        return jsonify(menu), 200
    return jsonify({"message": "Menu tidak ditemukan."}), 404

@app.route('/menus', methods=['POST'])
def create_menu():
    data = request.json
    new_menu = {
        "id": len(menus) + 1,
        "name": data.get("name"),
        "price": data.get("price"),
        "stock": data.get("stock", 0) #tambah stock default kalau tdk ada input
    }
    menus.append(new_menu)
    return jsonify(new_menu), 201

#route utk update stock
@app.route('/menus/<int:menu_id>/update-stock', methods=['PUT'])
def update_stock(menu_id):
    menu = next((m for m in menus if m["id"] == menu_id), None)
    if menu:
        data = request.json
        sold_quantity = data.get("sold_quantity")

        if sold_quantity is None or sold_quantity <= 0:
            return jsonify({"message": "Invalid quantity."}), 400
        
        if menu["stock"] >= sold_quantity:
            menu["stock"] -= sold_quantity
            return jsonify({"message": "Stok berhasil diperbarui.", "stock": menu["stock"]}), 200
        else:
            return jsonify({"message": "Stok tersedia tidak mencukupi."}), 400
        
    return jsonify({"message": "Menu tidak ditemukan."}), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)