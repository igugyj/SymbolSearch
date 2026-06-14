from PySide6.QtCore import QAbstractNativeEventFilter
from ctypes import wintypes, windll, Structure
from ctypes.wintypes import DWORD, HANDLE, UINT

WM_HOTKEY = 0x0312

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008


class MSG(Structure):
    _fields_ = [
        ("hwnd", HANDLE),
        ("message", UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", DWORD),
        ("pt", wintypes.POINT),
    ]


_VK_MAP = {
    "Esc": 0x1B,
    "Escape": 0x1B,
    "Tab": 0x09,
    "Backtab": 0x09,
    "Backspace": 0x08,
    "Return": 0x0D,
    "Enter": 0x0D,
    "Space": 0x20,
    "Delete": 0x2E,
    "Del": 0x2E,
    "Insert": 0x2D,
    "Ins": 0x2D,
    "Home": 0x24,
    "End": 0x23,
    "PageUp": 0x21,
    "PgUp": 0x21,
    "PageDown": 0x22,
    "PgDown": 0x22,
    "Up": 0x26,
    "Down": 0x28,
    "Left": 0x25,
    "Right": 0x27,
    "Pause": 0x13,
    "Print": 0x2A,
    "CapsLock": 0x14,
    "NumLock": 0x90,
    "ScrollLock": 0x91,
}

_MOD_MAP = {
    "Ctrl": MOD_CONTROL,
    "Alt": MOD_ALT,
    "Shift": MOD_SHIFT,
    "Win": MOD_WIN,
}


def _parse_hotkey_string(hotkey_str: str):
    parts = [p.strip() for p in hotkey_str.split("+")]
    mods = 0
    key_part = parts[-1]
    for p in parts[:-1]:
        m = _MOD_MAP.get(p)
        if m is not None:
            mods |= m

    if len(key_part) == 1 and key_part.isalpha():
        vk = ord(key_part.upper())
    elif len(key_part) == 1 and key_part.isdigit():
        vk = ord(key_part)
    elif len(key_part) >= 2 and key_part[0] == "F" and key_part[1:].isdigit():
        fn = int(key_part[1:])
        vk = 0x6F + fn if 1 <= fn <= 24 else 0
    else:
        vk = _VK_MAP.get(key_part, 0)

    return mods, vk


class HotkeyManager(QAbstractNativeEventFilter):
    def __init__(self, callback, parent=None):
        super().__init__()
        self._callback = callback
        self._hotkey_id = 1
        self._current_str = ""
        self._mods = 0
        self._vk = 0

    def register(self, hotkey_str: str):
        self.unregister()
        self._current_str = hotkey_str
        self._mods, self._vk = _parse_hotkey_string(hotkey_str)
        if self._mods == 0 and self._vk == 0:
            return False
        ok = windll.user32.RegisterHotKey(None, self._hotkey_id, self._mods, self._vk)
        return bool(ok)

    def unregister(self):
        if self._current_str:
            windll.user32.UnregisterHotKey(None, self._hotkey_id)
            self._current_str = ""

    def nativeEventFilter(self, eventType, message):
        if eventType == b"windows_generic_MSG":
            msg = MSG.from_address(message.__int__())
            if msg.message == WM_HOTKEY and msg.wParam == self._hotkey_id:
                self._callback()
                return True, 0
        return False, 0
