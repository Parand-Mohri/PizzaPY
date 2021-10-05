import mysql.connector
from flask import Flask, request, render_template, make_response, jsonify
from flask_cors import CORS

from Order.Adress import Adress
from Order.Customer import Customer
from Order.Order import Order
from menu.Pizza import Pizza
from models import get_table, post_order, post_customer, put_cancel
from models.calculationPizza import calculate_pizza
from controller.discountController import check_discount_code, discount_code_is_used
from time import time, sleep


app = Flask(__name__)
CORS(app)



# Pizza & Menu
@app.route("/pizza", methods=["GET"])
def get_pizza():
    # t = Timer(5.0, hello)
    # t.start()  # after 30 seconds, "hello, world" will be printed
    # for updating the proce for pizzas
    # calculate_pizza()
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


@app.route("/desert", methods=["GET"])
def get_desert():
    deserts = get_table.get_deserts()
    data = []
    for desert in deserts:
        data.append(desert.dictionary())
    return jsonify(message='desert',
                   category='success',
                   data=data,
                   status=200)


# Order & Customer
@app.route("/order/<order_id>", methods=["GET"])
def get_order(order_id: int):
    order = get_table.find_single_order(order_id)
    print(order)
    if len(order) == 2:
        return make_response("order id does not exist!")
    else:
        return make_response(order, 200)


@app.route("/purchase", methods=["POST"])
def create_order():
    order = Order(request.json["customer_id"], request.json["pizzas"], request.json["drinks"], request.json["desserts"], request.json["discount_code"])
    if order.discount_code is None:
        order = post_order.create_order(order)
        data = order.dictionary()
        if len(order.pizzas) == 0:
            return make_response({"error": f"you need to order atleast one pizza"})
        return jsonify(message='customer',
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
        if len(order.pizzas) == 0:
            return make_response({"error": f"you need to order atleast one pizza"})
        else:
            return jsonify(message='customer',
                           category='success',
                           data=data,
                           status=200)


@app.route('/purchase/cancel/<order_id>', methods=['PUT'])
def cancel_order(order_id: int):
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
    adress = post_customer.create_adress(adress)
    customer = Customer(request.json["customer_name"], adress.adress_id, request.json["phone_number"])
    customer = post_customer.create_customer(customer)
    data = customer.dictionary()
    return jsonify(message='customer',
                   category='success',
                   data=data,
                   status=200)


# while True:
#     sleep(60 - time() % 60)






