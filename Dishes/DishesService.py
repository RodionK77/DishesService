from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# dishes-services
#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rodionkasirin:@localhost:5432/items_db'
db = SQLAlchemy(app)


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)


def get_all_dishes_from_db():
    print(Dish.query.all())
    return Dish.query.all()


def get_dishes_by_id_from_db(dish_id):
    return Dish.query.get(dish_id)


def get_order_by_id_from_db(order_id):
    return Order.query.get(order_id)


def add_dish_to_db(new_dish):
    db.session.add(new_dish)
    db.session.commit()
    return True


def delete_dish_from_db(dish):
    db.session.delete(dish)
    db.session.commit()
    return True

def add_order(new_order):
    db.session.add(new_order)
    db.session.commit()
    return True


@app.route('/dishes', methods=['GET'])
def get_dishes():
    dishes = get_all_dishes_from_db()
    dish_list = [{'id': dish.id, 'name': dish.name, 'price': dish.price} for dish in dishes]
    return jsonify(dish_list)


@app.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    dish = get_dishes_by_id_from_db(dish_id)
    if dish is None:
        return jsonify({'error': 'Dish not found'}), 404

    return jsonify({'id': dish.id, 'name': dish.name, 'price': dish.price})


@app.route('/add_dish', methods=['POST'])
def create_dish():
    data = request.get_json()

    new_dish = Dish(name=data['name'], price=data['price'])
    if add_dish_to_db(new_dish):
        return jsonify({'id': new_dish.id, 'name': new_dish.name, 'price': new_dish.price})
    else:
        "Error"


@app.route('/del_dish/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    dish = get_dishes_by_id_from_db(dish_id)
    if dish is None:
        return jsonify({'error': 'Dish not found'}), 404

    if (delete_dish_from_db(dish)):
        return jsonify({'message': 'Dish deleted successfully'})
    else:
        return "Error"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)


def confirm_order(order_id, customer_id):
    order = get_order_by_id_from_db(order_id)
    # client = User.query.get(customer_id)
    if order:
        return f"Order {order_id} for client {customer_id} confirmed. Total price: {order['total_price']}"
    else:
        return f"Order {order_id} not found."


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/make_order', methods=['POST'])
def create_order():
    data = request.get_json()

    customer_id = data['customer_id']
    if not customer_id in [1, 2, 3]:
        return jsonify({'error': 'User not found'}), 404
    selected_dish_ids = data['dish_ids']

    total_price = 0
    for dish_id in selected_dish_ids:
        dish = get_dishes_by_id_from_db(dish_id)
        if dish:
            total_price += dish.price

    new_order = Order(customer_id=customer_id, total_price=total_price)
    if add_order(new_order):
        confirmation_message = confirm_order(new_order.id, customer_id)
        return jsonify({'confirmation_message': confirmation_message})
    else: return "Error"



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5015)
