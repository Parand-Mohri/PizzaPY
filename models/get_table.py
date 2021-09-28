import mysql.connector

mydb = mysql.connector.connect(host= "localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()


def get_table(table_name):
    mycursor.execute(f"select * from {table_name} ")
    return f'{mycursor.fetchall()}'


def find_single_order(order_id):
    mycursor.execute(f"select * from orders where order_id = {order_id}")
    return f'{mycursor.fetchall()}'


def find_single_pizza(pizza_id):
    mycursor.execute(f"select * from pizza where pizza_id={pizza_id}")
    return f'{mycursor.fetchall()}'


def find_pizza_info(pizza_id):
    mycursor.execute(f"select pizzatopping.topping_id,topping.name,topping.price,"
                     f" pizzatopping.pizza_id from pizzatopping left join topping on "
                     f"pizzatopping.topping_id = topping.topping_id where pizza_id = {pizza_id}")
    return f'{mycursor.fetchall()}'
