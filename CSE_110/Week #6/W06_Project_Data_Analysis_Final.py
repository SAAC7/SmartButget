# I have tried to complete all the requirements and I have tried to add some things like getting the information but by entity and also reusing code to show the list of data but for each entity or year. 

# Entity,         Code,   Year,     Life expectancy (years)
# Afghanistan,    AFG,    1950,     27.638
def load_data(ruta):
    data = []
    try:
        with open(ruta) as database:
            for line in database:
                line_parts = line.strip().split(",")
                if len(line_parts) < 4:
                    continue
                entity = line_parts[0]
                code = line_parts[1]
                try:
                    year = int(line_parts[2])
                    life_exp = float(line_parts[3])
                except ValueError:
                    continue
                data.append((entity, code, year, life_exp))
    except FileNotFoundError:
        print(f"El archivo '{ruta}' no se encontró")
    return data

def find_global_min_life_entity_year(data):
    min_life = None
    min_entity = None
    min_year = None
    for line in data:
        # entity, code, year, life_exp = line
        if min_life is None or line[3] < min_life:
            min_entity, _,min_year,min_life = line
    return min_life, min_entity, min_year

def find_global_max_life_entity_year(data):
    max_life = None
    max_entity = None
    for line in data:
        # entity, code, year, life_exp = line
        if max_life is None or line[3] > max_life:
            max_entity, _,max_year,max_life = line
    return max_life, max_entity, max_year

def find_min_max_average_life_entity(data, in_entity):
    entity_data = [record for record in data if record[0].lower() == in_entity.lower()]
    if not entity_data:
        return None  
    total = sum(record[3] for record in entity_data)
    average = total / len(entity_data)
    min_life, _, min_year= find_global_min_life_entity_year(entity_data)
    max_life, _, max_year= find_global_max_life_entity_year(entity_data)
    return average, min_life, max_life, len(entity_data),f"{min_year}-{max_year}"

def print_entity_statistics(entity, average, min_life, max_life, total_records,range_years):
    print("{:>35}|{:^15}|".format(entity.capitalize(), total_records) +
          ("{:^10.2f}|" * 3).format(average, min_life, max_life)+"{:^10}|".format(range_years))

def global_min_max_average_life(data):
    entities = []
    for line in data:
        entity, code, year, life_exp = line
        if entity not in entities:
            entities.append(entity)
    
    print("\n{:^35}|{:^15}|".format("Entity", "Total Records") +
          ("{:^10}|" * 4).format("Average", "Min life", "Max life","Year range"))
    for entity in entities:
        stats = find_min_max_average_life_entity(data, entity)
        if stats:
            average, min_life, max_life, total_records,range_years = stats
            print_entity_statistics(entity, average, min_life, max_life, total_records,range_years)


def find_min_max_average_life_year(data, in_year):
    year_data = [record for record in data if record[2] == in_year]
    if not year_data:
        return None  
    total = sum(record[3] for record in year_data)
    average = total / len(year_data)
    min_life, min_entity, min_year= find_global_min_life_entity_year(year_data)
    max_life, max_entity, max_year= find_global_max_life_entity_year(year_data)
    return average, min_life, max_life, len(year_data),min_entity,max_entity

def print_entity_statistics_by_year(year, average, min_life, max_life, total_records,min_entity,max_entity):
    print("{:^5}|{:^10.2f}|{:^10.2f}|{:^30}|{:^10.2f}|{:^30}|{:^15}|".format(year,average,min_life,min_entity,max_life,max_entity,total_records))

def global_min_max_average_life_by_year(data):
    years = []
    for line in data:
        entity, code, year, life_exp = line
        if year not in years:
            years.append(year)
    
    print("\n{:^5}|{:^10}|{:^10}|{:^30}|{:^10}|{:^30}|{:^15}|".format("Year","Average","Min life", "Entity Min Life Exp", "Max life","Entity Max Life Exp","Total Records"))
    for year in sorted(years):
        stats = find_min_max_average_life_year(data, year)
        if stats:
            average, min_life, max_life, total_records, min_entity,max_entity = stats
            print_entity_statistics_by_year(year, average, min_life, max_life, total_records,min_entity,max_entity)


data = load_data("CSE_110/Week #6/life-expectancy.csv")
while True:
    print(
        "\nHello, this is a tool to analyze the information"
        "\nYou can choose different options to get specific details of the information"
        "\nThese are the options (you can choose it by entering the No.):"
        "\n1. Get the lowest value in the world for life expectancy and its entity."
        "\n2. Get the highest value in the world for life expectancy and its entity."
        "\n3. Obtain statistics from a specific entity."
        "\n4. Obtain statistics from each entity."
        "\n5. Obtain statistics from a specific year."
        "\n6. Obtain statistics from each year."
        "\n7. Exit"
    )
    
    while True:
        try:
            option = int(input("Enter the No. Option (only numbers): ").strip())
            break
        except ValueError:
            print("Incorrect value, please enter a correct number.")
    
    if option == 1:
        life, entity, year = find_global_min_life_entity_year(data)
        print(f"\nThe lowest value for life expectancy is: {life}")
        print(f"The entity with the lowest value for life expectancy is: {entity}")
        print(f"The year with the lowest value for life expectancy is: {year}")
    elif option == 2:
        life, entity, year = find_global_max_life_entity_year(data)
        print(f"\nThe highest value for life expectancy is: {life}")
        print(f"The entity with the highest value for life expectancy is: {entity}")
        print(f"The year with the highest value for life expectancy is: {year}")
    elif option == 3:
        in_entity = input("Please enter an Entity: ")
        stats = find_min_max_average_life_entity(data, in_entity)
        if stats is None:
            print("Enter a correct entity")
            continue
        average, min_life, max_life, total_records,range_years = stats
        print("\n{:^35}|{:^15}|".format("Entity", "Total Records") +
              ("{:^10}|" * 4).format("Average", "Min life", "Max life","Year range"))
        print_entity_statistics(in_entity, average, min_life, max_life, total_records,range_years)
    elif option == 4:
        global_min_max_average_life(data)
    elif option == 5:
        in_year = int(input("Please enter a Year: ").strip())
        stats = find_min_max_average_life_year(data, in_year)
        if stats is None:
            print("Enter a correct entity")
            continue
        average, min_life, max_life, total_records, min_entity,max_entity = stats
        print("\n{:^5}|{:^10}|{:^10}|{:^30}|{:^10}|{:^30}|{:^15}|".format("Year","Average","Min life", "Entity Min Life Exp", "Max life","Entity Max Life Exp","Total Records"))
        print_entity_statistics_by_year(in_year, average, min_life, max_life, total_records,min_entity,max_entity)
    elif option == 6:
        global_min_max_average_life_by_year(data)
    elif option == 7:
        break
    else:
        print("Sorry, this value is out of range")
