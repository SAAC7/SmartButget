import math
def area_square(side):
    return side**2
def area_rectangle(length,width):
    return(length*width)
def area_cicle(radius):
    return (radius**2)*math.pi
def get_number(text):
    notError = True
    number = 0
    while notError:
        try:
            number = float(input(text))  
            notError = False            
        except ValueError as e:         
            print(f"Enter a valid number. Error: {e}")
    return number



print(get_number("Esto es una prueba "))