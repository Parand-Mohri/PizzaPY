from datetime import timedelta

import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()


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