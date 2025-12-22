"""
#### *Модуль работы с массивами вершин в Moon*

---

##### Версия: 1.0.0

*Автор: Павлов Иван (Pavlov Ivan)*

*Лицензия: MIT*
##### Реализованно на 95%

---

✓ Эффективное управление вершинами:
  - Создание и управление массивами вершин
  - Поддержка всех типов примитивов OpenGL
  - Оптимизированные операции через нативный код

✓ Гибкая система вершин:
  - Легковесный класс Vertex с поддержкой позиции, цвета и текстур
  - Быстрые операции изменения отдельных атрибутов
  - Массовые операции для эффективной работы

✓ Производительность и удобство:
  - Нативное управление памятью для максимальной скорости
  - Python-интерфейс для удобства разработки
  - Автоматическое управление ресурсами

✓ Готовые интерфейсы:
  - Vertex - контейнер данных вершины
  - VertexArray - массив вершин с типами примитивов
  - PrimitiveType - перечисление типов отрисовки

---

:Requires:

• Python 3.8+

• Библиотека ctypes (для работы с DLL)

• Moon.dll (нативная библиотека рендеринга)

• Moon.Colors (модуль цветов)

• Moon.Vectors (модуль векторов)

---

== Лицензия MIT ==================================================

[MIT License]
Copyright (c) 2025 Pavlov Ivan

Данная лицензия разрешает лицам, получившим копию данного программного обеспечения
и сопутствующей документации (в дальнейшем именуемыми «Программное Обеспечение»),
безвозмездно использовать Программное Обеспечение без ограничений, включая неограниченное
право на использование, копирование, изменение, слияние, публикацию, распространение,
сублицензирование и/или продажу копий Программного Обеспечения, а также лицам, которым
предоставляется данное Программное Обеспечение, при соблюдении следующих условий:

[ Уведомление об авторском праве и данные условия должны быть включены во все копии ]
[                 или значительные части Программного Обеспечения.                  ]

ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНО
ВЫРАЖЕННЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ, НО НЕ ОГРАНИЧИВАЯСЬ ГАРАНТИЯМИ ТОВАРНОЙ
ПРИГОДНОСТИ, СООТВЕТСТВИЯ ПО ЕГО КОНКРЕТНОМУ НАЗНАЧЕНИЮ И ОТСУТСТВИЯ НАРУШЕНИЙ ПРАВ.
НИ В КАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ НЕ НЕСУТ ОТВЕТСТВЕННОСТИ ПО ИСКАМ О
ВОЗМЕЩЕНИИ УЩЕРБА, УБЫТКОВ ИЛИ ДРУГИХ ТРЕБОВАНИЙ ПО ДЕЙСТВУЮЩЕМУ ПРАВУ ИЛИ ИНОМУ,
ВОЗНИКШИМ ИЗ, ИМЕЮЩИМ ПРИЧИНОЙ ИЛИ СВЯЗАННЫМ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ ИЛИ
ИСПОЛЬЗОВАНИЕМ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ ИЛИ ИНЫМИ ДЕЙСТВИЯМИ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ.
"""


from copy import copy
from csv import QUOTE_ALL
import ctypes
from enum import Enum
from typing import Self
from Moon.python.utils import find_library
from Moon.python.Vectors import Vec2f, Vec2i, Vec2T
from Moon.python.Colors import *

# Загружаем DLL библиотеку
try:
    LIB_MOON = ctypes.CDLL(find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")

VertexPtr = ctypes.c_void_p
VertexArrayPtr = ctypes.c_void_p

# Vertex биндинги
LIB_MOON._Vertex_Init.argtypes = []
LIB_MOON._Vertex_Init.restype = VertexPtr

LIB_MOON._Vertex_FromPtr.argtypes = [VertexPtr]
LIB_MOON._Vertex_FromPtr.restype = VertexPtr

LIB_MOON._Vertex_InitFromCoords.argtypes = [ctypes.c_double, ctypes.c_double]
LIB_MOON._Vertex_InitFromCoords.restype = VertexPtr

LIB_MOON._Vertex_InitFromCoordsAndColor.argtypes = [
    ctypes.c_double, ctypes.c_double,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int
]
LIB_MOON._Vertex_InitFromCoordsAndColor.restype = VertexPtr

LIB_MOON._Vertex_InitFromCoordsAndColorAndTexCoords.argtypes = [
    ctypes.c_double, ctypes.c_double,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_double, ctypes.c_double
]
LIB_MOON._Vertex_InitFromCoordsAndColorAndTexCoords.restype = VertexPtr

LIB_MOON._Vertex_Delete.argtypes = [VertexPtr]
LIB_MOON._Vertex_Delete.restype = None

LIB_MOON._Vertex_SetPosition.argtypes = [VertexPtr, ctypes.c_double, ctypes.c_double]
LIB_MOON._Vertex_SetPosition.restype = None

LIB_MOON._Vertex_SetColor.argtypes = [VertexPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Vertex_SetColor.restype = None

LIB_MOON._Vertex_SetTexCoords.argtypes = [VertexPtr, ctypes.c_double, ctypes.c_double]
LIB_MOON._Vertex_SetTexCoords.restype = None

LIB_MOON._Vertex_GetPositionX.argtypes = [VertexPtr]
LIB_MOON._Vertex_GetPositionX.restype = ctypes.c_double

LIB_MOON._Vertex_GetPositionY.argtypes = [VertexPtr]
LIB_MOON._Vertex_GetPositionY.restype = ctypes.c_double

LIB_MOON._Vertex_GetTexCoordX.argtypes = [VertexPtr]
LIB_MOON._Vertex_GetTexCoordX.restype = ctypes.c_double

LIB_MOON._Vertex_GetTexCoordY.argtypes = [VertexPtr]
LIB_MOON._Vertex_GetTexCoordY.restype = ctypes.c_double

LIB_MOON._Vertex_GetColorR.argtypes = [VertexPtr]
LIB_MOON._Vertex_GetColorR.restype = ctypes.c_int

LIB_MOON._Vertex_GetColorG.argtypes = [VertexPtr]
LIB_MOON._Vertex_GetColorG.restype = ctypes.c_int

LIB_MOON._Vertex_GetColorB.argtypes = [VertexPtr]
LIB_MOON._Vertex_GetColorB.restype = ctypes.c_int

LIB_MOON._Vertex_GetColorA.argtypes = [VertexPtr]
LIB_MOON._Vertex_GetColorA.restype = ctypes.c_int

# VertexArray биндинги
LIB_MOON._VertexArray_Init.argtypes = []
LIB_MOON._VertexArray_Init.restype = VertexArrayPtr

LIB_MOON._VertexArray_Delete.argtypes = [VertexArrayPtr]
LIB_MOON._VertexArray_Delete.restype = None

LIB_MOON._VertexArray_SetPrimitiveType.argtypes = [VertexArrayPtr, ctypes.c_int]
LIB_MOON._VertexArray_SetPrimitiveType.restype = None

LIB_MOON._VertexArray_Clear.argtypes = [VertexArrayPtr]
LIB_MOON._VertexArray_Clear.restype = None

LIB_MOON._VertexArray_GetVertexCount.argtypes = [VertexArrayPtr]
LIB_MOON._VertexArray_GetVertexCount.restype = ctypes.c_int

LIB_MOON._VertexArray_GetBoundsPosX.argtypes = [VertexArrayPtr]
LIB_MOON._VertexArray_GetBoundsPosX.restype = ctypes.c_double

LIB_MOON._VertexArray_GetBoundsPosY.argtypes = [VertexArrayPtr]
LIB_MOON._VertexArray_GetBoundsPosY.restype = ctypes.c_double

LIB_MOON._VertexArray_GetBoundsSizeW.argtypes = [VertexArrayPtr]
LIB_MOON._VertexArray_GetBoundsSizeW.restype = ctypes.c_double

LIB_MOON._VertexArray_GetBoundsSizeH.argtypes = [VertexArrayPtr]
LIB_MOON._VertexArray_GetBoundsSizeH.restype = ctypes.c_double

LIB_MOON._VertexArray_Resize.argtypes = [VertexArrayPtr, ctypes.c_int]
LIB_MOON._VertexArray_Resize.restype = None

LIB_MOON._VertexArray_IsEmpty.argtypes = [VertexArrayPtr]
LIB_MOON._VertexArray_IsEmpty.restype = ctypes.c_bool

LIB_MOON._VertexArray_AppendVertex.argtypes = [VertexArrayPtr, VertexPtr]
LIB_MOON._VertexArray_AppendVertex.restype = None

LIB_MOON._VertexArray_GetVertex.argtypes = [VertexArrayPtr, ctypes.c_int]
LIB_MOON._VertexArray_GetVertex.restype = VertexPtr

LIB_MOON._VertexArray_RemoveVertex.argtypes = [VertexArrayPtr, ctypes.c_int]
LIB_MOON._VertexArray_RemoveVertex.restype = None

LIB_MOON._VertexArray_InsertVertex.argtypes = [VertexArrayPtr, ctypes.c_int, VertexPtr]
LIB_MOON._VertexArray_InsertVertex.restype = None

LIB_MOON._VertexArray_PrependVertex.argtypes = [VertexArrayPtr, VertexPtr]
LIB_MOON._VertexArray_PrependVertex.restype = None

LIB_MOON._VertexArray_SetColor.argtypes = [VertexArrayPtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._VertexArray_SetColor.restype = None

class Vertex2d:
    @classmethod
    def FromPosition(cls, pos: Vec2T) -> "Vertex2d":
        """
        #### Создает `Vertex2d` из позиции

        ---

        :Args:
        - pos - Позиция в виде `Vector2Type` (обычно `Vector2f`/`Vector2i`)

        :Return:
        - `Vertex2d` - Новый объект вершины, инициализированный заданной позицией

        :Example:
        ```python
        v = Vertex2d.FromPosition(Vector2f(10, 20))
        ```
        """
        vertex = cls()
        ptr = LIB_MOON._Vertex_InitFromCoords(float(pos.x), float(pos.y))
        vertex.set_ptr(ptr)
        return vertex

    @classmethod
    def FromPositionAndColor(cls, pos: Vec2T, color: Color) -> "Vertex2d":
        """
        #### Создает `Vertex2d` из позиции и цвета

        ---

        :Args:
        - pos - Позиция в виде `Vector2Type`
        - color - Экземпляр `Color` для установки цвета вершины

        :Return:
        - `Vertex2d` - Новый объект вершины с позицией и цветом

        :Example:
        ```python
        v = Vertex2d.FromPositionAndColor(Vector2f(10,20), COLOR_RED)
        ```
        """
        vertex = cls()
        r, g, b, a = color.rgba
        ptr = LIB_MOON._Vertex_InitFromCoordsAndColor(float(pos.x), float(pos.y), r, g, b, a)
        vertex.set_ptr(ptr)
        return vertex

    @classmethod
    def FromPositionColorAndTexCoords(cls, pos: Vec2T, color: Color, tex_coords: Vec2i) -> "Vertex2d":
        """
        #### Создает `Vertex2d` с позицией, цветом и текстурными координатами

        ---

        :Args:
        - pos - Позиция в виде `Vector2Type`
        - color - Экземпляр `Color`
        - tex_coords - Текстурные координаты в виде `Vector2i`

        :Return:
        - `Vertex2d` - Новый объект вершины со всеми атрибутами

        :Example:
        ```python
        v = Vertex2d.FromPositionColorAndTexCoords(Vector2f(0,0), COLOR_WHITE, Vector2i(0,0))
        ```
        """
        vertex = cls()
        r, g, b, a = color.rgba
        ptr = LIB_MOON._Vertex_InitFromCoordsAndColorAndTexCoords(
            float(pos.x), float(pos.y), r, g, b, a, tex_coords.x, tex_coords.y
        )
        vertex.set_ptr(ptr)
        return vertex

    @classmethod
    def FromPtr(cls, ptr: VertexPtr) -> "Vertex2d":
        """
        #### Создает `Vertex2d` из нативного указателя

        ---

        :Args:
        - ptr - Нативный указатель на структуру вершины (`VertexPtr`)

        :Return:
        - `Vertex2d` - Обертка над существующей нативной вершиной (владение указателем передается вызову)

        :Example:
        ```python
        v = Vertex2d.FromPtr(native_ptr)
        ```
        """
        vertex = cls()
        vertex.set_ptr(ptr)
        return vertex

    def __init__(self):
        """
        #### Инициализация нового `Vertex2d`

        ---

        Создает новую нативную вершину через DLL и помечает объект как владельца указателя.
        """
        self.__ptr = LIB_MOON._Vertex_Init()
        self._owner = True

    def __str__(self) -> str:
        return f'Vertex2d<addr:{self.__ptr}>'

    def __repr__(self):
        return self.__str__()

    def __del__(self):
        if self.__ptr is not None and getattr(self, '_owner', False):
            LIB_MOON._Vertex_Delete(self.__ptr)

    def get_ptr(self) -> VertexPtr:
        """
        #### Возвращает нативный указатель вершины

        :Return:
        - `VertexPtr` - Указатель на нативную структуру вершины
        """
        return self.__ptr

    def set_ptr(self, ptr: VertexPtr) -> Self:
        """
        #### Устанавливает нативный указатель для этой обертки

        :Args:
        - ptr - Новый нативный указатель (`VertexPtr`).

        :Return:
        - `Vertex2d` - Текущий объект (для цепочки вызовов).

        :Note:
        - При замене указателя предыдущий нативный объект удаляется, если он принадлежал этой обертке.
        """
        if self.__ptr is not None:
            LIB_MOON._Vertex_Delete(self.__ptr)
        self.__ptr = ptr
        return self

    @property
    def position(self) -> Vec2f:
        x = LIB_MOON._Vertex_GetPositionX(self.__ptr)
        y = LIB_MOON._Vertex_GetPositionY(self.__ptr)
        return Vec2f(x, y)

    @position.setter
    def position(self, value: Vec2T) -> None:
        LIB_MOON._Vertex_SetPosition(self.__ptr, float(value.x), float(value.y))
        

    @property
    def color(self) -> Color:
        r = LIB_MOON._Vertex_GetColorR(self.__ptr)
        g = LIB_MOON._Vertex_GetColorG(self.__ptr)
        b = LIB_MOON._Vertex_GetColorB(self.__ptr)
        a = LIB_MOON._Vertex_GetColorA(self.__ptr)
        return Color(r, g, b, a)

    @color.setter
    def color(self, value: Color) -> None:
        r, g, b, a = value.rgba
        LIB_MOON._Vertex_SetColor(self.__ptr, r, g, b, a)

    @property
    def tex_coords(self) -> Vec2i:
        x = LIB_MOON._Vertex_GetTexCoordX(self.__ptr)
        y = LIB_MOON._Vertex_GetTexCoordY(self.__ptr)
        return Vec2i(x, y)

    @tex_coords.setter
    def tex_coords(self, value: Vec2i) -> None:
        LIB_MOON._Vertex_SetTexCoords(self.__ptr, value.x, value.y)

    def get_position_x(self) -> float:
        """
        #### Получить X координату позиции вершины

        :Return:
        - float - X координата в мировых/локальных единицах (зависит от использования)
        """
        return LIB_MOON._Vertex_GetPositionX(self.__ptr)

    def get_position_y(self) -> float:
        """
        #### Получить Y координату позиции вершины

        :Return:
        - float - Y координата в мировых/локальных единицах
        """
        return LIB_MOON._Vertex_GetPositionY(self.__ptr)

    def get_color_r(self) -> int:
        """
        #### Получить красную компоненту цвета вершины

        :Return:
        - int - Значение R в диапазоне 0-255
        """
        return LIB_MOON._Vertex_GetColorR(self.__ptr)

    def get_color_g(self) -> int:
        """
        #### Получить зеленую компоненту цвета вершины

        :Return:
        - int - Значение G в диапазоне 0-255
        """
        return LIB_MOON._Vertex_GetColorG(self.__ptr)

    def get_color_b(self) -> int:
        """
        #### Получить синюю компоненту цвета вершины

        :Return:
        - int - Значение B в диапазоне 0-255
        """
        return LIB_MOON._Vertex_GetColorB(self.__ptr)

    def get_color_a(self) -> int:
        """
        #### Получить альфа-компоненту цвета вершины

        :Return:
        - int - Значение A в диапазоне 0-255
        """
        return LIB_MOON._Vertex_GetColorA(self.__ptr)

    def get_tex_coord_x(self) -> float:
        """
        #### Получить X текстурной координаты вершины

        :Return:
        - float - Значение текстурной координаты X
        """
        return LIB_MOON._Vertex_GetTexCoordX(self.__ptr)

    def get_tex_coord_y(self) -> float:
        """
        #### Получить Y текстурной координаты вершины

        :Return:
        - float - Значение текстурной координаты Y
        """
        return LIB_MOON._Vertex_GetTexCoordY(self.__ptr)

    def copy(self) -> "Vertex2d":
        """
        #### Создает полную копию вершины

        ---

        :Return:
        - `Vertex2d` - Новый объект вершины с теми же позициями, цветом и текстурными координатами

        :Example:
        ```python
        v2 = v1.copy()
        ```
        """

        return Vertex2d.FromPositionColorAndTexCoords(
            self.position,
            self.color,
            self.tex_coords
        )

    def __eq__(self, other: object) -> bool:
        """
        #### Сравнение двух вершин на эквивалентность

        ---

        :Args:
        - other - Объект для сравнения

        :Return:
        - bool - True, если позиции, цвета и текстурные координаты равны
        """
        if not isinstance(other, Vertex2d):
            return False
        return (self.position == other.position and
                self.color == other.color and
                self.tex_coords == other.tex_coords)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

type NativeVertex2dPtr = Vertex2d

class VertexListTypes(Enum):
    Points = 0
    Lines = 1
    LineStrip = 2
    Triangles = 3
    TriangleStrip = 4
    TriangleFan = 5
    Quads = 6

class VertexList:
    def __init__(self, points_count: int = 0):
        """
        #### Инициализация `VertexList`

        ---

        :Args:
        - points_count - Начальное количество вершин (по умолчанию 0). Список будет сразу выделен под это количество.

        :Example:
        ```python
        vlist = VertexList(10)
        ```
        """
        self.__ptr = LIB_MOON._VertexArray_Init()
        LIB_MOON._VertexArray_Resize(self.__ptr, points_count)

    def resize(self, new_size: int):
        """
        #### Изменяет размер массива вершин

        :Args:
        - new_size - Новое количество вершин в массиве
        """
        LIB_MOON._VertexArray_Resize(self.__ptr, new_size)

    def get_ptr(self) -> VertexArrayPtr:
        """
        #### Возвращает нативный указатель на массив вершин

        :Return:
        - `VertexArrayPtr` - Указатель на внутреннюю нативную структуру массива вершин
        """
        return self.__ptr

    def __del__(self):
        LIB_MOON._VertexArray_Delete(self.__ptr)

    def set_primitive_type(self, primitive_type: VertexListTypes):
        """
        #### Устанавливает тип примитива для отрисовки

        ---

        :Args:
        - primitive_type - Значение `VertexListTypes`, определяющее, как будут интерпретироваться вершины (точки, линии, треугольники и т.д.)
        """
        LIB_MOON._VertexArray_SetPrimitiveType(self.__ptr, primitive_type.value)

    def clear(self):
        """
        #### Очищает массив вершин

        :Note:
        - После вызова массив будет пуст и его размер может быть сброшен нативной реализацией.
        """
        LIB_MOON._VertexArray_Clear(self.__ptr)

    def length(self) -> int:
        """
        #### Возвращает текущее количество вершин в массиве

        :Return:
        - int - Число вершин
        """
        return LIB_MOON._VertexArray_GetVertexCount(self.__ptr)

    def get_local_bound(self) -> tuple[Vec2f, Vec2f]:
        """
        #### Возвращает локальные границы массива вершин

        :Return:
        - tuple[Vector2f, Vector2f] - Кортеж `(position, size)`, где `position` — левый верхний угол, `size` — ширина/высота
        """
        return (
            Vec2f(LIB_MOON._VertexArray_GetBoundsPosX(self.__ptr), LIB_MOON._VertexArray_GetBoundsPosY(self.__ptr)),
            Vec2f(LIB_MOON._VertexArray_GetBoundsSizeW(self.__ptr), LIB_MOON._VertexArray_GetBoundsSizeH(self.__ptr))
        )

    def is_empty(self) -> bool:
        """
        #### Проверяет, пуст ли массив вершин

        :Return:
        - bool - True, если массив не содержит вершин
        """
        return LIB_MOON._VertexArray_IsEmpty(self.__ptr)

    def get(self, index: int) -> Vertex2d:
        """
        #### Получает вершину по индексу

        :Args:
        - index - Индекс вершины в массиве

        :Return:
        - `Vertex2d` - Обертка над нативной вершиной. Владелец указателя не передается (объект не удалит нативную память при сборке).
        """
        ptr = LIB_MOON._VertexArray_GetVertex(self.__ptr, index)
        vertex = Vertex2d.FromPtr(ptr)
        vertex._owner = False
        return vertex

    def remove(self, index: int):
        """
        #### Удаляет вершину по указанному индексу

        :Args:
        - index - Индекс удаляемой вершины
        """
        LIB_MOON._VertexArray_RemoveVertex(self.__ptr, index)

    def append(self, vertex: Vertex2d):
        """
        #### Добавляет вершину в конец массива

        :Args:
        - vertex - Экземпляр `Vertex2d` для добавления
        """
        LIB_MOON._VertexArray_AppendVertex(self.__ptr, vertex.get_ptr())

    def prepend(self, vertex: Vertex2d):
        """
        #### Вставляет вершину в начало массива

        :Args:
        - vertex - Экземпляр `Vertex2d` для вставки
        """
        LIB_MOON._VertexArray_PrependVertex(self.__ptr, vertex.get_ptr())

    def insert(self, index: int, vertex: Vertex2d):
        """
        #### Вставляет вершину в указанную позицию

        :Args:
        - index - Позиция для вставки
        - vertex - Экземпляр `Vertex2d` для вставки
        """
        LIB_MOON._VertexArray_InsertVertex(self.__ptr, index, vertex.get_ptr())

    def auto_prepend(self, vertex: Vertex2d):
        """
        #### Вставляет вершину в начало и автоматически подгоняет размер массива

        :Args:
        - vertex - Экземпляр `Vertex2d` для вставки
        """
        self.prepend(vertex)
        self.resize(self.length())

    def auto_append(self, vertex: Vertex2d):
        """
        #### Добавляет вершину в конец и автоматически подгоняет размер массива

        :Args:
        - vertex - Экземпляр `Vertex2d` для добавления
        """
        self.append(vertex)
        self.resize(self.length())

    def set_color(self, color: Color):
        """
        #### Устанавливает цвет для всех вершин массива

        :Args:
        - color - Экземпляр `Color`, который будет применен ко всем вершинам
        """
        LIB_MOON._VertexArray_SetColor(self.__ptr, color.r, color.g, color.b, color.a)
