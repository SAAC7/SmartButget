# src/smartbudget/__main__.py
from .app import create_app
from pathlib import Path

# Ruta a la base de datos
DB_FILE = Path(__file__).parent / "resources" / "SmartBudget.db"

# Crear la app Flask
app = create_app(DB_FILE)

# Inicializar la base de datos (crea tablas si no existen)
with app.app_context():
    app.init_db()   # <-- aquí se ejecuta init_db

# Levantar el servidor Flask (desarrollo)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
