"""
Welcome to the Shopping Cart Program!
This program not only helps you manage your shopping cart with ease,
but also adds a touch of style by formatting prices with a currency symbol.
Enjoy a seamless shopping experience where you can add items, view your cart neatly,
and see your total in a glance!
"""

items = []
prices = []
quantities = []

def menu():
    print(
        "\nPlease select one of the following:"
        "\n1. Add item"
        "\n2. View cart"
        "\n3. Remove item"
        "\n4. Compute total"
        "\n5. Quit")

def add_item():
    item = input("What item would you like to add? ")
    try:
        price = float(input(f"What is the price of '{item}'? "))
    except ValueError:
        print("Invalid price, the item was not added.")
        return
    quantity = 1
    choice = input("Would you like to add a quantity greater than 1? (y/n): ").lower()
    if choice == 'y':
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid quantity input. Defaulting to 1.")
            quantity = 1
    items.append(item)
    prices.append(price)
    quantities.append(quantity)
    print(f"'{item}' has been added to the cart.")

def view_cart():
    if not items:
        print("Your shopping cart is empty.")
    else:
        print("\nThe contents of the shopping cart are:\n")
        print("{:<5} {:<20} {:>12} {:>10}".format("No.", "Item", "Price", "Quantity"))
        for i in range(len(items)):
            price_str = f"${prices[i]:.2f}"
            print("{:<5} {:<20} {:>12} {:>10}".format(i+1, items[i], price_str, quantities[i]))

def remove_item():
    if not items:
        print("Your shopping cart is empty, nothing to remove.")
        return
    view_cart()
    try:
        item_index = int(input("Which item would you like to remove? (enter the item number): "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
    remove_index = item_index - 1
    if remove_index < 0 or remove_index >= len(items):
        print("Sorry, that is not a valid index.")
    else:
        item_to_remove = items.pop(remove_index)
        prices.pop(remove_index)
        quantities.pop(remove_index)
        print(f"The item '{item_to_remove}' has been removed.")

def total_of_cart():
    total = 0
    view_cart()
    print("{:>48}".format("-" * 50))
    for i in range(len(prices)):
        total += prices[i] * quantities[i]
    # Se muestra el total con el símbolo de dólar y redondeado a dos decimales.
    print("{:<10}   {:>37}".format("Total", f"${total:.2f}"))

print("Welcome to the Shopping Cart Program!")
while True:
    menu()
    try:
        action = int(input("Please enter an action: "))
    except ValueError:
        print("Invalid selection. Please try again.")
        continue

    if action == 1:
        add_item()
    elif action == 2:
        view_cart()
    elif action == 3:
        remove_item()
    elif action == 4:
        total_of_cart()
    elif action == 5:
        print("Thank you. Goodbye.")
        break
    else:
        print("Invalid selection. Please try again.")
