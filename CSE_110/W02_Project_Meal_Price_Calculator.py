text = (
    f"------------------------------------------------------------------"
    f"\n\t\tWelcome to the Price Calculator\n"
    f"This Program will help you to know the total price of your meal.\n"
    f"\t\tJust enter the following information\n"
    f"------------------------------------------------------------------"
)
print(text)
def get_number(text,tipo):
    notError = True
    number = 0
    while notError:
        try:
            if (tipo.lower() == "int") :
                number = int(input(text))
            else:
                number = float(input(text))
            notError = False            
        except ValueError as e:         
            print(f"Enter a valid number. Error: {e}")
    return number


price_child = get_number("What is the price of a child's meal? ","")
price_adult = get_number("What is the price of an adult's meal? ","")
numer_child = get_number("How many children are there? ","int")
number_adult = get_number("How many adults are there? ","int")
subtotal = (number_adult*price_adult)+(price_child*numer_child)

print(f"\nSubtotal: ${subtotal:.2f}\n")

tax_mount = get_number("What is the sales tax rate? ","int")
sales_tax = subtotal * (tax_mount/100)
total = sales_tax + subtotal
print(f"Sales Tax: ${sales_tax:.2f}")
print(f"Total: ${total:.2f}")

payment = 0

notFinished = True
while notFinished:
    payment = get_number("\nWhat is the payment amount? ","")
    notFinished = False if (payment>=total) else True;print("Enter the correct value, Money is missing")
        
print(f"Change: ${(payment-total):.2f}")