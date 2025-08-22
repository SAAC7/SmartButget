# src/smartbudget/__main__.py
from .app import create_app
from pathlib import Path
# Levantar el servidor Flask (desarrollo)
from .app import main

if __name__ == "__main__":
    main().main_loop()

