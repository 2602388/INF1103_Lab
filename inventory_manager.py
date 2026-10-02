import json

INVENTORY_FILE = "inventory.json"


def load_inventory(filename=INVENTORY_FILE):
    """Checks whether the inventory file exists and loads it if so.
    If the file doesn't exist (or is corrupted), starts with an empty
    inventory and continues running without producing an error."""
    try:
        with open(filename, "r") as f:
            print(f"{filename} found.")
            inventory = json.load(f)
            print("Inventory loaded successfully.")
            return inventory

    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty inventory.")
        return []

    except json.JSONDecodeError:
        print(f"Warning: {filename} is corrupted or unreadable. "
              f"Starting with an empty inventory.")
        return []


def display_all(inventory):
    """Displays all products currently in the inventory."""
    print("\nCurrent Inventory")
    print("-" * 48)
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 48)


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Saves the current inventory list to the file as JSON.
    Does not print anything itself -- callers handle context-specific messages."""
    with open(filename, "w") as f:
        json.dump(inventory, f, indent=4)


def find_product(inventory, product_id):
    """Returns the product dict with the given ID, or None if not found."""
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


def add_product(inventory):
    """Prompts for a new product's details and adds it to the inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if find_product(inventory, product_id):
        print(f"Error: Product ID '{product_id}' already exists. Entry rejected.")
        return

    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("Error: Price and Stock Quantity must be numeric. Entry rejected.")
        return

    if price < 0 or stock < 0:
        print("Error: Price and Stock Quantity cannot be negative. Entry rejected.")
        return

    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("\nProduct added successfully!")


def update_stock(inventory):
    """Prompts for a Product ID and updates its stock quantity."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = find_product(inventory, product_id)
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    new_stock_input = input("\nNew Stock Quantity: ").strip()
    if not new_stock_input.isdigit():
        print("Error: Stock quantity must be a non-negative whole number. Update rejected.")
        return

    product["stock"] = int(new_stock_input)
    print("\nStock updated successfully!")


def search_product(inventory):
    """Prompts for a Product ID and displays the matching product, if any."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = find_product(inventory, product_id)
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
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


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    # 3. Data Persistence: load from inventory.json if it exists,
    # otherwise start with an empty inventory
    inventory = load_inventory()

    while True:
        print_menu()
        option = input("\nEnter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
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
            print(f"Error: '{option}' is not a valid menu option. Please try again.")


if __name__ == "__main__":
    main()
