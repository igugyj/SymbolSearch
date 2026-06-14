from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QAction

from src.resources import APP_ICON_SVG, svg_to_icon
from src.hotkey_dialog import HotkeyDialog
from src.config import save_config


class TrayManager:
    def __init__(self, main_window, config):
        self._window = main_window
        self._config = config
        self._app = None
        self._menu = QMenu()

        self._settings_act = QAction("设置快捷键...")
        self._settings_act.triggered.connect(self._open_settings)
        self._menu.addAction(self._settings_act)

        self._menu.addSeparator()

        self._quit_act = QAction("退出")
        self._quit_act.triggered.connect(self._quit)
        self._menu.addAction(self._quit_act)

        icon = svg_to_icon(APP_ICON_SVG, 32)
        self.tray = QSystemTrayIcon(icon)
        self.tray.setToolTip("SymbolSearch")
        self.tray.setContextMenu(self._menu)
        self.tray.activated.connect(self._on_activated)
        self.tray.show()

    def set_app(self, app):
        self._app = app

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self._window.isVisible():
                self._window.hide()
            else:
                self._window.show()
                self._window.raise_()
                self._window.activateWindow()

    def _open_settings(self):
        current = self._config.get("hotkey", "Ctrl+Alt+S")
        dlg = HotkeyDialog(current, self._window)
        if dlg.exec() == HotkeyDialog.Accepted:
            new_hotkey = dlg.get_hotkey()
            self._config["hotkey"] = new_hotkey
            save_config(self._config)
            if self._app:
                self._app.rebuild_hotkey(new_hotkey)

    def _quit(self):
        QApplication.quit()
