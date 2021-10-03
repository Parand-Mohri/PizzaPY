from datetime import datetime


class Order():
    def __init__(self, customer_id, pizzas, drinks, desserts,  discount_code_recive):
        # deliveryperson_id, status, price,
        self.order_id = None
        self.customer_id =customer_id
        # self.deliveryperson_id = None
        self.date = datetime.now()
        # self.status = None
        self.price =None
        self.discount_code_recive =discount_code_recive
        self.pizzas=pizzas
        self.drinks=drinks
        self.desserts=desserts
        self.discount_code = None

    def dictionary(self):
        return {
            "order_id" : self.order_id,
            "customer_id" : self.customer_id,
            # "deliveryperson_id":self.deliveryperson_id,
            "date": self.date,
            # "status":self.status,
            "price":self.price,
            "discount_code_recive":self.discount_code_recive,
            "desserts": self.desserts,
            "drinks":self.drinks,
            "desserts":self.desserts,
            "discount_code": self.discount_code
        }
