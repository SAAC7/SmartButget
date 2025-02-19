import math
def area_square(side):
    return math.pow(side,2)
def area_rectangle(length, width):
    return length*width
def area_circle(radius):
    return math.pi * math.pow(radius,2)
def enter_number_rfloat(text):
    while True:
        try:
            option = float(input(text).strip())
        except ValueError:
            print("Worng Option, Please enter a Correct Number")
            continue
        break
    return option

shape = 0
while True:
    print(
        f"You will need to choose a shape\n"
        f"1.Square Area\n"
        f"2.Rectangle Area\n"
        f"3.Circle Area\n"
        f"4.Quit"
    )
    option = int(enter_number_rfloat("Enter the number of the option you wish to choose: "))
    if option == 1:
        side = enter_number_rfloat("What is the length of the side")
        area = area_square(side)
        print(f"\nThe area of the square is {area}\n")
    elif option == 2:
        x = enter_number_rfloat("What is the length? ")
        y = enter_number_rfloat("What is the width? ")
        area = area_rectangle(x,y)
        print(f"\nThe area of the rectangle is {area}\n")
    elif option == 3:
        radious = enter_number_rfloat("What is the length of the radious")
        area = area_circle(radious)
        print(f"\nThe area of the circle is {area:.2f}\n")
    elif option == 4:
        break
    else:
        print("Enter a correct Option")