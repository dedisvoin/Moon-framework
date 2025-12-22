"""
#### *Модуль работы с векторами в Moon*

---

##### Версия: 1.0.5

*Автор: Павлов Иван (Pavlov Ivan)*

*Лицензия: MIT*
##### Реализованно на 99%

---

✓ Двумерные векторы с плавающей точкой (Vector2f):
  - Математические операции (сложение, вычитание, умножение, деление)
  - Нормализация и вычисление длины
  - Поворот и работа с углами
  - Преобразование типов

✓ Двумерные целочисленные векторы (Vector2i):
  - Все основные математические операции
  - Преобразование в Vector2f
  - Оптимизированная работа с целыми числами

✓ Утилиты для работы с векторами:
  - Проверка параллельности и перпендикулярности
  - Вычисление углов между векторами
  - Скалярное и векторное произведение

---

:Requires:

• Python 3.8+

• Модуль math (стандартная библиотека)

• typing.Self для type hints

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

import math

from typing import Self
from random import uniform
from typing import Iterator, Sequence
from Moon.python.Types import Number


class Vec2f:
    """
    #### Класс двумерного вектора с плавающей точкой

    ---

    :Description:
    - Представляет точку или направление в 2D пространстве
    - Поддерживает все основные математические операции
    - Оптимизирован для работы с графикой и физикой

    ---

    :Features:
    - Математические операции (+, -, *, /, +=, -=, *=, /=)
    - Нормализация и работа с длиной вектора
    - Поворот на произвольный угол
    - Преобразование в целочисленный вектор
    """

    __slots__ = ("x", "y")

    @classmethod
    def one(cls) -> "Vec2f":
        """
        #### Создает единичный вектор (1, 1)

        ---

        :Returns:
        - Vector2f: Вектор с координатами (1, 1)

        ---

        :Example:
        ```python
        unit = Vector2f.one()
        print(unit)  # Vector2f(1.0, 1.0)
        ```
        """
        return Vec2f(1, 1)

    @classmethod
    def zero(cls) -> "Vec2f":
        """
        #### Создает нулевой вектор (0, 0)

        ---

        :Returns:
        - Vector2f: Вектор с координатами (0, 0)

        ---

        :Example:
        ```python
        origin = Vector2f.zero()
        print(origin)  # Vector2f(0.0, 0.0)
        ```
        """
        return Vec2f(0, 0)

    @classmethod
    def half(cls) -> "Vec2f":
        """
        #### Создает вектор (0.5, 0.5)

        ---
        :Returns:
        - Vector2f: Вектор с координатами (0.5, 0.5)

        ---

        :Example:
        ```python
        half_vec = Vector2f.half()
        print(half_vec)  # Vector2f(0.5, 0.5)
        ```
        """
        return Vec2f(0.5, 0.5)

    @classmethod
    def between(cls, point1: "Sequence[Number] | tuple[Number, Number] | Vec2f | Vec2i",
                     point2: "list[Number] | tuple[Number, Number] | Vec2f | Vec2i") -> "Vec2f":
        """
        #### Создает вектор направления между двумя точками

        ---

        :Args:
        - point1: Начальная точка [x, y] или (x, y) или Vector2f/Vector2i
        - point2: Конечная точка [x, y] или (x, y) или Vector2f/Vector2i

        ---

        :Returns:
        - Vector2f: Вектор от point1 к point2

        ---

        :Example:
        ```python
        direction = Vector2f.normal([0, 0], [3, 4])
        print(direction)  # Vector2f(3.0, 4.0)
        ```
        """
        if isinstance(point1, Vec2TT):
            point1 = point1.xy
        if isinstance(point2, Vec2TT):
            point2 = point2.xy
        return Vec2f(point2[0] - point1[0], point2[1] - point1[1])

    @classmethod
    def normal(cls, vector: "Vec2f") -> "NormVec2":
        """
        #### Создает нормальный (перпендикулярный) вектор

        ---

        :Args:
        - vector (Vector2f): Исходный вектор

        ---

        :Returns:
        - NormalisedVector: Нормализованный перпендикулярный вектор

        ---

        :Example:
        ```python
        vec = Vector2f(3, 4)
        normal = Vector2f.normal(vec)  # Перпендикулярный вектор
        """
        if vector.get_length() == 0:
            return Vec2f.zero()

        return vector.normalize().rotate(90)

    @classmethod
    def random(cls) -> "NormVec2":
        vector = Vec2f(1, 0).rotate_at(uniform(0, 360))
        return vector

    @classmethod
    def from_angle(cls, angle: Number, length: Number = 1) -> "Vec2f":
        """
        #### Создает вектор из угла и длины

        ---

        :Args:
        - angle (float | int): Угол в градусах
        - length (float | int): Длина вектора (по умолчанию 1)

        ---

        :Returns:
        - Vector2f: Вектор с заданным углом и длиной

        ---

        :Example:
        ```python
        vec = Vector2f.from_angle(45, 5)  # Вектор длиной 5 под углом 45 градусов
        ```
        """
        angle = -angle
        x = math.cos(angle * math.pi / 180) * length
        y = math.sin(angle * math.pi / 180) * length
        return Vec2f(x, y)

    @classmethod
    def from_array(cls, arr: "Sequence[Number] | tuple[Number, Number]") -> "Vec2f":
        """
        #### Создает вектор из массива или кортежа

        ---

        :Args:
        - arr (list | tuple): Список или кортеж с двумя элементами [x, y] или (x, y)

        ---

        :Returns:
        - Vector2f: Вектор с координатами из массива

        ---

        :Example:
        ```python
        vec = Vector2f.from_array([3.5, -2.1])
        print(vec)  # Vector2f(3.5, -2.1)
        ```
        """
        return Vec2f(float(arr[0]), float(arr[1]))

    def __init__(self, x: Number, y: Number) -> None:
        """
        #### Инициализация вектора с координатами

        ---

        :Args:
        - x (float | int): X координата
        - y (float | int): Y координата

        ---

        :Example:
        ```python
        vec = Vector2f(3.5, -2.1)
        ```
        """
        self.x = float(x)
        self.y = float(y)

    def to_int(self) -> "Vec2i":
        """
        #### Преобразует в целочисленный вектор

        ---

        :Returns:
        - Vector2i: Вектор с целочисленными координатами

        ---

        :Note:
        - Дробная часть отбрасывается (truncation)

        ---

        :Example:
        ```python
        vec = Vector2f(3.7, -2.3)
        int_vec = vec.to_int()  # Vector2i(3, -2)
        ```
        """
        return Vec2i(int(self.x), int(self.y))

    def as_tuple(self) -> tuple[float, float]:
        """
        #### Возвращает координаты как кортеж

        ---

        :Returns:
        - tuple[float, float]: Кортеж (x, y)
        """
        return (self.x, self.y)

    def as_list(self) -> list[float]:
        """
        #### Возвращает координаты как список

        ---

        :Returns:
        - list[float]: Список [x, y]
        """
        return [self.x, self.y]

    def scale(self, factor: Number) -> Self:
        """
        #### Масштабирует вектор на заданный коэффициент

        ---

        :Args:
        - factor (float | int): Коэффициент масштабирования

        ---

        :Returns:
        - Self: Возвращает self для цепочки вызовов

        ---

        :Example:
        ```python
        vec = Vector2f(3, 4)
        vec.scale(2)  # vec теперь (6, 8)
        ```
        """
        self.x *= factor
        self.y *= factor
        return self

    def set_scale(self, factor: Number) -> Self:
        """
        #### Устанавливает масштаб вектора на заданный коэффициент

        ---

        :Args:
        - factor (float | int): Новый коэффициент масштабирования

        ---

        :Returns:
        - Self: Возвращает self для цепочки вызовов

        ---

        :Example:
        ```python
        vec = Vector2f(3, 4)  # длина 5
        vec.set_scale(2)      # теперь (1.2, 1.6) длина 2
        ```
        """
        length = self.get_length()
        if length != 0:
            self.x = self.x / length * factor
            self.y = self.y / length * factor
        return self

    @property
    def xy(self) -> tuple[float, float]:
        """
        #### Возвращает координаты как кортеж

        ---

        :Returns:
        - tuple[float, float]: Кортеж (x, y)
        """
        return (self.x, self.y)

    @xy.setter
    def xy(self, value: tuple[Number, Number] | Sequence[Number]) -> None:
        """
        #### Устанавливает координаты из кортежа

        ---

        :Args:
        - value: Кортеж (x, y) с новыми координатами
        """
        self.x = float(value[0])
        self.y = float(value[1])

    def copy(self) -> "Vec2f":
        """
        #### Создает копию вектора

        ---

        :Returns:
        - Vector2f: Новый вектор с теми же координатами

        ---

        :Example:
        ```python
        original = Vector2f(1, 2)
        copy = original.copy()
        ```
        """
        return Vec2f(self.x, self.y)

    def reflect(self, normal: "Vec2f") -> "Vec2f":
        """
        #### Отражает вектор относительно нормали

        ---

        :Args:
        - normal (Vector2f): Нормализованный вектор нормали

        ---

        :Returns:
        - Vector2f: Отраженный вектор

        ---

        :Example:
        ```python
        incident = Vector2f(1, -1)
        normal = Vector2f(0, 1).normalize()
        reflected = incident.reflect(normal)
        ```
        """
        dot_product = self.x * normal.x + self.y * normal.y
        return Vec2f(self.x - 2 * dot_product * normal.x,
                        self.y - 2 * dot_product * normal.y)

    def reflect_at_x(self) -> Self:
        """
        #### Отражает данный вектор по оси X

        ---

        :Returns:
        - Self: Возвращает self для цепочки вызовов
        ---

        :Example:
        ```python
        vec = Vector2f(3, 4)
        reflected = vec.reflect_x()  # Vector2f(3, -4)
        ```
        """
        self.y = -self.y
        return self

    def reflect_at_y(self) -> Self:
        """
        #### Отражает вектор по оси Y

        ---

        :Returns:
        - Self: Возвращает self для цепочки вызовов

        ---

        :Example:
        ```python
        vec = Vector2f(3, 4)
        reflected = vec.reflect_y()  # Vector2f(-3, 4)
        ```
        """
        self.x = -self.x
        return self

    def get_length(self) -> float:
        """
        #### Вычисляет длину (модуль) вектора

        ---

        :Returns:
        - float: Длина вектора (√(x² + y²))

        ---

        :Example:
        ```python
        vec = Vector2f(3, 4)
        length = vec.get_length()  # 5.0
        ```
        """
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def get_length_squared(self) -> float:
        """
        #### Вычисляет квадрат длины вектора

        ---

        :Returns:
        - float: Квадрат длины вектора (x² + y²)

        ---

        :Example:
        ```python
        vec = Vector2f(3, 4)
        length_sq = vec.get_length_squared()  # 25.0
        ```
        """
        return self.x ** 2 + self.y ** 2

    def normalize_at(self) -> Self:
        """
        #### Нормализует вектор на месте (изменяет текущий)

        ---

        :Description:
        - Приводит длину вектора к 1, сохраняя направление
        - Изменяет текущий объект

        ---

        :Returns:
        - Self: Возвращает self для цепочки вызовов

        ---

        :Example:
        ```python
        vec = Vector2f(3, 4)
        vec.normalize_at()  # vec теперь (0.6, 0.8)
        ```
        """
        length = self.get_length()
        if length != 0:
            self.x /= length
            self.y /= length
        return self

    def normalize(self) -> "Vec2f":
        """
        #### Возвращает нормализованную копию вектора

        ---

        :Description:
        - Создает новый вектор единичной длины
        - Исходный вектор не изменяется

        ---

        :Returns:
        - Vector2f: Новый нормализованный вектор

        ---

        :Example:
        ```python
        vec = Vector2f(3, 4)
        normalized = vec.normalize()  # (0.6, 0.8)
        # vec остается (3, 4)
        ```
        """
        length = self.get_length()
        if length != 0:
            return Vec2f(self.x / length, self.y / length)
        return Vec2f(self.x, self.y)

    def rotate_at(self, angle: float | int) -> Self:
        """
        #### Поворачивает вектор на месте

        ---

        :Args:
        - angle (float | int): Угол поворота в градусах

        ---

        :Returns:
        - Self: Возвращает self для цепочки вызовов

        ---

        :Example:
        ```python
        vec = Vector2f(1, 0)
        vec.rotate_at(90)  # vec теперь (0, 1)
        ```
        """
        angle = -math.radians(angle)
        cos = math.cos(angle)
        sin = math.sin(angle)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y
        return self

    def rotate(self, angle: float | int) -> "Vec2f":
        """
        #### Возвращает повернутую копию вектора

        ---

        :Args:
        - angle (float | int): Угол поворота в градусах

        ---

        :Returns:
        - Vector2f: Новый повернутый вектор

        ---

        :Example:
        ```python
        vec = Vector2f(1, 0)
        rotated = vec.rotate(90)  # (0, 1)
        # vec остается (1, 0)
        ```
        """
        angle = -math.radians(angle)
        cos = math.cos(angle)
        sin = math.sin(angle)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vec2f(x, y)

    def get_angle(self) -> float:
        """
        #### Возвращает угол вектора в градусах

        ---

        :Returns:
        - float: Угол от 0 до 360 градусов

        ---

        :Example:
        ```python
        vec = Vector2f(1, 1)
        angle = vec.get_angle()  # 45.0
        ```
        """
        angle = -math.atan2(self.y, self.x) * 180 / math.pi
        return angle if angle >= 0 else angle + 360

    def set_angle(self, angle: float | int) -> Self:
        """
        #### Устанавливает угол вектора, сохраняя длину

        ---

        :Args:
        - angle (float | int): Новый угол в градусах

        ---

        :Returns:
        - Self: Возвращает self для цепочки вызовов

        ---

        :Example:
        ```python
        vec = Vector2f(5, 0)
        vec.set_angle(90)  # vec теперь (0, 5)
        ```
        """
        length = self.get_length()
        angle = -angle
        self.x = math.cos(angle * math.pi / 180) * length
        self.y = math.sin(angle * math.pi / 180) * length
        return self

    def set_length(self, lenght: float | int) -> Self:
        """
        #### Устанавливает длину вектора, сохраняя направление

        ---

        :Args:
        - lenght (float | int): Новая длина вектора

        ---

        :Returns:
        - Self: Возвращает self для цепочки вызовов

        ---

        :Example:
        ```python
        vec = Vector2f(3, 4)  # длина 5
        vec.set_lenght(10)    # теперь (6, 8)
        ```
        """
        length = self.get_length()
        if length != 0:
            self.x *= lenght / length
            self.y *= lenght / length
        return self

    def is_normalized(self) -> bool:
        """
        #### Проверяет, является ли вектор нормализованным

        ---

        :Returns:
        - bool: True если длина равна 1

        ---

        :Example:
        ```python
        vec = Vector2f(0.6, 0.8)
        print(vec.is_normalized())  # True
        ```
        """
        return self.get_length() == 1

    def is_zero(self) -> bool:
        """
        #### Проверяет, является ли вектор нулевым

        ---

        :Returns:
        - bool: True если обе координаты равны 0

        ---

        :Example:
        ```python
        vec = Vector2f.zero()
        print(vec.is_zero())  # True
        ```
        """
        return self.x == 0 and self.y == 0

    def __iter__(self):
        return iter((self.x, self.y))

    def __copy__(self) -> "Vec2f":
        return self.copy()

    def __repr__(self) -> str:
        return f"Vec2f({self.x}, {self.y})"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: "Vec2T | object") -> bool:
        if isinstance(other, Vec2TT):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other: "Vec2T | object") -> bool:
        return not self.__eq__(other)

    def __neg__(self) -> 'Vec2f':
        return Vec2f(-self.x, -self.y)

    def __abs__(self) -> 'Vec2f':
        return Vec2f(abs(self.x), abs(self.y))

    def __add__(self, other: "Vec2f | Vec2i") -> 'Vec2f':
        return Vec2f(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2f | Vec2i") -> 'Vec2f':
        return Vec2f(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: "Number | Vec2T") -> 'Vec2f':
        if isinstance(scalar, Vec2TT):
            return Vec2f(self.x * scalar.x, self.y * scalar.y)
        return Vec2f(self.x * scalar, self.y * scalar)

    def __pow__(self, scalar: "Number | Vec2T") -> 'Vec2f':
        if isinstance(scalar, Vec2TT):
            return Vec2f(self.x ** scalar.x, self.y ** scalar.y)
        return Vec2f(self.x ** scalar, self.y ** scalar)

    def __truediv__(self, scalar: "Number | Vec2T") -> 'Vec2f':
        if isinstance(scalar, Vec2TT):
            return Vec2f(self.x / scalar.x, self.y / scalar.y)
        return Vec2f(self.x / scalar, self.y / scalar)
    
    def __div__(self, scalar: "Number | Vec2T") -> 'Vec2i':
        if isinstance(scalar, Vec2TT):
            return Vec2i(self.x // scalar.x, self.y // scalar.y)
        return Vec2i(self.x // scalar, self.y // scalar)

    def __iadd__(self, other: "Vec2T") -> Self:
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: "Vec2T") -> Self:
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, scalar: "Number | Vec2T") -> Self:
        if isinstance(scalar, Vec2TT):
            self.x *= scalar.x
            self.y *= scalar.y
        else:
            self.x *= scalar
            self.y *= scalar
        return self

    def __itruediv__(self, scalar: "Number | Vec2T") -> Self:
        if isinstance(scalar, Vec2TT):
            self.x /= scalar.x
            self.y /= scalar.y
        else:
            self.x /= scalar
            self.y /= scalar
        return self
    
    def __idiv__(self, scalar: "Number | Vec2T") -> Self:
        if isinstance(scalar, Vec2TT):
            self.x //= scalar.x
            self.y //= scalar.y
        else:
            self.x //= scalar
            self.y //= scalar
        return self

# Тип нормализованного вектора == +
NormVec2 = Vec2f                  #
# =============================== +

class Vec2i(object):
    """
    #### Класс двумерного вектора с целочисленными координатами

    ---

    :Description:
    - Представляет точку или направление в 2D пространстве с целыми координатами
    - Оптимизирован для работы с пиксельными координатами
    - Поддерживает все основные математические операции

    ---

    :Features:
    - Математические операции с целыми числами
    - Преобразование в Vector2f
    - Защищенные координаты через свойства
    """

    __slots__ = ("__x", "__y")

    def __init__(self, x: int | float, y: int | float):
        """
        #### Инициализация целочисленного вектора

        ---

        :Args:
        - x (int | float): X координата (будет приведена к int)
        - y (int | float): Y координата (будет приведена к int)

        ---

        :Example:
        ```python
        vec = Vector2i(3.7, -2.3)  # Vector2i(3, -2)
        ```
        """
        self.__x = int(x)
        self.__y = int(y)

    @classmethod
    def zero(cls) -> "Vec2i":
        return Vec2i(0, 0)

    @classmethod
    def one(cls) -> "Vec2i":
        return Vec2i(1, 1)

    def as_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    def as_list(self) -> list[int]:
        return [self.x, self.y]

    def to_float(self) -> Vec2f:
        """
        #### Преобразует в вектор с плавающей точкой

        ---

        :Returns:
        - Vector2f: Вектор с координатами float

        ---

        :Example:
        ```python
        int_vec = Vector2i(3, -2)
        float_vec = int_vec.to_float()  # Vector2f(3.0, -2.0)
        ```
        """
        return Vec2f(float(self.__x), float(self.__y))

    def get_angle(self) -> float:
        """
        #### Возвращает угол вектора в градусах

        ---

        :Returns:
        - float: Угол от 0 до 360 градусов

        ---

        :Example:
        ```python
        vec = Vector2f(1, 1)
        angle = vec.get_angle()  # 45.0
        ```
        """
        angle = -math.atan2(self.y, self.x) * 180 / math.pi
        return angle if angle >= 0 else angle + 360

    def get_length(self) -> float:
        """
        #### Вычисляет длину вектора

        ---

        :Returns:
        - float: Длина вектора (√(x² + y²))

        ---

        :Example:
        ```python
        vec = Vector2i(3, 4)
        length = vec.get_lenght()  # 5.0
        ```
        """
        return math.sqrt(self.__x * self.__x + self.__y * self.__y)

    @property
    def x(self) -> int:
        return int(self.__x)

    @property
    def y(self) -> int:
        return int(self.__y)

    @x.setter
    def x(self, value: int | float) -> None:
        self.__x = int(value)

    @y.setter
    def y(self, value: int | float) -> None:
        self.__y = int(value)

    @property
    def xy(self) -> tuple[int, int]:
        return (int(self.__x), int(self.__y))

    @xy.setter
    def xy(self, xy: tuple[int | float, int | float]) -> None:
        self.__x = int(xy[0])
        self.__y = int(xy[1])

    def __iter__(self) -> Iterator[int | float]:
        return iter((self.__x, self.__y))

    def __repr__(self) -> str:
        return f"Vector2i({self.__x}, {self.__y})"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2i):
            return False
        return self.__x == other.x and self.__y == other.y

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Vec2i):
            return True
        return not self.__eq__(other)

    def __neg__(self) -> "Vec2i":
        return Vec2i(-self.__x, -self.__y)

    def __abs__(self) -> "Vec2i":
        return Vec2i(abs(self.__x), abs(self.__y))

    def __add__(self, other: "Vec2T") -> "Vec2T":
        if isinstance(other, Vec2f):
            return Vec2f(self.__x + other.x, self.__y + other.y)
        return Vec2i(self.__x + other.x, self.__y + other.y)

    def __sub__(self, other: "Vec2T") -> "Vec2T":
        if isinstance(other, Vec2f):
            return Vec2f(self.__x - other.x, self.__y - other.y)
        return Vec2i(self.__x - other.x, self.__y - other.y)

    def __mul__(self, scalar: "int | float | Vec2T") -> "Vec2T":
        if isinstance(scalar, Vec2i):
            return Vec2i(self.__x * scalar.x, self.__y * scalar.y)
        if isinstance(scalar, Vec2f):
            return Vec2f(self.__x * scalar.x, self.__y * scalar.y)
        if isinstance(scalar, int):
            return Vec2i(self.__x * scalar, self.__y * scalar)
        if isinstance(scalar, float):
            return Vec2f(self.__x * scalar, self.__y * scalar)

    def __truediv__(self, scalar: "int | float | Vec2T") -> "Vec2T":
        if isinstance(scalar, Vec2i):
            return Vec2i(self.__x / scalar.x, self.__y / scalar.y)
        if isinstance(scalar, Vec2f):
            return Vec2f(self.__x / scalar.x, self.__y / scalar.y)
        if isinstance(scalar, int):
            return Vec2i(self.__x / scalar, self.__y / scalar)
        if isinstance(scalar, float):
            return Vec2f(self.__x / scalar, self.__y / scalar)

    def __iadd__(self, other: "Vec2T") -> "Vec2T":
        if isinstance(other, Vec2f):
            return Vec2f(self.__x + other.x, self.__y + other.y)
        self.__x += other.x
        self.__y += other.y
        return self

    def __isub__(self, other: "Vec2T") -> "Vec2T":
        if isinstance(other, Vec2f):
            return Vec2f(self.__x - other.x, self.__y - other.y)
        self.__x -= other.x
        self.__y -= other.y
        return self

    def __imul__(self, scalar: "int | float | Vec2T") -> "Vec2T":
        if isinstance(scalar, Vec2i):
            self.__x *= scalar.x
            self.__y *= scalar.y
        elif isinstance(scalar, Vec2f):
            return Vec2f(self.__x * scalar.x, self.__y * scalar.y)
        elif isinstance(scalar, int):
            self.__x *= scalar
            self.__y *= scalar
        elif isinstance(scalar, float):
            return Vec2f(self.__x * scalar, self.__y * scalar)
        return self

    def __itruediv__(self, scalar: "int | float | Vec2T") -> "Vec2T":
        if isinstance(scalar, Vec2i):
            self.__x /= scalar.x
            self.__y /= scalar.y
            self.__x = int(self.__x)
            self.__y = int(self.__y)
        elif isinstance(scalar, Vec2f):
            return Vec2f(self.__x / scalar.x, self.__y / scalar.y)
        elif isinstance(scalar, int):
            self.__x //= scalar
            self.__y //= scalar
            self.__x = int(self.__x)
            self.__y = int(self.__y)
        elif isinstance(scalar, float):
            return Vec2f(self.__x / scalar, self.__y / scalar)
        return self

    
def to_vector_2f(data: tuple[Number, Number] | list[Number]) -> Vec2f:
    """
    Преобразует данные в вектор 2D с плавающей точкой.
    """
    if isinstance(data, tuple):
        return Vec2f(data[0], data[1])
    elif isinstance(data, list):
        return Vec2f(data[0], data[1])
    else:
        raise TypeError("Invalid data type")

def to_vector_2i(data: tuple[Number, Number] | list[Number]) -> Vec2i:
    """
    Преобразует данные в вектор 2D с целочисленными координатами.
    """
    if isinstance(data, tuple):
        return Vec2i(data[0], data[1])
    elif isinstance(data, list):
        return Vec2i(data[0], data[1])
    else:
        raise TypeError("Invalid data type")

def is_parallel(v1: "Vec2T", v2: "Vec2T") -> bool:
    """
    #### Проверяет параллельность двух векторов

    ---

    :Args:
    - v1 (VectorType): Первый вектор
    - v2 (VectorType): Второй вектор

    ---

    :Returns:
    - bool: True если векторы параллельны

    ---

    :Example:
    ```python
    v1 = Vector2f(2, 4)
    v2 = Vector2f(1, 2)
    print(is_parallel(v1, v2))  # True
    ```
    """
    return v1.x * v2.y == v1.y * v2.x

def is_perpendicular(v1: "Vec2T", v2: "Vec2T") -> bool:
    """
    #### Проверяет перпендикулярность двух векторов

    ---

    :Args:
    - v1 (VectorType): Первый вектор
    - v2 (VectorType): Второй вектор

    ---

    :Returns:
    - bool: True если векторы перпендикулярны

    ---

    :Example:
    ```python
    v1 = Vector2f(1, 0)
    v2 = Vector2f(0, 1)
    print(is_perpendicular(v1, v2))  # True
    ```
    """
    return v1.x * v2.x + v1.y * v2.y == 0

def angle_between(v1: "Vec2T", v2: "Vec2T") -> float:
    """
    #### Вычисляет угол между двумя векторами

    ---

    :Args:
    - v1 (VectorType): Первый вектор
    - v2 (VectorType): Второй вектор

    ---

    :Returns:
    - float: Угол в градусах (0-180)

    ---

    :Example:
    ```python
    v1 = Vector2f(1, 0)
    v2 = Vector2f(0, 1)
    angle = angle_between(v1, v2)  # 90.0
    ```
    """
    return math.degrees(math.acos((v1.x * v2.x + v1.y * v2.y) / (v1.get_length() * v2.get_length())))

def cross(v1: "Vec2T", v2: "Vec2T") -> float:
    """
    #### Вычисляет векторное произведение (в 2D - скаляр)

    ---

    :Args:
    - v1 (VectorType): Первый вектор
    - v2 (VectorType): Второй вектор

    ---

    :Returns:
    - float: Результат векторного произведения

    ---

    :Note:
    - Положительное значение означает поворот против часовой стрелки
    - Отрицательное - по часовой стрелке

    ---

    :Game Applications:
    - Определение стороны поворота (влево/вправо) для AI навигации
    - Проверка пересечения линий и коллизий
    - Вычисление площади треугольников и многоугольников
    - Определение направления вращения объектов
    - Алгоритмы поиска пути и обхода препятствий

    ---

    :Example:
    ```python
    # Определить, поворачивает ли игрок влево или вправо
    player_forward = Vector2f(1, 0)
    to_target = Vector2f(0, 1)
    turn_direction = cross(player_forward, to_target)  # 1.0 (влево)

    # Проверка пересечения отрезков для коллизий
    if cross(line1_dir, line2_dir) != 0:
        print("Линии пересекаются")
    ```
    """
    return v1.x * v2.y - v1.y * v2.x

def dot(v1: "Vec2T", v2: "Vec2T") -> float:
    """
    #### Вычисляет скалярное произведение векторов

    ---

    :Args:
    - v1 (VectorType): Первый вектор
    - v2 (VectorType): Второй вектор

    ---

    :Returns:
    - float: Результат скалярного произведения

    ---

    :Note:
    - Используется для определения угла между векторами
    - Равно 0 для перпендикулярных векторов
    - Положительное значение - острый угол, отрицательное - тупой

    ---

    :Game Applications:
    - Определение поля зрения (FOV) для AI и камер
    - Проверка направления взгляда персонажа на цель
    - Вычисление освещения (угол между светом и поверхностью)
    - Определение "за спиной" или "впереди" для стелс-механик
    - Расчет отражения снарядов и физических объектов
    - Оптимизация рендеринга (culling невидимых объектов)

    ---

    :Example:
    ```python
    # Проверить, видит ли игрок цель (в пределах 90° конуса)
    player_forward = Vector2f(1, 0).normalize()
    to_target = (target_pos - player_pos).normalize()
    visibility = dot(player_forward, to_target)
    if visibility > 0.7:  # cos(45°) ≈ 0.7
        print("Цель в поле зрения")

    # Определить, движется ли объект к игроку или от него
    to_player = (player_pos - enemy_pos).normalize()
    enemy_velocity_normalized = enemy_velocity.normalize()
    approaching = dot(to_player, enemy_velocity_normalized) > 0
    ```
    """
    return v1.x * v2.x + v1.y * v2.y


# Union подобный веткорый тип ========= +
type Vec2T = Vec2f | Vec2i              #
# ===================================== +

# Кортеж из двух типов векторов =================== +
Vec2TT: tuple[Vec2f, Vec2i] = (Vec2f, Vec2i)   #
# ================================================= +

class Vec3f(object):
    def __init__(self, x: Number, y: Number, z: Number):
        self.__x = x
        self.__y = y
        self.__z = z

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def z(self) -> float:
        return self.__z

    @x.setter
    def x(self, x: float) -> None:
        self.__x = x

    @y.setter
    def y(self, y: float) -> None:
        self.__y = y

    @z.setter
    def z(self, z: float) -> None:
        self.__z = z

    @property
    def xyz(self) -> tuple[float, float, float]:
        return (self.__x, self.__y, self.__z)

    @property
    def rgb(self) -> tuple[float, float, float]:
        return (self.__x, self.__y, self.__z)

    @property
    def xy(self) -> tuple[float, float]:
        return (self.__x, self.__y)

    @property
    def xz(self) -> tuple[float, float]:
        return (self.__x, self.__z)

    @property
    def yz(self) -> tuple[float, float]:
        return (self.__y, self.__z)

    def length(self) -> float:
        return math.sqrt(self.__x**2 + self.__y**2 + self.__z**2)

    def dot(self, other: "Vec3f"):
        """Вычисляет скалярное произведение двух векторов"""
        return (self.__x * other.__x + self.__y * other.__y + self.__z * other.__z)

    def cross(self, other: "Vec3f"):
        """Вычисляет векторное произведение двух векторов"""
        return Vec3f(self.__y * other.__z - self.__z * other.__y,
                        self.__z * other.__x - self.__x * other.__z,
                        self.__x * other.__y - self.__y * other.__x)

    def normalize(self) -> "Vec3f":
        length = self.length()
        if length == 0:
            return Vec3f(0, 0, 0)
        return Vec3f(self.__x / length, self.__y / length, self.__z / length)

    def normalize_at(self) -> Self:
        length = self.length()
        self.__x = self.__x / length
        self.__y = self.__y / length
        self.__z = self.__z / length
        return self

    def rotate(self, angle_vector: "Vec3f") -> "Vec3f":
        """
        Вращает вектор по осям x, y, z
        """
        x, y, z = self.__x, self.__y, self.__z
        a, b, c = angle_vector.__x, angle_vector.__y, angle_vector.__z
        cos_a, sin_a = math.cos(a), math.sin(a)
        cos_b, sin_b = math.cos(b), math.sin(b)
        cos_c, sin_c = math.cos(c), math.sin(c)
        x = x * cos_a * cos_b - y * sin_a * cos_b + z * sin_b
        y = x * cos_a * sin_b + y * sin_a * sin_b + z * cos_b
        z = -x * sin_a + y * cos_a
        return Vec3f(x, y, z)

    def rotate_at(self, angle_vector: "Vec3f") -> Self:
        """
        Вращает вектор по осям x, y, z
        """
        x, y, z = self.__x, self.__y, self.__z
        a, b, c = angle_vector.__x, angle_vector.__y, angle_vector.__z
        cos_a, sin_a = math.cos(a), math.sin(a)
        cos_b, sin_b = math.cos(b), math.sin(b)
        cos_c, sin_c = math.cos(c), math.sin(c)
        x = x * cos_a * cos_b - y * sin_a * cos_b + z * sin_b
        y = x * cos_a * sin_b + y * sin_a * sin_b + z * cos_b
        z = -x * sin_a + y * cos_a
        self.__x = x
        self.__y = y
        self.__z = z
        return self

    def __str__(self):
        return f"({self.__x}, {self.__y}, {self.__z})"

    def __repr__(self):
        return f"Vector3f({self.__x}, {self.__y}, {self.__z})"

    def __add__(self, other: "Vec3f") -> "Vec3f":
        return Vec3f(self.__x + other.__x, self.__y + other.__y, self.__z + other.__z)

    def __sub__(self, other: "Vec3f") -> "Vec3f":
        return Vec3f(self.__x - other.__x, self.__y - other.__y, self.__z - other.__z)

    def __mul__(self, other: float) -> "Vec3f":
        return Vec3f(self.__x * other, self.__y * other, self.__z * other)

    def __truediv__(self, other: float) -> "Vec3f":
        return Vec3f(self.__x / other, self.__y / other, self.__z / other)

    def __floordiv__(self, other: float) -> "Vec3f":
        return Vec3f(self.__x // other, self.__y // other, self.__z // other)

    def __mod__(self, other: float) -> "Vec3f":
        return Vec3f(self.__x % other, self.__y % other, self.__z % other)

    def __abs__(self) -> "Vec3f":
        return Vec3f(abs(self.__x), abs(self.__y), abs(self.__z))
