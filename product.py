from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class: the data and behaviour every product shares.

    Product cannot be instantiated directly; every product must be a
    concrete subtype (physical or digital)."""

    def __init__(self, product_id, name, price, stock):
        if price < 0:
            raise ValueError("Price cannot be negative.")

        # Private attributes: outside code uses the properties/methods below.
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = 0
        self.update_stock(stock)   # reuse the same validation as later updates

    # ----- Read-only access to the attributes -----
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    # ----- Behaviour -----
    def update_stock(self, quantity):
        """Sets the stock level. The Product decides what a valid value is."""
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Stock quantity must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = quantity

    def to_dict(self):
        """Returns the common data as a plain dict (used for JSON saving)."""
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock}

    @abstractmethod
    def get_fulfilment_info(self):
        """Returns a message describing how this product reaches the customer.
        Every subclass must provide its own implementation."""

    def display_information(self):
        """Prints a one-line summary of the common product information."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def display_details(self):
        """Prints the common detail lines (callers add any surrounding border)."""
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
