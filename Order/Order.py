from datetime import datetime

class Order():
    def __init__(self, customer_id, pizzas, drinks, desserts,  discount_code):
        self.order_id = None
        self.customer_id =customer_id
        self.deliveryperson_id = None
        self.date = datetime.now()
        self.status = "in process"
        self.price =None
        self.pizzas=pizzas
        self.drinks=drinks
        self.desserts=desserts
        self.discount_code = discount_code
        self.estimated_delivery_time = None

    def dictionary(self):
        return {
            "order_id" : self.order_id,
            "customer_id" : self.customer_id,
            "deliveryperson_id":self.deliveryperson_id,
            "date": self.date,
            "status":self.status,
            "price":self.price,
            "desserts": self.desserts,
            "drinks":self.drinks,
            "desserts":self.desserts,
            "discount_code": self.discount_code,
            "estimated_delivery_time": self.estimated_delivery_time
        }
