import os

if not os.path.exists(r"PySGL\dlls\PySGL.dll") or not os.path.exists(r"PySGL\src\PySGL.cpp"):
    os.system(r'python PySGL\build.py')


DLL_OUTPUT_PATH = r"dll\PySGL.dll"