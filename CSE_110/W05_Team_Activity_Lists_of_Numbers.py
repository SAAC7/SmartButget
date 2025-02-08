numbers = []
print(f"Enter a list of numbers, type 0 when finished.")
while True:
    number = float(input("Enter number: "))
    if number == 0:
        break
    numbers.append(number)

if not numbers:
    print("\nNo numbers entered.\n")
else:
    total = sum(numbers)
    average = total / len(numbers)
    maximus = max(numbers)
    print(f"The sum is: {total}")
    print(f"The average is: {average}")
    print(f"The largest number is: {maximus}")

    positive_numbers = [num for num in numbers if num > 0]
    if positive_numbers :
        smallest_positive_number = min(positive_numbers)
        print(f"The smallest positive number is: {smallest_positive_number}")
    else:
        print("There are no positive numbers")
    
    sorted_numbers = sorted(numbers)
    print("The sorted list is: ")
    for num in sorted_numbers:
        print(num)