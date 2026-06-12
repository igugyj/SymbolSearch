from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStatusBar
from PySide6.QtCore import Qt

from src.search_panel import SearchPanel
from src.symbol_list import SymbolList
from src.symbol_data import filter_symbols, get_categories
from src.resources import APP_ICON_SVG, svg_to_icon


class MainWindow(QMainWindow):
    def __init__(self, symbol_data):
        super().__init__()
        self._data = symbol_data

        self.setWindowTitle("SymbolSearch")
        self.setWindowIcon(svg_to_icon(APP_ICON_SVG, 32))
        self.setMinimumSize(480, 380)
        self.resize(620, 520)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 4)
        layout.setSpacing(4)

        categories = get_categories(self._data)
        self.search_panel = SearchPanel(categories)
        layout.addWidget(self.search_panel)

        self.symbol_list = SymbolList()
        self.symbol_list.set_toast_callback(self._show_toast)
        layout.addWidget(self.symbol_list, 1)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.search_panel.text_changed.connect(self._apply_filter)
        self.search_panel.category_changed.connect(self._apply_filter)

        self._apply_filter()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def _apply_filter(self, _=None):
        text = self.search_panel.search_input.text()
        cat = self.search_panel._selected_category
        filtered = filter_symbols(self._data, text, cat if cat else None)
        self.symbol_list.set_symbols(filtered)
        self.status_bar.showMessage(f"共 {len(filtered)} 个符号")

    def _show_toast(self, char: str):
        self.status_bar.showMessage(f"已复制: {char}", 3000)
