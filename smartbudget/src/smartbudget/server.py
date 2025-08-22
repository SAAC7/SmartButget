from flask import Flask, render_template_string, request, redirect
import sqlite3, os
from datetime import datetime

from pathlib import Path
import pkg_resources

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

def init_db(db_path: Path):
        """Inicializa la base de datos si no existe."""
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Accounts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT NOT NULL,
                bank_name TEXT NOT NULL,
                account_type TEXT,
                currency TEXT NOT NULL
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS Transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT,
                description TEXT,
                amount REAL NOT NULL,
                account_id INTEGER NOT NULL,
                FOREIGN KEY(account_id) REFERENCES Accounts(id)
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
                FOREIGN KEY(from_account) REFERENCES Accounts(id),
                FOREIGN KEY(to_account) REFERENCES Accounts(id)
            )""")
            conn.commit()
        print("DB initialized!")

def create_app(db_path:Path):

    app = Flask(
    __name__,
    static_folder=str(Path(__file__).parent / "resources" / "static"),
    static_url_path="/static"  # <-- esto asegura que Flask sirva /static/
    )

    print(app.static_folder)
    app.config["DB_PATH"] = Path(db_path)
    if not Path(db_path).exists():
        init_db(db_path)

    def get_db():
        db_file = Path(app.config["DB_PATH"])
        first_time = not db_file.exists()
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        if first_time:
            init_db(db_file)  # <-- pasamos el path
        return conn 



    app.get_db = get_db
    # --------------------------
    # DB Helpers
    # --------------------------
    def query_db(query, params=(), fetch=False):
        conn = app.get_db()
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        if fetch:
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
        return None

    # --------------------------
    # Funciones Summary
    # --------------------------
    def generate_summary(year, month):
        # Trae transacciones con la moneda de la cuenta
        rows = query_db("""
        SELECT t.*, a.currency
        FROM Transactions t
        JOIN Accounts a ON t.account_id = a.id
        
        WHERE strftime('%Y', t.date)=? AND strftime('%m', t.date)=?
        """, (str(year), f"{month:02d}"), fetch=True)

        transfer_row = query_db("""
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
            resumen = {
                "Currency": cur,
                "Total Income": total_income,
                "Total Expenses": total_expense,
                "Transfer Income": income_transfers,
                "Transfer Expenses": expense_transfers
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


    def account_balances():
        accounts = query_db("SELECT * FROM Accounts", fetch=True)
        balances = {a["id"]: {"account": a, "balance": 0} for a in accounts}

        # Procesar transacciones normales
        for t in query_db("SELECT * FROM Transactions", fetch=True):
            if t["type"] == "Income":
                balances[t["account_id"]]["balance"] += t["amount"]
            elif t["type"] == "Expense":
                balances[t["account_id"]]["balance"] -= t["amount"]

        # Procesar transferencias
        for tr in query_db("SELECT * FROM Transfers", fetch=True):
            amt = tr["amount"] - tr["commission"]
            balances[tr["from_account"]]["balance"] -= amt
            balances[tr["to_account"]]["balance"] += amt * tr["exchange_rate"]

        return balances

    # --------------------------
    # Rutas Flask
    # --------------------------
    @app.route("/")
    def index():
        resumen, rows = generate_summary(datetime.now().year, datetime.now().month)
        balances = account_balances()
        return render_template_string(TEMPLATE,
                                    entries=rows,
                                    resumen=resumen,
                                    accounts=balances.values(),
                                    CATEGORIES_INCOME=CATEGORIES_INCOME,
                                    CATEGORIES_EXPENSE=CATEGORIES_EXPENSE)

    @app.route("/add", methods=["POST"])
    def add():
        tipo = request.form.get("type")
        categoria = request.form.get("category")
        desc = request.form.get("description")
        dt_str = request.form.get("date_in")
        dt_obj = datetime.fromisoformat(dt_str)
        amount = float(request.form.get("amount"))
        account_id = int(request.form.get("account"))

        query_db("""INSERT INTO Transactions(date,type,category,description,amount,account_id)
                    VALUES(?,?,?,?,?,?)""",
                (dt_obj.isoformat(), tipo, categoria, desc, amount, account_id))
        return redirect("/")

    @app.route("/add_account", methods=["POST"])
    def add_account():
        acc_num = request.form.get("acc_num")
        bank = request.form.get("bank")
        acc_type = request.form.get("acc_type")
        currency = request.form.get("currency")
        query_db("""INSERT INTO Accounts(account_number,bank_name,account_type,currency)
                    VALUES(?,?,?,?)""", (acc_num, bank, acc_type, currency))
        return redirect("/")

    @app.route("/transfer", methods=["POST"])
    def transfer():
        from_acc = int(request.form.get("from_account"))
        to_acc = int(request.form.get("to_account"))
        amount = float(request.form.get("amount"))
        commission = float(request.form.get("commission") or 0)
        rate = float(request.form.get("exchange_rate") or 1)
        desc = request.form.get("description")
        dt_obj = datetime.fromisoformat(request.form.get("date_in"))

        query_db("""INSERT INTO Transfers(from_account,to_account,amount,commission,exchange_rate,date,description)
                    VALUES(?,?,?,?,?,?,?)""",
                (from_acc, to_acc, amount, commission, rate, dt_obj.isoformat(), desc))
        if commission>0:
            query_db("""INSERT INTO Transactions(date,type,category,description,amount,account_id)
                    VALUES(?,?,?,?,?,?)""",
                (dt_obj.isoformat(), "Expense", "Essential",f"Transfer fee from Account_Id {from_acc} to Account_Id {to_acc}" , commission, from_acc))
        
        return redirect("/")

    # --------------------------
    # TEMPLATE reducido
    # --------------------------
    TEMPLATE = """
    <!doctype html>
    <html>
    <head>
    <title>SmartBudget DB</title>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <script src="/static/js/bootstrap.bundle.min.js"></script>
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        const typeSelect = document.querySelector("select[name='type']");
        const categorySelect = document.querySelector("select[name='category']");

        // Categorías pre-cargadas desde Flask (JSON)
        const categoriesIncome = {{ CATEGORIES_INCOME | tojson }};
        const categoriesExpense = {{ CATEGORIES_EXPENSE | tojson }};

        function updateCategories() {
            const type = typeSelect.value;
            categorySelect.innerHTML = ""; // Limpiar opciones

            let categories;
            if (type === "Income") {
                categories = categoriesIncome;
            } else {
                categories = categoriesExpense;
            }

            for (let key in categories) {
                let option = document.createElement("option");
                option.value = key;
                option.textContent = key;
                categorySelect.appendChild(option);
            }
        }

        // Inicializar y escuchar cambios
        typeSelect.addEventListener("change", updateCategories);
        updateCategories();
    });
    </script>
    </head>
    <body class="px-3">
        
    <div class="container">
        <div class="row row-cols-1 row-cols-lg-1">
            <h1>SmartBudget DB</h1>
        </div>
    </div>
    <div class="container-fluid">
        <div class="row g-4 py-5 row-cols-1 row-cols-lg-2">
            <div class="col-lg-6 col-12">
                <div class="w-100">
                    <h2 class="text-center">Currency Movements</h2>
                    <table class="table table-striped table-hover w-100">
                    <thead>
                    <tr class="table-danger">
                        <th scope="col">Currency</th>
                        <th scope="col">Total Income</th>
                        <th scope="col">Total Expenses</th>
                        <th scope="col">Income From Transfers </th>
                        <th scope="col">Expenses From Transfers</th>
                        <th scope="col">Total</th>
                    </tr>
                    </thead>
                    <tbody>
                    {% for currency in resumen.keys() %}
                    <tr>
                        <th scope="row">{{ resumen[currency]["Currency"] }}</th>
                        <td>{{ "{:.2f}".format(resumen[currency]["Total Income"]) }}</td>
                        <td>{{ "{:.2f}".format(resumen[currency]["Total Expenses"]) }}</td>
                        <td>{{ "{:.2f}".format(resumen[currency]["Transfer Income"]) }}</td>
                        <td>{{ "{:.2f}".format(resumen[currency]["Transfer Expenses"]) }} </td>
                        <td>{{ "{:>10.2f}".format(resumen[currency]["Total Income"]+resumen[currency]["Transfer Income"]-resumen[currency]["Total Expenses"]-resumen[currency]["Transfer Expenses"]) }}</td>
                    </tr>
                    {% endfor %}
                    </tbody>
                    </table>
                </div>
            </div>
            <div class="col-lg-6 col-12">
                <div class="w-100">
                    <h2 class="text-center">Account Balances</h2>
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr class="table-info">
                                <th scope="col">Id</th>
                                <th scope="col">Cuenta</th>
                                <th scope="col">Banco</th>
                                <th scope="col">Moneda</th>
                                <th scope="col">Balance</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for b in accounts %}
                            <tr>
                                <th scope="row">{{ b.account.id }}</th>
                                <td>{{ b.account.account_number }}</td>
                                <td>{{ b.account.bank_name }}</td>
                                <td>{{ b.account.currency }}</td>
                                <td>{{ "%.2f"|format(b.balance) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div> 
            </div>
        </div>
    </div>


    <h2>Add Transaction</h2>
    <form method="post" action="/add" class="mb-3">
        <div class="row g-2">
            <div class="col-md-2">
                <input type="datetime-local" name="date_in" class="form-control" required>
            </div>
            <div class="col-md-1">
                <select name="type" class="form-select" required>
                    <option>Income</option>
                    <option>Expense</option>
                </select>
            </div>
            <div class="col-md-3">
                <select name="category" class="form-select" required></select>
            </div>
            <div class="col-md-3">
                <input type="text" name="description"  placeholder="Desc" class="form-control">
            </div>
            <div class="col-md-1">
                <input type="number" step="0.01" name="amount" placeholder="Amount" class="form-control" required>
            </div>
            <div class="col-md-1">
                <input type="number" name="account" placeholder="Account ID" class="form-control" required>
            </div>
            <div class="col-md-1">
                <button class="btn btn-primary w-100">Save</button>
            </div>
        </div>
    </form>
    
    <h2>Add Account</h2>
    <form method="post" action="/add_account" class="mb-3">
        <div class="row g-2">

        <div class="col-md-3">
            <input type="text" name="acc_num" placeholder="Número cuenta" class="form-control" required> 
        </div>
        <div class="col-md-3">
            <input type="text" name="bank" placeholder="Banco" class="form-control" required>
        </div>
        <div class="col-md-3">
            <input type="text" name="acc_type" placeholder="Tipo cuenta" class="form-control" required>
        </div>
        <div class="col-md-2">
            <input type="text" name="currency" placeholder="Moneda"  class="form-control" required>
        </div>
        <div class="col-md-1">
            <button class="btn btn-secondary w-100">Save</button>
        </div>
        </div>
    </form>
    
    <h2>Transfer</h2>
    <form method="post" action="/transfer" class="mb-3">
        <div class="row g-2">

        <div class="col-md-2">
            <input type="datetime-local" name="date_in" class="form-control" required>
        </div>
        <div class="col-md-1">
            <input type="number" name="from_account" placeholder="From Account ID" class="form-control" required>
        </div>
        <div class="col-md-1">
            <input type="number" name="to_account" placeholder="To Account ID" class="form-control" required>
        </div>
        <div class="col-md-2">
            <input type="number" step="0.01" name="amount" placeholder="Amount" class="form-control" required>
        </div>
        <div class="col-md-1">
            <input type="number" step="0.01" name="commission" placeholder="Comisión" class="form-control" required>
        </div>
        <div class="col-md-1">
            <input type="number" step="0.01" name="exchange_rate" placeholder="Tipo de cambio" value="1" class="form-control" required>
        </div>
        <div class="col-md-3">
            <input type="text" name="description" placeholder="Desc" class="form-control">
        </div>
        <div class="col-md-1">
            <button class="btn btn-success w-100">Transfer</button>
        </div>
        </div>
    </form>

    <h2>Transactions</h2>
    <table class="table table-striped-columns table-hover">
    <thead>
    <tr class="table-primary"><th>Date</th><th>Type</th><th>Category</th><th>Description</th><th>Amount</th><th>Account</th></tr>
    </thead>
    <tbody>
    {% for e in entries %}
    <tr><td>{{e.date}}</td><td>{{e.type}}</td><td>{{e.category}}</td><td>{{e.description}}</td><td>{{e.amount}}</td><td>{{e.account_id}}</td></tr>
    {% endfor %}
    </tbody>
    </table>

    </body>
    </html>
    """
    return app
