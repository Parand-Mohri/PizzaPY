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


def find_singe_postcode(postcode):
    mycursor.execute(f"select * from adress where postcode = '{postcode}'")
    if mycursor.fetchone() == None:
        # postcode does not exist
        return True
    else:
        return False


def find_customer_id(postcode):
    mycursor.execute(f"select customer_id from customer where adress_id = (select adress_id from adress where postcode = '{postcode}')")
    return mycursor.fetchone()[0]


def check_customer_id(customer_id):
    mycursor.execute(f"select * from customer where customer_id={customer_id}")
    if mycursor.fetchone() == None:
        # customer_id does not exist
        return True
    else:
        return False