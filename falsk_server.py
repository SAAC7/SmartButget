from smartbudget.src.smartbudget import server

# app = Flask(__name__)
DB_FILE = "/home/absar/SmartBudget.db"


def main():
    app = server.create_app(DB_FILE)
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()