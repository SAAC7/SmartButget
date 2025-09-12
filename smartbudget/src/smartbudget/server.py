from flask import Flask, render_template,render_template_string, request, redirect
from datetime import datetime
from pathlib import Path
from .services import SmartBudgetServices
from .data_access import CATEGORIES_EXPENSE,CATEGORIES_INCOME

def create_app(db_path:Path):

    app = Flask(
    __name__,
    static_folder=str(Path(__file__).parent / "resources" / "static"),
    template_folder= str(Path(__file__).parent / "resources" / "templates"),
    static_url_path="/static"  # <-- esto asegura que Flask sirva /static/
    )
    backend = SmartBudgetServices(db_path)
    # --------------------------
    # Rutas Flask
    # --------------------------
    @app.route("/", methods=["GET"])
    def index():
        monthyear = request.args.get("monthyear")

        if monthyear:
            # viene en formato "YYYY-MM", lo partimos
            selected_year, selected_month = map(int, monthyear.split("-"))
        else:
            # por defecto, mes actual
            now = datetime.now()
            selected_year, selected_month = now.year, now.month
            monthyear = f"{selected_year:04d}-{selected_month:02d}"

        # Genera el resumen y balances
        resumen, rows = backend.get_summary(selected_year, selected_month)
        # resumen, rows = generate_summary(datetime.now().year, datetime.now().month)
        balances,total_balances = backend.get_balances()

        # print(resumen)
        return render_template("menu.html",
                                    entries=rows,
                                    resumen=resumen,
                                    accounts=balances.values(),
                                    accounts_total=total_balances,
                                    CATEGORIES_INCOME=CATEGORIES_INCOME,
                                    CATEGORIES_EXPENSE=CATEGORIES_EXPENSE,
                                    monthyear=monthyear)

    @app.route("/add", methods=["POST"])
    def add():
        tipo = request.form.get("type")
        categoria = request.form.get("category")
        desc = request.form.get("description")
        dt_str = request.form.get("date_in")
        dt_obj = datetime.fromisoformat(dt_str)
        amount = float(request.form.get("amount"))
        account_id = int(request.form.get("account"))

        backend.add_transaction(dt_obj.isoformat(), tipo, categoria, desc, amount, account_id)

        return redirect("/")

    @app.route("/add_account", methods=["POST"])
    def add_account():
        acc_num = request.form.get("acc_num")
        bank = request.form.get("bank")
        acc_type = request.form.get("acc_type")
        currency = request.form.get("currency")

        backend.add_account(acc_num, bank, acc_type, currency)

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

        backend.add_transfer(from_acc, to_acc, amount, commission, rate, dt_obj.isoformat(), desc)

        return redirect("/")

    # --------------------------
    # TEMPLATE reducido
    # --------------------------
    # TEMPLATE = """

    # """
    return app
