import os
from flask import Flask, render_template,render_template_string, request, redirect, session, url_for
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
    app.secret_key = os.urandom(24)
    backend = SmartBudgetServices(db_path)
    # --------------------------
    # Rutas Flask
    # --------------------------
    @app.route("/", methods=["GET"])
    def index():
        version=backend.get_version()
        if version == 1:
            return redirect("/setup_user")
              
        user = session.get("user")
        if not user:
            usuario = "Invitado"
        elif user.get("name"):
            usuario = " ".join([user.get("name"), user.get("last_name") or ""])
        else:
            usuario = user.get("username")

        
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
        resumen, rows = backend.get_summary(user["id"],selected_year, selected_month)
        # resumen, rows = generate_summary(datetime.now().year, datetime.now().month)
        balances,total_balances = backend.get_balances(user["id"])

        # print(resumen)
        return render_template("menu.html",
                                    usuario = usuario,  
                                    entries=rows,
                                    resumen=resumen,
                                    accounts=balances.values(),
                                    accounts_total=total_balances,
                                    CATEGORIES_INCOME=CATEGORIES_INCOME,
                                    CATEGORIES_EXPENSE=CATEGORIES_EXPENSE,
                                    monthyear=monthyear)

    @app.route("/add", methods=["POST"])
    def add():
        user_id = int(session.get("user")["id"])
        tipo = request.form.get("type")
        categoria = request.form.get("category")
        desc = request.form.get("description")
        dt_str = request.form.get("date_in")
        dt_obj = datetime.fromisoformat(dt_str)
        amount = float(request.form.get("amount"))
        account_id = int(request.form.get("account"))

        backend.add_transaction(user_id,dt_obj.isoformat(), tipo, categoria, desc, amount, account_id)

        return redirect("/")

    @app.route("/add_account", methods=["POST"])
    def add_account():
        user_id = int(session.get("user")["id"])
        acc_num = request.form.get("acc_num")
        bank = request.form.get("bank")
        acc_type = request.form.get("acc_type")
        currency = request.form.get("currency")

        backend.add_account(user_id,acc_num, bank, acc_type, currency,user_id)

        return redirect("/")

    @app.route("/transfer", methods=["POST"])
    def transfer():
        user_id = int(session.get("user")["id"])
        from_acc = int(request.form.get("from_account"))
        to_acc = int(request.form.get("to_account"))
        amount = float(request.form.get("amount"))
        commission = float(request.form.get("commission") or 0)
        rate = float(request.form.get("exchange_rate") or 1)
        desc = request.form.get("description")
        dt_obj = datetime.fromisoformat(request.form.get("date_in"))

        backend.add_transfer(user_id,from_acc, to_acc, amount, commission, rate, dt_obj.isoformat(), desc)

        return redirect("/")
    
    @app.route("/setup_user", methods=["GET", "POST"])
    def setup_user():
        if request.method == "POST":
            
            username = request.form.get("username")
            password = request.form.get("password")
            name = request.form.get("name")
            last_name = request.form.get("last_name")

            backend.add_user(name,last_name,username,password)
            user=backend.get_user(username,password)
            version = backend.get_version()
            if version == 1:
                user_id=int(user[0]['id'])
                # print(user_id)
                backend.migrate(user_id)
            session["user"] = user[0]
            return redirect("/")
        return render_template("setup_user.html")  # plantilla con form usuario/contraseña


    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = backend.get_user(username, password)
            print(user)
            
            if user and len(user) > 0:
                session["user"] = user[0]
                return redirect("/")
            else:
                return render_template("login.html", error="User or Password Invalid")
        return render_template("login.html")    
    
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")

    @app.before_request
    def check_version_and_auth():
        version = backend.get_version()
        if version == 1 and request.endpoint != "setup_user":
            return redirect(url_for("setup_user"))
        if version >= 2:
            if not session.get("user") and request.endpoint not in ("login", "setup_user"):
                return redirect(url_for("login"))


    return app
