
import ctypes
from typing import Self, Final, final

from Moon.python.Types import *
from Moon.python.Colors import *
from Moon.python.Vectors import Vector2f, Vector2i, Vector2Type, Vector2TypeTuple
from Moon.python.Rendering.Vertexes import Vertex2d, VertexList, VertexListTypes, NativeVertex2dPtr

from Moon.python.utils import find_library


# Загружаем DLL библиотеку
try:
    LIB_MOON: Final[ctypes.CDLL] = ctypes.CDLL(find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")

@final
class Polyline:
    def __init__(self):
        self.__vertex_list = VertexList()
        self.__vertex_list.set_primitive_type(VertexListTypes.LineStrip)

        self.__color = COLOR_WHITE
        self.__vertex_list.set_color(self.__color)

    def clear(self):
        self.__vertex_list.clear()

    def append_point(self, point: Vector2f):
        self.__vertex_list.append(Vertex2d().FromPosition(point))

    def prepend_point(self, point: Vector2f):
        self.__vertex_list.prepend(Vertex2d().FromPosition(point))

    def set_color(self, color: Color):
        self.__vertex_list.set_color(color)

    def get_color(self) -> Color:
        return self.__color

    def get_points_count(self) -> int:
        return self.__vertex_list.length()

    def remove_point(self, index: int):
        self.__vertex_list.remove(index)

    def get_ptr(self) -> ctypes.c_void_p:
        return self.__vertex_list.get_ptr()


# Глобальные константы для часто используемых фигур.
# Использование Final гарантирует, что эти переменные не будут переназначены.
# Это удобно для стандартных, преднастроенных форм, которые можно переиспользовать.
POLYLINE_SHAPE:         Final[Polyline]         = Polyline()

@final
class LineShape:
    def __init__(self):
        self.__vertex_array = VertexList()
        self.__vertex_array.set_primitive_type(VertexListTypes.Lines)
        self.__color = None

    def clear(self):
        self.__vertex_array.clear()

    def set_color(self, color: Color) -> Self:
        self.__color = color
        self.__vertex_array.set_color(color)
        return self

    def get_color(self) -> Optional[Color]:
        return self.__color

    def init_points(self, point_1: Vector2Type = Vector2f.zero(), point_2: Vector2Type = Vector2f.zero()) -> Self:
        self.__vertex_array.auto_append(Vertex2d().FromPosition(point_1))
        self.__vertex_array.auto_append(Vertex2d().FromPosition(point_2))
        return self

    def set_start_point(self, point: Vector2Type) -> Self:
        self.__vertex_array.get(0).position = point
        return self

    def set_end_point(self, point: Vector2Type) -> Self:
        self.__vertex_array.get(1).position = point
        return self

    def get_start_point(self) -> NativeVertex2dPtr:
        return self.__vertex_array.get(0)

    def get_end_point(self) -> NativeVertex2dPtr:
        return self.__vertex_array.get(1)

    def get_ptr(self) -> ctypes.c_void_p:
        return self.__vertex_array.get_ptr()

LINE_SHAPE:             Final[LineShape]        = LineShape()
