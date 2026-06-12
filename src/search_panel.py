from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit,
    QPushButton, QScrollArea,
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QIcon

from src.resources import SEARCH_ICON_SVG, svg_to_icon


class SearchPanel(QWidget):
    text_changed = Signal(str)
    category_changed = Signal(str)

    def __init__(self, categories: list[str], parent=None):
        super().__init__(parent)
        self._categories = categories
        self._selected_category = ""
        self._debounce = QTimer()
        self._debounce.setSingleShot(True)
        self._debounce.timeout.connect(self._emit_search)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索符号...")
        icon = svg_to_icon(SEARCH_ICON_SVG, 20)
        self.search_input.addAction(
            icon, QLineEdit.ActionPosition.LeadingPosition
        )
        self.search_input.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.search_input)

        self._build_category_bar(layout)

    def _build_category_bar(self, parent_layout):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedHeight(52)

        bar = QWidget()
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.setSpacing(4)

        self._btns: list[QPushButton] = []
        all_btn = QPushButton("全部")
        all_btn.setCheckable(True)
        all_btn.setChecked(True)
        all_btn.clicked.connect(lambda: self._on_category(""))
        all_btn.setCursor(Qt.PointingHandCursor)
        bar_layout.addWidget(all_btn)
        self._btns.append(all_btn)

        for cat in self._categories:
            btn = QPushButton(cat)
            btn.setCheckable(True)
            btn.clicked.connect(lambda _=False, c=cat: self._on_category(c))
            btn.setCursor(Qt.PointingHandCursor)
            bar_layout.addWidget(btn)
            self._btns.append(btn)

        bar_layout.addStretch()
        scroll.setWidget(bar)
        parent_layout.addWidget(scroll)

    def _on_category(self, cat: str):
        self._selected_category = cat
        for b in self._btns:
            b.setChecked(False)
        if cat == "":
            self._btns[0].setChecked(True)
        else:
            idx = self._categories.index(cat) + 1
            self._btns[idx].setChecked(True)
        self.category_changed.emit(cat)

    def _on_text_changed(self, _text: str):
        self._debounce.start(200)

    def _emit_search(self):
        self.text_changed.emit(self.search_input.text())
