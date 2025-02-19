# I have developed some other functions to reduce the lines of code and use them in the Fahrenheit or celsius cases
def calculate_wind_chill(temperature:float,wind_speed:float) -> float:
    wind_chill =  35.74 + (0.6215*temperature) - (35.75*(wind_speed**0.16)) + (0.4275*temperature*(wind_speed**0.16))
    return wind_chill
def celsius_to_fahrenheit(temperature:float) -> float:
    return temperature*(9/5)+32
def enter_number_rfloat(text:float) -> float:
    while True:
        try:
            option = float(input(text).strip())
        except ValueError:
            print("Worng Option, Please enter a Correct Number")
            continue
        break
    return option

def print_values(temperature:float):
    for j in range(5,65,5):
        print("At temperature {:^3.1f}F, and wind speed {:>2.0f} mph, the windchill is: {:>6.2f}F".format(temperature,j,calculate_wind_chill(temperature,j)))


temperature = enter_number_rfloat("What is the temperature? ")
unit = input("Fahrenheit or Celsius (F/C)? ").strip().upper()
if unit == 'C':
    print_values(celsius_to_fahrenheit(temperature))
elif unit == 'F':
    print_values(temperature)
else:
    print("Invalid unit. Please enter 'F' for Fahrenheit or 'C' for Celsius.")