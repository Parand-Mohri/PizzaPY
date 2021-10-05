from datetime import timedelta
import mysql.connector
import string
import random
from threading import Timer

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()


def create_order(order):
    mycursor.execute(f"insert into orders(customer_id, date) values ({order.customer_id}, '{order.date}') ")
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
    if number_of_pizzas > 9 and order.discount_code is None:
        order.discount_code = discount_generator()
    return order


def check_discount_code(discount_code):
    mycursor.execute(f"select * from discount_code where discount_code = '{discount_code}'")
    if len(mycursor.fetchall()) > 0:
        # disount_code exist
        return True
    else:
        return False


def discount_code_is_used(discount_code):
    mycursor.execute(f"delete from discount_code where discount_code = '{discount_code}'")
    mydb.commit()


def discount_generator(size=6, chars=string.ascii_uppercase + string.digits):
    code = ''.join(random.choice(chars) for _ in range(size))
    if check_discount_code(code):
        code = discount_generator()
    else:
        mycursor.execute(f"insert into discount_code(discount_code) values('{code}')")
        mydb.commit()
    return code


def finding_area_code(customer_id):
    mycursor.execute(f"select postcode from adress where adress_id = (select adress_ID from customer where customer_id = {customer_id})")
    postcode = mycursor.fetchone()[0]
    return postcode[0]


def calculating_estimated_delivery_time(order):
    mycursor.execute(
        f"select deliveryPerson_id from deliveryPerson where areacode = {finding_area_code(order.customer_id)} and availability = true")
    for dpi in mycursor:
        if order.deliveryperson_id is None:
            order.deliveryperson_id = dpi[0]
            t = Timer(300.0, delivery_person_to_not_available(dpi[0]), status_to_on_the_way(order))
            p = Timer(1200.0, status_to_done(order))
            t.start()
            p.start()
    if order.deliveryperson_id is not None:
        order.estimated_delivery_time = order.date + timedelta(minutes=20)
    else:
        mycursor.execute(
            f"select deliveryPerson_id from deliveryPerson where areacode = {finding_area_code(order.customer_id)}")
        order.deliveryperson_id = mycursor.fetchone()[0]
        d = Timer(300.0,status_to_on_the_way(order))
        d.start()
        t = Timer(1800.0, delivery_person_to_not_available(order.deliveryperson_id))
        t.start()
        p = Timer(3000.0, status_to_done(order))
        p.start()
        order.estimated_delivery_time = order.date + timedelta(minutes=50)


def delivery_person_to_available(deliveryperson_id):
    mycursor.execute(f"update deliveryperson set availability = True where deliveryPerson_id = {deliveryperson_id}")
    mydb.commit()


def delivery_person_to_not_available(deliveryperson_id):
    mycursor.execute(f"update deliveryperson set availability = False where deliveryPerson_id = {deliveryperson_id}")
    mydb.commit()
    t = Timer(1800.0, delivery_person_to_available(deliveryperson_id))
    t.start()


def status_to_on_the_way(order):
    if order.status == "in process":
        mycursor.execute(f"update orders set status = 'on the way' where order_id = {order.order_id}")
        mydb.commit()
        order.status = "on the way"


def status_to_done(order):
        mycursor.execute(f"update orders set status = 'done' where order_id = {order.order_id}")
        mydb.commit()
        order.status = "done"