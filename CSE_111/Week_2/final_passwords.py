# passwords.py
import os
# —————————————————————
# Character type constants (lists from Sven)
LOWER = [
    "a","b","c","d","e","f","g","h","i","j","k","l","m",
    "n","o","p","q","r","s","t","u","v","w","x","y","z"
]
UPPER = [
    "A","B","C","D","E","F","G","H","I","J","K","L","M",
    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
]
DIGITS = ["0","1","2","3","4","5","6","7","8","9"]
SPECIAL = [
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
    "-", "_", "=", "+", "[", "]", "{", "}", "|", ";",
    ":", "\"", "'", ",", ".", "<", ">", "?", "/", "`", "~"
]
# —————————————————————

def word_in_file(word, filename, case_sensitive=False):
    """Return True if word is found in filename (one word per line)."""
    if not os.path.isfile(filename):
        return False
    with open(filename,"r") as file:
        for line in file:
            entry = line.strip()
            if case_sensitive:
                if word == entry:
                    return True
            else:
                if word.lower() == entry.lower():
                    return True
    return False

def word_has_character(word, character_list):
    """Return True if any character in word is in character_list."""
    for ch in word:
        if ch in character_list:
            return True
    return False

def word_complexity(word):
    """Return complexity score (0–4) based on character types used."""
    score = 0
    if word_has_character(word,LOWER):
        score +=1
    if word_has_character(word,UPPER):
        score +=1
    if word_has_character(word,DIGITS):
        score +=1
    if word_has_character(word,SPECIAL):
        score +=1

    return score

def password_strength(password, min_length=10, strong_length=16):
    """
    Return strength score (0–5) based on:
      1) dictionary match
      2) common passwords list
      3) minimum length
      4) strong length
      5) character-type complexity
    Prints messages for cases 1–4.
    """
    # 1) Dictionary word (case-insensitive)
    if word_in_file(password, "wordlist.txt", case_sensitive=False):
        print("Password is a dictionary word and is not secure.")
        return 0

    # 2) Common password (case-sensitive)
    if word_in_file(password, "toppasswords.txt", case_sensitive=True):
        print("Password is a commonly used password and is not secure.")
        return 0

    # 3) Too short
    if len(password) < min_length:
        print("Password is too short and is not secure.")
        return 1

    # 4) Long password overrides complexity
    if len(password) >= strong_length:
        print("Password is long, length trumps complexity—this is a good password.")
        return 5

    # 5) Complexity-based strength
    complexity = word_complexity(password)
    return 1 + complexity

def log_password_strength(password, strength):
    """Append the password and strength score to a log file."""
    with open("password_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{password},{strength}\n")


def main():
    """User input loop: prompt for passwords until Q or q to quit."""
    print("=== Password Strength Checker ===")
    while True:
        pwd = input("Enter a password (or Q to quit): ")
        if pwd.lower() == "q":
            print("Goodbye!")
            break

        strength = password_strength(pwd)
        print(f"Strength score: {strength}\n")

        # NEW: log password and strength
        log_password_strength(pwd, strength)

if __name__ == "__main__":
    main()

