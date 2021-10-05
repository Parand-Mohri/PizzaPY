import mysql.connector

from models.post_order import delivery_person_to_available

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()


def check_cancel_order(order_id):
    mycursor.execute(f"select status from orders where order_id = {order_id}")
    order_status = mycursor.fetchone()[0]
    print(order_status)
    if order_status == "in process":
        return True
    else:
        return False


def cancel_order(order):
    mycursor.execute(f"UPDATE orders SET status = 'canceled' WHERE order_id = {order.order_id}")
    mydb.commit()
    order.status = "canceled"
    delivery_person_to_available(order.deliveryperson_id)









