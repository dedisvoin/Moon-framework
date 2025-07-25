"""
Мощный модуль для работы с 2D векторами в PySGL
Автор: Павлов Иван (Pavlov Ivan)
Версия: 1.2.0
Дата последнего обновления: 2025-07-02
Лицензия: MIT
### Реализованно на 98% 

== Описание ===================================================

Профессиональный инструмент для:

- Манипуляций с 2D векторами (целочисленными и с плавающей точкой)

- Векторных математических операций

- Геометрических преобразований

- Работы с координатами и направлениями

- Физических расчетов и игровой логики

== Основные возможности ==========================================

✓ Базовый класс BaseVector2 с общими операциями

✓ Два специализированных класса: Vector2f и Vector2i

✓ 50+ методов работы с векторами

✓ Полный набор векторных операций (сложение, умножение и др.)

✓ Геометрические операции (поворот, нормализация, проекция)

✓ Поддержка как точных (float), так и дискретных (int) вычислений

✓ Оптимизированная работа с памятью (__slots__)

✓ Подробная документация и аннотации типов


== Примеры использования =========================================

from vector2d import Vector2f, Vector2i

# Создание векторов
v1 = Vector2f(1.5, 2.5)
v2 = Vector2i(10, 20)

# Векторные операции
sum_vec = v1 + Vector2f(3.0, 4.0)
rotated = v1.rotated(math.pi/2)

# Работа с направлениями
direction = Vector2f.from_angle(math.pi/4, length=5.0)

== Требования ====================================================

• Python 3.8+


== Ссылки ==

TODO добавить ссылки

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


from typing import Generator, Tuple, List, Union, TypeVar
from random import uniform, randint
from copy import copy
import math

# Типы для аннотаций
T = TypeVar('T', float, int)                               # Обобщенный тип для координат (float или int)
Position = Union[Tuple[T, T], List[T]]                     # Тип для позиции (кортеж или список)
VectorType = TypeVar('VectorType', bound='BaseVector2')    # Тип для наследников BaseVector2

class BaseVector2:
    """
    Базовый класс для 2D векторов с общими математическими операциями.
    
    Атрибуты:
        x (T): Координата X вектора
        y (T): Координата Y вектора
    """

    # Константы для сравнения чисел с плавающей точкой
    EPSILON = 1e-9  # Погрешность для сравнения float
    EPSILON_SQ = 1e-18  # Квадрат EPSILON для сравнения квадратов длин
    
    __slots__ = ('x', 'y')  # Оптимизация памяти - уменьшает объем памяти для хранения объекта
    
    def __init__(self, x: T, y: T):
        """
        Инициализация вектора.
        
        Аргументы:
            x (T): Координата X
            y (T): Координата Y
        """
        self.x = x
        self.y = y
    
    # ============== Фабричные методы (методы класса) ==============
    @classmethod
    def zero(cls) -> VectorType:
        """Возвращает нулевой вектор (0, 0)"""
        return cls(0, 0)
    
    @classmethod
    def one(cls) -> VectorType:
        """Возвращает вектор (1, 1)"""
        return cls(1, 1)
    
    @classmethod
    def up(cls) -> VectorType:
        """Возвращает единичный вектор направления вверх (0, 1)"""
        return cls(0, 1)
    
    @classmethod
    def down(cls) -> VectorType:
        """Возвращает единичный вектор направления вниз (0, -1)"""
        return cls(0, -1)
    
    @classmethod
    def left(cls) -> VectorType:
        """Возвращает единичный вектор направления влево (-1, 0)"""
        return cls(-1, 0)
    
    @classmethod
    def right(cls) -> VectorType:
        """Возвращает единичный вектор направления вправо (1, 0)"""
        return cls(1, 0)
    
    # ============== Основные операции ==============
    def copy(self) -> VectorType:
        """Возвращает полную копию вектора"""
        return self.__class__(copy(self.x), copy(self.y))
    
    def __eq__(self, other: object) -> bool:
        """
        Проверка на равенство с другим вектором (с учетом погрешности EPSILON).
        
        Аргументы:
            other (object): Объект для сравнения
            
        Возвращает:
            bool: True если векторы равны (с учетом погрешности)
        """
        if not isinstance(other, BaseVector2):
            return False
        return (abs(self.x - other.x) < self.EPSILON and 
                abs(self.y - other.y) < self.EPSILON)
    
    def approx_equal(self, other: 'BaseVector2', epsilon: float | None = None) -> bool:
        """
        Сравнение векторов с заданной точностью.
        
        Аргументы:
            other (BaseVector2): Вектор для сравнения
            epsilon (float, optional): Погрешность сравнения. По умолчанию self.EPSILON
            
        Возвращает:
            bool: True если векторы равны с заданной точностью
        """
        if epsilon is None:
            epsilon = self.EPSILON
        return (abs(self.x - other.x) < epsilon and 
                abs(self.y - other.y) < epsilon)
    
    def approx_zero(self, epsilon: float | None = None) -> bool:
        """
        Проверка, является ли вектор приблизительно нулевым.
        
        Аргументы:
            epsilon (float, optional): Погрешность сравнения. По умолчанию self.EPSILON
            
        Возвращает:
            bool: True если обе координаты близки к нулю
        """
        if epsilon is None:
            epsilon = self.EPSILON
        return abs(self.x) < epsilon and abs(self.y) < epsilon
    
    def __ne__(self, other: object) -> bool:
        """Проверка на неравенство векторов"""
        return not (self == other)
    
    def __add__(self, other: VectorType) -> VectorType:
        """Сложение двух векторов (поэлементно)"""
        return self.__class__(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: VectorType) -> VectorType:
        """Вычитание векторов (поэлементно)"""
        return self.__class__(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other: Union[T, VectorType]) -> VectorType:
        """
        Умножение вектора на скаляр или поэлементное умножение на другой вектор.
        
        Аргументы:
            other (T | VectorType): Число или вектор для умножения
            
        Возвращает:
            VectorType: Новый вектор-результат
        """
        if isinstance(other, BaseVector2):
            return self.__class__(self.x * other.x, self.y * other.y)
        return self.__class__(self.x * other, self.y * other)
    
    def __rmul__(self, other: Union[T, VectorType]) -> VectorType:
        """Умножение справа (аналогично __mul__)"""
        return self.__mul__(other)
    
    def __imul__(self, other: Union[T, VectorType]) -> VectorType:
        """
        Комбинированное умножение с присваиванием (in-place).
        
        Аргументы:
            other (T | VectorType): Число или вектор для умножения
            
        Возвращает:
            VectorType: Измененный текущий вектор
        """
        if isinstance(other, BaseVector2):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self
    
    def __truediv__(self, scalar: float) -> 'Vector2f':
        """Деление вектора на скаляр (возвращает Vector2f)"""
        return Vector2f(self.x / scalar, self.y / scalar)
    
    def __floordiv__(self, scalar: int) -> 'Vector2i':
        """Целочисленное деление вектора на скаляр (возвращает Vector2i)"""
        return Vector2i(self.x // scalar, self.y // scalar)
    
    def __neg__(self) -> VectorType:
        """Возвращает вектор с противоположным направлением"""
        return self.__class__(-self.x, -self.y)
    
    def __abs__(self) -> float:
        """Возвращает длину (модуль) вектора"""
        return math.hypot(self.x, self.y)
    
    def __iter__(self) -> Generator[T, T]:
        """Итератор по координатам вектора (позволяет распаковывать как x, y = vector)"""
        yield self.x
        yield self.y

    def __getitem__(self, index: int) -> T:
        """
        Доступ к координатам по индексу (0 = x, 1 = y).
        
        Аргументы:
            index (int): Индекс координаты (0 или 1)
            
        Возвращает:
            T: Значение координаты
            
        Выбрасывает:
            IndexError: Если индекс не 0 или 1
        """
        if index == 0: return self.x
        elif index == 1: return self.y
        else: raise IndexError("Vector index out of range")
    
    # ============== Векторные операции ==============
    def project(self, other: 'Vector2f') -> 'Vector2f':
        """
        Проекция этого вектора на другой вектор.
        
        Аргументы:
            other (Vector2f): Вектор, на который производится проекция
            
        Возвращает:
            Vector2f: Вектор проекции
        """
        return (self.dot(other) / other.length_squared()) * other

    def dot(self, other: VectorType) -> T:
        """
        Скалярное произведение векторов.
        
        Аргументы:
            other (VectorType): Второй вектор
            
        Возвращает:
            T: Результат скалярного произведения
        """
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: VectorType) -> T:
        """
        Векторное произведение (2D псевдоскаляр).
        
        Аргументы:
            other (VectorType): Второй вектор
            
        Возвращает:
            T: Псевдоскалярное значение (x1*y2 - y1*x2)
        """
        return self.x * other.y - self.y * other.x
    
    def angle_to(self, other: VectorType) -> float:
        """
        Угол между векторами в радианах (с учетом направления).
        
        Аргументы:
            other (VectorType): Второй вектор
            
        Возвращает:
            float: Угол в радианах от -π до π
        """
        return math.atan2(self.cross(other), self.dot(other))
    
    def distance_to(self, other: VectorType) -> float:
        """
        Евклидово расстояние между точками.
        
        Аргументы:
            other (VectorType): Вторая точка
            
        Возвращает:
            float: Расстояние между точками
        """
        return math.hypot(self.x - other.x, self.y - other.y)
    
    def lerp(self, other: VectorType, t: float) -> 'Vector2f':
        """
        Линейная интерполяция между векторами.
        
        Аргументы:
            other (VectorType): Конечный вектор интерполяции
            t (float): Параметр интерполяции (0 = текущий вектор, 1 = other)
            
        Возвращает:
            Vector2f: Интерполированный вектор
        """
        return Vector2f(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t
        )
    
    # ============== Утилиты ==============
    def as_tuple(self) -> Tuple[T, T]:
        """Возвращает координаты в виде кортежа (x, y)"""
        return (self.x, self.y)
    
    def as_list(self) -> List[T]:
        """Возвращает координаты в виде списка [x, y]"""
        return [self.x, self.y]
    
    def __repr__(self) -> str:
        """Официальное строковое представление вектора (для отладки)"""
        return f"{self.__class__.__name__}({self.x}, {self.y})"
    
    def __str__(self) -> str:
        """Неформальное строковое представление вектора (для пользователя)"""
        return f"({self.x}, {self.y})"
    
    @property
    def xy(self) -> Tuple[T, T]:
        """Свойство для доступа к координатам как к кортежу (x, y)"""
        return self.as_list()
    
    @xy.setter
    def xy(self, array: list[T] | Tuple[T, T]) -> None:
        """
        Установка координат через список или кортеж.
        
        Аргументы:
            array (list[T] | Tuple[T, T]): Новые координаты (должны быть 2 элемента)
        """
        self.x = array[0]
        self.y = array[1]


class Vector2f(BaseVector2):
    """
    Вектор с координатами типа float.
    
    Реализует все математические операции с высокой точностью.
    Подходит для физических расчетов, геометрии и других точных вычислений.
    """
    EPSILON = 1e-7  # Более подходящее значение для float операций
    
    def __init__(self, x: float, y: float):
        """
        Инициализация вектора с координатами типа float.
        
        Аргументы:
            x (float): Координата X
            y (float): Координата Y
        """
        super().__init__(float(x), float(y))
    
    # ============== Фабричные методы ==============
    @classmethod
    def random(cls, min_val: float = 0, max_val: float = 1) -> 'Vector2f':
        """
        Создает вектор со случайными координатами в заданном диапазоне.
        
        Аргументы:
            min_val (float, optional): Минимальное значение координат. По умолчанию 0
            max_val (float, optional): Максимальное значение координат. По умолчанию 1
            
        Возвращает:
            Vector2f: Вектор со случайными координатами
        """
        return cls(uniform(min_val, max_val), uniform(min_val, max_val))
    
    @classmethod
    def random_unit(cls) -> 'Vector2f':
        """
        Создает единичный вектор со случайным направлением.
        
        Возвращает:
            Vector2f: Единичный вектор (длина = 1) со случайным направлением
        """
        angle = uniform(0, 2 * math.pi)
        return cls(math.cos(angle), math.sin(angle))
    
    @classmethod
    def from_angle(cls, angle: float, length: float = 1.0) -> 'Vector2f':
        """
        Создает вектор из угла и длины.
        
        Аргументы:
            angle (float): Угол в радианах
            length (float, optional): Длина вектора. По умолчанию 1.0
            
        Возвращает:
            Vector2f: Вектор с заданным направлением и длиной
        """
        return cls(math.cos(angle) * length, math.sin(angle) * length)
    
    @classmethod
    def from_two_point(cls, point_1: tuple[int | float, int | float], point_2: tuple[int | float, int | float]) -> 'Vector2f':
        dx = point_1[0] - point_2[0]
        dy = point_1[1] - point_2[1]
        return Vector2f(dx, dy)
    
    # ============== Математические операции ==============
    def __truediv__(self, scalar: float) -> 'Vector2f':
        """Деление вектора на скаляр (возвращает новый Vector2f)"""
        return Vector2f(self.x / scalar, self.y / scalar)
    
    def __pow__(self, power: float) -> 'Vector2f':
        """
        Возводит компоненты вектора в степень.
        
        Аргументы:
            power (float): Степень возведения
            
        Возвращает:
            Vector2f: Новый вектор с возведенными в степень компонентами
        """
        return Vector2f(self.x ** power, self.y ** power)
    
    def pow(self, power: float) -> 'Vector2f':
        """Аналог оператора ** - возводит компоненты вектора в степень"""
        return self ** power
    
    def sqrt(self) -> 'Vector2f':
        """Возвращает вектор с квадратными корнями компонентов"""
        return Vector2f(math.sqrt(self.x), math.sqrt(self.y))
    
    def exp(self) -> 'Vector2f':
        """Возвращает вектор с экспонентами компонентов"""
        return Vector2f(math.exp(self.x), math.exp(self.y))
    
    def log(self, base: float = math.e) -> 'Vector2f':
        """
        Возвращает вектор с логарифмами компонентов.
        
        Аргументы:
            base (float, optional): Основание логарифма. По умолчанию e
            
        Возвращает:
            Vector2f: Вектор с логарифмами компонентов
        """
        if base == math.e:
            return Vector2f(math.log(self.x), math.log(self.y))
        return Vector2f(math.log(self.x, base), math.log(self.y, base))
    
    # ============== Геометрические операции ==============
    def angle(self) -> float:
        """
        Возвращает угол вектора в радианах.
        
        Возвращает:
            float: Угол в радианах от -π до π
        """
        return math.atan2(self.y, self.x)
    
    def angle_degrees(self) -> float:
        """
        Возвращает угол вектора в градусах.
        
        Возвращает:
            float: Угол в градусах от -180 до 180
        """
        return math.degrees(self.angle())
    
    def set_angle(self, angle: float) -> None:
        """
        Устанавливает направление вектора, сохраняя длину.
        
        Аргументы:
            angle (float): Новый угол в радианах
        """
        length = abs(self)
        self.x = math.cos(angle) * length
        self.y = math.sin(angle) * length
    
    def set_length(self, length: float) -> None:
        """
        Устанавливает длину вектора, сохраняя направление.
        
        Аргументы:
            length (float): Новая длина вектора
        """
        angle = self.angle()
        self.x = math.cos(angle) * length
        self.y = math.sin(angle) * length
    
    def length(self) -> float:
        """
        Возвращает длину (модуль) вектора.
        
        Возвращает:
            float: Длина вектора
        """
        return abs(self)
    
    def length_squared(self) -> float:
        """
        Возвращает квадрат длины вектора (оптимизация для сравнений).
        
        Возвращает:
            float: Квадрат длины вектора
        """
        return self.x * self.x + self.y * self.y
    
    def normalized(self) -> 'Vector2f':
        """
        Возвращает нормализованный вектор (длина = 1).
        
        Возвращает:
            Vector2f: Нормализованный вектор
            
        Примечание:
            Для нулевого вектора возвращает (0, 0)
        """
        length = self.length()
        if length == 0:
            return Vector2f(0, 0)
        return Vector2f(self.x / length, self.y / length)
    
    def normalize(self) -> None:
        """
        Нормализует текущий вектор (делает длину = 1).
        
        Примечание:
            Не изменяет нулевой вектор
        """
        length = self.length()
        if length != 0:
            self.x /= length
            self.y /= length
    
    def rotated(self, angle: float) -> 'Vector2f':
        """
        Возвращает повернутый вектор (в радианах).
        
        Аргументы:
            angle (float): Угол поворота в радианах
            
        Возвращает:
            Vector2f: Повернутый вектор
        """
        cos = math.cos(angle)
        sin = math.sin(angle)
        return Vector2f(
            self.x * cos - self.y * sin,
            self.x * sin + self.y * cos
        )
    
    def rotate(self, angle: float) -> None:
        """
        Поворачивает вектор (в радианах).
        
        Аргументы:
            angle (float): Угол поворота в радианах
        """
        cos = math.cos(angle)
        sin = math.sin(angle)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y
    
    def perpendicular(self) -> 'Vector2f':
        """
        Возвращает перпендикулярный вектор (поворот на 90° против часовой стрелки).
        
        Возвращает:
            Vector2f: Перпендикулярный вектор
        """
        return Vector2f(-self.y, self.x)
    
    def reflect(self, normal: 'Vector2f') -> 'Vector2f':
        """
        Отражение вектора относительно нормали.
        
        Аргументы:
            normal (Vector2f): Вектор нормали (должен быть нормализован)
            
        Возвращает:
            Vector2f: Отраженный вектор
        """
        dot = self.dot(normal)
        return Vector2f(
            self.x - 2 * dot * normal.x,
            self.y - 2 * dot * normal.y
        )
    
    # ============== Проверки и сравнения ==============
    def is_normalized(self) -> bool:
        """
        Проверяет, является ли вектор нормализованным (длина = 1).
        
        Возвращает:
            bool: True если длина вектора равна 1 с относительной погрешностью 1e-9
        """
        return math.isclose(self.length_squared(), 1.0, rel_tol=1e-9)
    
    def is_zero(self) -> bool:
        """
        Проверяет, является ли вектор нулевым.
        
        Возвращает:
            bool: True если обе координаты равны 0 с абсолютной погрешностью 1e-9
        """
        return math.isclose(self.x, 0.0, abs_tol=1e-9) and math.isclose(self.y, 0.0, abs_tol=1e-9)
    
    def is_parallel_to(self, other: 'Vector2f') -> bool:
        """
        Проверяет, параллельны ли векторы.
        
        Аргументы:
            other (Vector2f): Второй вектор для проверки
            
        Возвращает:
            bool: True если векторное произведение равно 0 (с погрешностью)
        """
        return math.isclose(self.cross(other), 0.0, abs_tol=1e-9)
    
    def is_perpendicular_to(self, other: 'Vector2f') -> bool:
        """
        Проверяет, перпендикулярны ли векторы.
        
        Аргументы:
            other (Vector2f): Второй вектор для проверки
            
        Возвращает:
            bool: True если скалярное произведение равно 0 (с погрешностью)
        """
        return math.isclose(self.dot(other), 0.0, abs_tol=1e-9)
    
    def is_normalized_to_epsilon(self) -> bool:
        """
        Проверяет нормализацию с использованием EPSILON.
        
        Возвращает:
            bool: True если квадрат длины отличается от 1 менее чем на EPSILON
        """
        return abs(self.length_squared() - 1.0) < self.EPSILON
    
    def is_parallel_to_to_epsilon(self, other: 'Vector2f') -> bool:
        """
        Проверяет параллельность с использованием EPSILON.
        
        Аргументы:
            other (Vector2f): Второй вектор для проверки
            
        Возвращает:
            bool: True если один из векторов нулевой или векторное произведение меньше EPSILON
        """
        return self.approx_zero() or other.approx_zero() or abs(self.cross(other)) < self.EPSILON
    
    def is_perpendicular_to_to_epsilon(self, other: 'Vector2f') -> bool:
        """
        Проверяет перпендикулярность с использованием EPSILON.
        
        Аргументы:
            other (Vector2f): Второй вектор для проверки
            
        Возвращает:
            bool: True если скалярное произведение меньше EPSILON
        """
        return abs(self.dot(other)) < self.EPSILON
    
    def angle_to_to_epsilon(self, other: 'Vector2f') -> float:
        """
        Угол между векторами с проверкой на нулевые векторы.
        
        Аргументы:
            other (Vector2f): Второй вектор
            
        Возвращает:
            float: Угол в радианах
            
        Выбрасывает:
            ValueError: Если один из векторов нулевой
        """
        if self.approx_zero() or other.approx_zero():
            raise ValueError("Cannot calculate angle for zero vector")
        return math.atan2(self.cross(other), self.dot(other))
    
    # ============== Преобразования ==============
    def to_int(self) -> 'Vector2i':
        """
        Преобразует в целочисленный вектор с округлением.
        
        Возвращает:
            Vector2i: Вектор с округленными координатами
        """
        return Vector2i(round(self.x), round(self.y))
    
    def to_int_floor(self) -> 'Vector2i':
        """
        Преобразует в целочисленный вектор с округлением вниз.
        
        Возвращает:
            Vector2i: Вектор с округленными вниз координатами
        """
        return Vector2i(math.floor(self.x), math.floor(self.y))
    
    def to_int_ceil(self) -> 'Vector2i':
        """
        Преобразует в целочисленный вектор с округлением вверх.
        
        Возвращает:
            Vector2i: Вектор с округленными вверх координатами
        """
        return Vector2i(math.ceil(self.x), math.ceil(self.y))
    
    def __mul__(self, other: Union[float, 'Vector2f']) -> 'Vector2f':
        """
        Умножение вектора на скаляр или поэлементное умножение на другой вектор.
        
        Аргументы:
            other (float | Vector2f): Множитель
            
        Возвращает:
            Vector2f: Результат умножения
        """
        if isinstance(other, Vector2f):
            return Vector2f(self.x * other.x, self.y * other.y)
        return Vector2f(self.x * other, self.y * other)
    
    def __rmul__(self, other: Union[float, 'Vector2f']) -> 'Vector2f':
        """Умножение справа (аналогично __mul__)"""
        return self.__mul__(other)
    
    def __imul__(self, other: Union[float, 'Vector2f']) -> 'Vector2f':
        """
        Комбинированное умножение с присваиванием (in-place).
        
        Аргументы:
            other (float | Vector2f): Множитель
            
        Возвращает:
            Vector2f: Измененный текущий вектор
        """
        if isinstance(other, Vector2f):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self


class Vector2i(BaseVector2):
    """
    Вектор с целочисленными координатами.
    
    Оптимизирован для дискретных операций и работы с пикселями.
    Подходит для работы с координатами в сетках, тайловых картах и других целочисленных системах.
    """
    EPSILON = 0  # Для целых чисел погрешность не нужна
    
    def __init__(self, x: int, y: int):
        """
        Инициализация вектора с целочисленными координатами.
        
        Аргументы:
            x (int): Координата X
            y (int): Координата Y
        """
        super().__init__(int(x), int(y))

    def __eq__(self, other: object) -> bool:
        """
        Проверка на равенство (точное для целых чисел).
        
        Аргументы:
            other (object): Объект для сравнения
            
        Возвращает:
            bool: True если координаты точно совпадают
        """
        if not isinstance(other, BaseVector2):
            return False
        return self.x == other.x and self.y == other.y
    
    def approx_equal(self, other: 'BaseVector2', epsilon: float | None = None) -> bool:
        """
        Для целых чисел работает как точное сравнение (epsilon игнорируется).
        
        Аргументы:
            other (BaseVector2): Вектор для сравнения
            epsilon (float, optional): Игнорируется
            
        Возвращает:
            bool: Результат точного сравнения
        """
        return self == other
    
    def approx_zero(self, epsilon: float | None = None) -> bool:
        """
        Для целых чисел работает как точная проверка на ноль (epsilon игнорируется).
        
        Возвращает:
            bool: True если обе координаты точно равны 0
        """
        return self.x == 0 and self.y == 0

    def __mul__(self, other: Union[int, 'Vector2i']) -> 'Vector2i':
        """
        Умножение вектора на скаляр или поэлементное умножение на другой вектор.
        
        Аргументы:
            other (int | Vector2i): Множитель
            
        Возвращает:
            Vector2i: Результат умножения
        """
        if isinstance(other, (Vector2i, Vector2f)):
            return Vector2i(self.x * other.x, self.y * other.y)
        return Vector2i(self.x * other, self.y * other)
    
    def __rmul__(self, other: Union[int, 'Vector2i']) -> 'Vector2i':
        """Умножение справа (аналогично __mul__)"""
        return self.__mul__(other)
    
    def __imul__(self, other: Union[int, 'Vector2i']) -> 'Vector2i':
        """
        Комбинированное умножение с присваиванием (in-place).
        
        Аргументы:
            other (int | Vector2i): Множитель
            
        Возвращает:
            Vector2i: Измененный текущий вектор
        """
        if isinstance(other, Vector2i):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self
    
    # ============== Фабричные методы ==============
    @classmethod
    def random(cls, min_val: int, max_val: int) -> 'Vector2i':
        """
        Создает вектор со случайными целыми координатами в заданном диапазоне.
        
        Аргументы:
            min_val (int): Минимальное значение координат
            max_val (int): Максимальное значение координат
            
        Возвращает:
            Vector2i: Вектор со случайными целыми координатами
        """
        return cls(randint(min_val, max_val), randint(min_val, max_val))
    
    # ============== Математические операции ==============
    def __floordiv__(self, scalar: int) -> 'Vector2i':
        """
        Целочисленное деление вектора на скаляр.
        
        Аргументы:
            scalar (int): Делитель
            
        Возвращает:
            Vector2i: Результат целочисленного деления
        """
        return Vector2i(self.x // scalar, self.y // scalar)
    
    def __mod__(self, scalar: int) -> 'Vector2i':
        """
        Остаток от деления компонентов вектора на скаляр.
        
        Аргументы:
            scalar (int): Делитель
            
        Возвращает:
            Vector2i: Вектор с остатками от деления
        """
        return Vector2i(self.x % scalar, self.y % scalar)
    
    # ============== Геометрические операции ==============
    def angle(self) -> float:
        """
        Возвращает угол вектора в радианах (как float).
        
        Возвращает:
            float: Угол в радианах от -π до π
        """
        return math.atan2(float(self.y), float(self.x))
    
    def angle_degrees(self) -> float:
        """
        Возвращает угол вектора в градусах (как float).
        
        Возвращает:
            float: Угол в градусах от -180 до 180
        """
        return math.degrees(self.angle())
    
    def length(self) -> float:
        """
        Возвращает длину вектора (как float).
        
        Возвращает:
            float: Длина вектора
        """
        return math.hypot(self.x, self.y)
    
    def length_squared(self) -> int:
        """
        Возвращает квадрат длины вектора (как целое число).
        
        Возвращает:
            int: x^2 + y^2
        """
        return self.x * self.x + self.y * self.y
    
    # ============== Преобразования ==============
    def to_float(self) -> 'Vector2f':
        """
        Преобразует в вектор с плавающей точкой.
        
        Возвращает:
            Vector2f: Вектор с теми же координатами, но типа float
        """
        return Vector2f(float(self.x), float(self.y))
    
    # Целочисленные векторы не поддерживают нормализацию и поворот напрямую
    def normalized(self) -> 'Vector2f':
        """
        Возвращает нормализованный вектор (как Vector2f).
        
        Возвращает:
            Vector2f: Нормализованный вектор с плавающей точкой
        """
        return self.to_float().normalized()
    
    def rotated(self, angle: float) -> 'Vector2f':
        """
        Возвращает повернутый вектор (как Vector2f).
        
        Аргументы:
            angle (float): Угол поворота в радианах
            
        Возвращает:
            Vector2f: Повернутый вектор с плавающей точкой
        """
        return self.to_float().rotated(angle)
    
    def perpendicular(self) -> 'Vector2i':
        """
        Возвращает перпендикулярный вектор (поворот на 90° против часовой стрелки).
        
        Возвращает:
            Vector2i: Перпендикулярный вектор с целыми координатами
        """
        return Vector2i(-self.y, self.x)