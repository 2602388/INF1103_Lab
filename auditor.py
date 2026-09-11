total_inventory = 0      # 1. Initialize inventory to zero
failed_entries = 0        # counter for invalid/rejected entries

while True:                # 2. Continuous loop until user types 'quit'
    user_input = input("Enter stock quantity (or 'quit' to finish): ").strip()

    if user_input.lower() == "quit":
        break

    # 4. Handle invalid input (reject non-integer strings)
    if not user_input.isdigit():
        print(f"Error: '{user_input}' is not a valid whole number. Entry rejected.")
        failed_entries += 1
        continue

    quantity = int(user_input)   # 3. Accept stock values as integers

    # 5. Enforce business rules: reject negative numbers
    # (isdigit() already blocks negative signs, but kept for clarity/safety)
    if quantity < 0:
        print(f"Error: {quantity} is negative. Entry rejected.")
        failed_entries += 1
        continue

    # 6. Manage state: running total
    total_inventory += quantity

    # 7. Trigger overstock alert
    if total_inventory > 500:
        print(f"ALERT: Overstock detected! Total inventory is {total_inventory}, which exceeds 500 units.")
        break
    elif total_inventory == 500:
        print("Notice: Inventory has reached exactly 500 units.")
    else:
        print(f"Accepted. Current total inventory: {total_inventory}")

# 8. Reporting
print("\n--- Final Report ---")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")
