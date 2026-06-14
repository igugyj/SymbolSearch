from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QKeySequenceEdit, QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence

from src.hotkey import _parse_hotkey_string


class HotkeyDialog(QDialog):
    def __init__(self, current_hotkey: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置全局快捷键")
        self.setFixedSize(380, 200)
        self._result_hotkey = current_hotkey

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        layout.addWidget(QLabel("当前快捷键:"))

        self._key_edit = QKeySequenceEdit()
        self._key_edit.setClearButtonEnabled(True)
        self._key_edit.setKeySequence(QKeySequence(current_hotkey))
        layout.addWidget(self._key_edit)

        hint = QLabel("点击输入框，按下新的快捷键组合")
        hint.setStyleSheet("color: #999; font-size: 11px;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        reset_btn = QPushButton("重置")
        reset_btn.clicked.connect(self._reset)
        btn_layout.addWidget(reset_btn)

        btn_layout.addStretch()

        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("保存")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self._save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def get_hotkey(self) -> str:
        return self._result_hotkey

    def _reset(self):
        self._key_edit.setKeySequence(QKeySequence("Ctrl+Alt+S"))

    def _save(self):
        seq = self._key_edit.keySequence()
        hotkey_str = seq.toString()

        mods, vk = _parse_hotkey_string(hotkey_str)
        if mods == 0 and vk == 0:
            QMessageBox.warning(self, "无效快捷键", "请输入有效的快捷键组合（至少包含一个修饰键）")
            return

        self._result_hotkey = hotkey_str
        self.accept()
