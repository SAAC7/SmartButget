number = -int(input("Enter a positive number"))
while number < 0:
    print("Sorrry that is a negative number.")
    number = int(input("Enter a positive number"))
print(f"The number is {number}") 

print()

answer = ""
while answer.lower() != "yes":
    answer=input("May I have a piece of candy? ")
print("Thnak you")