import math
import datetime



def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Wrong value. Please enter a correct value.")

def calculate_volume(width_mm:float,aspect_ratio:float,diameter_in:float):
    volume_liters = (math.pi * width_mm**2 * aspect_ratio * (width_mm * aspect_ratio + 2540 * diameter_in)) / 10000000000
    return volume_liters

def file_create(file_name:str,date_str: str, width: float, aspect: float, diam: float, volume: float):
    """Append to the end of the volumes.txt file one line of text that contains the following five values:

    current date (Do NOT include time)
    width of the tire
    aspect ratio of the tire
    diameter of the wheel
    volume of the tire (rounded to two decimal places)."""
    with open(file_name, "a") as file_create:
        file_create.write(f"{date_str}, {int(width)}, {int(aspect)}, {int(diam)}, {volume:.2f}\n")


while True:
    # Constants
    print("=== Tire Volume Calculation ===")
    FILENAME = "volumes.txt"
    DATE_NOW = datetime.datetime.now().strftime("%Y-%m-%d")
    print()
    width_mm = get_float("Enter the width of the tire in mm (ex 205): ")
    aspect_ratio = get_float("Enter the aspect ratio of the tire (ex 60): ")
    diameter_in = get_float("Enter the diameter of the wheel in inches (ex 15): ")
    volume_liters=calculate_volume(width_mm,aspect_ratio,diameter_in)

    print(f"The approximate volume is {volume_liters:.2f} liters")
    file_create(FILENAME,DATE_NOW,width_mm,aspect_ratio,diameter_in,volume_liters)

    again = input("Would you like to calculate another tire? (Y/N): ").strip().lower()
    if again != 'y':
        print("Thank you for using the volume calculator! 😊")
        break

