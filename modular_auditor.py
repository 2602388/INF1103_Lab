def get_valid_input():
    """Handles the prompt, validates input, and returns a valid integer
    or the string 'quit' as a signal to stop."""
    while True:
        user_input = input("Enter stock quantity (or 'quit' to finish): ").strip()

        if user_input.lower() == "quit":
            return "quit"

        # Handle invalid input (reject non-integer strings)
        if not user_input.isdigit():
            print(f"Error: '{user_input}' is not a valid whole number. Entry rejected.")
            return None

        quantity = int(user_input)

        # Enforce business rules: reject negative numbers
        # (isdigit() already blocks negative signs, but kept for clarity/safety)
        if quantity < 0:
            print(f"Error: {quantity} is negative. Entry rejected.")
            return None

        return quantity


def process_delivery(current_total, new_value):
    """Calculates the new running total and returns it."""
    return current_total + new_value


def calculate_tax(amount):
    """Takes a delivery amount and returns the tax (10% of that delivery)."""
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Prints the final summary report."""
    print("\n--- Final Report ---")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    total_inventory = 0      # 1. Initialize inventory to zero
    failed_entries = 0        # counter for invalid/rejected entries

    while True:                # 2. Continuous loop until user types 'quit'
        result = get_valid_input()

        if result == "quit":
            break

        if result is None:
            # Invalid entry (bad format or negative number)
            failed_entries += 1
            continue

        # 3. Valid value: process the delivery
        quantity = result
        total_inventory = process_delivery(total_inventory, quantity)

        tax = calculate_tax(quantity)
        print(f"Delivery accepted: {quantity} units. Tax owed: {tax:.2f}. "
              f"Running total: {total_inventory}")

        # Trigger overstock alert
        if total_inventory > 500:
            print(f"ALERT: Overstock detected! Total inventory is {total_inventory}, "
                  f"which exceeds 500 units.")
            break
        elif total_inventory == 500:
            print("Notice: Inventory has reached exactly 500 units.")

    # 4. Reporting
    generate_report(total_inventory, failed_entries)


if __name__ == "__main__":
    main()
