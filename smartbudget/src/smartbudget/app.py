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
    # Para mostrar la IP local si quieres entrar desde la PC
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
        # Carpeta de datos recomendada por Toga (cross-platform)
        # Android: ruta propia de la app; existe y es escribible.
        # https://toga.readthedocs.io/en/stable/reference/api/resources/app_paths.html
        data_dir = self.paths.data
        data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = data_dir / "SmartBudget.db"

        # Arrancar servidor Flask (hilo de fondo)
        self.port = DEFAULT_PORT
        self.host = "0.0.0.0"
        self._start_flask(self.db_path, self.host, self.port)

        # UI principal: WebView + barra con acciones
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.webview = toga.WebView(url=f"http://127.0.0.1:{self.port}/")
        self.status = toga.Label(
            f"DB: {self.db_path.name}  |  Servidor: http://{get_device_ip()}:{self.port}",
            style=Pack(padding_bottom=8)
        )

        box = toga.Box(
            children=[self.status, self.webview],
            style=Pack(direction=COLUMN)
        )
        self.main_window.content = box
        self.main_window.toolbar.add(
            toga.Command(self.cmd_open_db, text="Abrir DB"),
            toga.Command(self.cmd_new_db, text="Crear DB"),
            toga.Command(self.cmd_export_db, text="Exportar DB"),
            toga.Command(self.cmd_reload, text="Recargar")
        )
        self.main_window.show()

    def _start_flask(self, db_path: Path, host: str, port: int):
        app = create_app(db_path)

        def run():
            # Sin reloader para que no duplique hilos en Android
            app.run(host=host, port=port, debug=False, use_reloader=False)

        t = threading.Thread(target=run, daemon=True)
        t.start()

    async def cmd_open_db(self, widget):
        db_file = await self.main_window.open_file_dialog(
            title="Selecciona una base .db",
            multiselect=False,
            file_types=["db"]
        )
        if db_file:
            self.db_path = Path(db_file)
            self._start_flask(self.db_path, self.host, self.port)
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
            # El init_db se ejecuta en la primera carga del index
            self._start_flask(self.db_path, self.host, self.port)
            self.status.text = f"DB: {self.db_path.name}  |  Servidor: http://{get_device_ip()}:{self.port}"
            self.webview.url = f"http://127.0.0.1:{self.port}/"

    async def cmd_export_db(self, widget):
        if not self.db_path.exists():
            await self.main_window.info_dialog("Exportar DB", "No hay DB para exportar.")
            return
        save_to = await self.main_window.save_file_dialog(
            title="Exportar copia de DB",
            suggested_filename=self.db_path.name,
            file_types=["db"]
        )
        if save_to:
            Path(save_to).write_bytes(self.db_path.read_bytes())
            await self.main_window.info_dialog("Exportar DB", "Exportación completada.")

    async def cmd_reload(self, widget):
        self.webview.url = f"http://127.0.0.1:{self.port}/"


def main():
    return SmartBudget("SmartBudget", "com.tunombre.smartbudget")
