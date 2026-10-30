from can_be_shipped import CanBeShipped
from product import Product


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped.

    Inherits from ONE parent (Product) and signs ONE interface (CanBeShipped)."""

    BASE_SHIPPING_COST = 5.00    # flat handling fee
    COST_PER_KG = 2.00           # added per kilogram of weight

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)   # reuse Product setup
        if weight <= 0:
            raise ValueError("Weight must be greater than zero.")
        self.__weight = float(weight)                       # weight in kilograms

    @property
    def weight(self):
        return self.__weight

    def calculate_shipping_cost(self):
        """Simple rule: flat base fee plus a charge per kilogram."""
        return self.BASE_SHIPPING_COST + self.__weight * self.COST_PER_KG

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def display_information(self):
        super().display_information()                       # common info from parent
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def display_details(self):
        super().display_details()
        print(f"Weight: {self.__weight:.2f} kg")
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
