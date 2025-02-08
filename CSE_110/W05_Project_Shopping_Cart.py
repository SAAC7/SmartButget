items = []
prices = []
quantities = []
def menu():
    print(
        f"\nPlease select one of the following:"
        f"\n1. Add item"
        f"\n2. View cart"
        f"\n3. Remove item"
        f"\n4. Compute total"
        f"\n5. Quit")

def add_item():
    item = input("What item would you like to add? ")
    try:
        price = float(input(f"What is the price of '{item}'? "))
    except ValueError:
        print("Invalid price, the item not added.")
        return
    quantity = 1
    choise = input("Would you like to add quantity? (y/n): ").lower()
    if choise == 'y':
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid quantity. Defaulting to 1.")
            quantity = 1
    items.append(item)
    prices.append(price)
    quantities.append(quantity)
    print(f"{item} has been added to the cart.")

def view_cart():
    if not items:
        print("Your shopping cart is empty")
    else:
        print("\nThe contents of the shopping cart are:\n")
        print("{:<5} {:<20} {:>10} {:>10}".format("No.", "Item", "Price", "Quantity"))
        for i in range(len(items)):
            print("{:<5} {:<20} {:>10.2f} {:>10}".format(i+1, items[i], prices[i], quantities[i]))

print("Welcome to the Shopping Cart Program!")
while True:
    menu()
    try:
        action = int(input("Please enter an action: "))  
    except ValueError:
        print("Invalid selection. Please try again.")
    if action == 1:
        add_item()
    elif action == 2:
        view_cart()
    elif action == 3:
        print("This option is not available at this moment")
    elif action == 4:
        print("This option is not available at this moment")
    elif action == 5:
        print("Thank you. Goodbye.")
        break
    else:
        print("Invalid selection. Please try again.")
            
