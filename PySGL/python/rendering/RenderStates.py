import ctypes
from typing import Self
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

LIB_PYSGL._BlendMode_CreateFull.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                            ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_PYSGL._BlendMode_CreateFull.restype = ctypes.c_void_p
LIB_PYSGL._BlendMode_Delete.argtypes = [ctypes.c_void_p]
LIB_PYSGL._BlendMode_Delete.restype = None

class BlendMode:

    class Factor():
        Zero = 0             # (0, 0, 0, 0)
        One = 1              # (1, 1, 1, 1)
        SrcColor = 2         # (src.r, src.g, src.b, src.a)
        OneMinusSrcColor = 3 # (1, 1, 1, 1) - (src.r, src.g, src.b, src.a)
        DstColor = 4         # (dst.r, dst.g, dst.b, dst.a)
        OneMinusDstColor = 5 # (1, 1, 1, 1) - (dst.r, dst.g, dst.b, dst.a)
        SrcAlpha = 6         # (src.a, src.a, src.a, src.a)
        OneMinusSrcAlpha = 7 # (1, 1, 1, 1) - (src.a, src.a, src.a, src.a)
        DstAlpha = 8         # (dst.a, dst.a, dst.a, dst.a)
        OneMinusDstAlpha = 9  # (1, 1, 1, 1) - (dst.a, dst.a, dst.a, dst.a)
        
    class Equation():
        Add = 0             # Pixel = Src * SrcFactor + Dst * DstFactor
        Subtract = 1        # Pixel = Src * SrcFactor - Dst * DstFactor
        ReverseSubtract = 2 # Pixel = Dst * DstFactor - Src * SrcFactor
        Min = 3             # Pixel = min(Dst, Src)
        Max = 4             # Pixel = max(Dst, Src)

    def __init__(self, color_src_factor: Factor, color_dst_factor: Factor, color_eq: Equation,
                       alpha_src_factor: Factor, alpha_dst_factor: Factor, alpha_eq: Equation):
        self.__color_src_factor = color_src_factor
        self.__color_dst_factor = color_dst_factor
        self.__color_eq = color_eq

        self.__alpha_src_factor = alpha_src_factor
        self.__alpha_dst_factor = alpha_dst_factor
        self.__alpha_eq = alpha_eq

        self.__blend_mode_ptr = LIB_PYSGL._BlendMode_CreateFull(self.__color_src_factor, self.__color_dst_factor, self.__color_eq,
                                                                self.__alpha_src_factor, self.__alpha_dst_factor, self.__alpha_eq)


    def  __del__(self) -> None:
        LIB_PYSGL._BlendMode_Delete(self.__blend_mode_ptr)

    def get_ptr(self) -> ctypes.c_void_p:
        return self.__blend_mode_ptr




LIB_PYSGL._RenderStates_Create.argtypes = None
LIB_PYSGL._RenderStates_Create.restype = ctypes.c_void_p
LIB_PYSGL._RenderStates_Delete.argtypes = [ctypes.c_void_p]
LIB_PYSGL._RenderStates_Delete.restype = None
LIB_PYSGL._RenderStates_SetShader.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL._RenderStates_SetShader.restype = None
LIB_PYSGL._RenderStates_SetBlendMode.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL._RenderStates_SetBlendMode.restype = None

RenderStatesPtr = ctypes.c_void_p

class RenderStates:
    def __init__(self):
        self._ptr = LIB_PYSGL._RenderStates_Create()
        self.__shader: Shader | None = None
        self.__blend_mode = None

    def get_ptr(self) -> RenderStatesPtr:
        return self._ptr
    
    def set_shader(self, shader: Shader) -> Self:
        self.__shader = shader
        LIB_PYSGL._RenderStates_SetShader(self._ptr, self.__shader.get_ptr())
        return self
    
    def set_blend_mode(self, blend_mode: BlendMode) -> Self:
        self.__blend_mode =  blend_mode
        LIB_PYSGL._RenderStates_SetBlendMode(self._ptr, self.__blend_mode.get_ptr())

    def get_blend_mode(self) -> BlendMode:
        return self.__blend_mode

    def get_shader(self) -> Shader:
        return self.__shader

    
