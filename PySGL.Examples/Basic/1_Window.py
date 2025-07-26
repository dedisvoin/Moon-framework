import sys
sys.path.append("./")
from PySGL.python.Window import *

window = Window(style=Window.Style.No, title="test").set_view_info()
events = WindowEvents()
window.set_system_cursor(SystemCursors.Help)


import ctypes
from ctypes import wintypes
import sys

# Константы для DwmSetWindowAttribute
DWMWA_WINDOW_CORNER_PREFERENCE = 33

# Варианты скругления углов (DWM_WINDOW_CORNER_PREFERENCE)
DWMWCP_DEFAULT      = 0  # Системные настройки
DWMWCP_DONOTROUND   = 1  # Без скругления
DWMWCP_ROUND        = 2  # Скругление
DWMWCP_ROUNDSMALL   = 3  # Маленькое скругление

# Получаем HWND окна (например, для PyQt/PySide или tkinter)
# Импортируем необходимые функции из WinAPI
user32 = ctypes.WinDLL("user32")
dwmapi = ctypes.WinDLL("dwmapi")


def find_window_by_title(title: str) -> int:
    """Находит HWND окна по его заголовку."""   
    hwnd = user32.FindWindowW(None, title)
    if not hwnd:
        print(f"Окно с названием '{title}' не найдено!")
        return 0
    return hwnd

def enable_rounded_corners(hwnd: int) -> bool:
    """Включает скруглённые углы для окна."""
    try:
        preference = ctypes.c_int(DWMWCP_ROUND)
        result = dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd),
            DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(preference),
            ctypes.sizeof(preference),
        )
        return result == 0  # S_OK = 0 (успех)
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    

enable_rounded_corners(find_window_by_title("test"))


while window.update(events):
    window.clear()
    window.view_info()
    window.display()
