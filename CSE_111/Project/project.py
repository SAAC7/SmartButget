import csv
import os
from datetime import datetime 
from typing import List, Dict


FILENAME = "SmartBudget.csv"
CATEGORIES_EXPENSE = {
    'Growth':{
       'Rate': 0.25,
       'Phrase':"The 25% That Works For You!"
       },
    'Stability':{
        'Rate':0.15,
        'Phrase': "The 15% That Kepps You In The Game!"
        },
    'Essential':{
        'Rate':0.5,
        'Phrase':"The 50% That Feed You, Not Tour Ego!"
        },
    'Reward':{
        'Rate':0.1,
        'Phrase':"The 10% That Keeps You Sane!"
        }
}
CATEGORIES_INCOME = {
    'Employment Income':'Salary, wages, bonuses, commissions',
    'Business / Self-Employment Income':'Product sales, service fees',
    'Investment & Passive Income':'Rentals, dividends, interest, royalties',
    'Other Income':'Gifts, inheritances, asset sales, prizes'
}

def read_dictionary(filename: str = FILENAME) -> List[Dict]:
    entries = []
    if not os.path.isfile(filename):
        return entries
    try:
        with open(filename,"rt") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    row["Amount"] = float(row["Amount"])
                except ValueError:
                    print(f"Warning: Invalid amount '{row['Amount']}' skipped.")
                    continue
                entries.append(row)
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
    return entries


def save_dictionary(entries: Dict, filename: str = FILENAME):
    file_exists = os.path.isfile(filename)
    try:
        with open(filename, "a") as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=['Date','Type','Category','Description','Amount'])
            if not file_exists:
                writer.writeheader()
            writer.writerow(entries)
    except Exception as e:
        print(f"Error saving transaction: {e}")


def record_transaction(date_isoformat:str,income:bool,category:str,description:str,amount:float) -> Dict:
    """
    Create a transaction record.

    Parameters:
        date_isoformat (str): Date in ISO 8601 format.
        income (bool): True if it's an income, False if it's an expense.
        category (str): Transaction category.
        description (str): Description of the transaction.
        amount (float): Transaction amount.

    Returns:
        dict: A dictionary representing the transaction.
    """
    return{
        'Date': date_isoformat,
        'Type': 'Income' if income else 'Expense',
        'Category': category,
        'Description': description,
        'Amount': amount
    }

def enter_date() -> str:
    while True:
        date_input = input("Enter date (MM-DD-YY) and optionally time (HH:MM): ").strip()
        try:
            if len(date_input.split()) == 2:
                date_str, time_str = date_input.split()
                datetime_format = datetime.strptime(f"{date_str} {time_str}", "%m-%d-%y %H:%M")
            else:
                datetime_format = datetime.strptime(date_input, "%m-%d-%y")
            return datetime_format.isoformat()
        except ValueError:
            print("Invalid date/time format. Please try again.")


def choose_date_or_now() -> str:
    while True:
        choice = input("Use current date and time? (y/n): ").strip().lower()
        if choice == "y":
            return datetime.now().isoformat()
        elif choice == "n":
            return enter_date()
        else:
            print("Invalid input, please enter 'y' or 'n'.")


def filter_transactio(entries:List[Dict],year:int=None,month:int=None,day:int=None)->List[Dict]:
    """
    This filter filters transactions for a specific date.
    """
    return [entries_filter for entries_filter in entries if (
        (year is None or int(entries_filter['Date'][:4])==year) and
        (month is None or int(entries_filter['Date'][5:7])==month) and
        (day is None or int(entries_filter['Date'][8:10])==day)
    )]

def choose_categories(categories:Dict)->str:
    for i, cat in enumerate(categories.keys(),start=1):
        print(f"{i}. {cat}: {categories[cat]["Phrase"]}")
    while True:
        try:
            seleccion = int(input("Select a category (number):"))
            if 1 <= seleccion <= len(categories):
                return list(categories.keys())[seleccion - 1]
            else:
                print("Number out of range. Please try again.")
        except ValueError:
            print("Invalid input. Enter a number.")

def registrar_transaccion(is_income: bool, entries: List[Dict]):
    date = choose_date_or_now()
    categories = CATEGORIES_INCOME if is_income else CATEGORIES_EXPENSE
    cat = choose_categories(categories)
    desc = input("Description: ")
    while True:
        try:
            amt = float(input("Amount: "))
            if amt < 0:
                print("Amount cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")
    transaction = record_transaction(date, is_income, cat, desc, amt)
    save_dictionary(transaction)
    entries.append(transaction)
    print("Recorded Income." if is_income else "Recorded Expense.")



def generar_resumen(entries: List[Dict], year: int, month: int) -> Dict[str, float]:
    """
    Genera un diccionario con resumen total ingresos y gastos por categoría,
    además de las asignaciones ideales para ese mes y año.
    """
    transacciones = filter_transactio(entries, year=year, month=month)
    total_income = sum(t['Amount'] for t in transacciones if t['Type'] == 'Income')
    total_expense = sum(t['Amount'] for t in transacciones if t['Type'] == 'Expense')
    
    resumen = {'Total Income': total_income,'Total Encome':total_expense}
    
    for cat in CATEGORIES_EXPENSE.keys():
        gasto_cat = sum(t['Amount'] for t in transacciones if t['Type'] == 'Expense' and t['Category'] == cat)
        asignacion = total_income * CATEGORIES_EXPENSE[cat]['Rate'] if total_income else 0
        resumen[cat] = gasto_cat
        resumen[f'Alloc_{cat}'] = asignacion
        
    return resumen

def print_summary(summary: Dict[str, float]) -> None:
    """
    Muestra el resumen en pantalla con notificaciones de excedentes.
    """
    print(f"\n{'--- Budget Summary ---':^51}")
    print(f"Total: {summary['Total Encome']:^12.2f}/{summary['Total Income']:^12.2f}\n")
    for cat in CATEGORIES_EXPENSE.keys():
        spent = summary[cat]
        alloc = summary[f'Alloc_{cat}']
        status = ''
        if spent > alloc:
            status = f" (Exceeded {spent - alloc:.2f})"
        print(f"{cat:<10}: Spent {spent:>10.2f} / Allocated {alloc:>10.2f}{status}")
    print(f"{'-'*51}\n")

def print_detailed_transactions(entries: List[Dict], year: int = None, month: int = None, day: int = None) -> None:
    transacciones = filter_transactio(entries, year=year, month=month, day=day)
    if not transacciones:
        print("No transactions found for this period.\n")
        return
    
    # Encabezados
    print(f"{'Description':<30} {'Expense':>12} {'Income':>12}")
    print("-" * 56)
    
    for t in transacciones:
        desc = t['Description'][:28]
        expense_amt = f"{t['Amount']:.2f}" if t['Type'] == 'Expense' else ''
        income_amt = f"{t['Amount']:.2f}" if t['Type'] == 'Income' else ''
        print(f"{desc:<30} {expense_amt:>12} {income_amt:>12}")
    print("-" * 56 + "\n")

def show_filtered_transactions(entries: List[Dict]):
    print("\nFilter by:")
    print("1) Year")
    print("2) Month")
    print("3) Day")
    choice = input("Choose an option (1-3): ").strip()

    year = month = day = None

    try:
        if choice == '1':
            year = int(input("Enter year (yyyy): "))
            if year < 1:
                raise ValueError("Year must be positive.")

        elif choice == '2':
            year, month = map(int, input("Enter year and month (yyyy-mm): ").split("-"))
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 1 and 12.")

        elif choice == '3':
            year, month, day = map(int, input("Enter date (yyyy-mm-dd): ").split("-"))
            datetime(year, month, day)  # valida fecha real

        else:
            print("Invalid choice.")
            return

        print_detailed_transactions(entries, year=year, month=month, day=day)

    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception:
        print("Invalid format. Please enter numbers in the correct format.")

def main():
    entries = read_dictionary()
    while True:
        print("\nMenú SmartBudget:\n1) Record Income\n2) Record Expense\n3) Ver resumen\n4) Special Filter\n5) Salir")
        choice = input("Choose an option: ")
        if choice == '1':
            registrar_transaccion(True, entries)
        elif choice == '2':
            registrar_transaccion(False, entries)
        elif choice == '3':
            while True:
                date = input("Enter the year and month for the summary (yyyy-mm): ").strip()
                try:
                    year, month = map(int, date.split("-"))
                    if 1 <= month <= 12:
                        break
                    else:
                        print("Month must be between 1 and 12.")
                except Exception:
                    print("Invalid format. Please enter as yyyy-mm.")
            summary = generar_resumen(entries, year, month)
            print_summary(summary)
            print_detailed_transactions(entries,year, month)
        elif choice == '4':
            show_filtered_transactions(entries)
        elif choice == '5':
            print("¡Good Luck!")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == '__main__':
    main()
