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


def main():
    # 3. Data Persistence: load from inventory.json if it exists,
    # otherwise start with an empty inventory
    inventory = load_inventory()

    # Quick sanity check that loading worked as expected
    display_all(inventory)


if __name__ == "__main__":
    main()
