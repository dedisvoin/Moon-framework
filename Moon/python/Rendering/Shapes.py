
import ctypes
from typing import Self, Final, final

from Moon.python.Types import *
from Moon.python.Colors import *
from Moon.python.Vectors import Vector2f, Vector2i, Vector2Type, Vector2TypeTuple
from Moon.python.Rendering.Vertexes import Vertex2d, VertexList, VertexListTypes, NativeVertex2dPtr

from Moon.python.utils import find_library

# Псевдоним для типа указателя на шейп прямоугольника ======= +
RectanglePtr: Final[type[ctypes.c_void_p]] = ctypes.c_void_p  #
# =========================================================== +

# Тип указателя на шейп прямоугольника ====================== +
RectanglePtrType = type[RectanglePtr]                         #
# =========================================================== +

# Загружаем DLL библиотеку
try:
    LIB_MOON: Final[ctypes.CDLL] = ctypes.CDLL(find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")


LIB_MOON._Rectangle_Create.restype = RectanglePtr
LIB_MOON._Rectangle_Create.argtypes = [ctypes.c_float, ctypes.c_float]
LIB_MOON._Rectangle_GetPositionX.restype = ctypes.c_float
LIB_MOON._Rectangle_GetPositionX.argtypes = [RectanglePtr]
LIB_MOON._Rectangle_GetPositionY.restype = ctypes.c_float
LIB_MOON._Rectangle_GetPositionY.argtypes = [RectanglePtr]
LIB_MOON._Rectangle_GetWidth.restype = ctypes.c_float
LIB_MOON._Rectangle_GetWidth.argtypes = [RectanglePtr]
LIB_MOON._Rectangle_GetHeight.restype = ctypes.c_float
LIB_MOON._Rectangle_GetHeight.argtypes = [RectanglePtr]
LIB_MOON._Rectangle_SetPosition.restype = None
LIB_MOON._Rectangle_SetPosition.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Rectangle_SetColor.restype = None
LIB_MOON._Rectangle_SetColor.argtypes = [RectanglePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Rectangle_SetOrigin.restype = None
LIB_MOON._Rectangle_SetOrigin.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Rectangle_SetSize.restype = None
LIB_MOON._Rectangle_SetSize.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Rectangle_SetRotation.restype = None
LIB_MOON._Rectangle_SetRotation.argtypes = [RectanglePtr, ctypes.c_float]
LIB_MOON._Rectangle_SetOutlineThickness.restype = None
LIB_MOON._Rectangle_SetOutlineThickness.argtypes = [RectanglePtr, ctypes.c_float]
LIB_MOON._Rectangle_SetOutlineColor.restype = None
LIB_MOON._Rectangle_SetOutlineColor.argtypes = [RectanglePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Rectangle_SetScale.restype = None
LIB_MOON._Rectangle_SetScale.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]
LIB_MOON._Rectangle_Delete.restype = None
LIB_MOON._Rectangle_Delete.argtypes = [RectanglePtr]

@final
class RectangleShape:
    """
    #### Базовый класс для работы с прямоугольными фигурами

    ---

    :Description:
    - Низкоуровневая обертка для нативного прямоугольника из C++
    - Оптимизирован для максимальной производительности
    - Не поддерживает наследование (@final)

    ---

    :Features:
    - Управление размерами и геометрией
    - Настройка цвета и контура
    - Преобразования (поворот, масштаб, смещение)
    - Прямой доступ к нативному объекту

    ---

    :Note:
    - Все графические операции выполняются на стороне C++
    - Python-атрибуты синхронизируются с нативным объектом при изменениях
    """

    @final
    def __init__(self, width: Number = 1, height: Number = 1):
        """
        #### Создает новый прямоугольник

        ---

        :Description:
        - Инициализирует нативный объект в памяти C++
        - Устанавливает начальные параметры фигуры
        - Создает Python-обертку для управления

        ---

        :Args:
        - width (float): Начальная ширина прямоугольника (>0)
        - height (float): Начальная высота прямоугольника (>0)

        ---

        :Raises:
        - ValueError: При недопустимых размерах

        ---

        :Workflow:
        1. Создает нативный объект через LIB_PYSGL
        2. Инициализирует Python-атрибуты
        3. Устанавливает стандартные значения

        ---

        :Example:
        ```python
        # Создать прямоугольник 100x50
        rect = BaseRectangleShape(100.0, 50.0)
        ```
        """
        # Проверка корректности размеров
        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive")

        # Создание нативного объекта
        self._ptr = LIB_MOON._Rectangle_Create(float(width), float(height))

        # Инициализация Python-атрибутов
        self.__color: Color | None = None          # Основной цвет (None = прозрачный)
        self.__outline_color: Color | None = None  # Цвет контура
        self.__outline_thickness: float = 0        # Толщина контура
        self.__origin: Vector2f = Vector2f(0, 0)   # Точка преобразований
        self.__angle: float = 0                    # Угол поворота (градусы)
        self.__scale: Vector2f = Vector2f.one()    # Масштаб по осям

    @property
    def position(self) -> Vector2Type:
        return Vector2f(
            LIB_MOON._Rectangle_GetPositionX(self._ptr),
            LIB_MOON._Rectangle_GetPositionY(self._ptr)
        )

    @position.setter
    def position(self, position: Vector2Type) -> None:
        self.set_position(position)

    @property
    def color(self) -> Color | None:
        return self.get_color()
    
    @color.setter
    def color(self, color: Color) -> None:
        self.set_color(color)

    @property
    def size(self) -> Vector2Type:
        return Vector2f(
            LIB_MOON._Rectangle_GetWidth(self._ptr),
            LIB_MOON._Rectangle_GetHeight(self._ptr)
        )
    
    @size.setter
    def size(self, size: Vector2Type) -> None:
        self.set_size(size)

    @property
    def origin(self) -> Vector2Type:
        return self.get_origin()
    
    @origin.setter
    def origin(self, origin: Vector2Type) -> None:
        self.set_origin(origin)
    
    @property
    def angle(self) -> Number:
        return self.__angle
    
    @angle.setter
    def angle(self, angle: Number) -> None:
        self.set_angle(angle)

    @property
    def outline_color(self) -> Color | None:
        return self.get_outline_color()
    
    @outline_color.setter
    def outline_color(self, color: Color) -> None:
        self.set_outline_color(color)

    @property
    def outline_thickness(self) -> Number:
        return self.__outline_thickness
    
    @outline_thickness.setter
    def outline_thickness(self, thickness: Number) -> None:
        self.set_outline_thickness(thickness)

    @final
    def get_ptr(self) -> RectanglePtrType | None:
        """
        #### Возвращает указатель на нативный объект C++

        ---

        :Description:
        - Предоставляет прямой доступ к низкоуровневому объекту
        - Используется для интеграции с нативным кодом
        - Для внутреннего использования в PySGL

        ---

        :Returns:
        - RectanglePtrType | None: Указатель на объект Rectangle в памяти C++

        ---

        :Note:
        - Не изменяйте объект напрямую через указатель
        - Используйте только для передачи в API PySGL

        ---

        :Example:
        ```python
        # Передать указатель в нативную функцию
        native_function(rect.get_ptr())
        ```
        """
        return self._ptr

    @final
    def __str__(self) -> str:
        """
        #### Возвращает строковое представление прямоугольника

        ---

        :Description:
        - Формат: BaseRectangleShape(x, y, width, height)
        - Показывает текущие позицию и размеры
        - Не включает другие атрибуты (цвет, поворот и т.д.)

        ---

        :Returns:
        - str: Информационная строка о состоянии объекта

        ---

        :Example:
        ```python
        rect = BaseRectangleShape(100, 50)
        print(str(rect))  # "BaseRectangleShape(0.0, 0.0, 100.0, 50.0)"
        ```
        """
        pos = self.get_position()
        size = self.get_size()
        return f"BaseRectangleShape({pos.x}, {pos.y}, {size.x}, {size.y})"

    @final
    def __repr__(self) -> str:
        """
        #### Возвращает формальное строковое представление

        ---

        :Description:
        - Совпадает с __str__ для удобства
        - Позволяет eval(repr(obj)) для создания копии
        - Формат: BaseRectangleShape(x, y, width, height)

        ---

        :Returns:
        - str: Строка, пригодная для воссоздания объекта

        ---

        :Example:
        ```python
        rect = BaseRectangleShape(100, 50)
        print(repr(rect))  # "BaseRectangleShape(0.0, 0.0, 100.0, 50.0)"
        ```
        """
        return self.__str__()

    @final
    def __del__(self):
        """
        #### Освобождает ресурсы прямоугольника

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
        """
        if hasattr(self, '_ptr') and self._ptr:
            LIB_MOON._Rectangle_Delete(self._ptr)
            self._ptr = None


    @overload
    def set_position(self, arg1: Number, arg2: Number) -> Self:
        """
        #### Устанавливает позицию прямоугольника через координаты

        ---

        :Description:
        - Позиционирует прямоугольник по абсолютным координатам
        - Учитывает текущие преобразования (масштаб, поворот, точку отсчета)
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - x (float): Горизонтальная координата (в пикселях)
        - y (float): Вертикальная координата (в пикселях)

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Позиционирование по координатам
        rect.set_position(150.5, 200.0)
        ```
        """
        ...


    @overload
    def set_position(self, arg1: Vector2f | Vector2i) -> Self:
        """
        #### Устанавливает позицию прямоугольника через вектор

        ---

        :Description:
        - Позиционирует прямоугольник по вектору координат
        - Эквивалентно set_position(vector.x, vector.y)
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - vector (Vector2f): Вектор позиции {x, y}

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Позиционирование через вектор
        position = Vector2f(150.5, 200.0)
        rect.set_position(position)
        ```
        """
        ...


    def set_position(self, arg1: Union[Number, Vector2f | Vector2i], arg2: Optional[Number] = None) -> Self:
        """
        #### Основная реализация установки позиции

        ---

        :Description:
        - Обрабатывает оба варианта вызова (координаты или вектор)
        - Преобразует аргументы в нативный формат
        - Вызывает соответствующий метод C++

        ---

        :Raises:
        - ValueError: При недопустимых аргументах

        ---

        :Note:
        - Внутренний метод - используйте перегруженные версии
        """
        if isinstance(arg1, (Vector2f, Vector2i)) and arg2 is None:
            LIB_MOON._Rectangle_SetPosition(self._ptr, float(arg1.x), float(arg1.y))
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            LIB_MOON._Rectangle_SetPosition(self._ptr, float(arg1), float(arg2))
        else:
            raise ValueError(
                "Invalid arguments. "
                "Expected either (x: float, y: float) or (vector: Vector2f), "
                f"got ({type(arg1).__name__}, {type(arg2).__name__})"
            )
        return self

    @final
    def get_position(self) -> Vector2f:
        """
        #### Возвращает текущую позицию прямоугольника

        ---

        :Description:
        - Возвращает абсолютные координаты верхнего левого угла
        - Учитывает все примененные преобразования
        - Координаты в пикселях относительно окна

        ---

        :Returns:
        - Vector2f: Вектор позиции {x, y}

        ---

        :Example:
        ```python
        pos = rect.get_position()
        print(f"Прямоугольник находится в ({pos.x}, {pos.y})")
        ```
        """
        x = LIB_MOON._Rectangle_GetPositionX(self._ptr)
        y = LIB_MOON._Rectangle_GetPositionY(self._ptr)
        return Vector2f(x, y)

    @final
    def set_color(self, color: Color | None) -> Self:
        """
        #### Устанавливает цвет заливки прямоугольника

        ---

        :Description:
        - Определяет основной цвет отрисовки
        - Поддерживает прозрачность через альфа-канал
        - Автоматически обновляет нативный объект

        ---

        :Args:
        - color (Color): Цвет в формате RGBA

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Установить синий полупрозрачный цвет
        rect.set_color(Color(0, 0, 255, 128))
        ```
        """
        if color is None:
            LIB_MOON._Rectangle_SetColor(self._ptr, 0, 0, 0, 0)
        else:
            LIB_MOON._Rectangle_SetColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__color = color
        return self

    @final
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
        if rect.get_color() == Color.RED:
            print("Прямоугольник красный")
        ```
        """
        return self.__color


    @overload
    def set_origin(self, arg1: Number, arg2: Number) -> Self:
        """
        #### Устанавливает точку отсчета через координаты

        ---

        :Description:
        - Определяет центр преобразований (поворот/масштаб)
        - Относительно левого верхнего угла прямоугольника
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - x (float): Горизонтальное смещение точки отсчета
        - y (float): Вертикальное смещение точки отсчета

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Установить центр в середине прямоугольника
        rect.set_origin(width/2, height/2)
        ```
        """
        ...


    @overload
    def set_origin(self, arg1: Vector2f) -> Self:
        """
        #### Устанавливает точку отсчета через вектор

        ---

        :Description:
        - Определяет центр преобразований (поворот/масштаб)
        - Эквивалентно set_origin(vector.x, vector.y)
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - vector (Vector2f): Вектор смещения {x, y}

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Центр преобразований через вектор
        origin = Vector2f(50, 50)
        rect.set_origin(origin)
        ```
        """
        ...

    @final
    def set_origin(self, arg1: Union[Number, Vector2f], arg2: Optional[Number] = None) -> Self:
        """
        #### Основная реализация установки точки отсчета

        ---

        :Description:
        - Обрабатывает оба варианта вызова (координаты или вектор)
        - Синхронизирует состояние с нативным объектом
        - Обновляет локальный атрибут origin

        ---

        :Raises:
        - ValueError: При недопустимых аргументах

        ---

        :Note:
        - Координаты относительно левого верхнего угла фигуры
        """
        if isinstance(arg1, Vector2f) and arg2 is None:
            x, y = float(arg1.x), float(arg1.y)
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            x, y = float(arg1), float(arg2)
        else:
            raise ValueError(
                "Invalid arguments. "
                "Expected either (x: float, y: float) or (vector: Vector2f | Vector2i), "
                f"got ({type(arg1).__name__}, {type(arg2).__name__})"
            )

        LIB_MOON._Rectangle_SetOrigin(self._ptr, x, y)
        self.__origin.x = x
        self.__origin.y = y
        return self

    @final
    def get_origin(self) -> Vector2f:
        """
        #### Возвращает текущую точку отсчета

        ---

        :Description:
        - Возвращает точку, относительно которой применяются преобразования
        - Координаты относительно левого верхнего угла прямоугольника
        - Возвращает копию для безопасности данных

        ---

        :Returns:
        - Vector2f: Точка отсчета {x, y}

        ---

        :Example:
        ```python
        origin = rect.get_origin()
        print(f"Точка отсчета: ({origin.x}, {origin.y})")
        ```
        """
        return self.__origin.copy()

    @overload
    def set_size(self, arg1: Number, arg2: Number) -> Self:
        """
        #### Устанавливает размер прямоугольника через параметры

        ---

        :Description:
        - Изменяет геометрические размеры фигуры
        - Не влияет на текущие преобразования
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - width (float): Новая ширина (>0)
        - height (float): Новая высота (>0)

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Установить размер 200x100
        rect.set_size(200.0, 100.0)
        ```
        """
        ...


    @overload
    def set_size(self, arg1: Vector2f | Vector2i) -> Self:
        """
        #### Устанавливает размер прямоугольника через вектор

        ---

        :Description:
        - Изменяет геометрические размеры фигуры
        - Эквивалентно set_size(size.x, size.y)
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - size (Vector2f): Новые размеры {width, height}

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Установить размер через вектор
        rect.set_size(Vector2f(200.0, 100.0))
        ```
        """
        ...

    @final
    def set_size(self, arg1: Union[Number, Vector2f | Vector2i], arg2: Optional[Number] = None) -> Self:
        """
        #### Основная реализация изменения размера

        ---

        :Raises:
        - ValueError: При недопустимых размерах

        ---

        :Note:
        - Минимальный размер 1x1 пиксель
        """
        if isinstance(arg1, Vector2f) and arg2 is None:
            width, height = float(arg1.x), float(arg1.y)
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            width, height = float(arg1), float(arg2)
        else:
            raise ValueError(
                "Invalid arguments. "
                "Expected either (width: float, height: float) or (size: Vector2f), "
                f"got ({type(arg1).__name__}, {type(arg2).__name__})"
            )

        if width < 0 or height < 0:
            raise ValueError("Size values must be positive")

        LIB_MOON._Rectangle_SetSize(self._ptr, width, height)
        return self

    @final
    def get_size(self) -> Vector2f:
        """
        #### Возвращает текущие размеры прямоугольника

        ---

        :Description:
        - Возвращает фактические размеры в пикселях
        - Не включает масштабирование
        - Ширина = x, Высота = y

        ---

        :Returns:
        - Vector2f: Размеры {width, height}

        ---

        :Example:
        ```python
        size = rect.get_size()
        print(f"Ширина: {size.x}, Высота: {size.y}")
        ```
        """
        width = LIB_MOON._Rectangle_GetWidth(self._ptr)
        height = LIB_MOON._Rectangle_GetHeight(self._ptr)
        return Vector2f(width, height)

    @final
    def set_angle(self, angle: Number) -> Self:
        """
        #### Устанавливает угол поворота прямоугольника

        ---

        :Description:
        - Поворачивает прямоугольник относительно текущей точки отсчета
        - Угол задается в градусах (0-360)
        - Положительные значения - по часовой стрелке
        - Поддерживает fluent-interface

        ---

        :Args:
        - angle (float): Угол поворота в градусах

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Повернуть на 45 градусов
        rect.set_angle(45.0)

        # Комбинирование с другими методами
        rect.set_origin(50, 50).set_angle(30.0)
        ```
        """
        angle = float(angle)
        LIB_MOON._Rectangle_SetRotation(self._ptr, angle)
        self.__angle = angle % 360  # Нормализуем угол
        return self

    @final
    def get_angle(self) -> Number:
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
        # Анимация вращения
        rect.set_angle(rect.get_angle() + 1)
        ```
        """
        return self.__angle

    @final
    def set_outline_thickness(self, thickness: Number) -> Self:
        """
        #### Устанавливает толщину границы прямоугольника

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
        rect.set_outline_thickness(1.5)

        # Толстая граница
        rect.set_outline_thickness(5.0)
        ```
        """
        thickness = max(0.0, float(thickness))  # Гарантируем неотрицательное значение
        LIB_MOON._Rectangle_SetOutlineThickness(self._ptr, thickness)
        self.__outline_thickness = thickness
        return self

    @final
    def get_outline_thickness(self) -> Number:
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
        if rect.get_outline_thickness() > 0:
            print("Прямоугольник имеет границу")
        ```
        """
        return self.__outline_thickness

    @final
    def set_outline_color(self, color: Color | None) -> Self:
        """
        #### Устанавливает цвет границы прямоугольника

        ---

        :Description:
        - Определяет RGBA-цвет отображаемой границы
        - Полностью прозрачный цвет скроет границу
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - color (Color): Цвет границы

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        # Красная граница
        rect.set_outline_color(Color.RED)

        # Полупрозрачная синяя граница
        rect.set_outline_color(Color(0, 0, 255, 128))
        ```
        """
        if color is None:
            LIB_MOON._Rectangle_SetOutlineColor(self._ptr, 0, 0, 0, 0)
        else:
            LIB_MOON._Rectangle_SetOutlineColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__outline_color = color
        return self

    @final
    def get_outline_color(self) -> Color | None:
        """
        #### Возвращает текущий цвет границы

        ---

        :Description:
        - Возвращает последний установленный цвет
        - None означает отсутствие границы

        ---

        :Returns:
        - Color: Текущий цвет границы или None

        ---

        :Example:
        ```python
        border_color = rect.get_outline_color()
        if border_color == Color.BLACK:
            print("Граница черного цвета")
        ```
        """
        return self.__outline_color


    @overload
    def set_scale(self, arg1: Number) -> Self:
        """
        #### Равномерно масштабирует прямоугольник

        ---

        :Description:
        - Применяет одинаковый масштаб по обеим осям
        - 1.0 - исходный размер
        - меньше 1.0шение
        - больше величение
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
        rect.set_scale(2.0)

        # Уменьшить вдвое
        rect.set_scale(0.5)
        ```
        """
        ...

    @overload
    def set_scale(self, arg1: Number, arg2: Number) -> Self:
        """
        #### Масштабирует прямоугольник по осям

        ---

        :Description:
        - Позволяет задать разный масштаб для X и Y
        - Может вызывать искажение пропорций
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
        rect.set_scale(2.0, 1.0)

        # Сжать по вертикали
        rect.set_scale(1.0, 0.5)
        ```
        """
        ...

    def set_scale(self, arg1: Number, arg2: Optional[Number] = None) -> Self:
        """
        #### Основная реализация масштабирования

        ---

        :Raises:
        - ValueError: При недопустимых значениях масштаба

        ---

        :Note:
        - Масштаб применяется относительно точки отсчета
        - Отрицательные значения инвертируют изображение
        """
        if arg2 is None:
            scale_x = scale_y = float(arg1)
        else:
            scale_x, scale_y = float(arg1), float(arg2)

        if scale_x == 0 or scale_y == 0:
            raise ValueError("Scale values cannot be zero")

        LIB_MOON._Rectangle_SetScale(self._ptr, scale_x, scale_y)
        self.__scale.x = scale_x
        self.__scale.y = scale_y
        return self

    @final
    def get_scale(self) -> Vector2f:
        """
        #### Возвращает текущий масштаб прямоугольника

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
        scale = rect.get_scale()
        print(f"Горизонтальный масштаб: {scale.x}, Вертикальный: {scale.y}")
        ```
        """
        return self.__scale.copy()  # Возвращаем копию для безопасности

    @final
    def move(self, offset: Vector2f) -> Self:
        """
        #### Перемещает прямоугольник на заданный вектор

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
        rect.move(Vector2f(10, 5))

        # Комбинирование с другими методами
        rect.move(Vector2f(10, 0)).set_angle(45)
        ```
        """
        new_pos = self.get_position() + offset
        self.set_position(new_pos)
        return self

    def copy(self) -> "RectangleShape":
        """
        #### Создает полную копию прямоугольника

        ---

        :Description:
        - Создает новый объект с теми же параметрами
        - Копирует все атрибуты:
        - Размеры
        - Цвет и контур
        - Преобразования (позиция, поворот, масштаб)
        - Точку отсчета

        ---

        :Returns:
        - RectangleShape: Независимая копия прямоугольника

        ---

        :Example:
        ```python
        original = RectangleShape(100, 50)
        original.set_color(Color.RED)

        # Создание копии
        duplicate = original.copy()

        # Изменение копии не влияет на оригинал
        duplicate.set_color(Color.BLUE)
        ```

        :Note:
        - Копия является полностью независимым объектом
        - Изменения в копии не затрагивают оригинал
        - Все нативные ресурсы дублируются
        """
        # Создаем новый прямоугольник с теми же размерами
        _c = RectangleShape(*self.get_size().xy)

        # Копируем все визуальные атрибуты

        if self.get_outline_color() is not None:
            _c.set_outline_color(self.get_outline_color())

        _c.set_outline_thickness(self.get_outline_thickness())

        # Копируем все преобразования
        _c.set_origin(*self.get_origin().xy)
        _c.set_angle(self.get_angle())
        _c.set_scale(*self.get_scale().xy)
        _c.set_position(*self.get_position().xy)

        # Копируем основной цвет, если задан
        if self.get_color() is not None:
            _c.set_color(self.get_color())

        return _c




# --- Привязки C++ функций для кругов ---
# Эти строки определяют типы аргументов (argtypes) и возвращаемых значений (restype)
# для C++ функций, связанных с кругами.
LIB_MOON._Circle_Create.argtypes = [ctypes.c_float, ctypes.c_int]
LIB_MOON._Circle_Create.restype = ctypes.c_void_p
LIB_MOON._Circle_Delete.argtypes = [ctypes.c_void_p]
LIB_MOON._Circle_Delete.restype = None
LIB_MOON._Circle_SetPosition.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_MOON._Circle_SetPosition.restype = None
LIB_MOON._Circle_GetPositionX.argtypes = [ctypes.c_void_p]
LIB_MOON._Circle_GetPositionX.restype = ctypes.c_float
LIB_MOON._Circle_GetPositionY.argtypes = [ctypes.c_void_p]
LIB_MOON._Circle_GetPositionY.restype = ctypes.c_float
LIB_MOON._Circle_SetRadius.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_MOON._Circle_SetRadius.restype = None
LIB_MOON._Circle_GetRadius.argtypes = [ctypes.c_void_p]
LIB_MOON._Circle_GetRadius.restype = ctypes.c_float
LIB_MOON._Circle_SetRotation.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_MOON._Circle_SetRotation.restype = None
LIB_MOON._Circle_GetRotation.argtypes = [ctypes.c_void_p]
LIB_MOON._Circle_GetRotation.restype = ctypes.c_float
LIB_MOON._Circle_SetFillColor.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Circle_SetFillColor.restype = None
LIB_MOON._Circle_SetOutlineColor.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Circle_SetOutlineColor.restype = None
LIB_MOON._Circle_SetOutlineThickness.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_MOON._Circle_SetOutlineThickness.restype = None
LIB_MOON._Circle_SetScale.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_MOON._Circle_SetScale.restype = None
LIB_MOON._Circle_GetScaleX.argtypes = [ctypes.c_void_p]
LIB_MOON._Circle_GetScaleX.restype = ctypes.c_float
LIB_MOON._Circle_GetScaleY.argtypes = [ctypes.c_void_p]
LIB_MOON._Circle_GetScaleY.restype = ctypes.c_float
LIB_MOON._Circle_SetOrigin.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_MOON._Circle_SetOrigin.restype = None
LIB_MOON._Circle_GetOriginX.argtypes = [ctypes.c_void_p]
LIB_MOON._Circle_GetOriginX.restype = ctypes.c_float
LIB_MOON._Circle_GetOriginY.argtypes = [ctypes.c_void_p]
LIB_MOON._Circle_GetOriginY.restype = ctypes.c_float

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

        :Example:
        ```python
        # Круг с 50 точками аппроксимации
        circle = BaseCircleShape(50)
        ```
        """
        if approximation < 3:
            raise ValueError("Circle must have at least 3 points")

        self.__approximation = int(approximation)
        self._ptr: ctypes.c_void_p | None = LIB_MOON._Circle_Create(100, int(approximation))
        self.set_origin(100, 100)  # Центрируем точку отсчета

        # Инициализация атрибутов
        self.__outline_color: Color | None = None
        self.__outline_thickness: float = 0
        self.__color: Color | None = COLOR_GRAY



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
        1. Проверяет наличие указателя
        2. Вызывает нативное удаление объекта
        3. Обнуляет указатель

        ---

        :Example:
        ```python
        # Обычно не вызывается явно
        circle = BaseCircleShape()
        del circle  # Вызовет __del__ автоматически
        ```
        """
        if hasattr(self, '_ptr') and self._ptr:
            LIB_MOON._Circle_Delete(self._ptr)
            self._ptr = None  # Защита от повторного удаления


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
        circle = BaseCircleShape(50)
        print(circle.get_point_count())  # 50

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
        - int: Указатель на объект Circle в памяти C++

        ---

        :Example:
        ```python
        # Для передачи в нативные функции
        native_function(circle.get_ptr())
        ```

        :Warning:
        - Избегайте прямых манипуляций с указателем
        - Используйте только для интеграции с API PySGL
        """
        return self._ptr

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
    def set_position(self, arg1: Vector2f, arg2: None = None) -> Self:
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

    def set_position(self, arg1: Union[float, Vector2f], arg2: Optional[float] = None) -> Self:
        """
        #### Основная реализация установки позиции

        ---

        :Raises:
        - ValueError: При недопустимых аргументах

        ---

        :Note:
        - Координаты относятся к центру круга
        - Учитывает текущую точку отсчета
        """
        if isinstance(arg1, (Vector2f, Vector2i)) and arg2 is None:
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

    def get_position(self) -> Vector2f:
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
        return Vector2f(x, y)

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
        LIB_MOON._Circle_SetFillColor(self._ptr, color.r, color.g, color.b, color.a)
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

        :Raises:
        - ValueError: При недопустимых значениях масштаба

        ---

        :Note:
        - Масштаб применяется относительно точки отсчета
        - Отрицательные значения создают зеркальное отражение
        """
        if arg2 is None:
            scale_x = scale_y = float(arg1)
        else:
            scale_x, scale_y = float(arg1), float(arg2)

        if scale_x == 0 or scale_y == 0:
            raise ValueError("Scale values cannot be zero")

        LIB_MOON._Circle_SetScale(self._ptr, scale_x, scale_y)
        return self

    def get_scale(self) -> Vector2f:
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
        return Vector2f(
            LIB_MOON._Circle_GetScaleX(self._ptr),
            LIB_MOON._Circle_GetScaleY(self._ptr)
        )

    @overload
    def set_origin(self, arg1: Vector2f, arg2: None = None) -> Self:
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

    def set_origin(self, arg1: Union[Vector2f, float], arg2: Optional[float] = None) -> Self:
        """
        #### Основная реализация установки точки отсчета

        ---

        :Note:
        - Координаты интерпретируются относительно локальной системы
        - Отрицательные значения допустимы

        ---

        :Raises:
        - TypeError: При неверном типе аргументов
        """
        if isinstance(arg1, Vector2f):
            x, y = arg1.x, arg1.y
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            x, y = float(arg1), float(arg2)
        else:
            raise TypeError("Invalid argument types for set_origin")

        LIB_MOON._Circle_SetOrigin(self._ptr, x, y)
        return self

    def get_origin(self) -> Vector2f:
        """
        #### Возвращает текущую точку отсчета

        ---

        :Description:
        - Возвращает координаты относительно локальной системы
        - Может отличаться от геометрического центра

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
        return Vector2f(x, y)

    @final
    def move(self, offset: Vector2f) -> Self:
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
        """
        new_pos = self.get_position() + offset
        self.set_position(new_pos)
        return self



# Глобальные константы для часто используемых фигур.
# Использование Final гарантирует, что эти переменные не будут переназначены.
# Это удобно для стандартных, преднастроенных форм, которые можно переиспользовать.
CIRCLE_SHAPE:           Final[CircleShape]      = CircleShape(30)
RECTANGLE_SHAPE:        Final[RectangleShape]   = RectangleShape(100, 100)

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

class LineRect:
    def __init__(self, pos: Vector2Type, size: Vector2Type):

        self.__position = pos
        self.__size = size


        self.__vertex_array = VertexList(4)
        self.__vertex_array.set_primitive_type(VertexListTypes.LineStrip)
        self.__vertex_array.auto_append(Vertex2d().FromPosition(pos))
        self.__vertex_array.auto_append(Vertex2d().FromPosition(Vector2f(pos.x + size.x, pos.y)))
        self.__vertex_array.auto_append(Vertex2d().FromPosition(pos + size))
        self.__vertex_array.auto_append(Vertex2d().FromPosition(Vector2f(pos.x, pos.y + size.y)))

        self.__color = None

    def _reconstruct_all_vertex(self):
        self.__vertex_array.get(0).position = self.__position
        self.__vertex_array.get(1).position = Vector2f(self.__position.x + self.__size.x, self.__position.y)
        self.__vertex_array.get(2).position = self.__position + self.__size
        self.__vertex_array.get(3).position = Vector2f(self.__position.x, self.__position.y + self.__size.y)

    def get_ptr(self) -> ctypes.c_void_p:
        return self.__vertex_array.get_ptr()

    def set_outline_color(self, color: Color) -> Self:
        self.__color = color
        self.__vertex_array.set_color(color)
        return self

    def get_outline_color(self) -> Color | None:
        return self.__color

    def set_position(self, pos: Vector2Type) -> Self:
        if pos != self.__position:
            self.__position = pos
            self._reconstruct_all_vertex()
        return self

    def set_size(self, size: Vector2Type) -> Self:
        if self.__size != size:
            self.__size = size
            self._reconstruct_all_vertex()
        return self
