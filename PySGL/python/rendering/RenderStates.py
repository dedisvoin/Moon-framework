import ctypes
from .Shaders import *
import os

# Загрузка нативной библиотеки
class LibraryLoadError(Exception):
    """Ошибка загрузки нативной библиотеки"""
    pass


def _find_library() -> str:
    """
    #### Поиск пути к нативной библиотеке BUILD.dll
    
    ---
    
    :Returns:
        str: Абсолютный путь к библиотеке
        
    ---
    
    :Raises:
        LibraryLoadError: Если библиотека не найдена
    """
    try:
        # Поиск в папке dlls относительно корня пакета
        
        lib_path = r"PySGL/dlls/PySGL.dll"
        if not os.path.exists(lib_path):
            print("PySGL.RenderStates: Library not found at", lib_path)
            lib_path = "./dlls/PySGL.dll"
            if not os.path.exists(lib_path):
                print("Library not found at", lib_path)
                raise FileNotFoundError(f"Library not found at {lib_path}")
        
        return lib_path
    except Exception as e:
        raise LibraryLoadError(f"Library search failed: {e}")

# Загружаем DLL библиотеку
try:
    LIB_PYSGL = ctypes.CDLL(_find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")


LIB_PYSGL._RenderStates_Create.argtypes = None
LIB_PYSGL._RenderStates_Create.restype = ctypes.c_void_p
LIB_PYSGL._RenderStates_Delete.argtypes = [ctypes.c_void_p]
LIB_PYSGL._RenderStates_Delete.restype = None
LIB_PYSGL._RenderStates_SetShader.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL._RenderStates_SetShader.restype = None

RenderStatesPtr = ctypes.c_void_p

class RenderStates:
    def __init__(self):
        self._ptr = LIB_PYSGL._RenderStates_Create()
        self.__shader: Shader | None = None

    def get_ptr(self) -> RenderStatesPtr:
        return self._ptr
    
    def set_shader(self, shader: Shader) -> "RenderStates":
        self.__shader = shader
        LIB_PYSGL._RenderStates_SetShader(self._ptr, self.__shader.get_ptr())
        return self

    def get_shader(self) -> Shader:
        return self.__shader

    
