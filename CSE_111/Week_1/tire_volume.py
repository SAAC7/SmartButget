import math
import datetime

# Constants
FILENAME = "volumes.txt"
DATE_NOW = datetime.datetime.now().strftime("%Y-%m-%d")


width_mm = float(input("Enter the width of the tire in mm (ex 205): "))
aspect_ratio = float(input("Enter the aspect ratio of the tire (ex 60): "))
diameter_in = float(input("Enter the diameter of the wheel in inches (ex 15): "))

volume_liters = (math.pi * width_mm**2 * aspect_ratio * (width_mm * aspect_ratio + 2540 * diameter_in)) / 10000000000
print(f"The approximate volume is {volume_liters:.2f} liters")

with open(FILENAME, "at") as cities_file:
    print(f"{DATE_NOW}, {width_mm:.0f}, {aspect_ratio:.0f}, {diameter_in:.0f}, {volume_liters:.2f}",file=cities_file)
