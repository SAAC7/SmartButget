# passwords.py

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
    pass

def word_has_character(word, character_list):
    """Return True if any character in word is in character_list."""
    pass

def word_complexity(word):
    """Return complexity score (0–4) based on character types used."""
    pass

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
    pass

def main():
    """User input loop: prompt for passwords until Q or q to quit."""
    while True:
        pwd = input("Enter a password (or Q to quit): ")
        if pwd.lower() == "q":
            print("Goodbye!")
            break
        # For the milestone, just echo what was entered
        print(f"You entered: {pwd}\n")

if __name__ == "__main__":
    main()

