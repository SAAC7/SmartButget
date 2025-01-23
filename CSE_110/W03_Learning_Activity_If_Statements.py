men =(
    f"Welcome we will compare two integers"
    f"We can't use floats"
    f"Then we will compare our favorite animal"
    )
# I create a function to enter an integer, so check that it is only integers 
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
    
first_number = get_number("What is the first number? ","int")
second_number = get_number("What is the second number? ","int")
if first_number>second_number:
    print(f"The first number is greater")
else:
    print(f"The first number is not greater")
if (first_number==second_number):
    print(f"The numbers are equal")
else:
    print(f"The numbers are not equal")
if first_number<second_number:
    print(f"The second number is greater")
else:
    print(f"The second number is not greater")
    

print()
user_favorite_animal = input("What is your favorite animal? ")
admin_favorite_animal = "tiger"
mensaje = "That's my favorite animal too!" if user_favorite_animal.lower()==admin_favorite_animal.lower() else "That one is not my favorite."
print(mensaje)
