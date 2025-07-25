import ctypes
from enum import Enum

import os
from ..Vectors import Vector2f, Vector2i
from ..Colors import Color
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
            print("PySGL.Shaders: Library not found at", lib_path)
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



LIB_PYSGL._Shader_Create.argtypes = None
LIB_PYSGL._Shader_Create.restype = ctypes.c_void_p
LIB_PYSGL._Shader_LoadFromFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
LIB_PYSGL._Shader_LoadFromFile.restype = ctypes.c_bool
LIB_PYSGL._Shader_LoadFromStrings.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
LIB_PYSGL._Shader_LoadFromStrings.restype = ctypes.c_bool
LIB_PYSGL._Shader_LoadFromStringWithType.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
LIB_PYSGL._Shader_LoadFromStringWithType.restype = ctypes.c_bool
LIB_PYSGL._Shader_GetCurrentTexture.argtypes = None
LIB_PYSGL._Shader_GetCurrentTexture.restype = ctypes.c_void_p

LIB_PYSGL._Shader_SetUniformInt.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
LIB_PYSGL._Shader_SetUniformFloat.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_float]
LIB_PYSGL._Shader_SetUniformBool.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool]
LIB_PYSGL._Shader_SetUniformTexture.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]
LIB_PYSGL._Shader_SetUniformIntVector.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
LIB_PYSGL._Shader_SetUniformFloatVector.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._Shader_SetUniformColor.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]


ShaderPtr = ctypes.c_void_p

def get_current_texture() -> ctypes.c_void_p:
    return LIB_PYSGL._Shader_GetCurrentTexture()


class Shader:

    class Type(Enum):
        VERTEX = 0
        GEOMETRY = 1
        FRAGMENT = 2

    @classmethod
    def FromString(self, fragment: str, vertex: str) ->  "Shader":
        shader = Shader()
        shader.load_from_strings(fragment, vertex)
        return shader
    
    @classmethod
    def FromFile(self, fragment_path: str, vertex_path: str) -> "Shader":
        shader = Shader()
        shader.load_from_files(fragment_path, vertex_path)
        return shader
    
    @classmethod
    def FromType(self, type: Type, source: str):
        shader = Shader()
        if shader.load_from_type(type, source):
            print("Shader loaded!")
        else:
            print("Shader not loaded!")
        return shader

    def __init__(self):
        self._ptr: ShaderPtr | None = LIB_PYSGL._Shader_Create()
        self.__fragment_data: str = ""
        self.__vertex_data: str = ""

        self.__fragment_path: str | None = None
        self.__vertex_path: str | None =  None

    def set_uniform(self, name: str, value: int | float | bool | Vector2i | Vector2f | Color) -> "Shader":

        if isinstance(value, bool):
            LIB_PYSGL._Shader_SetUniformBool(self._ptr, name.encode('utf-8'), value)
        elif isinstance(value, int):
            LIB_PYSGL._Shader_SetUniformInt(self._ptr, name.encode('utf-8'), value)
        elif isinstance(value, float):
            LIB_PYSGL._Shader_SetUniformFloat(self._ptr, name.encode('utf-8'), value)
        elif isinstance(value, ctypes.c_void_p):
            LIB_PYSGL._Shader_SetUniformTexture(self._ptr, name.encode('utf-8'), value)
        elif isinstance(value, Vector2f):
            LIB_PYSGL._Shader_SetUniformFloatVector(self._ptr, name.encode('utf-8'), float(value.x), float(value.y))
        elif isinstance(value, Vector2i):
            LIB_PYSGL._Shader_SetUniformTexture(self._ptr, name.encode('utf-8'), int(value.x), int(value.y))
        elif isinstance(value, Color):
            LIB_PYSGL._Shader_SetUniformColor(self._ptr, name.encode('utf-8'), int(value.r), int(value.g), int(value.b), int(value.a))
        else:
            raise TypeError("Invalid uniform type.")

    def get_ptr(self) -> ShaderPtr:
        return self._ptr

    def set_ptr(self, ptr: ShaderPtr) -> "Shader":
        self._ptr = ptr
        return self
    
    def load_from_type(self, type: Type, source: str) -> bool:
        return LIB_PYSGL._Shader_LoadFromStringWithType(self._ptr, source.encode('utf-8'), type.value)
    
    def load_from_strings(self, fragment: str, vertex: str) -> "Shader":
        self.__fragment_data = fragment
        self.__vertex_data = vertex
        LIB_PYSGL._Shader_LoadFromStrings(self._ptr, self.__vertex_data.encode('utf-8'), self.__fragment_data.encode('utf-8'))

    def load_from_files(self, fragment_path: str, vertex_path: str) -> "Shader":
        self.__fragment_path = fragment_path
        self.__vertex_path = vertex_path
        self.__fragment_data = open(self.__fragment_path, 'r').read()
        self.__vertex_data = open(self.__vertex_path, 'r').read()
        LIB_PYSGL._Shader_LoadFromFile(self._ptr, self.__vertex_path.encode('utf-8'), self.__fragment_path.encode('utf-8'))
    