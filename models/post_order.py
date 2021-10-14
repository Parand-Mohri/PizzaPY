from datetime import timedelta
import mysql.connector
from threading import Timer
from controller.discountController import discount_generator

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()
mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")


def create_order(order):
    mycursor.execute(f"insert into orders(customer_id, date, status) values ({order.customer_id}, '{order.date}', '{order.status}') ")
    mydb.commit()
    mycursor.execute("select order_id from orders order by order_id desc limit 1;")
    order.order_id = mycursor.fetchone()[0]
    calculating_estimated_delivery_time(order)
    number_of_pizzas = 0
    for pizza in order.pizzas:
        mycursor.execute(f"select menuitem_id from menuItem where pizza_id = {pizza['pizza_id']}")
        menu_item = mycursor.fetchone()[0]
        quantity = pizza['quantity']
        number_of_pizzas = number_of_pizzas + quantity
        mycursor.execute(
            f"insert into orderitem (order_id, menuitem_id, quantity) values({order.order_id},{menu_item},{quantity})")
        mydb.commit()
        mycursor.execute(f"select price from pizza where pizza_id = {pizza['pizza_id']}")
        order.price = mycursor.fetchone()[0] * quantity

    for drink in order.drinks:
        mycursor.execute(f"select menuitem_id from menuItem where pizza_id = {drink['drink_id']}")
        menu_item = mycursor.fetchone()[0]
        quantity = drink['quantity']
        mycursor.execute(
            f"insert into orderitem (order_id, menuitem_id, quantity) values({order.order_id},{menu_item}, {quantity})")
        mydb.commit()
        mycursor.execute(f"select price from drink where drink_id = {drink['drink_id']}")
        order.price = order.price + (mycursor.fetchone()[0] * quantity)

    for dessert in order.desserts:
        mycursor.execute(f"select menuitem_id from menuItem where pizza_id = {dessert['dessert_id']}")
        menu_item = mycursor.fetchone()[0]
        quantity = dessert['quantity']
        mycursor.execute(
            f"insert into orderitem (order_id, menuitem_id, quantity) values({order.order_id},{menu_item}, {quantity})")
        mydb.commit()
        mycursor.execute(f"select price from desert where desert_id = {dessert['dessert_id']}")
        order.price = order.price + (mycursor.fetchone()[0] * quantity)
    mycursor.execute(f"update orders set price =({order.price}) where order_id = {order.order_id}")
    mydb.commit()
    if number_of_pizzas > 9 and order.discount_code is None:
        order.discount_code = discount_generator()
    return order


def finding_area_code(customer_id):
    mycursor.execute(f"select postcode from adress where adress_id = (select adress_ID from customer where customer_id = {customer_id})")
    postcode = mycursor.fetchone()[0]
    return postcode[0]


def calculating_estimated_delivery_time(order):
    mycursor.execute(
        f"select deliveryPerson_id from deliveryPerson where areacode = {finding_area_code(order.customer_id)} and availability = True")
    for dpi in mycursor:
        if order.deliveryperson_id == None:
            order.deliveryperson_id = dpi[0]
            mycursor.execute(f"update orders set deliveryperson_id ={order.deliveryperson_id} where order_id = {order.order_id}")
            mydb.commit()
            t = Timer(300.0, delivery_person_to_not_available, args=[dpi[0]])
            t1 = Timer(300.0, status_to_on_the_way, args=[order])
            t2 = Timer(1200.0, status_to_done, args=[order])
            t.start()
            t1.start()
            t2.start()
    if order.deliveryperson_id is not None:
        order.estimated_delivery_time = order.date + timedelta(minutes=20)
        mycursor.execute(
            f"update orders set estimated_delivery_time ='{order.estimated_delivery_time}' where order_id = {order.order_id}")
        mydb.commit()
    else:
        mycursor.execute(
            f"select deliveryPerson_id from deliveryPerson where areacode = {finding_area_code(order.customer_id)}")
        order.deliveryperson_id = mycursor.fetchone()[0]
        t3 = Timer(300.0, status_to_on_the_way, args=[order])
        t4 = Timer(1800.0, delivery_person_to_not_available, args=[order.deliveryperson_id])
        t5 = Timer(3000.0, status_to_done, args=[order])
        t3.start()
        t4.start()
        t5.start()
        order.estimated_delivery_time = order.date + timedelta(minutes=50)
        mycursor.execute(
            f"update orders set estimated_delivery_time ='{order.estimated_delivery_time}' where order_id = {order.order_id}")
        mydb.commit()


def delivery_person_to_available(deliveryperson_id):
    mycursor.execute(f"update deliveryperson set availability = True where deliveryPerson_id = {deliveryperson_id}")
    mydb.commit()


def delivery_person_to_not_available(deliveryperson_id):
    mycursor.execute(f"update deliveryperson set availability = False where deliveryPerson_id = {deliveryperson_id}")
    mydb.commit()
    t6 = Timer(1800.0, delivery_person_to_available, args=deliveryperson_id)
    t6.start()


def status_to_on_the_way(order):
    if order.status == "in process":
        mycursor.execute(f"update orders set status = 'on the way' where order_id = {order.order_id}")
        mydb.commit()
        order.status = "on the way"


def status_to_done(order):
        mycursor.execute(f"update orders set status = 'done' where order_id = {order.order_id}")
        mydb.commit()
        order.status = "done"