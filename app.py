import mysql.connector
from flask import Flask, request, render_template, make_response, jsonify

from Order.Adress import Adress
from Order.Customer import Customer
from Order.Order import Order
from menu.Pizza import Pizza
from models import get_table, post_order
from models.calculationPizza import calculate_pizza
from models.post_order import check_discount_code

app = Flask(__name__)


# Pizza & Menu
@app.route("/pizza", methods=["GET"])
def get_pizza():
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


# @app.route("/topping", methods=["GET"])
# def get_pizza_info():
#     pizza_id = request.json("pizza_id")
#     related_topping = get_table.find_pizza_info(pizza_id)
#
#     if len(related_topping) == 2:
#         return make_response("pizza dose not exist!")
#     else:
#         return related_topping


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
    if order.discound_code is None:
        order = post_order.create_order(order)
        data = order.dictionary()
        if len(order.pizzas) == 0:
            return make_response({"error": f"you need to order atleast one pizza"})
        else:
            return jsonify(message='customer',
                           category='success',
                           data=data,
                           status=200)
    else:
        if not check_discount_code(order.discound_code):
            return make_response({"error": f"discount code not exist"})
        order.price = order.price - (order.price * (10/100))
        order = post_order.create_order(order)
        data = order.dictionary()
        if len(order.pizzas) == 0:
            return make_response({"error": f"you need to order atleast one pizza"})
        else:
            return jsonify(message='customer',
                           category='success',
                           data=data,
                           status=200)


@app.route("/customer", methods=["POST"])
def create_customer():
    adress = Adress(request.json["street"], request.json["house_number"], request.json["postcode"])
    adress = post_order.create_adress(adress)
    customer = Customer(request.json["customer_name"], adress.adress_id, request.json["phone_number"])
    customer = post_order.create_customer(customer)
    data = customer.dictionary()

    return jsonify(message='customer',
                   category='success',
                   data=data,
                   status=200)
