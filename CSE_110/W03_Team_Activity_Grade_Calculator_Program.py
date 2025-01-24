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

# core requirements

grade = get_number("Please enter the grade percentage: ","")
letter = ""
if (grade >= 90):
    letter = "A"
elif (grade >= 80):
    letter = "B"
elif (grade >= 70):
    letter = "C"
elif (grade >= 60):
    letter = "D"
else :
    letter = "F"
    
# strech challenge
# No.1
sign = ""
last_digit_number = grade % 10
if last_digit_number >= 7:
    sign = "+"
elif last_digit_number < 3:
    sign = "-"
else:
    sign = ""
    
# No.2
if grade > 93:
    sign = ""
# No.3
if letter.upper() == "F":
    sign = ""
    
    
    
    
    
print(
    f"-------------------------------------\n"
    f"your score letter is {letter.upper()}{sign}"
    f"\n-------------------------------------"
    )
if grade >=70 :
    print(
        f"-------------------------------------\n"
        f"Congratulations for passing!"
        f"\n-------------------------------------"
        )
else:
    print(
        f"-------------------------------------\n"
        f"Good luck next time, you will pass the class next time."
        f"\n-------------------------------------"
        )

    
