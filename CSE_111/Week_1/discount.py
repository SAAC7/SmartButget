import datetime

DISCOUNT_RATE = 0.1
SALES_TAX_RATE = 0.06
DISCOUNT_THRESHOLD = 50.0


# weekday real: Monday=0, Tuesday=1, ..., Sunday=6
DISCOUNT_DAYS = [1,2]
today = datetime.datetime.now().weekday()
# today = 2



# Inicializar
subtotal = 0.0


print("\nEnter the price and quantity for each item. If you want to stop, enter 0 as quantity.")

# Leer ítems
while True:
    try:
        quantity = int(input("Enter quantity (0 to finish): "))
        if quantity == 0:
            break
        price = float(input("Enter price: $"))
        subtotal += price * quantity
    except ValueError:
        print("Please enter valid numeric values.")

print(f"\nSubtotal: ${subtotal:.2f}")

# Conservamos el subtotal antes de descuento para futuros cálculos
original_subtotal = subtotal
discount = 0.0


if original_subtotal >= DISCOUNT_THRESHOLD and today in DISCOUNT_DAYS:
    discount = original_subtotal * DISCOUNT_RATE
    subtotal = original_subtotal - discount
    print(f"Discount applied: -${discount:.2f}")


elif today in DISCOUNT_DAYS and original_subtotal < DISCOUNT_THRESHOLD:
    difference = DISCOUNT_THRESHOLD - original_subtotal
    print(f"Spend ${difference:.2f} more to get a 10% discount!")


sales_tax = subtotal * SALES_TAX_RATE
total = subtotal + sales_tax

print(f"Sales tax (6%): ${sales_tax:.2f}")
print(f"Total amount due: ${total:.2f}")
