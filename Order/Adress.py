class Adress():

    def __init__(self, street, houseNumber, postcode):
        self.adress_id = None
        self. street = street
        self.houseNumber = houseNumber
        self.postcode = postcode

    def dictionary(self):
        return {
            "adress_id": self.adress_id,
            "street": self.street,
            "house_number": self.houseNumber,
            "postcode": self.postcode
        }