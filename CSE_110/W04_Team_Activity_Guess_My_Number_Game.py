# This function is to control the possible errors that may appear, and with that I have a better program.
def get_number(text):
    isnumber = True
    number = 0
    
    while isnumber:
        try:
            number = int(input(text))
            isnumber = False
        except Exception as e:
            isnumber = True
            print(f"Wrong input, Please enter a correct value")
    return number
# This function is to get the random number, but I can reuse this code if needed
def magic_num():
    import random
    return random.randint(1,100)
# this is the main code of the game, but I made it as a function of the flexibility of replaying the game
def game():
    magic_number = magic_num()
    guess = None
    attempts = 0
    while (guess != magic_number):
        guess = get_number("What is your guess? ")
        attempts +=1
        print("Higher" if guess < magic_number else "Lower" if guess > magic_number else f"You guessed it! It took you {attempts} attempts.")
print(f"Welcom to guess the number\nThis game was made with some functions to have a cleanest code")
while True:
    game()
    if input("Do you want to play again? (yes/no) ").strip().lower() == "no":
        print("Thanks for playing!")
        break