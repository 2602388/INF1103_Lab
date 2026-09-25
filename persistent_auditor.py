ORDERS_FILE = "orders.txt"
STARTING_ID = 1001


def load_inventory(filename=ORDERS_FILE):
    """Reads previously saved orders from the file.
    Returns a list of orders, where each order is [order_id, product_name, quantity].
    If the file doesn't exist (or is empty/corrupted), starts fresh with no error."""
    orders = []
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()

        for line in lines:
            if not line.strip():
                continue
            parts = line.split(",")
            if len(parts) != 3:
                continue
            order_id, product_name, quantity = parts
            orders.append([int(order_id), product_name, int(quantity)])

    except FileNotFoundError:
        # No saved data yet -- start with an empty order list
        pass
    except ValueError:
        print(f"Warning: '{filename}' could not be read properly. Starting fresh.")
        return []

    return orders


def save_inventory(orders, filename=ORDERS_FILE):
    """Writes the full list of orders to the file, one order per line."""
    with open(filename, "w") as f:
        for order_id, product_name, quantity in orders:
            f.write(f"{order_id},{product_name},{quantity}\n")


def print_current_orders(orders):
    """Displays the orders currently on record."""
    print("Current Orders:\n")
    if not orders:
        print("(none yet)")
    else:
        for order_id, product_name, quantity in orders:
            print(f"{order_id}, {product_name}, {quantity}")
    print()


def get_next_order_id(orders):
    """Returns the next available order ID."""
    if not orders:
        return STARTING_ID
    return max(order[0] for order in orders) + 1


def get_valid_quantity():
    """Prompts for a quantity and returns a valid non-negative integer,
    or None if the entry was invalid/rejected."""
    user_input = input("Enter Quantity: ").strip()

    if not user_input.isdigit():
        print(f"Error: '{user_input}' is not a valid whole number. Entry rejected.")
        return None

    quantity = int(user_input)

    if quantity < 0:
        print(f"Error: {quantity} is negative. Entry rejected.")
        return None

    return quantity


def generate_report(total_orders, failed_attempts):
    """Prints the final summary report."""
    print("\n--- Final Report ---")
    print(f"Total Orders Processed: {total_orders}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    # Persistence: load whatever was saved from the last session
    orders = load_inventory()
    print_current_orders(orders)

    failed_entries = 0

    while True:                # Continuous loop until user types 'quit'
        product_name = input("Enter Product Name (or 'quit' to finish): ").strip()

        if product_name.lower() == "quit":
            break

        if not product_name:
            print("Error: Product name cannot be empty. Entry rejected.")
            failed_entries += 1
            continue

        quantity = get_valid_quantity()
        if quantity is None:
            failed_entries += 1
            continue

        new_id = get_next_order_id(orders)
        orders.append([new_id, product_name, quantity])

        print("\nNew Order Added:")
        print(f"{new_id},{product_name},{quantity}\n")

        # Write-Back: save immediately so no data is lost
        save_inventory(orders)
        print(f"Order successfully saved to {ORDERS_FILE}\n")

    generate_report(len(orders), failed_entries)


if __name__ == "__main__":
    main()
