from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    existing_cust = Customer.query.filter_by(email=data['email']).first()
    if existing_cust:
        return jsonify({"Message":f"Customer Exist Already with Same Email","data":data})
    new_customer = Customer(name=data['name'], email=data['email'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'id': new_customer.id, 'name': new_customer.name, 'email': new_customer.email}), 201

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(description=data['description'], amount=data['amount'], customer_id=data['customer_id'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'id': new_order.id, 'description': new_order.description, 'amount': new_order.amount, 'customer_id': new_order.customer_id}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({'id': order.id, 'description': order.description, 'amount': order.amount, 'customer_id': order.customer_id})

@app.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return jsonify([{'id': order.id, 'description': order.description, 'amount': order.amount} for order in orders])

if __name__ == '__main__':
    app.run(debug=True)
