import random
def main():
    numbers = [16.2,75.1,52.3]
    words=[]

    print(numbers)
    print(words)
    print("add new number")
    append_random_numbers(numbers,3)
    append_random_words(words,3)
    print(numbers)
    print(words)

def append_random_numbers(numbers_list,quantity=1):
    for i in range(quantity):
        numbers_list.append(round(random.uniform(0,100),1))

def append_random_words(words_list,quantity=1):
    words_candidates = ['big','Coca','Pepsi','arm','car',"arm", "car", "cloud", "head", "heal", "hydrogen", "jog",
        "join", "laugh", "love", "sleep", "smile", "speak",
        "sunshine", "toothbrush", "tree", "truth", "walk", "water"]
    for i in range(quantity):
        words_list.append(random.choice(words_candidates))

if __name__ == "__main__":
    main()