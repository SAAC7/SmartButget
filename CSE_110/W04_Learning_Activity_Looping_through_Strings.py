word = "commitment"
favorite_word = input("Enter your favorite letter. ")
for letter in word:
    if letter.lower() == favorite_word.lower():
        print(letter.upper(),end="")
    else:
        print(letter.lower(),end="")
        
print("")        
print("Hiden letter")        

for letter in word:
    if letter.lower() == favorite_word.lower():
        print("_",end="")
    else:
        print(letter.lower(),end="")
print("")        