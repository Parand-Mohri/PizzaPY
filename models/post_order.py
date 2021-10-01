import mysql.connector


mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()


def create_order(order):
    mycursor.execute(f"insert into orders(customer_id, date) values ({order.customer_id}, '{order.date}') ")
    mydb.commit()
    mycursor.execute("select order_id from orders order by order_id desc limit 1;")
    order.order_id = mycursor.fetchone()[0]
    for pizza in order.pizzas:
        mycursor.execute(f"select menuitem_id from menuItem where pizza_id = {pizza['pizza_id']}")
        menu_item = mycursor.fetchone()[0]
        quantity = pizza['quantity']
        mycursor.execute(f"insert into orderitem (order_id, menuitem_id, quantity) values({order.order_id},{menu_item},{quantity})")
        mydb.commit()

    for drink in order.drinks:
        mycursor.execute(f"select menuitem_id from menuItem where pizza_id = {drink['drink_id']}")
        menu_item = mycursor.fetchone()[0]
        quantity = drink['quantity']
        mycursor.execute(
            f"insert into orderitem (order_id, menuitem_id, quantity) values({order.order_id},{menu_item}, {quantity})")
        mydb.commit()

    for dessert in order.desserts:
        mycursor.execute(f"select menuitem_id from menuItem where pizza_id = {dessert['dessert_id']}")
        menu_item = mycursor.fetchone()[0]
        quantity = dessert['quantity']
        mycursor.execute(
            f"insert into orderitem (order_id, menuitem_id, quantity) values({order.order_id},{menu_item}, {quantity})")
        mydb.commit()

    return order


def create_customer(customer):
    mycursor.execute(
        f"insert into customer (phonenumber, name, adress_id) values({customer.phone_number},'{customer.name}', {customer.adress_id})")
    mydb.commit()
    mycursor.execute("select customer_id from customer order by customer_id desc limit 1;")
    customer.customer_id = mycursor.fetchone()[0]
    return customer


def create_adress(adress):
    mycursor.execute(
        f"insert into adress(street, houseNumber, postcode) values('{adress.street}', {adress.houseNumber}, '{adress.postcode}');")
    mydb.commit()
    mycursor.execute("select adress_id from adress order by adress_id desc limit 1;")
    adress.adress_id = mycursor.fetchone()[0]
    return adress


def check_discount_code(discount_code):
    mycursor.execute(f"select * from discount_code where discount_code = '{discount_code}'")
    if len(mycursor.fetchall())> 0:
        #disount_code exist
        discount_code_is_used(discount_code)
        return True
    else:
        return False


def discount_code_is_used(discount_code):
    mycursor.execute(f"delete from discount_code where discount_code = '{discount_code}'")
    mydb.commit()