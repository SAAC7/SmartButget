import csv
import os
import datetime
from typing import List, Dict


FILENAME = "SmartBudget.csv"
CATEGORIES = {
    'Growth':[0.25,"The 25% that works for you!"],
    'Stability':[0.15,"THAT KEPPS YOU IN THE GAME!"],
    'Essential':[0.5,"The 50% that feed you, not tour ego!"],
    'Reward':[0.1,"The 10% that keeps you sane!"]
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
