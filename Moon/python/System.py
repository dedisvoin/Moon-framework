from Moon.python.utils import find_library
import platform
from colorama import Fore
import ctypes
import psutil
import os
import sys

# Базовая директория
def get_base_dir():
    return sys.path[0]

def get_resource_path(base_dir: str, filename: str, foldername: str):
    """Создает надежный путь к файлу в папке 'data'"""
    # os.path.join автоматически выбирает правильный разделитель (\ или /)
    print(base_dir)
    path = os.path.join(base_dir, foldername, filename)
    print(path)
    return path

# Загружаем DLL библиотеку
try:
    LIB_MOON = ctypes.CDLL(find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")

LIB_MOON._Glsl_GetVersion.argtypes = []
LIB_MOON._Glsl_GetVersion.restype = ctypes.c_char_p
LIB_MOON._Glsl_GetVendor.argtypes = []
LIB_MOON._Glsl_GetVendor.restype = ctypes.c_char_p
LIB_MOON._Glsl_GetRenderer.argtypes = []
LIB_MOON._Glsl_GetRenderer.restype = ctypes.c_char_p

def get_gpu_version() -> str | None:
    core_message = LIB_MOON._Glsl_GetVersion().decode()
    if core_message == 'noinit':
        print(f'[ {Fore.CYAN}MoonCore{Fore.RESET} ] [ {Fore.YELLOW}warning{Fore.RESET} ] The window context is not initialized, so it is not possible to get the version')
        return None
    return core_message

def get_gpu_vendor() -> str | None:
    core_message = LIB_MOON._Glsl_GetVendor().decode()
    if core_message == 'noinit':
        print(f'[ {Fore.CYAN}MoonCore{Fore.RESET} ] [ {Fore.YELLOW}warning{Fore.RESET} ] The window context is not initialized, so it is not possible to get the vendor')
        return None
    return core_message

def get_gpu_renderer() -> str | None:
    core_message = LIB_MOON._Glsl_GetRenderer().decode()
    if core_message == 'noinit':
        print(f'[ {Fore.CYAN}MoonCore{Fore.RESET} ] [ {Fore.YELLOW}warning{Fore.RESET} ] The window context is not initialized, so it is not possible to get the renderer')
        return None
    return core_message

def get_cpu() -> str:
    return platform.processor()

def get_cpu_count(logical: bool = False) -> int:
    return psutil.cpu_count(logical)

def get_cpu_freq():
    return psutil.cpu_freq().current

def get_cpu_freq_max():
    return psutil.cpu_freq().max

def get_cpu_freq_min():
    return psutil.cpu_freq().min

def get_cpu_percent(interval: float = 0.1):
    return psutil.cpu_percent(interval)

def get_cpu_cores_percent(interval: float = 0.1):
    return psutil.cpu_percent(interval, percpu=True)

def get_architecture() -> tuple[str, str]:
    return platform.architecture()
