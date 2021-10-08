class Drink():
    def __init__(self, drink_id, name, price):
        self.drink_id = drink_id
        self.name=name
        self.price =price

    def dictionary(self):
        return {
            "drink_id": self.drink_id,
            "name": self.name,
            "cost": self.price,
        }

