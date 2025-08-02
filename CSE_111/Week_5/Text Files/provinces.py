def read_file(filename):
    text_list=[]
    with open(filename,"rt") as text_file:
        for line in text_file:
            text  = line.strip()
            text_list.append(text)
    return text_list

def main():
    provinces_text = read_file("provinces.txt")
    print(provinces_text)
    provinces_text.pop(0)
    provinces_text.pop()
    for i in range(len(provinces_text)):
        if provinces_text[i] == "AB":
            provinces_text[i] = "Alberta"
    count = provinces_text.count("Alberta")
    print()
    print(f"Alberta occurs {count} times in the modified list.")

if __name__ == "__main__":
        main()
