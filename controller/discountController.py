import mysql.connector
import string
import random

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()


def check_discount_code(discount_code):
    mycursor.execute(f"select * from discount_code where discount_code = '{discount_code}'")
    if len(mycursor.fetchall()) > 0:
        # disount_code already exist
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