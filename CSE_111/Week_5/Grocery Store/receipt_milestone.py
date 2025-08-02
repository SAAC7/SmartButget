import csv
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
    try:
        products_dict = read_dictionary('products.csv', 0)
    except FileNotFoundError as e:
        print(f"Error: missing file\n{e}")
        return
    except PermissionError as e:
        print(f"Error: permission denied\n{e}")
        return

    # Display all products dictionary
    print("All Products")
    print(products_dict)

    # Process request.csv
    try:
        with open('request.csv', newline='') as req_file:
            reader = csv.reader(req_file)
            next(reader)  # skip header
            print("Requested Items")
            for row in reader:
                prod_num, qty = row
                try:
                    prod_info = products_dict[prod_num]
                except KeyError:
                    print(f"Error: unknown product ID in the request.csv file\n'{prod_num}'")
                    return
                name = prod_info[1]
                price = prod_info[2]
                print(f"{name}: {qty} @ {price}")
    except FileNotFoundError as e:
        print(f"Error: missing file\n{e}")
    except PermissionError as e:
        print(f"Error: permission denied\n{e}")

if __name__ == "__main__":
    main()