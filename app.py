import mysql.connector
from flask import Flask, request, render_template, make_response, jsonify

from controller.orderController import chek_order
from models import get_table, post_order
from models.calculationPricePizza import calculate_price_pizza

app = Flask(__name__)


#Pizza & Menu
@app.route("/menu", methods=["GET"])
def get_menu():
    return get_table.get_table("pizza") + get_table.get_table("drink") + get_table.get_table("desert")


@app.route("/pizza", methods=["GET"])
def get_pizza():
    # for updating the proce for pizzas
    # calculate_price_pizza()
    return get_table.get_table("pizza")


@app.route("/drink", methods=["GET"])
def get_drink():
    return get_table.get_table("drink")


@app.route("/desert", methods=["GET"])
def get_desert():
    return get_table.get_table("desert")


@app.route("/pizza/<pizza_id>", methods=["GET"])
def get_pizza_info(pizza_id: int):

    related_topping = get_table.find_pizza_info(pizza_id)

    if len(related_topping) == 2:
        return make_response("pizza dose not exist!")
    else:
        return related_topping



#Order & Customer
@app.route("/orders/<order_id>")
def get_order(order_id: int):
    order = get_table.find_single_order(order_id)
    print(order)
    if (len(order )== 2):
        return make_response("order id does not exist!")
    else:
        return make_response(order, 200)


@app.route("/order", methods=["POST"])
def create_order():
    customer_id = request.json["customer_id"]
    menu_items = request.json["menu_items"]
    quantity = request.json["quantity"]
    discount_code = request.json["discount_code"]
    if chek_order(menu_items):
        post_order.create_order(customer_id=customer_id, menu_items= menu_items , quantity=quantity, discount_code= discount_code)
        return jsonify(request.json)
    else:
        return make_response({"error": f"you need to order atleast one pizza"})


@app.route("/customer", methods=["POST"])
def create_customer():
    street = request.json["street"]
    houseNumber = request.json["houseNumber"]
    postcode = request.json["postcode"]
    phone_number = request.json["phone_number"]
    name = request.json["name"]
    number_of_pizzas = 0
    adress_id = post_order.create_adress(street,houseNumber, postcode)
    post_order.create_customer(phone_number,name,number_of_pizzas,adress_id)
    return jsonify(request.json)





