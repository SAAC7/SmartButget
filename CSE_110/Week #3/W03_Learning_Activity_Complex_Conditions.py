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

print("For each of these questions, please provide a 1-10 rating:")

large_loan = get_number("How large is the loan? ","int")
credit_history = get_number("How good is your credit history? ","int")
income = get_number("How high is your income? ","int")
down_payment = get_number("How large is your down payment? ","int")
should_loan = False

if large_loan>=5:
    if credit_history >=7 and income >=7:
        should_loan = True
    elif credit_history >=7 or income >=7:
        if down_payment >=5 :
            should_loan = True
        else:
            should_loan = False
    else:
        should_loan = False
else:
    if credit_history < 4 :
        should_loan = False
    else:
        if income >= 7 or down_payment >= 7:
            should_loan = True
        elif income >= 4 and down_payment >= 4:
            should_loan = True
        else:
            should_loan = False
            
mensaje = "yes. This is a good loan" if should_loan else "no. You shouldn't lend this money."
print(f"The decision is {mensaje}")
            