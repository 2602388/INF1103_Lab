from product import Product


class PhysicalProduct(Product):
    """A product that is stored and shipped. (A PhysicalProduct is-a Product.)"""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)   # reuse Product setup
        if weight <= 0:
            raise ValueError("Weight must be greater than zero.")
        self.__weight = float(weight)                       # weight in kilograms

    @property
    def weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()                       # common info from parent
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def display_details(self):
        super().display_details()
        print(f"Weight: {self.__weight:.2f} kg")
