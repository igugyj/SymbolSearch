from PySide6.QtWidgets import (
    QListView, QStyledItemDelegate, QStyle, QApplication,
)
from PySide6.QtCore import Qt, QModelIndex, QAbstractListModel, QRect
from PySide6.QtGui import QPainter, QFont, QColor, QPen


class SymbolModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data: list = []

    def set_symbols(self, symbols: list):
        self.beginResetModel()
        self._data = symbols[:]
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data):
            return None
        entry = self._data[index.row()]
        if role == Qt.UserRole:
            return entry.char
        if role == Qt.UserRole + 1:
            return "  ".join(entry.keywords[:6])
        return None


class SymbolDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._sym_font = QFont()
        self._sym_font.setPointSize(18)
        self._kw_font = QFont()
        self._kw_font.setPointSize(10)

    def paint(self, painter: QPainter, option, index: QModelIndex):
        char = index.data(Qt.UserRole)
        kw_text = index.data(Qt.UserRole + 1)
        if char is None:
            return

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        r = option.rect

        if option.state & QStyle.State_Selected:
            painter.fillRect(r, QColor("#e3f2fd"))
        elif option.state & QStyle.State_MouseOver:
            painter.fillRect(r, QColor("#f0f7ff"))

        painter.setPen(QPen(QColor("#f0f0f0"), 1))
        painter.drawLine(r.bottomLeft().x(), r.bottomLeft().y(),
                         r.bottomRight().x(), r.bottomRight().y())

        sym_rect = QRect(r.left() + 12, r.top(), 48, r.height())
        painter.setFont(self._sym_font)
        painter.setPen(QColor("#333"))
        painter.drawText(sym_rect, Qt.AlignCenter, char)

        kw_rect = QRect(r.left() + 72, r.top(), r.width() - 84, r.height())
        painter.setFont(self._kw_font)
        painter.setPen(QColor("#999"))
        painter.drawText(kw_rect, Qt.AlignLeft | Qt.AlignVCenter, kw_text)

        painter.restore()

    def sizeHint(self, option, index: QModelIndex):
        from PySide6.QtCore import QSize
        return QSize(0, 48)


class SymbolList(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = SymbolModel(self)
        self._delegate = SymbolDelegate(self)
        self.setModel(self._model)
        self.setItemDelegate(self._delegate)
        self.setMouseTracking(True)
        self.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self.doubleClicked.connect(self._copy_symbol)
        self._toast_cb = None

    def set_toast_callback(self, cb):
        self._toast_cb = cb

    def set_symbols(self, symbols: list):
        self._model.set_symbols(symbols)

    def _copy_symbol(self, index: QModelIndex):
        char = self._model.data(index, Qt.UserRole)
        if char:
            QApplication.clipboard().setText(char)
            if self._toast_cb:
                self._toast_cb(char)
