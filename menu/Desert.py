class Desert():
    def __init__(self,desert_id,name, price):
        self.desert_id=desert_id
        self.name=name
        self.price=price

    def dictionary(self):
        return {
            "dessert_id": self.desert_id,
            "name": self.name,
            "cost": self.price,
        }