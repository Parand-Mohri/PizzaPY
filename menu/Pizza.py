class Pizza():

    def __init__(self, pizza_id, name, price, price_with_VAT, vegetarian):
        self.pizza_id =pizza_id
        self.name = name
        self.price = price
        self. price_with_VAT =price_with_VAT
        self.vegetarian = vegetarian
        self.toppings = []

    def dictionary(self):
        return {
            "pizza_id":self.pizza_id,
            "name": self.name,
            "price": self.price,
            "price_with_VAT": self.price_with_VAT,
            "vegetarian": self.vegetarian,
            "toppings": self.toppings
        }