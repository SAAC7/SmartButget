import os
def make_periodic_table():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(base_dir, "elements.csv")
    # filename="elements.csv"
    print(filename)
    periodic_table={}
    if not os.path.isfile(filename):
        return False
    with open(filename, "r", encoding="utf-8-sig") as file:
        for line in file:
            entry = line.strip().replace('"', '').split(",")
            if not entry or entry[0].strip()=="Symbol" or len(entry) < 3:
                continue
            
            periodic_table[entry[0]]=[entry[1],float(entry[2])]
    
    return periodic_table
