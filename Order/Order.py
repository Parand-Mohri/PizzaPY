from datetime import datetime


class Order():
    def __init__(self,customer_id, pizzas, drinks, desserts,  discount_code):
        # deliveryperson_id, status, price,
        self.order_id = None
        self.customer_id =customer_id
        # self.deliveryperson_id = None
        self.date = datetime.now()
        # self.status = None
        # self.price =None
        self.discound_code =discount_code
        self.pizzas=pizzas
        self.drinks=drinks
        self.desserts=desserts

    def dictionary(self):
        return {
            "order_id" : self.order_id,
            "customer_id" : self.customer_id,
            # "deliveryperson_id":self.deliveryperson_id,
            "date": self.date,
            # "status":self.status,
            # "price":self.price,
            # "discount_code": self.discount_code,
            "desserts": self.desserts,
            "drinks":self.drinks,
            "desserts":self.desserts
        }