from . import data_access
from pathlib import Path
from datetime import datetime
class SmartBudgetServices:
    def __init__(self, db_path:Path):
        self.db_path = db_path
        data_access.init_db(self.db_path)

    def add_account(self,number,bank,type,currency):
        account={
            "number":number,
            "bank":bank,
            "type":type, 
            "currency":currency
        }
        data_access.add_account(self.db_path ,account)
    def add_transaction(self,date,type,category,description,amount,account_id):
        transaction={
            "date":date,
            "type":type,
            "category":category,
            "description":description,
            "amount":amount,
            "account_id":account_id
        }
        data_access.add_transaction(self.db_path ,transaction)

    def add_transfer(self,from_account,to_account,amount,commission,rate,date,description):
        transfer={
           "from_acc":from_account,
           "to_acc":to_account,
           "amount":amount,
           "commission":commission,
           "rate":rate,
           "date":date,
           "description":description
        }
        data_access.add_transfer(self.db_path ,transfer)
    
    def get_summary(self,year,month):
        return data_access.generate_summary(self.db_path,year,month)
    
    def get_balances(self):
        return data_access.account_balances(self.db_path)