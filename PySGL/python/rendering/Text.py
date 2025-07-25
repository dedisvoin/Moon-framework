import ctypes
from enum import Enum, auto
import os
from typing import Any, Self
from ..Colors import *
from ..Vectors import Vector2f
from ..Types import OriginTypes

# Load the shared library
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
            print("PySGL.Text: Library not found at", lib_path)
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


LIB_PYSGL.loadSystemFont.argtypes = [ctypes.c_char_p]
LIB_PYSGL.loadSystemFont.restype = ctypes.c_void_p

LIB_PYSGL.createText.argtypes = [ctypes.c_void_p]
LIB_PYSGL.createText.restype =  ctypes.c_void_p

LIB_PYSGL.setText.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
LIB_PYSGL.setText.restype = None

LIB_PYSGL.setTextSize.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL.setTextSize.restype = None

LIB_PYSGL.setTextColor.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_PYSGL.setTextColor.restype = None

LIB_PYSGL.setTextPosition.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL.setTextPosition.restype = None

LIB_PYSGL.setTextOfsset.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL.setTextOfsset.restype = None

LIB_PYSGL.setTextAngle.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_PYSGL.setTextAngle.restype = None

LIB_PYSGL.setStyle.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL.setStyle.restype = None

LIB_PYSGL.setOutlineColor.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_PYSGL.setOutlineColor.restype = None

LIB_PYSGL.setOutlineThickness.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_PYSGL.setOutlineThickness.restype = None

LIB_PYSGL.setLetterSpacing.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_PYSGL.setLetterSpacing.restype = None

LIB_PYSGL.getTextWidth.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getTextWidth.restype = ctypes.c_double

LIB_PYSGL.getTextHeight.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getTextHeight.restype = ctypes.c_double

LIB_PYSGL.setFont.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.setFont.restype = None

LIB_PYSGL.setTextScale.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL.setTextScale.restype = None

class Font:
    @classmethod
    def SystemFont(self, name: str):
        font_path = "C:/Windows/Fonts/" + name.capitalize() + ".ttf"
        if os.path.isfile(font_path):
            return Font(font_path)
        else:
            raise FileNotFoundError(f"Font file not found: {font_path}")

    def __init__(self, font_path: str):
        self.__font_path = font_path
        self.__font_ptr = LIB_PYSGL.loadSystemFont(self.__font_path.encode('utf-8'))

    def get_font_ptr(self):
        return self.__font_ptr

    def get_font_path(self):
        return self.__font_path
    

def get_all_system_font_names() -> list[str]:
    """Возвращает массив путей системных шрифтов"""
    fonts = []
    for font_name in os.listdir("C:/Windows/Fonts"):
        if font_name.endswith(".ttf"):
            fonts.append(font_name[:-4])
    return fonts

ARRAY_OF_SYSTEM_FONTS: list[Font] | None = None

def init_system_fonts():
    """Инициализирует массив системных шрифтов"""
    global ARRAY_OF_SYSTEM_FONTS
    ARRAY_OF_SYSTEM_FONTS = []
    for i, name in enumerate(get_all_system_font_names()):
        try:
            ARRAY_OF_SYSTEM_FONTS.append(Font.SystemFont(name))
        except:
            print(f"FontLoader: Font '{name}' has not been loaded.")
    print(f"FontLoader: Loaded {len(ARRAY_OF_SYSTEM_FONTS)} fonts.")

init_system_fonts()


def get_system_font(index: int):
    """Возвращает системный шрифт по индексу"""
    try:
        return ARRAY_OF_SYSTEM_FONTS[index]
    except IndexError:
        raise IndexError(f"Index out of range. Maximum index is {len(ARRAY_OF_SYSTEM_FONTS) - 1}")


BaseTextPtr = ctypes.c_void_p


class TextStyle:
    REGULAR = 0
    BOLD = 1 << 0
    ITALIC = 1 << 1
    UNDERLINE = 1 << 2
    STRIKEOUT = 1 << 3

class BaseText:

    __slots__ = ('__font', '__text_ptr', '__text', '__scale', '__angle', '__origin', '__outline_color', '__outline_thickness', '__color', '__letter_spacing')

    def __init__(self, font: Font):
        self.__font = font
        self.__text_ptr: BaseTextPtr = LIB_PYSGL.createText(self.__font.get_font_ptr())
        self.__text: str = ""
        self.__scale: list[float, float] = [1, 1]
        self.__origin: Vector2f = Vector2f(0, 0)
        self.__angle: float = 0
        self.__outline_color: Color | None = None
        self.__outline_thickness: float = 0
        self.__color: Color = Color(0, 0, 0, 255)
        self.__letter_spacing: float = 0
        LIB_PYSGL.setTextColor(self.__text_ptr, self.__color.r, self.__color.g, self.__color.b, self.__color.a)

    def get_ptr(self) -> BaseTextPtr:
        return self.__text_ptr
    
    def get_scale(self) -> list[float]:
        return self.__scale
        
    def set_text(self, text: str) -> Self:
        self.__text = text
        LIB_PYSGL.setText(self.__text_ptr, text.encode('utf-8'))
        return self
    
    def set_text_scale_xy(self, x: float | None = None, y: float | None = None) -> Self:
        if x is not None :
            self.__scale[0] = x
        if y is not None :
            self.__scale[1] = y
        LIB_PYSGL.setTextScale(self.__text_ptr, self.__scale[0], self.__scale[1])
        return self
    
    def set_text_scale(self, scale: float) -> Self:
        self.__scale[0] = scale
        self.__scale[1] = scale
        LIB_PYSGL.setTextScale(self.__text_ptr, self.__scale[0], self.__scale[1])
        return self
    
    def set_fast_text(self, value: Any) -> Self:
        LIB_PYSGL.setText(self.__text_ptr, str(value).encode('utf-8'))
        return self
        
    def set_size(self, size: int | float) -> Self:
        LIB_PYSGL.setTextSize(self.__text_ptr, int(size))
        return self
        
    def set_color(self, color: Color) -> Self:
        self.__color = color
        LIB_PYSGL.setTextColor(self.__text_ptr, color.r, color.g, color.b, color.a)
        return self
        
    def set_position(self, x: float, y: float) -> Self:
        LIB_PYSGL.setTextPosition(self.__text_ptr, x, y)
        return self
        
    def set_origin(self, x: float, y: float) -> Self:
        LIB_PYSGL.setTextOfsset(self.__text_ptr, x, y)
        self.__origin.x = x
        self.__origin.y = y
        return self
    
    def get_origin(self) -> Vector2f:
        return self.__origin
        
    def set_angle(self, angle: float) -> Self:
        LIB_PYSGL.setTextAngle(self.__text_ptr, angle)
        self.__angle = angle
        return self

    def get_angle(self) -> float:
        return self.__angle

    def set_style(self, style: TextStyle) -> Self:
        LIB_PYSGL.setStyle(self.__text_ptr, style)
        return self
    
    def set_font(self, font: Font) -> Self:
        LIB_PYSGL.setFont(self.__text_ptr, font.get_font_ptr())
        return self

    def set_outline_color(self, color: Color) -> Self:
        LIB_PYSGL.setOutlineColor(self.__text_ptr, color.r, color.g, color.b, color.a)
        self.__outline_color = color
        return self
    
    def get_outline_color(self) -> Color:
        return self.__outline_color

    def set_outline_thickness(self, thickness: float) -> Self:
        LIB_PYSGL.setOutlineThickness(self.__text_ptr, thickness)
        self.__outline_thickness = thickness
        return self
    
    def get_outline_thickness(self) -> float:
        return self.__outline_thickness

    def set_letter_spacing(self, spacing: float) -> Self:
        LIB_PYSGL.setLetterSpacing(self.__text_ptr, spacing)
        self.__letter_spacing = spacing
        return self
    
    def get_letter_spacing(self) -> float:
        return self.__letter_spacing
    
    def get_text_width(self) -> float:
        return LIB_PYSGL.getTextWidth(self.__text_ptr)
    
    def get_text_height(self) -> float:
        return LIB_PYSGL.getTextHeight(self.__text_ptr)
    
    def get_uninitialized_text_width(self, text: str) -> float:
        saved_text = self.__text
        self.set_text(text)
        width = LIB_PYSGL.getTextWidth(self.__text_ptr)
        self.set_text(saved_text)
        return width
    
    def get_uninitialized_text_height(self, text: str) -> float:
        saved_text = self.__text
        self.set_text(text)
        height = LIB_PYSGL.getTextHeight(self.__text_ptr)
        self.set_text(saved_text)
        return height
    


    
class Text(BaseText):

    __slots__ = ('__typed_origin', '__origin_padding')

    def __init__(self, font: Font):
        super().__init__(font)

        self.__typed_origin: OriginTypes = OriginTypes.TOP_LEFT
        self.__origin_padding: Vector2f = Vector2f.zero()
        self.set_origin(0, 0)

    def set_origin_padding(self, padding: float):
        self.__origin_padding.x = padding
        self.__origin_padding.y = padding

    def set_origin_padding_y(self, padding: float):
        self.__origin_padding.y = padding

    def set_origin_padding_x(self, padding: float):
        self.__origin_padding.x = padding

    def get_origin_padding(self) -> Vector2f:
        return self.__origin_padding

    def get_typed_origin(self) -> OriginTypes:
        return self.__typed_origin

    def set_typed_origin(self, origin_type: OriginTypes):
        self.__typed_origin = origin_type

        width = self.get_text_width()
        height = self.get_text_height()
       

        match (self.__typed_origin):
            case OriginTypes.CENTER:
                self.set_origin((width / 2 + self.__origin_padding.x) / self.get_scale()[0],    (height / 2  + self.__origin_padding.y) / self.get_scale()[1])

            case OriginTypes.TOP_CENTER:
                self.set_origin((width / 2 + self.__origin_padding.x) / self.get_scale()[0],    (0  + self.__origin_padding.y) / self.get_scale()[1])
            case OriginTypes.DOWN_CENTER:
                self.set_origin((width / 2 + self.__origin_padding.x) / self.get_scale()[0],    (height  + self.__origin_padding.y) / self.get_scale()[1])
            case OriginTypes.LEFT_CENTER:
                self.set_origin((0 + self.__origin_padding.x) / self.get_scale()[0],            (height / 2  + self.__origin_padding.y) / self.get_scale()[1])
            case OriginTypes.RIGHT_CENTER:
                self.set_origin((width + self.__origin_padding.x) / self.get_scale()[0],        (height / 2  + self.__origin_padding.y) / self.get_scale()[1])

            case OriginTypes.TOP_LEFT:
                self.set_origin((0 + self.__origin_padding.x) / self.get_scale()[0],            (0 + self.__origin_padding.y) / self.get_scale()[1])
            case OriginTypes.TOP_RIGHT:
                self.set_origin((width + self.__origin_padding.x) / self.get_scale()[0],        (0 + self.__origin_padding.y) / self.get_scale()[1])
            case OriginTypes.DOWN_LEFT:
                self.set_origin((0 + self.__origin_padding.x) / self.get_scale()[0],            (height + self.__origin_padding.y) / self.get_scale()[1])
            case OriginTypes.DOWN_RIGHT:
                self.set_origin((width + self.__origin_padding.x) / self.get_scale()[0],        (height + self.__origin_padding.y) / self.get_scale()[1])
            case _:
                raise TypeError("Invalid origin type!")




    
