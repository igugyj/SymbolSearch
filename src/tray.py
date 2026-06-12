from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QAction

from src.resources import APP_ICON_SVG, svg_to_icon


class TrayManager:
    def __init__(self, main_window):
        self._window = main_window
        self._menu = QMenu()
        self._quit_act = QAction("退出")
        self._quit_act.triggered.connect(self._quit)
        self._menu.addAction(self._quit_act)

        icon = svg_to_icon(APP_ICON_SVG, 32)
        self.tray = QSystemTrayIcon(icon)
        self.tray.setToolTip("SymbolSearch")
        self.tray.setContextMenu(self._menu)
        self.tray.activated.connect(self._on_activated)
        self.tray.show()

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self._window.isVisible():
                self._window.hide()
            else:
                self._window.show()
                self._window.raise_()
                self._window.activateWindow()

    def _quit(self):
        QApplication.quit()
