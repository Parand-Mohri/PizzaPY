import mysql.connector

mydb = mysql.connector.connect(host= "localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()


def get_table(table_name):
    mycursor.execute(f"select * from {table_name} ")
    return f'{mycursor.fetchall()}'


def find_single_order(order_id):
    mycursor.execute(f"select * from orders where order_id = {order_id}")
    return f'{mycursor.fetchall()}'
