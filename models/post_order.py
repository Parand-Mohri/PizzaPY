import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(host= "localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()

def create_order(customer_id, menu_items, quantity,discount_code):
    mycursor.execute(f"insert into orders(customer_id, date) values ({customer_id}, '{datetime.now()}') ")
    mydb.commit()
    mycursor.execute(f"select numberofpizzas from customer where customer_id = {customer_id} ")
    if(mycursor.fetchone()[0] == 10):
        mycursor.execute(f"update customer set numberOfPizzas = 1 where customer_id = {customer_id}")
        #need to generate a discount code
    else:
        mycursor.execute(f"update customer set numberOfPizzas = numberOfPizzas +1 where customer_id = {customer_id}")
    mydb.commit()
    mycursor.execute("select order_id from orders order by order_id desc limit 1;")
    order_id = mycursor.fetchone()[0]
    for i in range(len(menu_items)):
        mycursor.execute(f"insert into orderitem (order_id, menuitem_id, quantity) values({order_id},{menu_items[i]}, {quantity[i]})")
    mydb.commit()


def create_customer(phoneNumber,name,numberOfPizzas,adress_id):
    mycursor.execute(f"insert into customer (phonenumber, name, numberofpizzas, adress_id) values({phoneNumber},'{name}', {numberOfPizzas}, {adress_id})")
    mydb.commit()


def create_adress(street, houseNumber, postcode):
    mycursor.execute(f"insert into adress(street, housenumber, postcode) values('{street}', {houseNumber}, '{postcode}');")
    mydb.commit()
    mycursor.execute(f"select adress_id from adress where postcode ='{postcode}'")
    return mycursor.fetchone()[0]



