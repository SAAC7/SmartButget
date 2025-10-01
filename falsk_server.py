from smartbudget.src.smartbudget import server

# app = Flask(__name__)
# DB_FILE = "/home/absar/SmartBudget.db"
DB_FILE = "/run/media/absar/HOME/absar/SmartBudget.db"
# DB_FILE = "/run/media/arch-ab/HOME/absar/SmartBudget.db"





def main():
    app = server.create_app(DB_FILE)
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()