# Enhancements: Days until New Years Sale calculation and Return-by date 30 days from now at 9 PM.

import csv
from datetime import datetime, timedelta
def read_dictionary(filename, key_column_index):
    products = {}
    with open(filename,"rt") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            key = row[key_column_index]
            products[key]=row
    return products

def main():
    STORE_NAME = "Inkom Emporium"
    TAX_RATE = 0.06

    try:
        products_dict = read_dictionary('products.csv', 0)
        with open('request.csv', newline='') as req_file:
            reader = csv.reader(req_file)
            next(reader)

            items = []
            total_qty = 0
            subtotal = 0.0

            for row in reader:
                prod_num, qty_str = row
                qty = int(qty_str)
                try:
                    prod_info = products_dict[prod_num]
                except KeyError:
                    print(f"Error: unknown product ID in the request.csv file\n'{prod_num}'")
                    return
                name = prod_info[1]
                price = float(prod_info[2])
                items.append((name, qty, price))
                total_qty += qty
                subtotal += price * qty

    except FileNotFoundError as e:
        print(f"Error: missing file\n{e}")
        return
    except PermissionError as e:
        print(f"Error: permission denied\n{e}")
        return

    print(STORE_NAME)
    for name, qty, price in items:
        print(f"{name}: {qty} @ {price:.2f}")

    tax = subtotal * TAX_RATE
    total = subtotal + tax

    print(f"Number of Items: {total_qty}")
    print(f"Subtotal: {subtotal:.2f}")
    print(f"Sales Tax: {tax:.2f}")
    print(f"Total: {total:.2f}")


    now = datetime.now()
    next_year = now.year + 1
    new_year = datetime(next_year, 1, 1)
    days_until = (new_year - now).days
    print(f"Days until New Years Sale: {days_until}")

    return_by = (now + timedelta(days=30)).replace(hour=21, minute=0, second=0, microsecond=0)
    print(f"Return by: {return_by.strftime('%a %b %d %I:%M %p %Y')}")

    print(f"Thank you for shopping at the {STORE_NAME}.")
    print(now.strftime('%a %b %d %H:%M:%S %Y'))

if __name__ == "__main__":
    main()