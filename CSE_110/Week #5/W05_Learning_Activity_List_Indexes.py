shopping_list = []
print("Please enter the items of the shopping list (type: quit to finish): ")
while True:
    product = input("Item: ")
    if product.lower() == "quit":
        break
    shopping_list.append(product.title())

print("\nThe shopping list is:")
for product in shopping_list:
    print(product)

print("\nThe shopping list with indices is:")
for i in range(len(shopping_list)):
    print(f"{i}. {shopping_list[i]}")

# Convertir la entrada a entero para usarlo como índice
index = int(input("\nWhich item would you like to change? (enter the index) "))
new_product = input("What is the new item? ")
shopping_list[index] = new_product.title()

print("\nThe updated shopping list with indices is:")
for i in range(len(shopping_list)):
    print(f"{i}. {shopping_list[i]}")
