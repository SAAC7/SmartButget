import sqlite3, os
from datetime import datetime
import json
from pathlib import Path

CATEGORIES_EXPENSE = {
    'Growth': {'Rate': 0.25, 'Phrase': "The 25% That Works For You!"},
    'Stability': {'Rate': 0.15, 'Phrase': "The 15% That Keeps You In The Game!"},
    'Essential': {'Rate': 0.5, 'Phrase': "The 50% That Feed You, Not Your Ego!"},
    'Reward': {'Rate': 0.1, 'Phrase': "The 10% That Keeps You Sane!"}
}
CATEGORIES_INCOME = {
    'Employment Income': {'Phrase': 'Salary, wages, bonuses, commissions'},
    'Business / Self-Employment Income': {'Phrase': 'Product sales, service fees'},
    'Investment & Passive Income': {'Phrase': 'Rentals, dividends, interest, royalties'},
    'Other Income': {'Phrase': 'Gifts, inheritances, asset sales, prizes'}
}

def sting_json(any):
    return json.dumps(any)

def init_db(db_path: Path):
        """Inicializa la base de datos si no existe."""
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()

            cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                last name TEXT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )""")

            cur.execute("""CREATE TABLE IF NOT EXISTS Accounts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT NOT NULL,
                bank_name TEXT NOT NULL,
                account_type TEXT,
                currency TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES Users(id),       
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS Transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT,
                description TEXT,
                amount REAL NOT NULL,
                account_id INTEGER NOT NULL,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES Users(id),       
                FOREIGN KEY(account_id) REFERENCES Accounts(id),
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS Transfers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_account INTEGER NOT NULL,
                to_account INTEGER NOT NULL,
                amount REAL NOT NULL,
                commission REAL DEFAULT 0,
                exchange_rate REAL DEFAULT 1,
                date TEXT NOT NULL,
                description TEXT,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES Users(id),       
                FOREIGN KEY(from_account) REFERENCES Accounts(id),
                FOREIGN KEY(to_account) REFERENCES Accounts(id),       
            )""")


            conn.commit()
        print("DB initialized!")

def upgrade(db_path:Path):
    with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                last name TEXT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )""")
            cur.execute(
                """
                ALTER TABLE Transfers ADD COLUMN user_id INTEGER,
                ALTER TABLE Transactions ADD COLUMN user_id INTEGER,
                ALTER TABLE Accounts ADD COLUMN user_id INTEGER,

                UPDATE  SET

                """
            )
def get_connection(db_path:Path):
        first_time = not db_path.exists()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        if first_time:
            init_db(db_path)  # <-- pasamos el path
        return conn

def query_db(db_path:Path , query, params=(), fetch=False):
        conn = get_connection(db_path)
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        if fetch:
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
        return None

def generate_summary(db_path:Path,year, month):
        # Trae transacciones con la moneda de la cuenta
        rows = query_db(db_path,"""
        SELECT t.*, a.currency
        FROM Transactions t
        JOIN Accounts a ON t.account_id = a.id

        WHERE strftime('%Y', t.date)=? AND strftime('%m', t.date)=?
        """, (str(year), f"{month:02d}"), fetch=True)

        transfer_row = query_db(db_path,"""
            SELECT t.*, a.currency, 'out' AS direction
            FROM Transfers t
            JOIN Accounts a ON t.from_account = a.id
            WHERE strftime('%Y', t.date)=? AND strftime('%m', t.date)=?
            UNION ALL
            SELECT t.*, a.currency, 'in' AS direction
            FROM Transfers t
            JOIN Accounts a ON t.to_account = a.id
            WHERE strftime('%Y', t.date)=? AND strftime('%m', t.date)=?
        """, (str(year), f"{month:02d}",str(year),f"{month:02d}"), fetch=True)


        # Agrupar por currency
        currencies = set(r["currency"] for r in rows)
        summaries = {}

        for cur in currencies:
            # Filtrar solo transacciones de esta moneda
            rows_cur = [r for r in rows if r["currency"] == cur]
            rows_transfer_cur = [r for r in transfer_row if r["currency"] == cur]

            income_transfers = sum(((r["amount"]-r["commission"])*(r["exchange_rate"]))for r in rows_transfer_cur if r["direction"] == "in")
            expense_transfers = sum((r["amount"]-r["commission"]) for r in rows_transfer_cur if r["direction"] == "out")

            total_income = sum(r["amount"] for r in rows_cur if r["type"] == "Income")
            total_expense = sum(r["amount"] for r in rows_cur if r["type"] == "Expense")
            dime = (total_income + income_transfers - expense_transfers-sum((r["commission"]) for r in rows_transfer_cur if r["direction"] == "out"))*.1
            resumen = {
                "Currency": cur,
                "Total Income": total_income,
                "Total Expenses": total_expense,
                "Transfer Income": income_transfers,
                "Transfer Expenses": expense_transfers,
                "Dime":dime
            }
            # Calcular por categoría (solo gastos)
            for cat in CATEGORIES_EXPENSE.keys():
                gasto_cat = sum(
                    r['amount'] for r in rows_cur if r['type'] == 'Expense' and r['category'] == cat
                )
                asignacion = total_income * CATEGORIES_EXPENSE[cat]['Rate'] if total_income else 0
                resumen[cat] = gasto_cat
                resumen[f'Alloc_{cat}'] = asignacion

            summaries[cur] = resumen
            summaries = dict(sorted(summaries.items()))

        return summaries, rows


def account_balances(db_path:Path):
    accounts = query_db(db_path,"SELECT * FROM Accounts", fetch=True)
    balances = {a["id"]: {"account": a, "balance": 0} for a in accounts}
    balances_total = set(r["currency"] for r in accounts)
    # print(balances)
    # Procesar transacciones normales
    for t in query_db(db_path,"SELECT * FROM Transactions", fetch=True):
        if t["type"] == "Income":
            balances[t["account_id"]]["balance"] += t["amount"]
        elif t["type"] == "Expense":
            balances[t["account_id"]]["balance"] -= t["amount"]
    # Procesar transferencias
    for tr in query_db(db_path,"SELECT * FROM Transfers", fetch=True):
        amt = tr["amount"] - tr["commission"]
        balances[tr["from_account"]]["balance"] -= amt
        balances[tr["to_account"]]["balance"] += amt * tr["exchange_rate"]
    totals_by_currency = {}
    for b in balances.values():
        type_account = b["account"]["account_type"]
        if "tarjeta" not in type_account.lower() or b["balance"]<0:
            cur = b["account"]["currency"]
            totals_by_currency[cur] = totals_by_currency.get(cur, 0) + b["balance"]
    return balances, totals_by_currency

def add_transfer(db_path:Path,transfer):
    query_db(db_path,"""INSERT INTO Transfers(from_account,to_account,amount,commission,exchange_rate,date,description)
                    VALUES(?,?,?,?,?,?,?)""",
                (transfer["from_acc"], transfer["to_acc"],transfer["amount"],transfer["commission"],transfer["rate"],transfer["date"], transfer["description"]))
    if transfer["commission"]>0:
        query_db(db_path,"""INSERT INTO Transactions(date,type,category,description,amount,account_id)
                    VALUES(?,?,?,?,?,?)""",
                (transfer["desc"],"Expense", "Essential",f"Transfer fee from Account_Id {transfer["from_acc"]} to Account_Id {transfer["to_acc"]}" , transfer["commission"], transfer["from_acc"]))
        
def add_transaction(db_path:Path,transactions):
     query_db(db_path,"""INSERT INTO Transactions(date,type,category,description,amount,account_id)
                    VALUES(?,?,?,?,?,?)""",
                (transactions["date"], transactions["type"], transactions["category"], transactions["description"], transactions["amount"], transactions["account_id"]))
     
def add_account(db_path:Path,account):
     query_db(db_path,"""INSERT INTO Accounts(account_number,bank_name,account_type,currency)
                    VALUES(?,?,?,?)""", (account["number"], account["bank"], account["type"], account["currency"]))
