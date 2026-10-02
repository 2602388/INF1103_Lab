def display_all(inventory):
    """Displays all products currently in the inventory."""
    print("\nCurrent Inventory")
    print("-" * 48)
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 48)


def main():
    # 1. Data Representation: inventory items as dictionaries in a list
    inventory = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
    ]

    # Quick sanity check that the data structure looks right
    display_all(inventory)


if __name__ == "__main__":
    main()
