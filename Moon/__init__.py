import os

if not os.path.exists(r"Moon\dlls\PySGL.dll") or not os.path.exists(r"Moon\src\PySGL.cpp"):
    os.system(r'python PySGL\build.py')


DLL_OUTPUT_PATH = r"dll\PySGL.dll"

DLL_FOUND_PATH = r"Moon/dlls/PySGL.dll"