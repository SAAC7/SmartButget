import csv
import os
import datetime
from typing import List, Dict


FILENAME = "SmartBudget.csv"
CATEGORIES = {
    'Growth':{
       'Rate': 0.25,
       'Phrase':"The 25% that works for you!"
       },
    'Stability':{
        'Rate':0.15,
        'Phrase': "THAT KEPPS YOU IN THE GAME!"
        },
    'Essential':{
        'Rate':0.5,
        'Phrase':"The 50% that feed you, not tour ego!"
        },
    'Reward':{
        'Rate':0.1,
        'Phrase':"The 10% that keeps you sane!"
        }
}

def read_dictionary(filename: str = FILENAME) -> List[Dict]:
    """
    This read the csv file an return a list of diccionaries
    """
    entries = []
    with open(filename,"rt") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            row["Amount"] = float(row["Amount"])
            entries.append(row)
    return entries

def save_dictionary(entries: Dict, filename: str = FILENAME):
    """
    This save all the entries in a csv file
    """
    file_exists = os.path.isfile(filename)
    with open(filename, "a") as csv_file:
        writer = csv.DictWriter(csv_file,fieldnames=['Date','Type','Category','Description','Amount'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(entries)

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
    """
    Ask the user for a date in MM-DD-YY format and optionally time in HH:MM.
    """
    date_input = input("Enter date (MM-DD-YY) and optionally time (HH:MM): ")
    if len(date_input.strip().split()) == 2:
        date_str, time_str = date_input.strip().split()
        datetime_format = datetime.strptime(f"{date_str} {time_str}", "%m-%d-%y %H:%M")
    else:
        datetime_format = datetime.strptime(date_input.strip(), "%m-%d-%y")
    return datetime_format.isoformat()

def filter_transactio(entries:List[Dict],year:int=None,month:int=None,day:int=None)->List[Dict]:
    """
    This filter filters transactions for a specific date.
    """
    return [entries_filter for entries_filter in entries if (
        (year is None or int(entries_filter['Date'][:4])==year) and
        (month is None or int(entries_filter['Date'][5:7])==month) and
        (day is None or int(entries_filter['Date'][8:10])==day)
    )]
