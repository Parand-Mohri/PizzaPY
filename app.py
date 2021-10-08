import mysql.connector
from flask import Flask, request, render_template, make_response, jsonify
from flask_cors import CORS

from Order.Adress import Adress
from Order.Customer import Customer
from Order.Order import Order
from models import get_table, post_order, post_customer, put_cancel
from controller.discountController import check_discount_code, discount_code_is_used

from models.post_customer import find_singe_postcode, find_customer_id, check_customer_id

app = Flask(__name__)
CORS(app)



# Pizza & Menu
@app.route("/pizza", methods=["GET"])
def get_pizza():
    pizzas = get_table.get_pizzas()
    data = []
    for pizza in pizzas:
        data.append(pizza.dictionary())
    return jsonify(message='pizzas',
                   category='success',
                   data=data,
                   status=200)


@app.route("/drink", methods=["GET"])
def get_drink():
    drinks = get_table.get_drinks()
    data = []
    for drink in drinks:
        data.append(drink.dictionary())
    return jsonify(message='drinks',
                   category='success',
                   data=data,
                   status=200)


@app.route("/dessert", methods=["GET"])
def get_desert():
    deserts = get_table.get_deserts()
    data = []
    for desert in deserts:
        data.append(desert.dictionary())
    return jsonify(message='dessert',
                   category='success',
                   data=data,
                   status=200)


# Order & Customer
@app.route("/order", methods=["GET"])
def get_order():
    order_id = request.json["order_id"]
    order = get_table.find_single_order(order_id)
    print(order)
    if len(order) == 2:
        return make_response("order id does not exist!")
    else:
        return make_response(order, 200)


# this api is for testing for front part
@app.route("/all_orders", methods=["GET"])
def get_all_order():
    order = get_table.find_all_order()
    return make_response(order, 200)


@app.route("/purchase", methods=["POST"])
def create_order():
    order = Order(request.json["customer_id"], request.json["pizzas"], request.json["drinks"], request.json["desserts"], request.json["discount_code"])
    if len(order.pizzas) == 0:
        return make_response({"error": f"you need to order atleast one pizza"})
    if check_customer_id(order.customer_id):
        return make_response({"error": f"customer_id does not exist"})
    if order.discount_code is None:
        order = post_order.create_order(order)
        data = order.dictionary()
        if len(order.pizzas) == 0:
            return make_response({"error": f"you need to order atleast one pizza"}, 404)
        return jsonify(message='Order',
                       category='success',
                       data=data,
                       status=200)

    else:
        if not check_discount_code(order.discount_code):
            return make_response({"error": f"discount code not exist"})
        discount_code_is_used(order.discount_code)
        order = post_order.create_order(order)
        order.price = order.price - (order.price * (10 / 100))
        order.discount_code = None
        data = order.dictionary()
        return jsonify(message='Order',
                        category='success',
                        data=data,
                        status=200)


@app.route('/purchase', methods=['PUT'])
def cancel_order():
    order_id = request.json["order_id"]
    print(str(order_id))
    order = get_table.find_single_order(order_id)
    if len(order) == 2:
        return make_response("order id does not exist!")
    else:
        if put_cancel.check_cancel_order(order_id):
            put_cancel.cancel_order(order_id)
            return make_response("Order has been canceled")
        else:
            return make_response("Canceling time has been passed")


@app.route("/customer", methods=["POST"])
def create_customer():
    adress = Adress(request.json["street"], request.json["house_number"], request.json["postcode"])
    if not find_singe_postcode(adress.postcode):
        return make_response({"error": f"a customer with this postcode is aready exist with customer_id {find_customer_id(adress.postcode)}"}, 400)
    adress = post_customer.create_adress(adress)
    customer = Customer(request.json["customer_name"], adress.adress_id, request.json["phone_number"])
    customer = post_customer.create_customer(customer)
    data = customer.dictionary()
    return make_response(jsonify(message='customer',
                   category='success',
                   data=data), 200)








