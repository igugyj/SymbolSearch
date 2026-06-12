from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer


def svg_to_icon(svg_str: str, size: int = 32) -> QIcon:
    renderer = QSvgRenderer(QByteArray(svg_str.encode()))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


APP_NAME = "SymbolSearch"

SEARCH_ICON_SVG = """<svg viewBox="0 0 24 24" width="20" height="20">
<circle cx="10" cy="10" r="6" fill="none" stroke="#888" stroke-width="2"/>
<line x1="14.5" y1="14.5" x2="21" y2="21" stroke="#888" stroke-width="2" stroke-linecap="round"/>
</svg>"""

CLOSE_ICON_SVG = """<svg viewBox="0 0 24 24" width="16" height="16">
<line x1="6" y1="6" x2="18" y2="18" stroke="#888" stroke-width="2" stroke-linecap="round"/>
<line x1="18" y1="6" x2="6" y2="18" stroke="#888" stroke-width="2" stroke-linecap="round"/>
</svg>"""

APP_ICON_SVG = """<svg viewBox="0 0 32 32" width="32" height="32">
<rect x="2" y="2" width="28" height="28" rx="6" fill="#4A90D9"/>
<text x="16" y="24" font-size="22" fill="white" text-anchor="middle" font-family="serif" font-weight="bold" font-style="italic">&#945;</text>
</svg>"""

QSS_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}
QLineEdit {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    background: white;
}
QLineEdit:focus {
    border-color: #4A90D9;
}
QPushButton {
    padding: 4px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
    font-size: 12px;
    min-height: 24px;
}
QPushButton:hover {
    background: #e8f0fe;
    border-color: #4A90D9;
}
QPushButton:checked {
    background: #4A90D9;
    color: white;
    border-color: #4A90D9;
}
QListView {
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    background: white;
    outline: none;
}
QStatusBar {
    font-size: 12px;
    color: #666;
}
QScrollArea {
    border: none;
    background: transparent;
}
"""
