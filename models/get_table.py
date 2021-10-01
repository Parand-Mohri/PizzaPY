import mysql.connector

from menu.Desert import Desert
from menu.Drink import Drink
from menu.Pizza import Pizza

mydb = mysql.connector.connect(host= "localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()


def get_pizzas():
    mycursor.execute(f"SELECT pizza_id, name, price, price_with_VAT, vegetarian from pizza;")
    cursor = mycursor.fetchall()
    pizzas = []
    for (pizza_id, name, price, price_with_VAT, vegetarian) in cursor:
        pizza = Pizza(pizza_id, name, price, price_with_VAT, vegetarian)
        get_topping(pizza)
        pizzas.append(pizza)
    return pizzas


def get_drinks():
    mycursor.execute(f"SELECT drink_id,name, price from drink;")
    drinks=[]
    for (drink_id,name, price) in mycursor:
        drinks.append(Drink(drink_id,name, price))
    return drinks


def get_deserts():
    mycursor.execute(f"SELECT desert_id,name, price from desert;")
    desert=[]
    for (desert_id,name, price) in mycursor:
        desert.append(Desert(desert_id,name, price))
    return desert


def find_single_order(order_id):
    mycursor.execute(f"select * from orders where order_id = {order_id}")
    return f'{mycursor.fetchall()}'


def find_single_pizza(pizza_id):
    mycursor.execute(f"select * from pizza where pizza_id={pizza_id}")
    return f'{mycursor.fetchall()}'


def find_pizza_info(pizza_id):
    mycursor.execute(f"select topping.name,topping.price,"
                     f" pizzatopping.pizza_id,topping.vegetarian from pizzatopping left join topping on "
                     f"pizzatopping.topping_id = topping.topping_id where pizza_id = {pizza_id}")
    return f'{mycursor.fetchall()}'


def get_topping(pizza):
    mycursor.execute(f"select topping.name from pizzatopping left join topping on pizzatopping.topping_id = topping.topping_id where pizza_id = {pizza.pizza_id}")
    for topping in mycursor:
        pizza.toppings.append(topping)