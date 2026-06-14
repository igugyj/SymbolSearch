from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication

from src.lock import SingleInstance
from src.config import load_config
from src.hotkey import HotkeyManager
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

        config = load_config()

        data_path = Path(__file__).resolve().parent.parent / "data" / "symbols.json"
        self._data = load_data(str(data_path))

        self.main_window = MainWindow(self._data)
        self.tray = TrayManager(self.main_window, config)
        self.tray.set_app(self)

        self._hotkey = HotkeyManager(self.main_window.toggle_visibility)
        self._apply_hotkey(config.get("hotkey", "Ctrl+Alt+S"))

        self.qt_app.installNativeEventFilter(self._hotkey)

    def rebuild_hotkey(self, hotkey_str: str):
        self._apply_hotkey(hotkey_str)

    def _apply_hotkey(self, hotkey_str: str):
        self._hotkey.register(hotkey_str)

    def run(self):
        return self.qt_app.exec()
