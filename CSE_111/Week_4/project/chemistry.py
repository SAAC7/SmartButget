import os
from formula import parse_formula
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

def compute_molar_mass(symbol_quantity_list, periodic_table_dict):
    """
    Compute and return the total molar mass for the given symbol-quantity list.
    """
    total_mass = 0.0
    for symbol, quantity in symbol_quantity_list:
        atomic_mass = periodic_table_dict[symbol][1]
        total_mass += atomic_mass * quantity
    return total_mass


def main():
    known_formulas = {
        "H2O": "Water",
        "NaCl": "Sodium Chloride",
        "C6H12O6": "Glucose",
        "NaOH": "Sodium Hydroxide",
        "CH4": "Methane",
        "NH3": "Ammonia",
        "CO2": "Carbon Dioxide"
    }
    # Get user inputs
    formula = input("Enter the molecular formula of the sample: ")
    if formula in known_formulas:
        print(f"Known compound detected: {known_formulas[formula]}")
    sample_mass = float(input("Enter the mass in grams of the sample: "))

    # Build periodic table
    periodic_table = make_periodic_table()

    # Parse formula into symbol-quantity list
    symbol_quantity_list = parse_formula(formula, periodic_table)
    print(symbol_quantity_list)

    # Compute molar mass
    molar_mass = compute_molar_mass(symbol_quantity_list, periodic_table)
    print(f"Molar mass: {molar_mass:.5f} grams/mole")

    # Compute number of moles
    number_of_moles = sample_mass / molar_mass
    print(f"Number of moles: {number_of_moles:.5f} moles")


if __name__ == "__main__":
    main()
