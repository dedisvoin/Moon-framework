"""
#### *Модуль прокси-объектов для управления фигурами в Moon*

---

##### Версия: 1.0.0

*Автор: Павлов Иван (Pavlov Ivan)*

*Лицензия: MIT*
##### Реализованно на 100%

---

✓ ShapePositionProxy - управление позицией фигур:
  - Прямой доступ к координатам X и Y
  - Немедленная синхронизация с нативными объектами C++
  - Наследование от Vector2f для математических операций

✓ ShapeSizeProxy - управление размерами прямоугольников:
  - Двойной интерфейс (W/H и X/Y)
  - Автоматическое обновление размеров
  - Проверка допустимости значений

✓ ShapeOriginProxy - управление точкой отсчета:
  - Центр преобразований (поворот, масштаб)
  - Координаты относительно локальной системы
  - Влияние на все геометрические операции

✓ ShapeColorProxy - управление цветом фигур:
  - Независимое управление компонентами RGBA
  - Проверка диапазона значений (0-255)
  - Наследование от базового класса Color

---

:Architecture:

• Паттерн Proxy для синхронизации Python и C++ объектов
• Наследование от математических типов (Vector2f, Color)
• Прозрачное делегирование вызовов нативным функциям
• Минимальные накладные расходы при доступе

:Features:

• Прямой доступ к атрибутам через свойства
• Автоматическая проверка допустимости значений
• Немедленное применение изменений к отображению
• Поддержка как прямоугольников, так и кругов
• Единый интерфейс для различных типов фигур

:Performance:

• Минимальные overhead при использовании прокси
• Прямые вызовы C++ функций через ctypes
• Кэширование значений где это возможно
• Оптимизированные проверки и обновления

:Integration:

• Полная совместимость с RectangleShape и CircleShape
• Автоматическое определение типа фигуры
• Единообразный API для всех геометрических примитивов
• Поддержка цепочек вызовов и fluent-интерфейса

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

import ctypes
from typing import Final

from Moon.python.Types import *
from Moon.python.Colors import *
from Moon.python.Vectors import Vec2f

from Moon.python.utils import find_library

# =====================================================================================
# ТИПЫ УКАЗАТЕЛЕЙ ДЛЯ НАТИВНЫХ ОБЪЕКТОВ C++
# =====================================================================================

# Псевдоним для типа указателя на шейп прямоугольника
RectanglePtr: Final[type[ctypes.c_void_p]] = ctypes.c_void_p

# Псевдоним для типа указателя на шейп круга
CirclePtr: Final[type[ctypes.c_void_p]] = ctypes.c_void_p

# =====================================================================================
# ЗАГРУЗКА НАТИВНОЙ БИБЛИОТЕКИ
# =====================================================================================

# Загружаем DLL библиотеку
try:
    LIB_MOON: Final[ctypes.CDLL] = ctypes.CDLL(find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")

# =====================================================================================
# ОПРЕДЕЛЕНИЕ СИГНАТУР ФУНКЦИЙ ДЛЯ ПРЯМОУГОЛЬНИКОВ
# =====================================================================================

# Функции получения позиции прямоугольника
LIB_MOON._Rectangle_GetPositionX.restype = ctypes.c_float
LIB_MOON._Rectangle_GetPositionX.argtypes = [RectanglePtr]
LIB_MOON._Rectangle_GetPositionY.restype = ctypes.c_float
LIB_MOON._Rectangle_GetPositionY.argtypes = [RectanglePtr]

# Функции получения точки отсчета прямоугольника
LIB_MOON._Rectangle_GetOriginX.restype = ctypes.c_double
LIB_MOON._Rectangle_GetOriginX.argtypes = [RectanglePtr]
LIB_MOON._Rectangle_GetOriginY.restype = ctypes.c_double
LIB_MOON._Rectangle_GetOriginY.argtypes = [RectanglePtr]

# Функции получения размеров прямоугольника
LIB_MOON._Rectangle_GetWidth.restype = ctypes.c_float
LIB_MOON._Rectangle_GetWidth.argtypes = [RectanglePtr]
LIB_MOON._Rectangle_GetHeight.restype = ctypes.c_float
LIB_MOON._Rectangle_GetHeight.argtypes = [RectanglePtr]

# Функции установки свойств прямоугольника
LIB_MOON._Rectangle_SetPosition.restype = None
LIB_MOON._Rectangle_SetPosition.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Rectangle_SetColor.restype = None
LIB_MOON._Rectangle_SetColor.argtypes = [RectanglePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Rectangle_SetOrigin.restype = None
LIB_MOON._Rectangle_SetOrigin.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Rectangle_SetSize.restype = None
LIB_MOON._Rectangle_SetSize.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]

# =====================================================================================
# ОПРЕДЕЛЕНИЕ СИГНАТУР ФУНКЦИЙ ДЛЯ КРУГОВ
# =====================================================================================

# Функции установки позиции круга
LIB_MOON._Circle_SetPosition.argtypes = [CirclePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Circle_SetPosition.restype = None

# Функции получения позиции круга
LIB_MOON._Circle_GetPositionX.argtypes = [CirclePtr]
LIB_MOON._Circle_GetPositionX.restype = ctypes.c_float
LIB_MOON._Circle_GetPositionY.argtypes = [CirclePtr]
LIB_MOON._Circle_GetPositionY.restype = ctypes.c_float

# Функции управления цветом круга
LIB_MOON._Circle_SetColor.argtypes = [CirclePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Circle_SetColor.restype = None

# Функции управления точкой отсчета круга
LIB_MOON._Circle_SetOrigin.argtypes = [CirclePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Circle_SetOrigin.restype = None
LIB_MOON._Circle_GetOriginX.argtypes = [CirclePtr]
LIB_MOON._Circle_GetOriginX.restype = ctypes.c_float
LIB_MOON._Circle_GetOriginY.argtypes = [CirclePtr]
LIB_MOON._Circle_GetOriginY.restype = ctypes.c_float

# =====================================================================================
# КЛАСС ShapePositionProxy - УПРАВЛЕНИЕ ПОЗИЦИЕЙ ФИГУРЫ
# =====================================================================================

class ShapePositionProxy(Vec2f):
    """
    #### Прокси-объект для управления позицией фигуры
    Реализовывает связанный вектор над базовым двумерным вектором с плавающей точкой для точности

    ---

    :Description:
    - Позволяет напрямую обращаться и изменять компоненты X и Y
    - Обеспечивает немедленную синхронизацию с нативным объектом C++
    - Используется через свойство `position` родительской фигуры (e.g., `rect.position.x = 10`)

    ---

    :Inheritance:
    - Vector2f: Позволяет использовать методы и операторы класса Vector2f
    """
    def __init__(self, shape: "RectangleShape | CircleShape"):                                                      # pyright: ignore
        """
        :Args:
        - shape: Ссылка на родительский объект, который нужно контролировать
        """
        self.__shape = shape
        self.__type = shape.__class__.__name__

    @property
    def x(self) -> Number:
        """
        #### Возвращает горизонтальную координату (X)

        ---

        :Returns:
        - Number: Текущая координата X (в пикселях)
        """
        if self.__type == 'RectangleShape':
            return LIB_MOON._Rectangle_GetPositionX(self.__shape.get_ptr())
        elif self.__type == 'CircleShape':
            return LIB_MOON._Circle_GetPositionX(self.__shape.get_ptr())
        raise ValueError(f"Unsupported shape type: {self.__type}")

    @property
    def y(self) -> Number:
        """
        #### Возвращает вертикальную координату (Y)

        ---

        :Returns:
        - Number: Текущая координата Y (в пикселях)
        """
        if self.__type == 'RectangleShape':
            return LIB_MOON._Rectangle_GetPositionY(self.__shape.get_ptr())
        elif self.__type == 'CircleShape':
            return LIB_MOON._Circle_GetPositionY(self.__shape.get_ptr())
        raise ValueError(f"Unsupported shape type: {self.__type}")

    @property
    def xy(self) -> tuple[Number, Number]:
        """
        #### Возвращает позицию как кортеж (x, y)

        ---

        :Returns:
        - tuple[Number, Number]: Кортеж текущих координат (X, Y)
        """
        return (self.x, self.y)

    @x.setter
    def x(self, value: Number):
        """
        #### Устанавливает горизонтальную координату (X)

        ---

        :Description:
        - Обновляет позицию фигуры, сохраняя текущую координату Y
        - Немедленно синхронизируется с нативным объектом C++

        :Args:
        - value (Number): Новая координата X
        """
        if self.x == value: return
        if self.__type == 'RectangleShape':
            LIB_MOON._Rectangle_SetPosition(self.__shape.get_ptr(), value, self.y)
        elif self.__type == 'CircleShape':
            LIB_MOON._Circle_SetPosition(self.__shape.get_ptr(), value, self.y)
        else:
            raise ValueError(f"Unsupported shape type: {self.__type}")

    @y.setter
    def y(self, value: Number):
        """
        #### Устанавливает вертикальную координату (Y)

        ---

        :Description:
        - Обновляет позицию фигуры, сохраняя текущую координату X
        - Немедленно синхронизируется с нативным объектом C++

        :Args:
        - value (Number): Новая координата Y
        """
        if self.y == value: return
        if self.__type == 'RectangleShape':
            LIB_MOON._Rectangle_SetPosition(self.__shape.get_ptr(), self.x, value)
        elif self.__type == 'CircleShape':
            LIB_MOON._Circle_SetPosition(self.__shape.get_ptr(), self.x, value)
        else:
            raise ValueError(f"Unsupported shape type: {self.__type}")

    def __repr__(self) -> str:
        """
        #### Возвращает строковое представление прокси

        ---

        :Returns:
        - str: Формат: `[Shape] < PositionProxy(x, y)`
        """
        return f"{self.__shape} < PositionProxy({self.x}, {self.y})"

# =====================================================================================
# КЛАСС ShapeSizeProxy - УПРАВЛЕНИЕ РАЗМЕРАМИ ФИГУРЫ
# =====================================================================================

class ShapeSizeProxy(Vec2f):
    """
    #### Прокси-объект для управления размерами фигуры (ширина/высота)
    Реализовывает связанный вектор над базовым двумерным вектором с плавающей точкой для точности

    ---

    :Description:
    - Позволяет напрямую обращаться и изменять размеры с использованием W/H или X/Y
    - Обеспечивает немедленную синхронизацию с нативным объектом C++
    - Используется через свойство `size` родительской фигуры (e.g., `rect.size.w = 50`)

    ---

    :Important:
    - Применяется только к прямоугольникам (RectangleShape)
    - Для кругов управление размером осуществляется через радиус

    :Inheritance:
    - Vector2f: Позволяет использовать методы и операторы класса Vector2f
    """
    def __init__(self, shape: "RectangleShape | CircleShape"):                                                      # pyright: ignore
        """
        :Args:
        - shape: Ссылка на родительский объект, который нужно контролировать
        """
        self.__shape = shape
        self.__type = type(shape).__name__

    @property
    def w(self) -> Number:
        """
        #### Возвращает ширину (W) фигуры

        ---

        :Returns:
        - Number: Текущая ширина фигуры
        """
        if self.__type == 'RectangleShape':
            return LIB_MOON._Rectangle_GetWidth(self.__shape.get_ptr())
        raise ValueError(f"Unsupported shape type: {self.__type}")

    @property
    def h(self) -> Number:
        """
        #### Возвращает высоту (H) фигуры

        ---

        :Returns:
        - Number: Текущая высота фигуры
        """
        return LIB_MOON._Rectangle_GetHeight(self.__shape.get_ptr())

    @property
    def x(self) -> Number:
        """
        #### Псевдоним для ширины (W) в контексте вектора (X)

        ---

        :Returns:
        - Number: Текущая ширина фигуры
        """
        return self.w

    @property
    def y(self) -> Number:
        """
        #### Псевдоним для высоты (H) в контексте вектора (Y)

        ---

        :Returns:
        - Number: Текущая высота фигуры
        """
        return self.h

    @x.setter
    def x(self, value: Number):
        """
        #### Устанавливает ширину фигуры (через X)

        ---

        :Description:
        - Обновляет ширину фигуры, сохраняя текущую высоту

        :Args:
        - value (Number): Новая ширина
        """
        if self.x == value:
            return
        LIB_MOON._Rectangle_SetSize(self.__shape.get_ptr(), value, self.h)

    @y.setter
    def y(self, value: Number):
        """
        #### Устанавливает высоту фигуры (через Y)

        ---

        :Description:
        - Обновляет высоту фигуры, сохраняя текущую ширину

        :Args:
        - value (Number): Новая высота
        """
        if self.y == value:
            return
        LIB_MOON._Rectangle_SetSize(self.__shape.get_ptr(), self.w, value)

    @property
    def xy(self) -> tuple[Number, Number]:
        """
        #### Возвращает размеры как кортеж (x, y) = (width, height)

        ---

        :Returns:
        - tuple[Number, Number]: Кортеж текущих размеров (Ширина, Высота)
        """
        return self.wh

    @property
    def wh(self) -> tuple[Number, Number]:
        """
        #### Возвращает размеры как кортеж (w, h) = (width, height)

        ---

        :Returns:
        - tuple[Number, Number]: Кортеж текущих размеров (Ширина, Высота)
        """
        return (self.w, self.h)

    @w.setter
    def w(self, value: Number):
        """
        #### Устанавливает ширину фигуры (через W)

        ---

        :Description:
        - Обновляет ширину фигуры, сохраняя текущую высоту

        :Args:
        - value (Number): Новая ширина
        """
        self.x = value

    @h.setter
    def h(self, value: Number):
        """
        #### Устанавливает высоту фигуры (через H)

        ---

        :Description:
        - Обновляет высоту фигуры, сохраняя текущую ширину

        :Args:
        - value (Number): Новая высота
        """
        self.y = value

    def __repr__(self) -> str:
        """
        #### Возвращает строковое представление прокси

        ---

        :Returns:
        - str: Формат: `[Shape] < SizeProxy(width, height)`
        """
        return f"{self.__shape} < SizeProxy({self.x}, {self.y})"

# =====================================================================================
# КЛАСС ShapeOriginProxy - УПРАВЛЕНИЕ ТОЧКОЙ ОТСЧЕТА ФИГУРЫ
# =====================================================================================

class ShapeOriginProxy(Vec2f):
    """
    #### Прокси-объект для управления точкой отсчета (Origin) фигуры
    Реализовывает связанный вектор над базовым двумерным вектором с плавающей точкой для точности

    ---

    :Description:
    - Определяет центр преобразований (поворот, масштаб)
    - Позволяет напрямую обращаться и изменять компоненты X и Y
    - Обеспечивает немедленную синхронизацию с нативным объектом C++
    - Используется через свойство `origin` родительской фигуры (e.g., `rect.origin.x = 25`)

    ---

    :Inheritance:
    - Vector2f: Позволяет использовать методы и операторы класса Vector2f
    """
    def __init__(self, shape: "RectangleShape | CircleShape"):                                                       # pyright: ignore
        """
        :Args:
        - shape: Ссылка на родительский объект, который нужно контролировать
        """
        self.__shape = shape
        self.__type = shape.__class__.__name__

    @property
    def x(self) -> Number:
        """
        #### Возвращает горизонтальное смещение (X) точки отсчета

        ---

        :Returns:
        - Number: Смещение X относительно верхнего левого угла фигуры
        """
        if self.__type == 'RectangleShape':
            return LIB_MOON._Rectangle_GetOriginX(self.__shape.get_ptr())
        elif self.__type == 'CircleShape':
            return LIB_MOON._Circle_GetOriginX(self.__shape.get_ptr())
        raise ValueError(f"Unsupported shape type: {self.__type}")

    @property
    def y(self) -> Number:
        """
        #### Возвращает вертикальное смещение (Y) точки отсчета

        ---

        :Returns:
        - Number: Смещение Y относительно верхнего левого угла фигуры
        """
        if self.__type == 'RectangleShape':
            return LIB_MOON._Rectangle_GetOriginY(self.__shape.get_ptr())
        elif self.__type == 'CircleShape':
            return LIB_MOON._Circle_GetOriginY(self.__shape.get_ptr())

        raise ValueError(f"Unsupported shape type: {self.__type}")

    @property
    def xy(self) -> tuple[Number, Number]:
        """
        #### Возвращает смещение Origin как кортеж (x, y)

        ---

        :Returns:
        - tuple[Number, Number]: Кортеж текущих смещений (X, Y)
        """
        return (self.x, self.y)

    @x.setter
    def x(self, value: Number):
        """
        #### Устанавливает горизонтальное смещение (X) Origin

        ---

        :Description:
        - Обновляет точку отсчета, сохраняя текущее смещение Y
        - Немедленно синхронизируется с нативным объектом C++

        :Args:
        - value (Number): Новое смещение X
        """
        if self.x == value:
            return
        if self.__type == 'RectangleShape':
            LIB_MOON._Rectangle_SetOrigin(self.__shape.get_ptr(), value, self.y)
        elif self.__type == 'CircleShape':
            LIB_MOON._Circle_SetOrigin(self.__shape.get_ptr(), value, self.y)
        else:
            raise ValueError(f"Unsupported shape type: {self.__type}")

    @y.setter
    def y(self, value: Number):
        """
        #### Устанавливает вертикальное смещение (Y) Origin

        ---

        :Description:
        - Обновляет точку отсчета, сохраняя текущее смещение X
        - Немедленно синхронизируется с нативным объектом C++

        :Args:
        - value (Number): Новое смещение Y
        """
        if self.y == value: return
        if self.__type == 'RectangleShape':
            LIB_MOON._Rectangle_SetOrigin(self.__shape.get_ptr(), self.x, value)
        elif self.__type == 'CircleShape':
            LIB_MOON._Circle_SetOrigin(self.__shape.get_ptr(), self.x, value)
        else:
            raise ValueError(f"Unsupported shape type: {self.__type}")

    def __repr__(self) -> str:
        """
        #### Возвращает строковое представление прокси

        ---

        :Returns:
        - str: Формат: `[Shape] < OriginProxy(x, y)`
        """
        return f"{self.__shape} < OriginProxy({self.x}, {self.y})"

# =====================================================================================
# КЛАСС ShapeColorProxy - УПРАВЛЕНИЕ ЦВЕТОМ ФИГУРЫ
# =====================================================================================

class ShapeColorProxy(Color):
    """
    #### Прокси-объект для управления цветом заливки фигуры
    Наследует функциональность класса Color для работы с цветовыми компонентами

    ---

    :Description:
    - Позволяет независимо управлять компонентами RGBA цвета
    - Обеспечивает проверку допустимости значений (0-255)
    - Немедленно применяет изменения к нативному объекту
    - Используется через свойство `color` родительской фигуры

    ---

    :Inheritance:
    - Color: Наследует все методы и свойства базового класса цвета
    """
    def __init__(self, shape: "RectangleShape | CircleShape"):      # pyright: ignore
        """
        :Args:
        - shape: Ссылка на родительский объект фигуры
        """
        self.__shape = shape
        self.__type = type(shape).__name__

    def __check_value(self, value: Number) -> bool:
        """
        #### Проверяет корректность значения цветового компонента

        ---

        :Args:
        - value (Number): Проверяемое значение

        :Raises:
        - ValueError: Если значение вне диапазона 0-255

        :Returns:
        - bool: True если значение корректно
        """
        if not (0 <= value <= 255):
            raise ValueError(f"Invalid value, color component must be between 0 and 255")
        return True

    @property
    def r(self) -> Number:
        """
        #### Возвращает красную компоненту цвета (R)

        ---

        :Returns:
        - Number: Значение красного компонента (0-255)
        """
        return self.__shape.get_color().r

    @property
    def g(self) -> Number:
        """
        #### Возвращает зеленую компоненту цвета (G)

        ---

        :Returns:
        - Number: Значение зеленого компонента (0-255)
        """
        return self.__shape.get_color().g

    @property
    def b(self) -> Number:
        """
        #### Возвращает синюю компоненту цвета (B)

        ---

        :Returns:
        - Number: Значение синего компонента (0-255)
        """
        return self.__shape.get_color().b

    @property
    def a(self) -> Number:
        """
        #### Возвращает альфа-компоненту цвета (прозрачность)

        ---

        :Returns:
        - Number: Значение альфа-компонента (0-255)
        """
        return self.__shape.get_color().a

    @r.setter
    def r(self, value: Number):
        """
        #### Устанавливает красную компоненту цвета (R)

        ---

        :Args:
        - value (Number): Новое значение красного компонента (0-255)
        """
        if self.r == value: return
        self.__check_value(value)
        if self.__type == 'RectangleShape':
            self.__shape.set_color(Color(value, self.g, self.b, self.a))
        elif self.__type == 'CircleShape':
            self.__shape.set_color(Color(value, self.g, self.b, self.a))
        else:
            raise ValueError(f"Unsupported shape type: {self.__type}")

    @g.setter
    def g(self, value: Number):
        """
        #### Устанавливает зеленую компоненту цвета (G)

        ---

        :Args:
        - value (Number): Новое значение зеленого компонента (0-255)
        """
        if self.g == value: return
        self.__check_value(value)
        if self.__type == 'RectangleShape':
            self.__shape.set_color(Color(self.r, value, self.b, self.a))
        elif self.__type == 'CircleShape':
            self.__shape.set_color(Color(self.r, value, self.b, self.a))
        else:
            raise ValueError(f"Unsupported shape type: {self.__type}")

    @b.setter
    def b(self, value: Number):
        """
        #### Устанавливает синюю компоненту цвета (B)

        ---

        :Args:
        - value (Number): Новое значение синего компонента (0-255)
        """
        if self.b == value: return
        self.__check_value(value)
        if self.__type == 'RectangleShape':
            self.__shape.set_color(Color(self.r, self.g, value, self.a))
        elif self.__type == 'CircleShape':
            self.__shape.set_color(Color(self.r, self.g, value, self.a))
        else:
            raise ValueError(f"Unsupported shape type: {self.__type}")

    @a.setter
    def a(self, value: Number):
        """
        #### Устанавливает альфа-компоненту цвета (прозрачность)

        ---

        :Args:
        - value (Number): Новое значение альфа-компонента (0-255)
        """
        if self.a == value: return
        self.__check_value(value)
        if self.__type == 'RectangleShape':
            self.__shape.set_color(Color(self.r, self.g, self.b, value))
        elif self.__type == 'CircleShape':
            self.__shape.set_color(Color(self.r, self.g, self.b, value))
        else:
            raise ValueError(f"Unsupported shape type: {self.__type}")

    def __repr__(self) -> str:
        """
        #### Возвращает строковое представление прокси

        ---

        :Returns:
        - str: Формат: `[Shape] < ColorProxy(r, g, b, a)`
        """
        return f"{self.__shape} < ColorProxy({self.r}, {self.g}, {self.b}, {self.a})"
