import ctypes
from enum import Enum
import os
from typing import Self
from ..Colors import Color, COLOR_BLACK
from ..Vectors import Vector2f
from Moon import DLL_FOUND_PATH

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
        
        lib_path = DLL_FOUND_PATH
        if not os.path.exists(lib_path):
            print("PySGL.Vertexes: Library not found at", lib_path)
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

# --- Настройка функций для работы с VertexArray ---
# Передаем только те функции, которые взаимодействуют с VertexArray
LIB_PYSGL._VertexArray_Create.restype = ctypes.c_void_p
LIB_PYSGL._VertexArray_Delete.argtypes = [ctypes.c_void_p]
LIB_PYSGL._VertexArray_Delete.restype = None
LIB_PYSGL._VertexArray_AddVertexForPositionAndColor.argtypes = [
    ctypes.c_void_p, ctypes.c_double, ctypes.c_double, 
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int
]
LIB_PYSGL._VertexArray_AddVertexForPositionAndColor.restype = None
LIB_PYSGL._VertexArray_Clear.argtypes = [ctypes.c_void_p]
LIB_PYSGL._VertexArray_Clear.restype = None
LIB_PYSGL._VertexArray_GetVertexCount.argtypes = [ctypes.c_void_p]
LIB_PYSGL._VertexArray_GetVertexCount.restype = ctypes.c_int
LIB_PYSGL._VertexArray_GetPrimitiveType.argtypes = [ctypes.c_void_p]
LIB_PYSGL._VertexArray_GetPrimitiveType.restype = ctypes.c_int
LIB_PYSGL._VertexArray_Resize.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL._VertexArray_Resize.restype = None
LIB_PYSGL._VertexArray_SetPrimitiveType.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL._VertexArray_SetPrimitiveType.restype = None
LIB_PYSGL._VertexArray_SetVertexForPositionAndColor.argtypes = [
    ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.c_double, 
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int
]
LIB_PYSGL._VertexArray_SetVertexForPositionAndColor.restype = None

# Оптимизированные функции для прямого доступа к данным вершин
LIB_PYSGL._VertexArray_SetVertexPosition.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._VertexArray_SetVertexPosition.restype = None
LIB_PYSGL._VertexArray_SetVertexColor.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_PYSGL._VertexArray_SetVertexColor.restype = None
LIB_PYSGL._VertexArray_SetAllVerticesColor.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_PYSGL._VertexArray_SetAllVerticesColor.restype = None

# Функции для работы с текстурными координатами
LIB_PYSGL._VertexArray_AddVertexWithTexCoords.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._VertexArray_AddVertexWithTexCoords.restype = None
LIB_PYSGL._VertexArray_SetVertexTexCoords.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._VertexArray_SetVertexTexCoords.restype = None
LIB_PYSGL._VertexArray_SetQuadTexCoords.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._VertexArray_SetQuadTexCoords.restype = None

class Vertex:
    """Легковесный контейнер для данных вершины."""
    __slots__ = ('position', 'color', 'tex_coords')
    
    def __init__(self, pos: Vector2f = None, color: Color = None, tex_coords: Vector2f = None):
        self.position = pos if pos is not None else Vector2f(0, 0)
        self.color = color if color is not None else COLOR_BLACK
        self.tex_coords = tex_coords if tex_coords is not None else Vector2f(0, 0)
        
    def __repr__(self):
        return f"Vertex({self.position.x}, {self.position.y}, {self.color}, {self.tex_coords})"


class VertexArray:
    """
    Класс массива вершин для графического рендеринга.

    Позволяет управлять набором вершин и определяет, как они будут отрисовываться
    (точки, линии, треугольники и т.д.). Вершины управляются внутренне в нативной
    библиотеке для лучшей производительности.
    """

    class PrimitiveType(Enum):
        """Типы примитивов для отрисовки массива вершин."""
        POINTS = 0        # Отдельные точки
        LINES = 1         # Пары вершин как отдельные линии
        LINE_STRIP = 2    # Связанные линии (полилиния)
        TRIANGLES = 3     # Тройки вершин как треугольники
        TRIANGLE_STRIP = 4 # Полоса соединенных треугольников
        TRIANGLE_FAN = 5  # Веер треугольников
        QUADS = 6         # Четверки вершин как четырехугольники
    
    def __init__(self):
        """Инициализирует пустой массив вершин."""
        self._ptr = LIB_PYSGL._VertexArray_Create()

    def get_ptr(self):
        return self._ptr
    
    def __del__(self):
        """Освобождает ресурсы нативного массива при удалении объекта Python."""
        if self._ptr: # Проверяем, что указатель существует перед удалением
            LIB_PYSGL._VertexArray_Delete(self._ptr)
            self._ptr = None # Обнуляем указатель после удаления

    def __len__(self) -> int:
        """Возвращает количество вершин в массиве."""
        return LIB_PYSGL._VertexArray_GetVertexCount(self._ptr)

    def __getitem__(self, index: int) -> Vertex:
        """
        Возвращает вершину по индексу.

        Примечание: Возвращает *новую* Python-вершину, заполненную данными из нативной стороны.
        Изменение этой возвращенной вершины не обновит массив, используйте `set_vertex` для обновления.
        """
        if not (0 <= index < len(self)):
            raise IndexError(f"Vertex index {index} out of bounds for VertexArray of size {len(self)}.")
        
        pos_x = LIB_PYSGL._VertexArray_GetVertexPositionX(self._ptr, index)
        pos_y = LIB_PYSGL._VertexArray_GetVertexPositionY(self._ptr, index)
        color_r = LIB_PYSGL._VertexArray_GetVertexColorR(self._ptr, index)
        color_g = LIB_PYSGL._VertexArray_GetVertexColorG(self._ptr, index)
        color_b = LIB_PYSGL._VertexArray_GetVertexColorB(self._ptr, index)
        color_a = LIB_PYSGL._VertexArray_GetVertexColorA(self._ptr, index)
        
        return Vertex(Vector2f(pos_x, pos_y), Color(color_r, color_g, color_b, color_a))

    def set_primitive_type(self, primitive_type: PrimitiveType) -> Self:
        """
        Устанавливает тип примитива для отрисовки.

        Args:
            primitive_type (PrimitiveType): Один из типов PrimitiveType.
        """
        if not isinstance(primitive_type, self.PrimitiveType):
            raise TypeError("primitive_type must be an instance of VertexArray.PrimitiveType")
        LIB_PYSGL._VertexArray_SetPrimitiveType(self._ptr, primitive_type.value)
        return self

    def get_primitive_type(self) -> PrimitiveType:
        """Возвращает текущий тип примитива."""
        return VertexArray.PrimitiveType(LIB_PYSGL._VertexArray_GetPrimitiveType(self._ptr))

    def append(self, vertex: Vertex) -> None:
        """
        Добавляет вершину в массив.

        Args:
            vertex (Vertex): Вершина для добавления.
        """
        if not isinstance(vertex, Vertex):
            raise TypeError("Argument 'vertex' must be an instance of Vertex.")
        
        if hasattr(vertex, 'tex_coords') and vertex.tex_coords is not None:
            LIB_PYSGL._VertexArray_AddVertexWithTexCoords(
                self._ptr,
                vertex.position.x, vertex.position.y,
                vertex.color.r, vertex.color.g, vertex.color.b, vertex.color.a,
                float(vertex.tex_coords.x), float(vertex.tex_coords.y)
            )
        else:

            LIB_PYSGL._VertexArray_AddVertexForPositionAndColor(
                self._ptr, 
                vertex.position.x, vertex.position.y, 
                vertex.color.r, vertex.color.g, vertex.color.b, vertex.color.a
            )
    
    def extend(self, vertices: list[Vertex]) -> None:
        """
        Добавляет список вершин в массив.

        Args:
            vertices (list[Vertex]): Список вершин для добавления.
        """
        for vertex in vertices:
            self.append(vertex)

    def clear(self) -> None:
        """Очищает массив вершин."""
        LIB_PYSGL._VertexArray_Clear(self._ptr)

    def set_quad_texture_coords(self, start_index: int, tex_left: float = 0.0, tex_top: float = 0.0, tex_right: float = 1.0, tex_bottom: float = 1.0) -> None:
        """
        Устанавливает текстурные координаты для квада (четырех вершин).
        
        Args:
            start_index (int): Индекс первой вершины квада
            tex_left, tex_top, tex_right, tex_bottom (float): Границы текстуры (0.0-1.0)
        """
        LIB_PYSGL._VertexArray_SetQuadTexCoords(self._ptr, start_index, tex_left, tex_top, tex_right, tex_bottom)

    def resize(self, size: int) -> None:
        """
        Изменяет размер нативного массива вершин.
        
        Если новый размер меньше текущего, вершины обрезаются.
        Если больше, новые вершины инициализируются значениями по умолчанию.

        Args:
            size (int): Новый размер массива.
        """
        if not isinstance(size, int) or size < 0:
            raise ValueError("Size must be a non-negative integer.")
        LIB_PYSGL._VertexArray_Resize(self._ptr, size) 
        LIB_PYSGL._VertexArray_Resize(self._ptr, size)

    def set_vertex(self, index: int, vertex: Vertex) -> None:
        """
        Заменяет вершину по указанному индексу.

        Args:
            index (int): Индекс заменяемой вершины.
            vertex (Vertex): Новая вершина.
        """
        if not isinstance(vertex, Vertex):
            raise TypeError("Argument 'vertex' must be an instance of Vertex.")
        if not (0 <= index < len(self)):
            raise IndexError(f"Vertex index {index} out of bounds for VertexArray of size {len(self)}.")
        
        LIB_PYSGL._VertexArray_SetVertexForPositionAndColor(
            self._ptr, index, 
            vertex.position.x, vertex.position.y, 
            vertex.color.r, vertex.color.g, vertex.color.b, vertex.color.a
        )

    def set_vertex_position(self, index: int, x: float, y: float) -> None:
        """Быстро устанавливает позицию вершины."""
        if not (0 <= index < len(self)):
            raise IndexError(f"Vertex index {index} out of bounds")
        LIB_PYSGL._VertexArray_SetVertexPosition(self._ptr, index, x, y)

    def set_vertex_color(self, index: int, color: Color) -> None:
        """Быстро устанавливает цвет вершины."""
        if not (0 <= index < len(self)):
            raise IndexError(f"Vertex index {index} out of bounds")
        LIB_PYSGL._VertexArray_SetVertexColor(self._ptr, index, color.r, color.g, color.b, color.a)

    def set_color(self, color: Color) -> None:
        """Быстро устанавливает цвет для всех вершин."""
        LIB_PYSGL._VertexArray_SetAllVerticesColor(self._ptr, color.r, color.g, color.b, color.a)

    def add_vertices(self, vertices: list[Vertex]) -> Self:
        """Быстро добавляет множество вершин."""
        for vertex in vertices:
            self.append(vertex)
        return self

    def add_vertex_with_texture(self, x: float, y: float, color: Color, tex_x: float, tex_y: float) -> None:
        """Добавляет вершину с текстурными координатами."""
        LIB_PYSGL._VertexArray_AddVertexWithTexCoords(
            self._ptr, x, y, color.r, color.g, color.b, color.a, tex_x, tex_y
        )

    def set_vertex_texture_coords(self, index: int, tex_x: float, tex_y: float) -> None:
        """Устанавливает текстурные координаты вершины."""
        if not (0 <= index < len(self)):
            raise IndexError(f"Vertex index {index} out of bounds")
        LIB_PYSGL._VertexArray_SetVertexTexCoords(self._ptr, index, tex_x, tex_y)

    def set_quad_texture_coords(self, start_index: int, left: float, top: float, width: float, height: float) -> None:
        """Устанавливает текстурные координаты для квада (4 вершины)."""
        if not (0 <= start_index < len(self) - 3):
            raise IndexError(f"Quad start index {start_index} out of bounds")
        LIB_PYSGL._VertexArray_SetQuadTexCoords(self._ptr, start_index, left, top, width, height)

    def add_textured_quad(self, x: float, y: float, width: float, height: float, color: Color, 
                         tex_left: float, tex_top: float, tex_width: float, tex_height: float) -> None:
        """Добавляет текстурированный квад."""
        start_index = len(self)
        
        # Добавляем 4 вершины квада
        self.add_vertex_with_texture(x, y, color, tex_left, tex_top)
        self.add_vertex_with_texture(x + width, y, color, tex_left + tex_width, tex_top)
        self.add_vertex_with_texture(x + width, y + height, color, tex_left + tex_width, tex_top + tex_height)
        self.add_vertex_with_texture(x, y + height, color, tex_left, tex_top + tex_height)