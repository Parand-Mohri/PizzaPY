class Customer():
    def __init__(self, name, adress_id, phone_number):
        self.customer_id= None
        self.name = name
        self.adress_id = adress_id
        self.phone_number = phone_number

    def dictionary(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "adress_id": self.adress_id,
            "phone_number": self.phone_number,
        }