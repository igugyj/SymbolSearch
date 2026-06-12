from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication

from src.lock import SingleInstance
from src.main_window import MainWindow
from src.tray import TrayManager
from src.symbol_data import load_data
from src.resources import APP_NAME, QSS_STYLE, APP_ICON_SVG, svg_to_icon


def _set_windows_taskbar_icon():
    try:
        import ctypes
        app_id = f"SymbolSearch.{APP_NAME}"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass


class App:
    def __init__(self, argv=None):
        self._lock = SingleInstance(APP_NAME)
        _set_windows_taskbar_icon()
        self.qt_app = QApplication(argv or sys.argv)
        self.qt_app.setApplicationName(APP_NAME)
        self.qt_app.setWindowIcon(svg_to_icon(APP_ICON_SVG, 32))
        self.qt_app.setStyleSheet(QSS_STYLE)

        data_path = Path(__file__).resolve().parent.parent / "data" / "symbols.json"
        self._data = load_data(str(data_path))

        self.main_window = MainWindow(self._data)
        self.tray = TrayManager(self.main_window)

    def run(self):
        self.main_window.show()
        return self.qt_app.exec()
