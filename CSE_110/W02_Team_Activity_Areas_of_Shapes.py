text = (
    f"----------------------------------------------------------"
    f"\n\t\tThe Calculator"
    f"\nwill help you to know the areas of 3 types of shapes"
    f"\n\t\tsquare, cirle, rectangle"
    f"\n\t\tand secret things"
    f"\n----------------------------------------------------------"
)
print(text)

import math
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
# Core Requirements
# square
side = get_number("What is the length of a side of the square? ")
print(f"The area of the square is: {(side**2):.2f}")
# rectangle
length = get_number("What is the length of rectangle? ")
width = get_number("What is the width of the rectangle? ")
print(f"The area of the rectangle is: {(length*width):.2f}")
# circle 
radius = get_number("What is the radius of the circle? ")
print(f"The area of the circle is: {(3.14*(radius**2)):.2f}")
print()
# strech challenge
# No.1
radius = get_number("What is the radius of the circle? ")
print(f"The area of the circle is: {(math.pi*(radius**2)):.2f}")
print()
# No.2
value = get_number("Enter the value to use ")
area_square = value**2
volume_cube = value**3
area_circle = (value**2)*math.pi
volume_sphere = (4/3)*math.pi*(value**3)

# display results
print(f"Area of a square: {area_square:.2f}")
print(f"Area of a circle: {area_circle:.2f}")
print(f"Volume of a cube: {volume_cube:.2f}")
print(f"Volume of a sphere: {volume_sphere:.2f}")
print()
# No.3
constant_meter = 100**2
# square
side = get_number("\nWhat is the length of a side of the square? (in cm) ")
area = side**2
print(f"The area of the square is: {(area):.2f} cm^2")
print(f"The area of the square is: {((area)/(constant_meter)):.2f} m^2")
# rectangle
length = get_number("\nWhat is the length of rectangle? (in cm) ")
width = get_number("What is the width of the rectangle? (in cm) ")
area = length*width
print(f"The area of the rectangle is: {(area):.2f} cm^2")
print(f"The area of the rectangle is: {((area)/(constant_meter)):.2f} m^2")
# circle 
radius = get_number("\nWhat is the radius of the circle? (in cm) ")
area = (3.14*(radius**2))
print(f"The area of the circle is: {(area):.2f} cm^2")
print(f"The area of the circle is: {((area)/(constant_meter)):.2f} m^2")