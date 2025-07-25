
from ctypes import windll

# MessageBoxA (для ANSI) или MessageBoxW (для Unicode)
windll.user32.MessageBoxW(0, "Привет, Windows API!", "Окно", 1)