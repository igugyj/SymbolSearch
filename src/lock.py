import os
import sys
import atexit
import tempfile


def _is_pid_running(pid: int) -> bool:
    try:
        import ctypes
        handle = ctypes.windll.kernel32.OpenProcess(0x100000, False, pid)
        if handle:
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        return False
    except Exception:
        return False


class SingleInstance:
    def __init__(self, name: str):
        username = os.environ.get("USERNAME", "unknown")
        lock_name = f"{username}_{name}.lock"
        self._path = os.path.join(tempfile.gettempdir(), lock_name)
        self._fd = None

        if os.path.exists(self._path):
            try:
                with open(self._path) as f:
                    pid = int(f.read().strip())
                if pid == os.getpid() or _is_pid_running(pid):
                    print(f"SymbolSearch is already running (PID: {pid})")
                    sys.exit(1)
            except (ValueError, OSError):
                pass
            os.remove(self._path)

        try:
            self._fd = os.open(
                self._path,
                os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                0o644,
            )
            os.write(self._fd, str(os.getpid()).encode())
            os.close(self._fd)
        except OSError:
            print("SymbolSearch is already running")
            sys.exit(1)

        atexit.register(self._cleanup)

    def _cleanup(self):
        if self._path and os.path.exists(self._path):
            try:
                os.remove(self._path)
            except OSError:
                pass
