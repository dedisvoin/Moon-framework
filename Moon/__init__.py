import os
import sys

if not os.path.exists(r"Moon\dlls\PySGL.dll") or not os.path.exists(r"Moon\src\PySGL.cpp"):
    os.system(r'python PySGL\build.py')


if sys.platform == 'win32':
    DLL_OUTPUT_PATH = r"Moon\libs\Moon.dll"
    DLL_FOUND_PATH = r"Moon\libs\Moon.dll"
    DLL_LOCAL_FOUND_PATH = r"./libs/Moon.dll"
    DLL_MODULE_FOUND_PATH = r"../libs/Moon.dll"
elif sys.platform == 'linux':
    DLL_OUTPUT_PATH = r"dlls/Moon.so"
    DLL_FOUND_PATH = r"Moon/dlls/Moon.so"
    DLL_LOCAL_FOUND_PATH = r"./dlls/Moon.so"
    DLL_MODULE_FOUND_PATH = r"../dlls/Moon.so"

if os.name != 'nt':  # Only for Windows
    from colorama import Fore
    print(f"[ {Fore.RED}Error{Fore.RESET} ] Moon framework is not support ({os.name}) system.")
