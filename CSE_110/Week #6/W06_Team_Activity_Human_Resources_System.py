with open("CSE_110/Week #6/hr_system.txt") as line_hr_system:
    for data in line_hr_system:
        name = data.split()[0]
        id_number = data.split()[1]
        title = data.split()[2]
        salary = float(data.split()[3])/24
        print("Name: {:<10} (ID: {:>5}) Title: {:<10}- ${:>10.2f}".format(name+",", id_number,title,salary+1000 if title.lower() == "engineer" else salary))