import mysql.connector
from flask import Flask, request, render_template, make_response, jsonify
from flask_cors import CORS

from Order.Adress import Adress
from Order.Customer import Customer
from Order.Order import Order
from models import get_table, post_order, post_customer, put_cancel
from controller.discountController import check_discount_code, discount_code_is_used
from models.get_table import find_single_order, get_order_info

from models.post_customer import find_singe_postcode, find_customer_id, check_customer_id
from models.put_cancel import check_cancel_order

app = Flask(__name__)
CORS(app)


# Pizza & Menuz
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
@app.route("/purchase/<order_id>", methods=["GET"])
def get_order(order_id: int):
    # print(request.args[])
    # return True
    # order_id = request.args

    if find_single_order(order_id):
        return make_response(jsonify(message='Order id does not exist!',
                       category='error'))

    else:
        order = get_order_info(order_id)
        data = order.dictionary()
        return jsonify(message='OrderInfo',
                       category='success',
                       data=data,
                       status=200)


# this api is for testing for front part
@app.route("/all_orders", methods=["GET"])
def get_all_order():
    order = get_table.find_all_order()
    return make_response(order, 200)


@app.route("/purchase", methods=["POST"])
def create_order():
    order = Order(request.json["customer_id"], request.json["pizzas"], request.json["drinks"], request.json["desserts"],
                  request.json["discount_code"])
    if len(order.pizzas) == 0:
        return make_response(jsonify(message='You need to order at least one pizza!',
                                     category='error'))
    if check_customer_id(order.customer_id):
        return make_response(jsonify(message='Customer_id does not exist',
                                     category='error'))
    if order.discount_code is None:
        order = post_order.create_order(order)
        data = order.dictionary()
        if len(order.pizzas) == 0:
            return make_response(jsonify(message='You need to order at least one pizza!',
                                         category='error'))
        return jsonify(message='Order',
                       category='success',
                       data=data,
                       status=200)

    else:
        if not check_discount_code(order.discount_code):
            return make_response(jsonify(message='Discount code not exist',
                                         category='error'))
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
    order_id = request.json["purchase_id"]
    if find_single_order(order_id):
        return make_response(jsonify(message='Order id does not exist!',
                                     category='error',
                                     ))
    else:
        if check_cancel_order(order_id):
            put_cancel.cancel_order(order_id)
            return make_response(jsonify(message='Order has been canceled',
                                         category='success',
                                         ))
        else:
            return make_response(jsonify(message='Canceling time has been passed',
                                         category='error',
                                         ))


@app.route("/customer", methods=["POST"])
def create_customer():
    adress = Adress(request.json["street"], request.json["house_number"], request.json["postcode"])
    if not find_singe_postcode(adress.postcode):
        return make_response(jsonify(message=f"a customer with this postcode is already exist with customer_id {find_customer_id(adress.postcode)}",
                                     category='error',
                                     ))
    adress = post_customer.create_adress(adress)
    customer = Customer(request.json["customer_name"], adress.adress_id, request.json["phone_number"])
    customer = post_customer.create_customer(customer)
    data = customer.dictionary()
    return make_response(jsonify(message='customer',
                                 category='success',
                                 data=data), 200)
