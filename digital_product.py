from product import Product


class DigitalProduct(Product):
    """A product delivered by download. (A DigitalProduct is-a Product.)"""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)   # reuse Product setup
        if download_size <= 0:
            raise ValueError("Download size must be greater than zero.")
        self.__download_size = float(download_size)         # size in megabytes

    @property
    def download_size(self):
        return self.__download_size

    def get_fulfilment_info(self):
        return "Delivered digitally via download."

    def display_information(self):
        super().display_information()                       # common info from parent
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")

    def display_details(self):
        super().display_details()
        print(f"Download Size: {self.__download_size:.2f} MB")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
