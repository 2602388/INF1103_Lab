import json

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct

INVENTORY_FILE = "inventory.json"

# Registry: type identifier (as saved in JSON) -> class used to rebuild it.
PRODUCT_TYPES = {cls.TYPE: cls for cls in (PhysicalProduct, DigitalProduct)}

# What the "Add Product" menu offers: (choice, type identifier, label, extra-field prompt)
ADD_PRODUCT_CHOICES = [
    ("1", PhysicalProduct.TYPE, "Physical Product", "Weight (kg)"),
    ("2", DigitalProduct.TYPE, "Digital Product", "Download Size (MB)"),
]


# ---------------------------------------------------------------
# File handling
# ---------------------------------------------------------------
def load_inventory(filename=INVENTORY_FILE):
    """Loads the JSON file into an Inventory, rebuilding each product as the
    correct subclass using its saved "type". Missing/unreadable file -> empty Inventory."""
    inventory = Inventory()
    try:
        with open(filename, "r") as f:
            print(f"{filename} found.")
            records = json.load(f)

        for record in records:
            product_class = PRODUCT_TYPES[record["type"]]
            inventory.add_product(product_class.from_dict(record))

        print("Inventory loaded successfully.")
        return inventory

    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty inventory.")
        return Inventory()

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print(f"Warning: {filename} is corrupted, unreadable or has an unknown "
              f"product type. Starting with an empty inventory.")
        return Inventory()


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Writes every product (with its type and extra attributes) to the JSON file."""
    records = [product.to_dict() for product in inventory.get_products()]
    with open(filename, "w") as f:
        json.dump(records, f, indent=4)


# ---------------------------------------------------------------
# Menu handlers (user input lives here, not in the classes)
# ---------------------------------------------------------------
def handle_add_product(inventory):
    print("\nAdd New Product")
    print("Select Product Type:")
    for choice, _, label, _ in ADD_PRODUCT_CHOICES:
        print(f"{choice}. {label}")
    selected = input("Enter choice: ").strip()

    entry = next((e for e in ADD_PRODUCT_CHOICES if e[0] == selected), None)
    if entry is None:
        print("Error: Invalid product type. Entry rejected.")
        return
    _, type_id, _, extra_prompt = entry

    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
        extra_value = float(input(f"{extra_prompt}: ").strip())
    except ValueError:
        print("Error: Price, Stock Quantity and "
              f"{extra_prompt} must be numeric. Entry rejected.")
        return

    try:
        product = PRODUCT_TYPES[type_id](product_id, name, price, stock, extra_value)
    except ValueError as error:
        print(f"Error: {error} Entry rejected.")
        return

    if inventory.add_product(product):
        print("\nProduct added successfully!")
    else:
        print(f"Error: Product ID {product_id} already exists. Entry rejected.")


def handle_update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    new_stock = input("\nNew Stock Quantity: ").strip()
    if not new_stock.isdigit():
        print("Error: Stock quantity must be a non-negative whole number. "
              "Update rejected.")
        return

    product.update_stock(int(new_stock))
    print("\nStock updated successfully!")


def handle_search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    product.display_details()
    print("-" * 48)


def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-----------------------------")


# ---------------------------------------------------------------
# Main program
# ---------------------------------------------------------------
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        print_menu()
        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            handle_add_product(inventory)
        elif option == "3":
            handle_update_stock(inventory)
        elif option == "4":
            handle_search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print(f"Error: {option} is not a valid menu option. Please try again.")


if __name__ == "__main__":
    main()
