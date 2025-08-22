# src/smartbudget/app.py
import threading
from pathlib import Path
import socket
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from .server import create_app

DEFAULT_PORT = 5000


def get_device_ip():
    """Obtiene la IP local para mostrar acceso desde otra PC en la red."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class SmartBudget(toga.App):
    def startup(self):
        self.db_path = None  # no DB al iniciar
        self.port = DEFAULT_PORT
        self.host = "0.0.0.0"

        # Ventana principal
        self.main_window = toga.MainWindow(title=self.formal_name)

        self.status = toga.Label(
            "No DB cargada",
            style=Pack(padding_bottom=8)
        )

        self.webview = toga.WebView()
        self.webview.style.update(flex=1) 

        box = toga.Box(
            children=[self.status, self.webview],
            style=Pack(direction=COLUMN,flex=1)
        )

        self.main_window.content = box
        self.main_window.toolbar.add(
            toga.Command(self.cmd_open_db, text="Open DB"),
            toga.Command(self.cmd_new_db, text="Create DB"),
            toga.Command(self.cmd_reload, text="Reload")
        )

        self.main_window.show()

    def _start_flask(self, db_path: Path):
        """Arranca el servidor Flask en segundo plano"""
        self.app = create_app(db_path)

        def run():
            self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)

        t = threading.Thread(target=run, daemon=True)
        t.start()

    async def cmd_open_db(self, widget):
        db_file = await self.main_window.open_file_dialog(
            title="Selecciona una base .db",
            multiple_select=False,
            file_types=["db"]
        )
        if db_file:
            self.db_path = Path(db_file)
            self._start_flask(self.db_path)
            self.status.text = f"DB: {self.db_path.name}  |  Servidor: http://{get_device_ip()}:{self.port}"
            self.webview.url = f"http://127.0.0.1:{self.port}/"

    async def cmd_new_db(self, widget):
        save_to = await self.main_window.save_file_dialog(
            title="Crear base de datos",
            suggested_filename="SmartBudget.db",
            file_types=["db"]
        )
        if save_to:
            self.db_path = Path(save_to)
            # Flask se arranca con la DB recién creada
            self._start_flask(self.db_path)
            self.status.text = f"DB: {self.db_path.name}  |  Servidor: http://{get_device_ip()}:{self.port}"
            self.webview.url = f"http://127.0.0.1:{self.port}/"

    async def cmd_reload(self, widget):
        """Recargar la web view si Flask ya está corriendo"""
        if self.db_path:
            self.webview.url = f"http://127.0.0.1:{self.port}/"

def main():
    return SmartBudget("SmartBudget", "com.tunombre.smartbudget")
