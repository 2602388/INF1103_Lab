class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Adds a Product. Returns False (and adds nothing) if the ID already exists."""
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Returns the Product with the given ID, or None if not found."""
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def display_all(self):
        """Displays every product in the inventory."""
        print("\nCurrent Inventory")
        print("-" * 48)
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def get_products(self):
        """Returns a copy of the product list (e.g. for saving to a file)."""
        return list(self.__products)
