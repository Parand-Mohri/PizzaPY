import mysql.connector

mydb = mysql.connector.connect(host= "localhost", user="root", passwd="", database="pizza")

mycursor = mydb.cursor()


def calculate_pizza():
    mycursor.execute(f"select pizza_id from pizza")
    pizza_ids =  [ int(i[0]) for i in mycursor.fetchall()]
    for pizza_id in pizza_ids:
        mycursor.execute(f"update pizza set price={get_topping_price(pizza_id)} where pizza_id = {pizza_id}")
        mydb.commit()
        mycursor.execute(f"update pizza set price_with_VAT={get_pizza_price_VAT(pizza_id)} where pizza_id = {pizza_id}")
        mydb.commit()
        mycursor.execute(f"update pizza set vegetarian={calculating_vegetarian(pizza_id)} where pizza_id = {pizza_id}")
        mydb.commit()


# pizza prices are built up from their ingredients, which have prices and each pizza has a 40% margin for profit.
def get_topping_price(pizza_id):
    mycursor.execute(f"select topping.price from pizzatopping left join topping on pizzatopping.topping_id = topping.topping_id where pizza_id = {pizza_id}")
    prices = [int(i[0]) for i in mycursor.fetchall()]
    return sum(prices) + (sum(prices) * (40/100))


# its price (including 9% VAT)
def get_pizza_price_VAT(pizza_id):
    mycursor.execute(f"select price from pizza where pizza_id = {pizza_id}")
    price = mycursor.fetchone()[0]
    return round(price + (price * (9 /100)), 2)


# whether the pizza is vegetarian or not based on its ingredients.
def calculating_vegetarian(pizza_id):
    mycursor.execute(
        f"select topping.vegetarian from pizzatopping left join topping on pizzatopping.topping_id = topping.topping_id where pizza_id = {pizza_id}")
    vegetarian = [int(i[0]) for i in mycursor.fetchall()]
    if 0 in vegetarian:
        return False;
    else:
        return True;
