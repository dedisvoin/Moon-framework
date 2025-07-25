import ctypes
from enum import Enum
import os
from ..Colors import Color, COLOR_BLACK
from ..Vectors import Vector2f

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

# Функции для получения данных о вершине из VertexArray напрямую
# Изменено на ctypes.c_float для точности позиции
LIB_PYSGL._VertexArray_GetVertexPositionX.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL._VertexArray_GetVertexPositionX.restype = ctypes.c_float
LIB_PYSGL._VertexArray_GetVertexPositionY.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL._VertexArray_GetVertexPositionY.restype = ctypes.c_float
LIB_PYSGL._VertexArray_GetVertexColorR.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL._VertexArray_GetVertexColorR.restype = ctypes.c_int
LIB_PYSGL._VertexArray_GetVertexColorG.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL._VertexArray_GetVertexColorG.restype = ctypes.c_int
LIB_PYSGL._VertexArray_GetVertexColorB.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL._VertexArray_GetVertexColorB.restype = ctypes.c_int
LIB_PYSGL._VertexArray_GetVertexColorA.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL._VertexArray_GetVertexColorA.restype = ctypes.c_int

class Vertex:
    """
    Класс вершины для графического рендеринга.

    Содержит информацию о **позиции** и **цвете** вершины. Этот класс является
    просто контейнером данных для удобства, фактические данные хранятся
    в нативном VertexArray.
    """

    def __init__(self, pos: Vector2f = Vector2f(0, 0), color: Color = COLOR_BLACK):
        """
        Инициализирует новую вершину.

        Args:
            pos (Vector2f): Начальная позиция вершины (по умолчанию (0, 0)).
            color (Color): Начальный цвет вершины (по умолчанию черный).
        """
        self.__position = pos
        self.__color = color

    @property
    def position(self) -> Vector2f:
        """
        Возвращает или устанавливает позицию вершины.

        Пример:
            >>> vertex.position = Vector2f(10, 20)
            >>> print(vertex.position.x)
        """
        return self.__position

    @position.setter
    def position(self, new_pos: Vector2f):
        if not isinstance(new_pos, Vector2f):
            raise TypeError("Position must be a Vector2f object.")
        self.__position = new_pos

    @property
    def color(self) -> Color:
        """
        Возвращает или устанавливает цвет вершины.

        Пример:
            >>> vertex.color = Color(255, 0, 0)
            >>> print(vertex.color.r)
        """
        return self.__color

    @color.setter
    def color(self, new_color: Color):
        if not isinstance(new_color, Color):
            raise TypeError("Color must be a Color object.")
        self.__color = new_color

    def __repr__(self):
        return f"Vertex(pos={self.position}, color={self.color})"


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

    def set_primitive_type(self, primitive_type: PrimitiveType) -> None:
        """
        Устанавливает тип примитива для отрисовки.

        Args:
            primitive_type (PrimitiveType): Один из типов PrimitiveType.
        """
        if not isinstance(primitive_type, self.PrimitiveType):
            raise TypeError("primitive_type must be an instance of VertexArray.PrimitiveType")
        LIB_PYSGL._VertexArray_SetPrimitiveType(self._ptr, primitive_type.value)

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
        """
        Устанавливает позицию вершины по индексу.

        Args:
            index (int): Индекс вершины.
            x (float): Новая X-координата.
            y (float): Новая Y-координата.
        """
        if not (0 <= index < len(self)):
            raise IndexError(f"Vertex index {index} out of bounds for VertexArray of size {len(self)}.")
        
        # Получаем текущий цвет, чтобы не изменить его
        current_vertex = self[index] 
        self.set_vertex(index, Vertex(Vector2f(x, y), current_vertex.color))

    def set_vertex_color(self, index: int, color: Color) -> None:
        """
        Устанавливает цвет вершины по индексу.

        Args:
            index (int): Индекс вершины.
            color (Color): Новый цвет.
        """
        if not isinstance(color, Color):
            raise TypeError("Argument 'color' must be an instance of Color.")
        if not (0 <= index < len(self)):
            raise IndexError(f"Vertex index {index} out of bounds for VertexArray of size {len(self)}.")
        
        # Получаем текущую позицию, чтобы не изменить её
        current_vertex = self[index]
        self.set_vertex(index, Vertex(current_vertex.position, color))

    def set_color(self, color: Color) -> None:
        """
        Устанавливает цвет для всех вершин в массиве.

        Args:
            color (Color): Новый цвет.
        """
        if not isinstance(color, Color):
            raise TypeError("Argument 'color' must be an instance of Color.")
        
        for i in range(len(self)):
            # Получаем текущую позицию, чтобы не менять её
            current_pos = self[i].position 
            self.set_vertex(i, Vertex(current_pos, color))

    # fluent interface для удобства
    def with_primitive_type(self, primitive_type: PrimitiveType) -> 'VertexArray':
        """Устанавливает тип примитива и возвращает VertexArray для цепочки вызовов."""
        self.set_primitive_type(primitive_type)
        return self

    def with_resize(self, size: int) -> 'VertexArray':
        """Изменяет размер массива и возвращает VertexArray для цепочки вызовов."""
        self.resize(size)
        return self

    def with_color(self, color: Color) -> 'VertexArray':
        """Устанавливает цвет для всех вершин и возвращает VertexArray для цепочки вызовов."""
        self.set_color(color)
        return self