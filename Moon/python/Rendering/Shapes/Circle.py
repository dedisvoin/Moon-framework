"""
#### *Модуль работы с круговыми фигурами в Moon*

---

##### Версия: 1.0.0

*Автор: Павлов Иван (Pavlov Ivan)*

*Лицензия: MIT*
##### Реализованно на 100%

---

✓ Класс CircleShape - полная реализация круговой фигуры:
  - Создание кругов с настраиваемой гладкостью (аппроксимация)
  - Управление геометрическими параметрами (радиус, позиция)
  - Преобразования (поворот, масштаб, перемещение)
  - Настройка внешнего вида (цвет заливки, контур, толщина)

✓ Прокси-объекты для удобного управления:
  - ShapePositionProxy - управление позицией через свойства
  - ShapeColorProxy - управление цветом через RGBA-компоненты
  - ShapeOriginProxy - управление точкой отсчета

✓ Fluent-интерфейс для цепочек вызовов:
  - Все методы модификации возвращают self
  - Возможность комбинирования операций
  - Удобство для последовательных преобразований

✓ Безопасное управление памятью:
  - Автоматическое создание/удаление нативных объектов C++
  - Защита от утечек памяти в деструкторе
  - Безопасная работа с указателями

✓ Полная интеграция с нативной библиотекой:
  - Низкоуровневые привязки через ctypes
  - Минимальные накладные расходы
  - Прямой доступ к C++ объектам

---

:Features:

• Создание кругов с заданной точностью аппроксимации (≥3 точек)
• Динамическое изменение радиуса с проверкой допустимости
• Управление цветом заливки и прозрачностью (RGBA)
• Настройка контура (цвет, толщина)
• Геометрические преобразования (поворот, масштаб, смещение)
• Центрированная точка отсчета по умолчанию
• Fluent-интерфейс для последовательных операций
• Полное копирование объектов с сохранением состояния
• Автоматическое управление памятью

:Performance:

• Оптимизированные вызовы нативных C++ функций
• Минимальные накладные расходы при использовании прокси
• Эффективное использование математических операций
• Автоматическая нормализация углов

:Requires:

• Python 3.8+
• Модуль ctypes (стандартная библиотека)
• typing.Self для type hints
• Нативная библиотека Moon (DLL)

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
from typing import Self, Final, final

from Moon.python.Types import *
from Moon.python.Colors import *
from Moon.python.Rendering.Shapes.Proxys import *            # pyright: ignore

from Moon.python.Vectors import Vec2f, Vec2i, Vec2T

from Moon.python.utils import find_library



# Загружаем DLL библиотеку
try:
    LIB_MOON: Final[ctypes.CDLL] = ctypes.CDLL(find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")

# =====================================================================================
# ТИПЫ УКАЗАТЕЛЕЙ ДЛЯ НАТИВНЫХ ОБЪЕКТОВ C++
# =====================================================================================

# Псевдоним для типа указателя на шейп круга
CirclePtr: Final[type[ctypes.c_void_p]] = ctypes.c_void_p

# Тип указателя на шейп круга (альтернативное определение)
CirclePtrType = type[RectanglePtr]

# =====================================================================================
# ПРИВЯЗКИ C++ ФУНКЦИЙ ДЛЯ КРУГОВ
# =====================================================================================

# Эти строки определяют типы аргументов (argtypes) и возвращаемых значений (restype)
# для C++ функций, связанных с кругами.

# Функции создания и удаления круга
LIB_MOON._Circle_Create.argtypes = [ctypes.c_float, ctypes.c_int]
LIB_MOON._Circle_Create.restype = CirclePtr
LIB_MOON._Circle_Delete.argtypes = [ctypes.c_void_p]
LIB_MOON._Circle_Delete.restype = None

# Функции управления позицией
LIB_MOON._Circle_SetPosition.argtypes = [CirclePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Circle_SetPosition.restype = None
LIB_MOON._Circle_GetPositionX.argtypes = [CirclePtr]
LIB_MOON._Circle_GetPositionX.restype = ctypes.c_float
LIB_MOON._Circle_GetPositionY.argtypes = [CirclePtr]
LIB_MOON._Circle_GetPositionY.restype = ctypes.c_float

# Функции управления радиусом
LIB_MOON._Circle_SetRadius.argtypes = [CirclePtr, ctypes.c_float]
LIB_MOON._Circle_SetRadius.restype = None
LIB_MOON._Circle_GetRadius.argtypes = [CirclePtr]
LIB_MOON._Circle_GetRadius.restype = ctypes.c_float

# Функции управления поворотом
LIB_MOON._Circle_SetRotation.argtypes = [CirclePtr, ctypes.c_float]
LIB_MOON._Circle_SetRotation.restype = None
LIB_MOON._Circle_GetRotation.argtypes = [CirclePtr]
LIB_MOON._Circle_GetRotation.restype = ctypes.c_float

# Функции управления цветом и стилями
LIB_MOON._Circle_SetColor.argtypes = [CirclePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Circle_SetColor.restype = None
LIB_MOON._Circle_SetOutlineColor.argtypes = [CirclePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Circle_SetOutlineColor.restype = None
LIB_MOON._Circle_SetOutlineThickness.argtypes = [CirclePtr, ctypes.c_float]
LIB_MOON._Circle_SetOutlineThickness.restype = None

# Функции управления масштабом и точкой отсчета
LIB_MOON._Circle_SetScale.argtypes = [CirclePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Circle_SetScale.restype = None
LIB_MOON._Circle_GetScaleX.argtypes = [CirclePtr]
LIB_MOON._Circle_GetScaleX.restype = ctypes.c_float
LIB_MOON._Circle_GetScaleY.argtypes = [CirclePtr]
LIB_MOON._Circle_GetScaleY.restype = ctypes.c_float
LIB_MOON._Circle_SetOrigin.argtypes = [CirclePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Circle_SetOrigin.restype = None
LIB_MOON._Circle_GetOriginX.argtypes = [CirclePtr]
LIB_MOON._Circle_GetOriginX.restype = ctypes.c_float
LIB_MOON._Circle_GetOriginY.argtypes = [CirclePtr]
LIB_MOON._Circle_GetOriginY.restype = ctypes.c_float

# =====================================================================================
# КЛАСС CircleShape - ОСНОВНОЙ КЛАСС ДЛЯ РАБОТЫ С КРУГАМИ
# =====================================================================================

@final
class CircleShape:
    """
    #### Базовый класс для работы с круговыми фигурами

    ---

    :Description:
    - Низкоуровневая обертка для нативного круга из C++
    - Оптимизирован для максимальной производительности
    - Не поддерживает наследование (@final)

    ---

    :Features:
    - Управление радиусом и гладкостью
    - Настройка цвета и контура
    - Преобразования (поворот, масштаб, смещение)
    - Прямой доступ к нативному объекту

    ---

    :Initial State:
    - Начальный радиус: 100 пикселей
    - Центр преобразований: середина круга
    - Цвет: не задан (прозрачный)
    - Контур: толщина 1 пиксель, цвет не задан

    ---

    :Memory Management:
    - Автоматическое создание/удаление нативных ресурсов
    - Защита от утечек памяти в деструкторе
    - Безопасная работа с указателями

    ---

    :Performance:
    - Минимальные накладные расходы при вызовах C++
    - Эффективное использование прокси-объектов
    - Оптимизированные математические операции
    """

    def __init__(self, approximation: int = 30):
        """
        #### Создает новый круг

        ---

        :Description:
        - Инициализирует нативный объект в памяти C++
        - Устанавливает стандартные параметры фигуры
        - Центрирует точку отсчета

        ---

        :Args:
        - approximation (int): Количество точек аппроксимации (≥3)

        ---

        :Raises:
        - ValueError: При approximation < 3

        ---

        :Note:
        - Больше точек = более гладкий круг, но выше нагрузка
        - Рекомендуемые значения: 30-100 для баланса качества/производительности

        ---

        :Internal State:
        - Создает нативный объект через LIB_MOON._Circle_Create()
        - Инициализирует атрибуты цвета и преобразований
        - Автоматически центрирует точку отсчета

        ---

        :Example:
        ```python
        # Круг с 50 точками аппроксимации
        circle = CircleShape(50)

        # Круг со стандартной детализацией (30 точек)
        circle = CircleShape()
        ```
        """
        if approximation < 3:
            raise ValueError("Circle must have at least 3 points")

        self.__approximation = int(approximation)
        self._ptr: ctypes.c_void_p | None = LIB_MOON._Circle_Create(100, int(approximation))
        self.set_origin(100, 100)  # Центрируем точку отсчета

        # Инициализация атрибутов состояния
        self.__outline_color: Color | None = None
        self.__outline_thickness: float = 0
        self.__color: Color | None = COLOR_GRAY
        self.__angle: float = 0.0

    def __str__(self) -> str:
        return f"CircleShape({self.radius})"

    def __del__(self):
        """
        #### Освобождает ресурсы круга

        ---

        :Description:
        - Автоматически вызывается при удалении объекта
        - Удаляет нативный объект из памяти C++
        - Предотвращает утечки памяти

        ---

        :Safety:
        - Проверяет существование указателя
        - Защищает от двойного освобождения
        - Устанавливает указатель в None после удаления

        ---

        :Note:
        - Не вызывайте явно - использует механизм сборки мусора Python
        - Гарантирует корректное освобождение ресурсов C++

        ---

        :Workflow:
        1. Проверяет наличие указателя через hasattr()
        2. Вызывает нативное удаление объекта через LIB_MOON._Circle_Delete()
        3. Обнуляет указатель для предотвращения повторного использования

        ---

        :Example:
        ```python
        # Обычно не вызывается явно
        circle = CircleShape()
        del circle  # Вызовет __del__ автоматически
        ```
        """
        if hasattr(self, '_ptr') and self._ptr:
            LIB_MOON._Circle_Delete(self._ptr)
            self._ptr = None  # Защита от повторного удаления

    # =================================================================================
    # СВОЙСТВА (PROPERTIES) ДЛЯ УДОБНОГО ДОСТУПА К АТРИБУТАМ
    # =================================================================================

    @property
    def position(self) -> ShapePositionProxy:
        """
        #### Прокси-объект для управления позицией круга

        ---

        :Description:
        - Предоставляет удобный интерфейс для работы с координатами
        - Поддерживает поэлементное обновление (x, y)
        - Автоматически синхронизируется с нативным объектом

        ---

        :Returns:
        - ShapePositionProxy: Прокси для управления позицией

        ---

        :Example:
        ```python
        # Установка позиции через прокси
        circle.position.x = 100
        circle.position.y = 200

        # Получение позиции
        x = circle.position.x
        y = circle.position.y
        ```
        """
        return ShapePositionProxy(self)

    @position.setter
    def position(self, position: Vec2T) -> None:
        """
        #### Устанавливает позицию круга через вектор

        ---

        :Description:
        - Альтернативный способ установки позиции
        - Принимает любой тип, совместимый с Vector2Type
        - Делегирует вызов методу set_position()

        ---

        :Args:
        - position (Vector2Type): Вектор новой позиции

        ---

        :Note:
        - Эквивалентно вызову set_position(position)
        - Обеспечивает согласованность интерфейса
        """
        LIB_MOON._Circle_SetPosition(self._ptr, position.x, position.y)

    @property
    def color(self) -> ShapeColorProxy:
        """
        #### Прокси-объект для управления цветом круга

        ---

        :Description:
        - Позволяет независимо управлять компонентами RGBA
        - Обеспечивает проверку допустимости значений
        - Автоматически применяет изменения

        ---

        :Returns:
        - ShapeColorProxy: Прокси для управления цветом

        ---

        :Example:
        ```python
        # Установка цвета через прокси
        circle.color.r = 255
        circle.color.g = 0
        circle.color.b = 0
        circle.color.a = 128

        # Получение текущего цвета
        red = circle.color.r
        alpha = circle.color.a
        ```
        """
        return ShapeColorProxy(self)

    @color.setter
    def color(self, color: Color) -> None:
        """
        #### Устанавливает цвет круга

        ---

        :Description:
        - Альтернативный способ установки цвета
        - Делегирует вызов методу set_color()
        - Поддерживает полную замену цветового объекта

        ---

        :Args:
        - color (Color): Новый цвет круга

        ---

        :Note:
        - Эквивалентно вызову set_color(color)
        - Обновляет все цветовые компоненты одновременно
        """
        self.set_color(color)

    @property
    def radius(self) -> Number:
        """
        #### Текущий радиус круга

        ---

        :Description:
        - Возвращает геометрический радиус в пикселях
        - Не включает влияние масштабирования
        - Только для чтения (используйте setter для изменения)

        ---

        :Returns:
        - Number: Текущий радиус в пикселях

        ---

        :Example:
        ```python
        # Проверка радиуса
        if circle.radius > 100:
            print("Круг слишком большой")
        ```
        """
        return LIB_MOON._Circle_GetRadius(self._ptr)

    @radius.setter
    def radius(self, radius: Number) -> None:
        """
        #### Устанавливает новый радиус круга

        ---

        :Description:
        - Изменяет геометрический размер круга
        - Автоматически обновляет отображение
        - Выполняет проверку допустимости значения

        ---

        :Args:
        - radius (Number): Новый радиус (>0)

        ---

        :Raises:
        - ValueError: При radius < 0

        ---

        :Note:
        - Для автоматической центровки используйте set_origin_radius()
        - Радиус применяется до масштабирования
        """
        if radius < 0:
            raise ValueError("Radius must be positive")

        LIB_MOON._Circle_SetRadius(self._ptr, radius)

    @property
    def origin(self) -> ShapeOriginProxy:
        """
        #### Прокси-объект для управления точкой отсчета

        ---

        :Description:
        - Предоставляет удобный интерфейс для работы с точкой отсчета
        - Позволяет независимо управлять координатами x и y
        - Автоматически синхронизируется с нативным объектом

        ---

        :Returns:
        - ShapeOriginProxy: Прокси для управления точкой отсчета

        ---

        :Example:
        ```python
        # Установка точки отсчета через прокси
        circle.origin.x = 50
        circle.origin.y = 50

        # Получение текущей точки отсчета
        origin_x = circle.origin.x
        origin_y = circle.origin.y
        ```
        """
        return ShapeOriginProxy(self)

    @origin.setter
    def origin(self, origin: Vec2T) -> None:
        """
        #### Устанавливает точку отсчета круга

        ---

        :Description:
        - Альтернативный способ установки точки отсчета
        - Делегирует вызов методу set_origin()
        - Принимает любой тип, совместимый с Vector2Type

        ---

        :Args:
        - origin (Vector2Type): Вектор новой точки отсчета

        ---

        :Note:
        - Эквивалентно вызову set_origin(origin)
        - Обеспечивает согласованность интерфейса
        """
        self.set_origin(origin)

    @property
    def angle(self) -> Number:
        """
        #### Текущий угол поворота круга

        ---

        :Description:
        - Возвращает угол поворота в градусах
        - Значение нормализовано в диапазон 0-360
        - Только для чтения (используйте setter для изменения)

        ---

        :Returns:
        - Number: Угол поворота в градусах

        ---

        :Example:
        ```python
        # Проверка угла поворота
        if circle.angle == 0:
            print("Круг не повернут")
        ```
        """
        return self.__angle

    @angle.setter
    def angle(self, angle: Number) -> None:
        """
        #### Устанавливает угол поворота круга

        ---

        :Description:
        - Поворачивает круг относительно точки отсчета
        - Автоматически нормализует угол в диапазон 0-360
        - Делегирует вызов методу set_angle()

        ---

        :Args:
        - angle (Number): Новый угол поворота в градусах

        ---

        :Note:
        - Эквивалентно вызову set_angle(angle)
        - Положительные значения - поворот по часовой стрелке
        """
        self.set_angle(angle)

    @property
    def outline_color(self) -> Color | None:
        """
        #### Текущий цвет контура круга

        ---

        :Description:
        - Возвращает последний установленный цвет контура
        - None означает, что контур не установлен
        - Только для чтения (используйте setter для изменения)

        ---

        :Returns:
        - Color | None: Цвет контура или None

        ---

        :Example:
        ```python
        # Проверка цвета контура
        if circle.outline_color is None:
            print("Контур не установлен")
        ```
        """
        return self.get_outline_color()

    @outline_color.setter
    def outline_color(self, color: Color) -> None:
        """
        #### Устанавливает цвет контура круга

        ---

        :Description:
        - Определяет цвет границы круга
        - Работает только при толщине контура > 0
        - Делегирует вызов методу set_outline_color()

        ---

        :Args:
        - color (Color): Новый цвет контура

        ---

        :Note:
        - Эквивалентно вызову set_outline_color(color)
        - Для отображения контура требуется установить толщину
        """
        self.set_outline_color(color)

    @property
    def outline_thickness(self) -> Number:
        """
        #### Текущая толщина контура круга

        ---

        :Description:
        - Возвращает толщину контура в пикселях
        - 0 означает, что контур не отображается
        - Только для чтения (используйте setter для изменения)

        ---

        :Returns:
        - Number: Толщина контура в пикселях

        ---

        :Example:
        ```python
        # Проверка толщины контура
        if circle.outline_thickness == 0:
            print("Контур отключен")
        ```
        """
        return self.__outline_thickness

    @outline_thickness.setter
    def outline_thickness(self, thickness: Number) -> None:
        """
        #### Устанавливает толщину контура круга

        ---

        :Description:
        - Определяет толщину отображаемой границы
        - 0 отключает отображение контура
        - Делегирует вызов методу set_outline_thickness()

        ---

        :Args:
        - thickness (Number): Новая толщина контура (≥0)

        ---

        :Note:
        - Эквивалентно вызову set_outline_thickness(thickness)
        - Рекомендуемая толщина < 1/2 радиуса круга
        """
        self.set_outline_thickness(thickness)

    # =================================================================================
    # ОСНОВНЫЕ МЕТОДЫ УПРАВЛЕНИЯ КРУГОМ
    # =================================================================================

    def get_approximation(self) -> int:
        """
        #### Возвращает количество точек аппроксимации круга

        ---

        :Description:
        - Определяет гладкость отображения круга
        - Больше точек = более плавный контур
        - Меньше точек = лучшая производительность

        ---

        :Returns:
        - int: Текущее количество точек контура

        ---

        :Note:
        - Устанавливается при создании объекта
        - Для изменения нужно создать новый круг

        ---

        :Example:
        ```python
        circle = CircleShape(50)
        print(circle.get_approximation())  # 50

        # Типичные значения:
        # - 30: базовое качество
        # - 100: высокое качество
        # - 10: низкое качество (многоугольник)
        ```
        """
        return self.__approximation

    def copy(self) -> "CircleShape":
        """
        #### Создает полную независимую копию круга

        ---

        :Description:
        - Создает новый объект CircleShape с идентичными параметрами
        - Глубоко копирует все атрибуты:
        * Точность аппроксимации
        * Визуальные свойства (цвет, контур)
        * Геометрические преобразования
        * Состояние отображения

        ---

        :Returns:
        - CircleShape: Новая независимая копия круга

        ---

        :Example:
        ```python
        original = CircleShape(30)
        original.set_color(Color.RED)

        # Создание копии
        duplicate = original.copy()

        # Модификация копии
        duplicate.set_color(Color.BLUE)  # Не влияет на оригинал
        ```

        :Workflow:
        1. Создает новый круг с тем же количеством точек
        2. Копирует все визуальные атрибуты
        3. Применяет одинаковые преобразования
        4. Возвращает готовую копию

        :Note:
        - Копия использует собственные нативные ресурсы
        - Изменения копии не затрагивают оригинал
        - Для сложных объектов предпочтительнее copy() над созданием вручную
        """
        # Создаем базовую копию с одинаковым уровнем детализации
        _c = CircleShape(self.get_approximation())

        # Копирование стилей отображения
        if (outline_color := self.get_outline_color()) is not None:
            _c.set_outline_color(outline_color)
        _c.set_outline_thickness(self.get_outline_thickness())

        # Копирование геометрических преобразований
        _c.set_origin(*self.get_origin().xy)
        _c.set_angle(self.get_angle())
        _c.set_scale(*self.get_scale().xy)
        _c.set_position(*self.get_position().xy)

        # Копирование основного цвета с проверкой
        if (fill_color := self.get_color()) is not None:
            _c.set_color(fill_color)

        return _c

    def set_origin_radius(self, radius: float) -> Self:
        """
        #### Устанавливает радиус с автоматической центровкой

        ---

        :Description:
        - Устанавливает новый радиус круга
        - Автоматически центрирует точку отсчета
        - Оптимизировано для преобразований (вращение/масштаб)
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - radius (float): Новый радиус (>0)

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Круг радиусом 50 с центром в середине
        circle.set_origin_radius(50)

        # Комбинирование с другими методами
        circle.set_origin_radius(100).set_angle(45)
        ```

        :Note:
        - Эквивалентно последовательному вызову set_radius() и set_origin()
        - Центровка упрощает работу с преобразованиями
        """
        radius = float(radius)
        if radius <= 0:
            raise ValueError("Radius must be positive")

        self.set_radius(radius)
        self.set_origin(radius, radius)
        return self

    def get_ptr(self) -> ctypes.c_void_p | None:
        """
        #### Возвращает указатель на нативный объект C++

        ---

        :Description:
        - Предоставляет доступ к низкоуровневому объекту
        - Для внутреннего использования в PySGL
        - Не изменяйте объект напрямую

        ---

        :Returns:
        - ctypes.c_void_p | None: Указатель на объект Circle в памяти C++

        ---

        :Example:
        ```python
        # Для передачи в нативные функции
        native_function(circle.get_ptr())
        ```

        :Warning:
        - Избегайте прямых манипуляций с указателем
        - Используйте только для интеграции с API PySGL
        - Возвращает None если объект был удален
        """
        return self._ptr

    # =================================================================================
    # МЕТОДЫ УПРАВЛЕНИЯ ПОЗИЦИЕЙ И ПРЕОБРАЗОВАНИЯМИ
    # =================================================================================

    @overload
    def set_position(self, arg1: float, arg2: float) -> Self:
        """
        #### Устанавливает позицию круга через координаты

        ---

        :Description:
        - Позиционирует круг по абсолютным координатам
        - Учитывает текущие преобразования (масштаб, поворот)
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - x (float): Горизонтальная координата центра
        - y (float): Вертикальная координата центра

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Позиционирование по координатам
        circle.set_position(150.5, 200.0)

        # Комбинирование методов
        circle.set_position(100, 100).set_angle(45)
        ```
        """
        ...

    @overload
    def set_position(self, arg1: Vec2f, arg2: None = None) -> Self:
        """
        #### Устанавливает позицию круга через вектор

        ---

        :Description:
        - Позиционирует круг по вектору координат
        - Эквивалентно set_position(position.x, position.y)
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - position (Vector2f): Вектор позиции {x, y}

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Позиционирование через вектор
        pos = Vector2f(150.5, 200.0)
        circle.set_position(pos)
        ```
        """
        ...

    def set_position(self, arg1: Union[float, Vec2f], arg2: Optional[float] = None) -> Self:
        """
        #### Основная реализация установки позиции

        ---

        :Description:
        - Обрабатывает оба варианта вызова (координаты или вектор)
        - Выполняет проверку типов аргументов
        - Делегирует вызов нативной функции

        ---

        :Args:
        - arg1: Координата X или вектор позиции
        - arg2: Координата Y или None

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Raises:
        - ValueError: При недопустимых аргументах

        ---

        :Note:
        - Координаты относятся к центру круга
        - Учитывает текущую точку отсчета
        - Немедленно применяет изменения к отображению
        """
        if isinstance(arg1, (Vec2f, Vec2i)) and arg2 is None:
            x, y = float(arg1.x), float(arg1.y)
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            x, y = float(arg1), float(arg2)
        else:
            raise ValueError(
                "Invalid arguments. "
                "Expected either (x: float, y: float) or (position: Vector2f), "
                f"got ({type(arg1).__name__}, {type(arg2).__name__})"
            )

        LIB_MOON._Circle_SetPosition(self._ptr, x, y)
        return self

    def get_position(self) -> Vec2f:
        """
        #### Возвращает текущую позицию центра круга

        ---

        :Description:
        - Возвращает абсолютные координаты центра
        - Учитывает все примененные преобразования
        - Координаты в пикселях относительно окна

        ---

        :Returns:
        - Vector2f: Вектор позиции {x, y}

        ---

        :Example:
        ```python
        pos = circle.get_position()
        print(f"Круг находится в ({pos.x:.1f}, {pos.y:.1f})")

        # Использование в расчетах
        distance = (circle.get_position() - target.get_position()).length()
        ```
        """
        x = LIB_MOON._Circle_GetPositionX(self._ptr)
        y = LIB_MOON._Circle_GetPositionY(self._ptr)
        return Vec2f(x, y)

    def set_radius(self, radius: float) -> Self:
        """
        #### Устанавливает новый радиус круга

        ---

        :Description:
        - Изменяет геометрический размер круга
        - Автоматически обновляет отображение
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - radius (float): Новый радиус (>0)

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Установить радиус 50 пикселей
        circle.set_radius(50.0)

        # Анимация увеличения
        circle.set_radius(circle.get_radius() + 0.5)
        ```

        :Note:
        - Для изменения точки отсчета используйте set_origin_radius()
        - Радиус применяется до масштабирования
        """
        if radius < 0:
            raise ValueError("Radius must be positive")

        LIB_MOON._Circle_SetRadius(self._ptr, radius)
        return self

    def get_radius(self) -> float:
        """
        #### Возвращает текущий радиус круга

        ---

        :Description:
        - Возвращает фактический радиус в пикселях
        - Не включает масштабирование
        - Значение всегда положительное

        ---

        :Returns:
        - float: Текущий радиус (>0)

        ---

        :Example:
        ```python
        # Проверить размер круга
        if circle.get_radius() > 100:
            print("Круг слишком большой")

        # Расчет площади
        area = math.pi * circle.get_radius() ** 2
        ```
        """
        return LIB_MOON._Circle_GetRadius(self._ptr)

    def set_angle(self, angle: float) -> Self:
        """
        #### Устанавливает угол поворота круга

        ---

        :Description:
        - Поворачивает круг относительно точки отсчета
        - Угол в градусах (0-360)
        - Положительные значения - по часовой стрелке
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - angle (float): Угол поворота в градусах

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Поворот на 45 градусов
        circle.set_angle(45.0)

        # Плавное вращение
        circle.set_angle(circle.get_angle() + 0.5)
        ```
        """
        angle = float(angle) % 360  # Нормализация угла
        self.__angle = angle
        LIB_MOON._Circle_SetRotation(self._ptr, angle)
        return self

    def get_angle(self) -> float:
        """
        #### Возвращает текущий угол поворота

        ---

        :Description:
        - Возвращает значение в градусах (0-360)
        - Учитывает последний вызов set_angle()
        - Не зависит от системы координат

        ---

        :Returns:
        - float: Текущий угол поворота

        ---

        :Example:
        ```python
        # Проверка ориентации
        if 90 < circle.get_angle() < 270:
            print("Круг перевернут")
        ```
        """
        return LIB_MOON._Circle_GetRotation(self._ptr)

    # =================================================================================
    # МЕТОДЫ УПРАВЛЕНИЯ ЦВЕТОМ И СТИЛЯМИ
    # =================================================================================

    def set_color(self, color: Color) -> Self:
        """
        #### Устанавливает основной цвет круга

        ---

        :Description:
        - Определяет цвет заливки круга
        - Поддерживает прозрачность (альфа-канал)
        - Автоматически обновляет отображение
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - color (Color): Цвет в формате RGBA

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Сплошной красный цвет
        circle.set_color(Color.RED)

        # Полупрозрачный синий
        circle.set_color(Color(0, 0, 255, 128))
        ```

        :Note:
        - None отключает заливку (полная прозрачность)
        - Цвет кэшируется в Python-объекте
        """
        LIB_MOON._Circle_SetColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__color = color
        return self

    def get_color(self) -> Color | None:
        """
        #### Возвращает текущий цвет заливки

        ---

        :Description:
        - Возвращает последний установленный цвет
        - None означает отсутствие заливки

        ---

        :Returns:
        - Color: Текущий цвет или None

        ---

        :Example:
        ```python
        # Проверка цвета
        if circle.get_color() == Color.GREEN:
            print("Круг зеленый")
        ```
        """
        return self.__color

    def set_outline_color(self, color: Color) -> Self:
        """
        #### Устанавливает цвет границы круга

        ---

        :Description:
        - Определяет цвет контурной линии
        - Работает только при толщине > 0
        - Поддерживает прозрачность
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - color (Color): Цвет в формате RGBA

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Черная граница
        circle.set_outline_color(Color.BLACK)

        # Полупрозрачная граница
        circle.set_outline_color(Color(255, 255, 255, 128))
        ```
        """
        LIB_MOON._Circle_SetOutlineColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__outline_color = color
        return self

    def get_outline_color(self) -> Color | None:
        """
        #### Возвращает текущий цвет границы

        ---

        :Description:
        - Возвращает последний установленный цвет
        - None означает отсутствие границы

        ---

        :Returns:
        - Color: Текущий цвет или None

        ---

        :Example:
        ```python
        # Проверка цвета границы
        if circle.get_outline_color() is None:
            print("Граница отключена")
        ```
        """
        return self.__outline_color

    def set_outline_thickness(self, thickness: float) -> Self:
        """
        #### Устанавливает толщину границы круга

        ---

        :Description:
        - Определяет толщину отображаемой границы
        - 0 = граница не отображается
        - Отрисовывается внутрь от контура фигуры
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - thickness (float): Толщина в пикселях (≥0)

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Тонкая граница
        circle.set_outline_thickness(1.5)

        # Толстая граница (максимум 1/2 радиуса)
        circle.set_outline_thickness(min(10, circle.get_radius()/2))
        ```

        :Note:
        - Рекомендуемая толщина < 1/2 радиуса
        - При thickness > radius граница может отображаться некорректно
        """
        thickness = max(0.0, float(thickness))  # Гарантируем неотрицательное значение
        LIB_MOON._Circle_SetOutlineThickness(self._ptr, thickness)
        self.__outline_thickness = thickness
        return self

    def get_outline_thickness(self) -> float:
        """
        #### Возвращает текущую толщину границы

        ---

        :Description:
        - Возвращает последнее установленное значение
        - 0 означает отсутствие границы

        ---

        :Returns:
        - float: Текущая толщина в пикселях

        ---

        :Example:
        ```python
        # Адаптивное изменение толщины
        current = circle.get_outline_thickness()
        if current > 0:
            circle.set_outline_thickness(current * 1.1)
        ```
        """
        return self.__outline_thickness

    # =================================================================================
    # МЕТОДЫ УПРАВЛЕНИЯ МАСШТАБОМ И ТОЧКОЙ ОТСЧЕТА
    # =================================================================================

    @overload
    def set_scale(self, arg1: float, arg2: None = None) -> Self:
        """
        #### Равномерно масштабирует круг

        ---

        :Description:
        - Применяет одинаковый масштаб по обеим осям
        - 1.0 - исходный размер
        - меньше 1.0 - уменьшение
        - больше 1.0 - увеличение
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - scale (float): Коэффициент масштабирования (>0)

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Увеличить в 2 раза
        circle.set_scale(2.0)

        # Уменьшить вдвое
        circle.set_scale(0.5)
        ```
        """
        ...

    @overload
    def set_scale(self, arg1: float, arg2: float) -> Self:
        """
        #### Масштабирует круг по осям

        ---

        :Description:
        - Позволяет задать разный масштаб для X и Y
        - Может вызывать искажение (эллипс)
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - scale_x (float): Масштаб по горизонтали (>0)
        - scale_y (float): Масштаб по вертикали (>0)

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Растянуть по горизонтали
        circle.set_scale(2.0, 1.0)

        # Сжать по вертикали
        circle.set_scale(1.0, 0.5)
        ```
        """
        ...

    def set_scale(self, arg1: float, arg2: Optional[float] = None) -> Self:
        """
        #### Основная реализация масштабирования

        ---

        :Description:
        - Обрабатывает оба варианта вызова (равномерный и анизотропный)
        - Выполняет проверку допустимости значений
        - Делегирует вызов нативной функции

        ---

        :Args:
        - arg1: Коэффициент масштаба или масштаб по X
        - arg2: Масштаб по Y или None

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Raises:
        - ValueError: При недопустимых значениях масштаба

        ---

        :Note:
        - Масштаб применяется относительно точки отсчета
        - Отрицательные значения создают зеркальное отражение
        - Нулевые значения запрещены для предотвращения вырождения
        """
        if arg2 is None:
            scale_x = scale_y = float(arg1)
        else:
            scale_x, scale_y = float(arg1), float(arg2)

        if scale_x == 0 or scale_y == 0:
            raise ValueError("Scale values cannot be zero")

        LIB_MOON._Circle_SetScale(self._ptr, scale_x, scale_y)
        return self

    def get_scale(self) -> Vec2f:
        """
        #### Возвращает текущий масштаб круга

        ---

        :Description:
        - Возвращает отдельные коэффициенты для X и Y
        - {1,1} означает исходный размер
        - Значения могут быть отрицательными (отражение)

        ---

        :Returns:
        - Vector2f: Масштаб по осям {x, y}

        ---

        :Example:
        ```python
        scale = circle.get_scale()
        if scale.x != scale.y:
            print("Круг искажен в эллипс")
        ```
        """
        return Vec2f(
            LIB_MOON._Circle_GetScaleX(self._ptr),
            LIB_MOON._Circle_GetScaleY(self._ptr)
        )

    @overload
    def set_origin(self, arg1: Vec2T, arg2: None = None) -> Self:
        """
        #### Устанавливает точку отсчета через вектор

        ---

        :Description:
        - Принимает готовый 2D-вектор
        - Удобно для передачи предварительно созданных координат
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - origin (Vector2f): Вектор с координатами {x, y}

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        circle.set_origin(Vector2f(10, 20))
        ```
        """
        ...

    @overload
    def set_origin(self, arg1: float, arg2: float) -> Self:
        """
        #### Устанавливает точку отсчета через координаты

        ---

        :Description:
        - Принимает отдельные координаты X и Y
        - Подходит для прямого указания значений
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - x (float): Координата X точки отсчета
        - y (float): Координата Y точки отсчета

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        circle.set_origin(10.5, 15.0)
        ```
        """
        ...

    def set_origin(self, arg1: Union[Vec2T, float], arg2: Optional[float] = None) -> Self:
        """
        #### Основная реализация установки точки отсчета

        ---

        :Description:
        - Обрабатывает оба варианта вызова (вектор или координаты)
        - Выполняет проверку типов аргументов
        - Делегирует вызов нативной функции

        ---

        :Args:
        - arg1: Вектор или координата X
        - arg2: Координата Y или None

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Raises:
        - TypeError: При неверном типе аргументов

        ---

        :Note:
        - Координаты интерпретируются относительно локальной системы
        - Отрицательные значения допустимы
        - Точка отсчета влияет на все преобразования (поворот, масштаб)
        """
        if isinstance(arg1, Vec2f):
            x, y = arg1.x, arg1.y
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            x, y = float(arg1), float(arg2)
        else:
            raise TypeError("Invalid argument types for set_origin")

        LIB_MOON._Circle_SetOrigin(self._ptr, x, y)
        return self

    def get_origin(self) -> Vec2f:
        """
        #### Возвращает текущую точку отсчета

        ---

        :Description:
        - Возвращает координаты относительно локальной системы
        - Может отличаться от геометрического центра
        - Используется как центр преобразований

        ---

        :Returns:
        - Vector2f: Вектор с координатами {x, y}

        ---

        :Example:
        ```python
        origin = circle.get_origin()
        print(f"Точка отсчета: ({origin.x}, {origin.y})")
        ```
        """
        x = LIB_MOON._Circle_GetOriginX(self._ptr)
        y = LIB_MOON._Circle_GetOriginY(self._ptr)
        return Vec2f(x, y)

    # =================================================================================
    # МЕТОДЫ ПЕРЕМЕЩЕНИЯ И ТРАНСФОРМАЦИЙ
    # =================================================================================

    @final
    def move(self, offset: Vec2f) -> Self:
        """
        #### Перемещает круг на заданный вектор

        ---

        :Description:
        - Добавляет вектор смещения к текущей позиции
        - Учитывает все текущие преобразования
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - offset (Vector2f): Вектор смещения {x, y}

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Сместить на 10 пикселей вправо и 5 вниз
        circle.move(Vector2f(10, 5))

        # Комбинирование с другими методами
        circle.move(Vector2f(10, 0)).set_angle(45)
        ```

        :Note:
        - Относительное перемещение (не абсолютная позиция)
        - Эквивалентно set_position(get_position() + offset)
        - Удобно для анимаций и инкрементальных перемещений
        """
        new_pos = self.get_position() + offset
        self.set_position(new_pos)
        return self
