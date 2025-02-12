# develop this function to generate the hint and use it at any other time if required
def generate_hint(hidden_word,guess):
    hint=[]
    for i in range(len(hidden_word)):
        if guess[i].lower()==hidden_word[i].lower():
            hint.append(guess[i].upper())

        elif guess[i].lower() in [letter.lower() for letter in hidden_word]:
            hint.append(guess[i].lower())
        else:
            hint.append("_")
    return " ".join(hint)
# I develop this funcion to recive array of words and return the hidden word
def random_word(array):
    import random
    return array[random.randint(0,len(array)-1)]
def word_guessing_game():
    # I add this array to posible words to guess 
    posible_words=["mosiah","Alma","MORONI","NEPHI","jacob","Helaman","Mormon"]
    hidden_word = random_word(posible_words)
    guess_count = 0
    correct_guess = False
    print("Welcome to the word guessing game!\nIn this game you can play without any problem because this game has code to avoid any problem.\n")
    print(f"Your initial hint is {'_ '*len(hidden_word)}\n")

    while not correct_guess:
        guess = input("What is your guess? ").lower()
        guess_count += 1

        if len(hidden_word) != len(guess):
            print(f"Sorry, the guessed word must have the same number of letters as the secret word.")
            continue

        if guess.lower() == hidden_word.lower():
            correct_guess = True
            print(f"Congratulations! You guessed it!")
            print(f"It took you {guess_count} guesses.")
        else:
            hint = generate_hint(hidden_word,guess)
            print(f"Your guess was not correct.\nYou will have a hint.\nYour hint is {hint}")


word_guessing_game()