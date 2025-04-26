from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menus.db'
db = SQLAlchemy(app)

# Model Menu
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

# Initialize database
with app.app_context():
    db.create_all()

# GET semua menu
@app.route('/menus', methods=['GET'])
def get_menus():
    menus = Menu.query.all()
    return jsonify([menu.to_dict() for menu in menus]), 200

# GET menu by id
@app.route('/menus/<int:menu_id>', methods=['GET'])
def get_menu_by_id(menu_id):
    menu = Menu.query.get(menu_id)
    if menu:
        return jsonify(menu.to_dict()), 200
    return jsonify({"message": "Menu tidak ditemukan."}), 404

# POST menu baru
@app.route('/menus', methods=['POST'])
def create_menu():
    data = request.json
    new_menu = Menu(
        name=data.get("name"),
        price=data.get("price"),
        stock=data.get("stock", 0)
    )
    db.session.add(new_menu)
    db.session.commit()
    return jsonify(new_menu.to_dict()), 201

# PUT update stock menu
@app.route('/menus/<int:menu_id>/update-stock', methods=['PUT'])
def update_stock(menu_id):
    menu = Menu.query.get(menu_id)
    if menu:
        data = request.json
        sold_quantity = data.get("sold_quantity")

        if sold_quantity is None or sold_quantity <= 0:
            return jsonify({"message": "Invalid quantity."}), 400
        
        if menu.stock >= sold_quantity:
            menu.stock -= sold_quantity
            db.session.commit()
            return jsonify({"message": "Stok berhasil diperbarui.", "stock": menu.stock}), 200
        else:
            return jsonify({"message": "Stok tersedia tidak mencukupi."}), 400
        
    return jsonify({"message": "Menu tidak ditemukan."}), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)
