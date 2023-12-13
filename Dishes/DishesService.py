from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rodionkasirin:12345@postgres:5432/items_db'
db = SQLAlchemy(app)

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/dishes', methods=['GET'])
def get_dishes():
    dishes = Dish.query.all()
    dish_list = [{'id': dish.id, 'name': dish.name, 'price': dish.price} for dish in dishes]
    return jsonify(dish_list)

@app.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if dish is None:
        return jsonify({'error': 'Dish not found'}), 404

    return jsonify({'id': dish.id, 'name': dish.name, 'price': dish.price})

@app.route('/add_dish', methods=['POST'])
def create_dish():
    data = request.get_json()

    new_dish = Dish(name=data['name'], price=data['price'])
    db.session.add(new_dish)
    db.session.commit()

    return jsonify({'id': new_dish.id, 'name': new_dish.name, 'price': new_dish.price})

@app.route('/del_dish/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if dish is None:
        return jsonify({'error': 'Dish not found'}), 404

    db.session.delete(dish)
    db.session.commit()

    return jsonify({'message': 'Dish deleted successfully'})

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

def confirm_order(order_id, customer_id):
    order = Order.query.get(order_id)
    client = User.query.get(customer_id)
    if order:
        return f"Order {order_id} for client {client.name} confirmed. Total price: {order.total_price}"
    else:
        return f"Order {order_id} not found."

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/make_order', methods=['POST'])
def create_order():
    data = request.get_json()

    customer_id = data['customer_id']
    if not User.query.get(customer_id):
        return jsonify({'error': 'User not found'}), 404
    selected_dish_ids = data['dish_ids']

    total_price = 0
    for dish_id in selected_dish_ids:
        dish = Dish.query.get(dish_id)
        if dish:
            total_price += dish.price

    new_order = Order(customer_id=customer_id, total_price=total_price)
    db.session.add(new_order)
    db.session.commit()

    confirmation_message = confirm_order(new_order.id, customer_id)

    return jsonify({'confirmation_message': confirmation_message})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5015)
