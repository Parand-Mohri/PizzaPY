import string
import random


def chek_order(menuItems):
    menuItems.sort()
    if menuItems[0] > 10:
        return False
    else:
        return True


discount_code_in_use=None
def discount_generator(size=6, chars=string.ascii_uppercase + string.digits):
    code =  ''.join(random.choice(chars) for _ in range(size))
    if(code in discount_code_in_use):
        code = discount_generator
    else:
        discount_code_in_use.append(code)
    return code

# def check_customerId(customer_id):
