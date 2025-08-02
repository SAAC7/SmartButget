import csv
def get_dictionary(filename,key_column):
    dictionary = {}
    with open(filename,"rt") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row_list in reader:
            key = row_list[key_column]
            dictionary[key]=row_list
    return dictionary

def main():
    I_NUMBER_INDEX = 0
    NAME_INDEX = 1
    
    student_dic = get_dictionary("students.csv",I_NUMBER_INDEX)
    print(student_dic)
    inumber = input("Please enter an I-Number (xxxxxxxxx): ")
    #inumber = inumber.replace("-","")
    if not inumber.isdigit():
        print("Invalid I-Number")
    else:
        if len(inumber) < 9:
            print("Invalid I-Number: too few digits")
        elif len(inumber) > 9:
            print("Invalid I-Number: too many digits")
        else:
            if inumber not in student_dic:
                print("No such student")
            else:
                value = student_dic[inumber]
                name = value[NAME_INDEX]
                print(name)

if __name__ == "__main__":
    main()