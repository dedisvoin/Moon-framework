import ctypes
import os
from typing import Self, Final, final

from PySGL.python.Types import *
from PySGL.python.Colors import *
from PySGL.python.Vectors import Vector2f  
from PySGL.python.Rendering.Vertexes import VertexArray, Vertex  


# Псевдоним для типа указателя на шейп прямоугольника == +
RectanglePtr: Final[ctypes.c_void_p] = ctypes.c_void_p
# ====================================================== +

@final
class LibraryLoadError(Exception):
    """Ошибка загрузки нативной библиотеки"""
    pass


@final
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
            print("PySGL.Shapes: Library not found at", lib_path)
            lib_path = "./dlls/PySGL.dll"
            if not os.path.exists(lib_path):
                print("Library not found at", lib_path)
                raise FileNotFoundError(f"Library not found at {lib_path}")
        
        return lib_path
    except Exception as e:
        raise LibraryLoadError(f"Library search failed: {e}")

# Загружаем DLL библиотеку
try:
    LIB_PYSGL: Final[ctypes.CDLL] = ctypes.CDLL(_find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")


LIB_PYSGL._Rectangle_Create.restype = RectanglePtr
LIB_PYSGL._Rectangle_Create.argtypes = [ctypes.c_float, ctypes.c_float]
LIB_PYSGL._Rectangle_GetPositionX.restype = ctypes.c_float
LIB_PYSGL._Rectangle_GetPositionX.argtypes = [RectanglePtr]
LIB_PYSGL._Rectangle_GetPositionY.restype = ctypes.c_float
LIB_PYSGL._Rectangle_GetPositionY.argtypes = [RectanglePtr]
LIB_PYSGL._Rectangle_GetWidth.restype = ctypes.c_float
LIB_PYSGL._Rectangle_GetWidth.argtypes = [RectanglePtr]
LIB_PYSGL._Rectangle_GetHeight.restype = ctypes.c_float
LIB_PYSGL._Rectangle_GetHeight.argtypes = [RectanglePtr]
LIB_PYSGL._Rectangle_SetPosition.restype = None
LIB_PYSGL._Rectangle_SetPosition.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._Rectangle_SetColor.restype = None
LIB_PYSGL._Rectangle_SetColor.argtypes = [RectanglePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_PYSGL._Rectangle_SetOrigin.restype = None
LIB_PYSGL._Rectangle_SetOrigin.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._Rectangle_SetSize.restype = None
LIB_PYSGL._Rectangle_SetSize.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._Rectangle_SetRotation.restype = None
LIB_PYSGL._Rectangle_SetRotation.argtypes = [RectanglePtr, ctypes.c_float]
LIB_PYSGL._Rectangle_SetOutlineThickness.restype = None
LIB_PYSGL._Rectangle_SetOutlineThickness.argtypes = [RectanglePtr, ctypes.c_float]
LIB_PYSGL._Rectangle_SetOutlineColor.restype = None
LIB_PYSGL._Rectangle_SetOutlineColor.argtypes = [RectanglePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_PYSGL._Rectangle_SetScale.restype = None
LIB_PYSGL._Rectangle_SetScale.argtypes = [RectanglePtr, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._Rectangle_Delete.restype = None
LIB_PYSGL._Rectangle_Delete.argtypes = [RectanglePtr]

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
    def __init__(self, width: float, height: float):
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
        self._ptr = LIB_PYSGL._Rectangle_Create(float(width), float(height))
        
        # Инициализация Python-атрибутов
        self.__color: Color | None = None          # Основной цвет (None = прозрачный)
        self.__outline_color: Color | None = None  # Цвет контура
        self.__outline_thickness: float = 0        # Толщина контура
        self.__origin: Vector2f = Vector2f(0, 0)   # Точка преобразований
        self.__angle: float = 0                    # Угол поворота (градусы)
        self.__scale: Vector2f = Vector2f.one()    # Масштаб по осям
    
    @final
    def get_ptr(self) -> int:
        """
        #### Возвращает указатель на нативный объект C++
        
        ---
        
        :Description:
        - Предоставляет прямой доступ к низкоуровневому объекту
        - Используется для интеграции с нативным кодом
        - Для внутреннего использования в PySGL
        
        ---
        
        :Returns:
        - int: Указатель на объект Rectangle в памяти C++
        
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
            LIB_PYSGL._Rectangle_Delete(self._ptr)
            self._ptr = None

    @final
    @overload
    def set_position(self, x: Number, y: Number) -> Self:
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

    @final
    @overload
    def set_position(self, vector: Vector2f) -> Self:
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

    @final
    def set_position(self, arg1: Union[float, Vector2f], arg2: Optional[float] = None) -> Self:
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
        if isinstance(arg1, Vector2f) and arg2 is None:
            LIB_PYSGL._Rectangle_SetPosition(self._ptr, float(arg1.x), float(arg1.y))
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            LIB_PYSGL._Rectangle_SetPosition(self._ptr, float(arg1), float(arg2))
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
        x = LIB_PYSGL._Rectangle_GetPositionX(self._ptr)
        y = LIB_PYSGL._Rectangle_GetPositionY(self._ptr)
        return Vector2f(x, y)

    @final
    def set_color(self, color: Color) -> Self:
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
        LIB_PYSGL._Rectangle_SetColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__color = color
        return self

    @final
    def get_color(self) -> Color:
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
    
    @final
    @overload
    def set_origin(self, x: float, y: float) -> Self:
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

    @final
    @overload
    def set_origin(self, vector: Vector2f) -> Self:
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
    def set_origin(self, arg1: Union[float, Vector2f], arg2: Optional[float] = None) -> Self:
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
                "Expected either (x: float, y: float) or (vector: Vector2f), "
                f"got ({type(arg1).__name__}, {type(arg2).__name__})"
            )
        
        LIB_PYSGL._Rectangle_SetOrigin(self._ptr, x, y)
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

    @final
    @overload
    def set_size(self, width: float, height: float) -> Self:
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

    @final
    @overload
    def set_size(self, size: Vector2f) -> Self:
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
    def set_size(self, arg1: Union[float, Vector2f], arg2: Optional[float] = None) -> Self:
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
        
        if width <= 0 or height <= 0:
            raise ValueError("Size values must be positive")
        
        LIB_PYSGL._Rectangle_SetSize(self._ptr, width, height)
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
        width = LIB_PYSGL._Rectangle_GetWidth(self._ptr)
        height = LIB_PYSGL._Rectangle_GetHeight(self._ptr)
        return Vector2f(width, height)
    
    @final
    def set_angle(self, angle: float) -> Self:
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
        LIB_PYSGL._Rectangle_SetRotation(self._ptr, angle)
        self.__angle = angle % 360  # Нормализуем угол
        return self

    @final
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
        # Анимация вращения
        rect.set_angle(rect.get_angle() + 1)
        ```
        """
        return self.__angle
    
    @final
    def set_outline_thickness(self, thickness: float) -> Self:
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
        LIB_PYSGL._Rectangle_SetOutlineThickness(self._ptr, thickness)
        self.__outline_thickness = thickness
        return self

    @final
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
        if rect.get_outline_thickness() > 0:
            print("Прямоугольник имеет границу")
        ```
        """
        return self.__outline_thickness

    @final
    def set_outline_color(self, color: Color) -> Self:
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
        LIB_PYSGL._Rectangle_SetOutlineColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__outline_color = color
        return self

    @final
    def get_outline_color(self) -> Color:
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
    
    @final
    @overload
    def set_scale(self, scale: float) -> Self:
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

    @final
    @overload
    def set_scale(self, scale_x: float, scale_y: float) -> Self:
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

    @final
    def set_scale(self, arg1: float, arg2: Optional[float] = None) -> Self:
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
        
        LIB_PYSGL._Rectangle_SetScale(self._ptr, scale_x, scale_y)
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


LIB_PYSGL._Circle_Create.argtypes = [ctypes.c_float, ctypes.c_int]
LIB_PYSGL._Circle_Create.restype = ctypes.c_void_p
LIB_PYSGL._Circle_Delete.argtypes = [ctypes.c_void_p]
LIB_PYSGL._Circle_Delete.restype = None
LIB_PYSGL._Circle_SetPosition.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._Circle_SetPosition.restype = None
LIB_PYSGL._Circle_GetPositionX.argtypes = [ctypes.c_void_p]
LIB_PYSGL._Circle_GetPositionX.restype = ctypes.c_float
LIB_PYSGL._Circle_GetPositionY.argtypes = [ctypes.c_void_p]
LIB_PYSGL._Circle_GetPositionY.restype = ctypes.c_float
LIB_PYSGL._Circle_SetRadius.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_PYSGL._Circle_SetRadius.restype = None
LIB_PYSGL._Circle_GetRadius.argtypes = [ctypes.c_void_p]
LIB_PYSGL._Circle_GetRadius.restype = ctypes.c_float
LIB_PYSGL._Circle_SetRotation.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_PYSGL._Circle_SetRotation.restype = None
LIB_PYSGL._Circle_GetRotation.argtypes = [ctypes.c_void_p]
LIB_PYSGL._Circle_GetRotation.restype = ctypes.c_float
LIB_PYSGL._Circle_SetFillColor.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_PYSGL._Circle_SetFillColor.restype = None
LIB_PYSGL._Circle_SetOutlineColor.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_PYSGL._Circle_SetOutlineColor.restype = None
LIB_PYSGL._Circle_SetOutlineThickness.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_PYSGL._Circle_SetOutlineThickness.restype = None
LIB_PYSGL._Circle_SetScale.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._Circle_SetScale.restype = None
LIB_PYSGL._Circle_GetScaleX.argtypes = [ctypes.c_void_p]
LIB_PYSGL._Circle_GetScaleX.restype = ctypes.c_float
LIB_PYSGL._Circle_GetScaleY.argtypes = [ctypes.c_void_p]
LIB_PYSGL._Circle_GetScaleY.restype = ctypes.c_float
LIB_PYSGL._Circle_SetOrigin.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._Circle_SetOrigin.restype = None
LIB_PYSGL._Circle_GetOriginX.argtypes = [ctypes.c_void_p]
LIB_PYSGL._Circle_GetOriginX.restype = ctypes.c_float
LIB_PYSGL._Circle_GetOriginY.argtypes = [ctypes.c_void_p]
LIB_PYSGL._Circle_GetOriginY.restype = ctypes.c_float

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
            
        self.__approximation = approximation
        self._ptr = LIB_PYSGL._Circle_Create(100, approximation)
        self.set_origin(100, 100)  # Центрируем точку отсчета
        
        # Инициализация атрибутов
        self.__outline_color: Color | None = None
        self.__outline_thickness: float = 1
        self.__color: Color | None = None



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
            LIB_PYSGL._Circle_Delete(self._ptr)
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

    def get_ptr(self) -> int:
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
    def set_position(self, x: float, y: float) -> Self:
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
    def set_position(self, position: Vector2f) -> Self:
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
        if isinstance(arg1, Vector2f) and arg2 is None:
            x, y = float(arg1.x), float(arg1.y)
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            x, y = float(arg1), float(arg2)
        else:
            raise ValueError(
                "Invalid arguments. "
                "Expected either (x: float, y: float) or (position: Vector2f), "
                f"got ({type(arg1).__name__}, {type(arg2).__name__})"
            )
        
        LIB_PYSGL._Circle_SetPosition(self._ptr, x, y)
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
        x = LIB_PYSGL._Circle_GetPositionX(self._ptr)
        y = LIB_PYSGL._Circle_GetPositionY(self._ptr)
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
        
        LIB_PYSGL._Circle_SetRadius(self._ptr, radius)
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
        return LIB_PYSGL._Circle_GetRadius(self._ptr)

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
        LIB_PYSGL._Circle_SetRotation(self._ptr, angle)
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
        return LIB_PYSGL._Circle_GetRotation(self._ptr)

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
        LIB_PYSGL._Circle_SetFillColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__color = color
        return self

    def get_color(self) -> Color:
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
        LIB_PYSGL._Circle_SetOutlineColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__outline_color = color
        return self

    def get_outline_color(self) -> Color:
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
        LIB_PYSGL._Circle_SetOutlineThickness(self._ptr, thickness)
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
    def set_scale(self, scale: float) -> Self:
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
    def set_scale(self, scale_x: float, scale_y: float) -> Self:
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
        
        LIB_PYSGL._Circle_SetScale(self._ptr, scale_x, scale_y)
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
            LIB_PYSGL._Circle_GetScaleX(self._ptr),
            LIB_PYSGL._Circle_GetScaleY(self._ptr)
        )
    
    @overload
    def set_origin(self, origin: Vector2f) -> Self:
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
    def set_origin(self, x: float, y: float) -> Self:
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
        
        LIB_PYSGL._Circle_SetOrigin(self._ptr, x, y)
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
        x = LIB_PYSGL._Circle_GetOriginX(self._ptr)
        y = LIB_PYSGL._Circle_GetOriginY(self._ptr)
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

@final
class BaseLineShape:
    """
    #### Базовый класс для работы с толстыми линиями
    
    ---
    
    :Description:
    - Реализует линию как прямоугольник с опциональными скругленными концами
    - Поддерживает настройку толщины, цвета и формы концов
    - Внутренне использует комбинацию RectangleShape и CircleShape
    
    ---
    
    :Example:
    ```python
    line = BaseLineShape(COLOR_RED)
    line.set_points(0, 0, 100, 100).set_width(5).enable_rounded_corners()
    ```
    """

    @final
    def __init__(self, color: Color = COLOR_GRAY) -> None:
        """
        #### Инициализирует новую линию
        
        ---
        
        :Description:
        - Создает линию с параметрами по умолчанию
        - Начальная и конечная позиции: (0, 0)
        - Толщина: 1 пиксель
        - Квадратные концы (без скругления)
        
        ---
        
        :Args:
        - color (Color): Начальный цвет линии (по умолчанию COLOR_GRAY)
        
        ---
        
        :Members:
        - __rectangle_shape: Внутренний прямоугольник для тела линии
        - __round_circles: Круги для скругленных концов (если включены)
        """
        self.__start_pos = [0, 0]
        self.__end_pos = [0, 0]
        self.__color = color
        self.__width = 1

        self.__rectangle_shape = RectangleShape(10, 10)
        self.__rectangle_shape.set_color(COLOR_BLACK)
        
        self.__rounded_corners = False
        self.__round_circles = CircleShape(15)
        self.__round_circles.set_color(COLOR_BLACK)

    @final
    @overload
    def set_points(self, start: Vector2f, end: Vector2f) -> Self:
        """
        #### Устанавливает точки линии через векторы
        
        ---
        
        :Description:
        - Принимает готовые 2D-векторы для начальной и конечной точек
        - Автоматически обновляет геометрию линии
        - Поддерживает fluent-интерфейс
        
        ---
        
        :Args:
        - start (Vector2f): Вектор начальной точки {x, y}
        - end (Vector2f): Вектор конечной точки {x, y}
        
        ---
        
        :Returns:
        - Self: Текущий объект для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        line.set_points(Vector2f(10, 10), Vector2f(100, 50))
        ```
        """
        ...

    @final
    @overload
    def set_points(self, x1: float, y1: float, x2: float, y2: float) -> Self:
        """
        #### Устанавливает точки линии через координаты
        
        ---
        
        :Description:
        - Принимает отдельные координаты для начальной и конечной точек
        - Подходит для прямого указания значений
        - Поддерживает fluent-интерфейс
        
        ---
        
        :Args:
        - x1 (float): Начальная X-координата
        - y1 (float): Начальная Y-координата
        - x2 (float): Конечная X-координата
        - y2 (float): Конечная Y-координата
        
        ---
        
        :Returns:
        - Self: Текущий объект для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        line.set_points(0, 0, 150, 75)
        ```
        """
        ...

    @final
    def set_points(self, arg1: Union[Vector2f, float], arg2: Union[Vector2f, float], 
                  arg3: Optional[float] = None, arg4: Optional[float] = None) -> Self:
        """
        #### Основная реализация установки точек линии
        
        ---
        
        :Raises:
        - TypeError: При неверной комбинации аргументов
        
        ---
        
        :Note:
        - Автоматически пересчитывает геометрию при изменении точек
        """
        if isinstance(arg1, Vector2f) and isinstance(arg2, Vector2f):
            self.__start_pos = [arg1.x, arg1.y]
            self.__end_pos = [arg2.x, arg2.y]
        elif all(isinstance(x, (int, float)) for x in [arg1, arg2, arg3, arg4]):
            self.__start_pos = [float(arg1), float(arg2)]
            self.__end_pos = [float(arg3), float(arg4)]
        else:
            raise TypeError("Invalid argument types for set_points")
        
        return self

    @final
    def set_rounded(self, round: bool = True) -> Self:
        """
        #### Устанавливает скругление концов линии
        
        ---
        
        :Description:
        - Включает/выключает визуальное скругление концов линии
        - При активации добавляет полукруги на концах
        - При деактивации оставляет прямоугольные концы
        - Поддерживает fluent-интерфейс
        
        ---
        
        :Args:
        - round (bool): Флаг скругления (по умолчанию True)
        
        ---
        
        :Returns:
        - Self: Текущий объект для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Включить скругленные концы
        line.set_rounded()
        
        # Выключить скругленные концы
        line.set_rounded(False)
        ```
        """
        self.__rounded_corners = round
        return self
    
    @final
    def get_rounded(self) -> bool:
        """
        #### Проверяет статус скругления концов
        
        ---
        
        :Description:
        - Возвращает текущее состояние флага скругления
        - Не изменяет состояние объекта
        
        ---
        
        :Returns:
        - bool: True если концы скруглены, False если прямые
        
        ---
        
        :Example:
        ```python
        if line.get_rounded():
            print("Линия имеет скругленные концы")
        ```
        """
        return self.__rounded_corners

    @final
    @overload
    def set_start_point(self, point: Vector2f) -> Self:
        """
        #### Устанавливает начальную точку линии через вектор
        
        ---
        
        :Description:
        - Принимает готовый 2D-вектор координат
        - Автоматически обновляет геометрию линии
        - Поддерживает fluent-интерфейс
        
        ---
        
        :Args:
        - point (Vector2f): Вектор с координатами {x, y}
        
        ---
        
        :Returns:
        - Self: Текущий объект для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        line.set_start_point(Vector2f(10, 20))
        ```
        """
        ...

    @final
    @overload
    def set_start_point(self, x: float, y: float) -> Self:
        """
        #### Устанавливает начальную точку линии через координаты
        
        ---
        
        :Description:
        - Принимает отдельные координаты X и Y
        - Подходит для прямого указания значений
        - Поддерживает fluent-интерфейс
        
        ---
        
        :Args:
        - x (float): Координата X начальной точки
        - y (float): Координата Y начальной точки
        
        ---
        
        :Returns:
        - Self: Текущий объект для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        line.set_start_point(15.5, 25.0)
        ```
        """
        ...

    @final
    def set_start_point(self, arg1: Union[Vector2f, float], arg2: Optional[float] = None) -> Self:
        """
        #### Основная реализация установки начальной точки
        
        ---
        
        :Raises:
        - TypeError: При неверной комбинации аргументов
        
        ---
        
        :Note:
        - Автоматически пересчитывает геометрию линии
        """
        if isinstance(arg1, Vector2f):
            self.__start_pos = [arg1.x, arg1.y]
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            self.__start_pos = [float(arg1), float(arg2)]
        else:
            raise TypeError("Invalid argument types for set_start_point")

        return self

    @final
    @overload
    def set_end_point(self, point: Vector2f) -> Self:
        """
        #### Устанавливает конечную точку линии через вектор
        
        ---
        
        :Description:
        - Принимает готовый 2D-вектор координат
        - Автоматически обновляет геометрию линии
        - Поддерживает fluent-интерфейс
        
        ---
        
        :Args:
        - point (Vector2f): Вектор с координатами {x, y}
        
        ---
        
        :Returns:
        - Self: Текущий объект для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        line.set_end_point(Vector2f(100, 200))
        ```
        """
        ...

    @final
    @overload
    def set_end_point(self, x: float, y: float) -> Self:
        """
        #### Устанавливает конечную точку линии через координаты
        
        ---
        
        :Description:
        - Принимает отдельные координаты X и Y
        - Подходит для прямого указания значений
        - Поддерживает fluent-интерфейс
        
        ---
        
        :Args:
        - x (float): Координата X конечной точки
        - y (float): Координата Y конечной точки
        
        ---
        
        :Returns:
        - Self: Текущий объект для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        line.set_end_point(150.0, 250.5)
        ```
        """
        ...

    @final
    def set_end_point(self, arg1: Union[Vector2f, float], arg2: Optional[float] = None) -> Self:
        """
        #### Основная реализация установки конечной точки
        
        ---
        
        :Raises:
        - TypeError: При неверной комбинации аргументов
        
        ---
        
        :Note:
        - Автоматически пересчитывает геометрию линии
        """
        if isinstance(arg1, Vector2f):
            self.__end_pos = [arg1.x, arg1.y]
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            self.__end_pos = [float(arg1), float(arg2)]
        else:
            raise TypeError("Invalid argument types for set_end_point")
        
        return self
    
    @final
    def set_color(self, color: Color) -> Self:
        """
        #### Устанавливает цвет всей линии
        
        ---
        
        :Description:
        - Применяет указанный цвет к телу линии и скругленным концам
        - `Не совсем поддерживает прозрачность (альфа-канал)`
        - Автоматически обновляет все внутренние элементы
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
        # Установить красный цвет
        line.set_color(Color(255, 0, 0))
        
        # Полупрозрачный синий
        line.set_color(Color(0, 0, 255, 128))
        ```
        """
        self.__color = color
        self.__rectangle_shape.set_color(color)
        self.__round_circles.set_color(color)
        return self

    @final
    def set_width(self, width: float) -> Self:
        """
        #### Устанавливает толщину линии
        
        ---
        
        :Description:
        - Контролирует визуальную толщину/ширину линии
        - Автоматически корректирует позиционирование скругленных концов
        - Поддерживает fluent-интерфейс
        
        ---
        
        :Args:
        - width (float): Новая толщина линии (>0)
        
        ---
        
        :Returns:
        - Self: Текущий объект для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Тонкая линия
        line.set_width(1.0)
        
        # Толстая линия
        line.set_width(10.0)
        ```
        
        :Note:
        - При значениях < 0.1 автоматически устанавливается 0.1
        """
        self.__width = float(width)
        self.__round_circles.set_origin(self.__width / 2, self.__width / 2)

        return self

    @final
    def get_width(self) -> float:
        """
        #### Возвращает текущую толщину линии
        
        ---
        
        :Description:
        - Возвращает актуальное значение толщины
        - Не изменяет состояние объекта
        
        ---
        
        :Returns:
        - float: Текущая толщина линии в пикселях
        
        ---
        
        :Example:
        ```python
        width = line.get_width()
        print(f"Текущая толщина линии: {width}px")
        ```
        """
        return self.__width
    
    @final
    def get_start_pos(self) -> Vector2f:
        """
        #### Возвращает начальную позицию линии
        
        ---
        
        :Description:
        - Возвращает текущую начальную точку линии
        - Координаты представлены как объект Vector2f
        - Не изменяет состояние объекта
        
        ---
        
        :Returns:
        - Vector2f: Вектор начальной позиции {x, y}
        
        ---
        
        :Example:
        ```python
        start = line.get_start_pos()
        print(f"Начало линии: x={start.x}, y={start.y}")
        ```
        """
        return Vector2f(*self.__start_pos)
    
    @final
    def get_end_pos(self) -> Vector2f:
        """
        #### Возвращает конечную позицию линии
        
        ---
        
        :Description:
        - Возвращает текущую конечную точку линии
        - Координаты представлены как объект Vector2f
        - Не изменяет состояние объекта
        
        ---
        
        :Returns:
        - Vector2f: Вектор конечной позиции {x, y}
        
        ---
        
        :Example:
        ```python
        end = line.get_end_pos()
        print(f"Конец линии: {end}")
        ```
        """
        return Vector2f(*self.__end_pos)
    
    @final
    def get_color(self) -> Color:
        """
        #### Возвращает текущий цвет линии
        
        ---
        
        :Description:
        - Возвращает объект Color линии
        - Включает значения RGBA
        - Не изменяет состояние объекта
        
        ---
        
        :Returns:
        - Color: Текущий цвет линии
        
        ---
        
        :Example:
        ```python
        color = line.get_color()
        if color == COLOR_RED:
            print("Линия красного цвета")
        ```
        """
        return self.__color
    
    @final
    def update(self) -> None:
        """
        #### Обновляет геометрию линии
        
        ---
        
        :Description:
        - Пересчитывает все параметры отрисовки на основе текущего состояния:
          * Позицию и размер прямоугольника (тело линии)
          * Радиус и позицию скругленных концов
          * Угол поворота всех элементов
        - Автоматически вызывается при попытке отрисовки фигуры
        
        ---
        
        :Algorithm:
        1. Вычисляет вектор направления между точками
        2. Определяет длину и угол линии
        3. Настраивает прямоугольник (тело линии):
           - Длина = расстояние между точками
           - Высота = толщина линии
           - Угол = угол вектора направления
        4. Настраивает скругленные концы (если включены):
           - Радиус = половина толщины линии
           - Позиция = крайние точки линии
        
        ---

        :Note:
        - Для оптимальной производительности избегайте прямых вызовов
        """
        # Вычисляем вектор направления
        vector = Vector2f.from_two_point(self.__start_pos, self.__end_pos)
        length = vector.length()
        normal = vector.normalized()
        angle = normal.angle_degrees()

        # Настройка прямоугольника (тело линии)
        self.__rectangle_shape.set_size(length, self.__width)
        self.__rectangle_shape.set_angle(angle - 180)
        self.__rectangle_shape.set_origin(0, self.__width / 2)
        self.__rectangle_shape.set_position(*self.__start_pos)
        
        # Настройка скругленных концов
        if self.__rounded_corners:
            radius = self.__width / 2
            self.__round_circles.set_radius(radius)
            
    @final
    def special_draw(self, window):
        """
        #### Выполняет отрисовку линии с автоматическим обновлением
        
        ---
        
        :Description:
        - Автоматически обновляет геометрию перед отрисовкой
        - Отрисовывает основные компоненты линии:
          * Прямоугольник (тело линии)
          * Скругленные концы (если включены)
        - Гарантирует согласованное отображение всех элементов
        
        ---
        
        :Args:
        - window (RenderWindow): Целевое окно для отрисовки
        
        ---
        
        :Rendering Process:
        1. Обновление геометрии (вызов update())
        2. Отрисовка прямоугольника (основная линия)
        3. Если включены скругленные концы:
           - Отрисовка круга в начальной точке
           - Отрисовка круга в конечной точке
        
        ---
        
        :Example:
        ```python
        # В основном цикле отрисовки
        while window.is_open():
            window.clear()
            line.special_draw(window)
            window.display()
        ```
        
        :Note:
        - Для кастомной отрисовки можно использовать отдельно:
          * update()
          * Отрисовку компонентов через window.draw()
        - При изменении параметров линии не требуется
          явно вызывать update() перед special_draw()
        """
        self.update() # Убеждаемся, что геометрия линии актуальна.
        window.draw(self.__rectangle_shape) # Отрисовываем основное тело линии (прямоугольник).

        # Отрисовываем скругленные концы, только если они включены.
        if self.__rounded_corners:
            # Позиционируем первый круг в начальной точке линии.
            self.__round_circles.set_position(self.__start_pos[0], self.__start_pos[1])
            window.draw(self.__round_circles)

            # Позиционируем второй круг в конечной точке линии.
            self.__round_circles.set_position(self.__end_pos[0], self.__end_pos[1])
            window.draw(self.__round_circles)
    
    @final
    def get_ptr(self) -> Self:
        """
        #### Возвращает ссылку на текущий объект линии
        
        ---
        
        :Description:
        - В отличие от других фигур, LineShape не имеет единого C++ объекта
        - Возвращает сам Python-объект для совместимости с API
        - Фактическая отрисовка выполняется внутренними фигурами:
          * Прямоугольник (тело линии)
          * Круги (скругленные концы)
        
        ---
        
        :Returns:
        - BaseLineShape: Текущий экземпляр объекта
        
        ---
        
        :Example:
        ```python
        line_ptr = line.get_ptr()
        assert line_ptr is line  # Это один и тот же объект
        ```
        
        :Note:
        - Основное использование - для совместимости с API других фигур
        - Не предоставляет доступа к нативным C++ объектам
        - Для работы с компонентами используйте специальные методы
        """
        return self

@final 
class LineShape(BaseLineShape):
    """
    Класс для работы с линиями, которые могут иметь контур (обводку).
    Наследует функциональность от `BaseLineShape` и добавляет возможность настройки контура.
    """

    def __init__(self):
        """
        Инициализирует объект `LineShape`.
        Вызывает конструктор родительского класса и настраивает атрибуты контура.
        """
        super().__init__()

        self.__thickness = 10                  # Толщина контура (обводки) вокруг основной линии.
        self.__thickness_color = COLOR_BLACK   # Цвет контура.

        # Дополнительная линия, используемая для отрисовки самого контура.
        # Она будет толще основной линии и будет отрисовываться под ней.
        self.__thickness_shape = BaseLineShape()

    def set_outline_thickness(self, value: float) -> Self:
        """
        Устанавливает толщину контура (обводки) линии.
        Положительное значение увеличит контур наружу, отрицательное значение вызовет ошибку.

        Args:
            value: Желаемая толщина контура.

        Returns:
            Self: Экземпляр объекта LineShape (для цепочки вызовов).
        """
        self.__thickness = value
        # Толщина вспомогательной линии (контура) должна быть равна
        # толщине основной линии плюс толщина контура.
        self.__thickness_shape.set_width(value * 2 + self.get_width())
        return self
    
    def set_outline_color(self, color: Color) -> Self:
        """
        Устанавливает цвет контура (обводки) линии.

        Args:
            color: Объект Color, определяющий RGBA значения для контура.

        Returns:
            Self: Экземпляр объекта LineShape (для цепочки вызовов).
        """
        self.__thickness_color = color
        self.__thickness_shape.set_color(color) # Устанавливаем цвет вспомогательной линии.
        return self
    
    def get_outline_thickness(self) -> float:
        """
        Возвращает текущую толщину контура линии.

        Returns:
            float: Толщина контура.
        """
        return self.__thickness
    
    def get_outline_color(self) -> Color:
        """
        Возвращает текущий цвет контура линии.

        Returns:
            Color: Объект Color, представляющий цвет контура.
        """
        return self.__thickness_color
    
    def update(self):
        """
        Обновляет геометрию основной линии и ее контура.
        Этот метод должен вызываться перед отрисовкой, если параметры линии или контура изменились.
        """
        super().update() # Обновляем геометрию основной линии.
        
        self.__thickness_shape.set_rounded(super().get_rounded()) # Синхронизируем скругление концов с основной линией.
        
        # Если углы не скруглены, необходимо скорректировать положение контура,
        # чтобы он равномерно облегал основную линию.
        if not self._BaseLineShape__rounded_corners:
            # Вычисляем нормализованный вектор линии.
            n = Vector2f.from_two_point(self._BaseLineShape__start_pos, self._BaseLineShape__end_pos)
            n.normalize()
            # Умножаем его на половину толщины контура для смещения.
            n *= self.__thickness * 2
            
            # Смещаем начальную и конечную точки контура для создания эффекта обводки.
            # Половина толщины контура добавляется к начальной точке и вычитается из конечной
            # для создания симметричного контура вокруг основной линии.
            self.__thickness_shape.set_start_point(self.get_start_pos()[0] + n.x / 2, self.get_start_pos()[1] + n.y / 2) 
            self.__thickness_shape.set_end_point(self.get_end_pos()[0] - n.x / 2, self.get_end_pos()[1] - n.y / 2)
        else:
            # Если углы скруглены, контур просто использует те же начальную и конечную точки,
            # но с увеличенной толщиной, чтобы круги контура были больше.
            self.__thickness_shape.set_start_point(*self.get_start_pos())
            self.__thickness_shape.set_end_point(*self.get_end_pos())
        
    def special_draw(self, window):
        """
        Специальный метод для отрисовки линии с контуром.
        Сначала отрисовывает контур (если он есть), затем основную линию.

        Args:
            window: Объект окна, который предоставляет метод `draw()` для отрисовки фигур.
        """
        self.update() # Обновляем геометрию перед отрисовкой.

        # Отрисовываем контур, только если его толщина больше нуля.
        if self.__thickness > 0:
            window.draw(self.__thickness_shape)
        elif self.__thickness < 0:
            # Выбрасываем ошибку, если толщина контура отрицательная, так как это нелогично.
            raise TypeError(f'Недопустимая толщина ({self.__thickness}). Толщина контура не может быть отрицательной.')
        
        super().special_draw(window) # Отрисовываем основную линию (вызываем метод родительского класса).

@final 
class LineThin:
    """
    Класс для работы с тонкими линиями.
    Эти линии отрисовываются напрямую с использованием вершинных массивов, что обеспечивает
    высокую производительность для простых, однопиксельных или очень тонких линий,
    без дополнительной геометрии прямоугольников и кругов.
    """

    def __init__(self):
        """
        Инициализирует объект `LineThin`.
        Создает вершинный массив с двумя начальными вершинами, формирующими линию.
        """
        # Вершинный массив для отрисовки линии.
        self.__vertex_array = VertexArray()
        # Устанавливаем тип примитива как LINE_STRIP, что означает,
        # что вершины будут соединены последовательно, образуя линию.
        self.__vertex_array.set_primitive_type(VertexArray.PrimitiveType.LINE_STRIP)
        # Добавляем две начальные вершины (точки) линии.
        self.__vertex_array.append(Vertex(Vector2f(0, 0), COLOR_BLACK))
        self.__vertex_array.append(Vertex(Vector2f(0, 0), COLOR_BLACK))

    def get_ptr(self):
        """
        Возвращает указатель на базовый C++ вершинный массив.
        Этот метод используется для передачи объекта в низкоуровневые функции отрисовки.

        Returns:
            Указатель: Указатель на объект вершинного массива в C++.
        """
        return self.__vertex_array.get_ptr()

    def set_start_pos(self, x: float, y: float) -> Self:
        """
        Устанавливает начальную позицию линии.

        Args:
            x: Координата X начальной точки.
            y: Координата Y начальной точки.

        Returns:
            Self: Экземпляр объекта LineThin (для цепочки вызовов).
        """
        # Обновляем позицию первой вершины в вершинном массиве.
        self.__vertex_array.set_vertex_position(0, x, y)
        return self
    
    def set_end_pos(self, x: float, y: float) -> Self:
        """
        Устанавливает конечную позицию линии.

        Args:
            x: Координата X конечной точки.
            y: Координата Y конечной точки.

        Returns:
            Self: Экземпляр объекта LineThin (для цепочки вызовов).
        """
        # Обновляем позицию второй вершины в вершинном массиве.
        self.__vertex_array.set_vertex_position(1, x, y)
        return self
    
    def set_color(self, color: Color) -> Self:
        """
        Устанавливает один и тот же цвет для всей линии (обеих вершин).

        Args:
            color: Объект Color, определяющий RGBA значения для линии.

        Returns:
            Self: Экземпляр объекта LineThin (для цепочки вызовов).
        """
        # Устанавливаем один и тот же цвет для обеих вершин.
        self.__vertex_array.set_vertex_color(0, color)
        self.__vertex_array.set_vertex_color(1, color)
        return self
    
    def set_start_color(self, color: Color) -> Self:
        """
        Устанавливает цвет только для начальной точки линии.
        Это позволяет создавать линии с градиентным переходом цвета.

        Args:
            color: Объект Color, определяющий RGBA значения для начальной точки.

        Returns:
            Self: Экземпляр объекта LineThin (для цепочки вызовов).
        """
        # Устанавливаем цвет для первой вершины.
        self.__vertex_array.set_vertex_color(0, color)
        return self
    
    def set_end_color(self, color: Color) -> Self:
        """
        Устанавливает цвет только для конечной точки линии.
        Это позволяет создавать линии с градиентным переходом цвета.

        Args:
            color: Объект Color, определяющий RGBA значения для конечной точки.

        Returns:
            Self: Экземпляр объекта LineThin (для цепочки вызовов).
        """
        # Устанавливаем цвет для второй вершины.
        self.__vertex_array.set_vertex_color(1, color)
        return self

    def get_start_pos(self) -> tuple[float, float]:
        """
        Возвращает начальную позицию линии.

        Returns:
            tuple[float, float]: Кортеж (x, y) начальной точки.
        """
        # Извлекаем позицию первой вершины из вершинного массива.
        return self.__vertex_array.get_vertex(0).get_position().xy
    
    def get_end_pos(self) -> tuple[float, float]:
        """
        Возвращает конечную позицию линии.

        Returns:
            tuple[float, float]: Кортеж (x, y) конечной точки.
        """
        # Извлекаем позицию второй вершины из вершинного массива.
        return self.__vertex_array.get_vertex(1).get_position().xy
    
    def get_colors(self) -> tuple[Color, Color]:
        """
        Возвращает цвета начальной и конечной точек линии.

        Returns:
            tuple[Color, Color]: Кортеж из двух объектов Color (цвет начальной, цвет конечной).
        """
        return (
            self.__vertex_array.get_vertex(0).get_color(), # Цвет первой вершины.
            self.__vertex_array.get_vertex(1).get_color()  # Цвет второй вершины.
        )
    
    def get_vertex(self, index: int) -> Vertex:
        """
        Возвращает объект Vertex по указанному индексу.
        Полезно для прямого доступа и модификации отдельных вершин.

        Args:
            index: Индекс вершины (0 для начальной, 1 для конечной).

        Returns:
            Vertex: Объект Vertex.
        """
        return self.__vertex_array.get_vertex(index)


# Глобальные константы для часто используемых фигур.
# Использование Final гарантирует, что эти переменные не будут переназначены.
# Это удобно для стандартных, преднастроенных форм, которые можно переиспользовать.
CIRCLE_SHAPE: Final[CircleShape] = CircleShape(30)       # Стандартный круг с 30 точками.
RECTANGLE_SHAPE: Final[RectangleShape] = RectangleShape(100, 100) # Стандартный прямоугольник 100x100.
LINE_SHAPE: Final[LineShape] = LineShape()                       # Стандартная линия с контуром.
LINE_THIN: Final[LineThin] = LineThin()                         # Стандартная тонкая линия.


# Указатель на объект LinesThin в C++ (это псевдоним, используется для VertexArrayPtr).
LinesThinPtr = ctypes.c_void_p

class LinesThin:
    """
    Класс для работы с ломаными линиями (полилиниями) на основе вершинных массивов.
    Позволяет создавать сложные линии, состоящие из множества соединенных сегментов.
    """

    def __init__(self):
        """
        Инициализация объекта ломаной линии.
        """
        self.__colors: list[Color] = []       # Список объектов Color, по одному для каждой точки.
        self.__points: list[Vector2f] = []    # Список 2D-векторов Vector2f, представляющих координаты точек.
        
        # Вершинный массив для отрисовки линии.
        self.__vertex_array = VertexArray()
        # Устанавливаем тип примитива как LINE_STRIP, что означает,
        # что точки будут соединяться последовательно, образуя ломаную линию.
        self.__vertex_array.set_primitive_type(VertexArray.PrimitiveType.LINE_STRIP)

    def clear(self) -> "LinesThin":
        """
        Очищает ломаную линию, удаляя все точки и их цвета.
        Это приводит линию в исходное пустое состояние.

        Returns:
            Self: Возвращает сам объект для цепочки вызовов (fluent interface).
        """
        self.__colors.clear()
        self.__points.clear()
        self.__vertex_array.clear() # Очищаем базовый вершинный массив C++.
        return self

    def update_vertex_array(self):
        """
        Полностью перестраивает внутренний вершинный массив C++
        на основе текущих списков точек и цветов, хранящихся в Python.
        Этот метод эффективен, когда необходимо изменить несколько точек сразу,
        так как он очищает и заново заполняет весь массив.
        """
        self.__vertex_array.clear() # Очищаем текущий вершинный массив.
        # Пересоздаем вершинный массив из текущих данных Python.
        for point, point_color in zip(self.__points, self.__colors):
            self.__vertex_array.append(Vertex(point, point_color))

    def __len__(self) -> int:
        """
        Возвращает количество точек в ломаной линии.
        Это позволяет использовать функцию `len()` с объектами LinesThin.

        Returns:
            int: Количество точек, составляющих линию.
        """
        return len(self.__points)
    
    def remove_last_point(self) -> "LinesThin":
        """
        Удаляет последнюю точку из ломаной линии.
        Обновляет внутренние списки Python и перестраивает вершинный массив C++.

        Returns:
            Self: Возвращает сам объект для цепочки вызовов.
        """
        # Удаляем последний элемент из списков точек и цветов.
        self.__colors = self.__colors[:-1]
        self.__points = self.__points[:-1]
        self.update_vertex_array() # Полностью обновляем вершинный массив.
        return self

    def remove_first_point(self) -> "LinesThin":
        """
        Удаляет первую точку из ломаной линии.
        Обновляет внутренние списки Python и перестраивает вершинный массив C++.

        Returns:
            Self: Возвращает сам объект для цепочки вызовов.
        """
        # Удаляем первый элемент из списков точек и цветов.
        self.__colors = self.__colors[1:]
        self.__points = self.__points[1:]
        self.update_vertex_array() # Полностью обновляем вершинный массив.
        return self

    def append_point_to_end(self, x: float, y: float, color: Color = COLOR_BLACK):
        """
        Добавляет новую точку в конец ломаной линии.
        Это наиболее эффективный способ добавления точек, так как он
        напрямую добавляет вершину в вершинный массив C++ без полной его перестройки.

        Args:
            x: Координата X новой точки.
            y: Координата Y новой точки.
            color: Цвет новой точки (по умолчанию черный).
        """
        self.__colors.append(color)          # Добавляем цвет в список цветов.
        self.__points.append(Vector2f(x, y)) # Добавляем точку в список точек.
        # Оптимизация: добавляем только новую вершину в C++ массив,
        # вместо полной его перестройки, что быстрее.
        self.__vertex_array.append(Vertex(Vector2f(x, y), color))

    def append_point_to_begin(self, x: float, y: float, color: Color = COLOR_BLACK) -> "LinesThin":
        """
        Добавляет новую точку в начало ломаной линии.
        Этот метод менее эффективен, чем `append_point_to_end`,
        так как он требует полной перестройки вершинного массива C++.

        Args:
            x: Координата X новой точки.
            y: Координата Y новой точки.
            color: Цвет новой точки (по умолчанию черный).
            
        Returns:
            Self: Возвращает сам объект для цепочки вызовов.
        """
        self.__colors.insert(0, color)          # Вставляем цвет в начало списка цветов.
        self.__points.insert(0, Vector2f(x, y)) # Вставляем точку в начало списка точек.
        # Поскольку точка вставляется в начало, требуется полная перестройка вершинного массива.
        self.update_vertex_array()
        return self
        
    def set_point_color(self, index: int, color: Color) -> "LinesThin":
        """
        Устанавливает цвет точки по указанному индексу.

        Args:
            index: Индекс точки, цвет которой нужно изменить.
            color: Новый объект Color для этой точки.
            
        Returns:
            Self: Возвращает сам объект для цепочки вызовов.
        """
        self.__colors[index] = color # Обновляем цвет в списке Python.
        self.__vertex_array.set_vertex_color(index, color) # Обновляем цвет в вершинном массиве C++.
        return self

    def set_point_position(self, index: int, position: Vector2f) -> "LinesThin":
        """
        Устанавливает новую позицию для точки по указанному индексу.

        Args:
            index: Индекс точки, позицию которой нужно изменить.
            position: Новый 2D-вектор Vector2f, представляющий координаты точки.
            
        Returns:
            Self: Возвращает сам объект для цепочки вызовов.
        """
        self.__points[index] = position # Обновляем позицию в списке Python.
        self.__vertex_array.set_vertex_position(index, *position.xy) # Обновляем позицию в вершинном массиве C++.
        return self

    def move_point(self, index: int, vector: Vector2f) -> "LinesThin":
        """
        Сдвигает (перемещает) точку по указанному индексу на заданный вектор смещения.

        Args:
            index: Индекс точки, которую нужно сдвинуть.
            vector: 2D-вектор Vector2f, представляющий смещение по осям X и Y.
            
        Returns:
            Self: Возвращает сам объект для цепочки вызовов.
        """
        self.__points[index] = self.__points[index] + vector # Добавляем вектор смещения к текущей позиции.
        self.__vertex_array.set_vertex_position(index, *self.__points[index].xy) # Обновляем позицию в C++ массиве.
        return self

    def get_vertex_array(self) -> VertexArray:
        """
        Возвращает внутренний объект `VertexArray`, который используется для отрисовки линии.
        Полезно для прямого взаимодействия с вершинным массивом, если это необходимо.

        Returns:
            VertexArray: Объект вершинного массива, используемый для отрисовки линии.
        """
        return self.__vertex_array
    
    def get_ptr(self) -> LinesThinPtr:
        """
        Возвращает указатель на базовый C++ вершинный массив.
        Этот метод используется для передачи объекта в низкоуровневые функции отрисовки.

        Returns:
            LinesThinPtr: Указатель на C++ объект (фактически, указатель на VertexArray).
        """
        return self.__vertex_array.get_ptr()
    
    def __getitem__(self, index: int) -> tuple[Vector2f, Color]:
        """
        Позволяет получить точку и ее цвет по индексу, используя синтаксис `line[index]`.

        Args:
            index: Индекс точки, которую нужно получить.
            
        Returns:
            tuple: Кортеж, содержащий 2D-вектор (координаты точки) и объект Color (цвет точки).
            
        Raises:
            IndexError: Если индекс выходит за пределы диапазона доступных точек.
        """
        return (self.__points[index], self.__colors[index])
    
# Глобальная константа для стандартного объекта LinesThin.
# Это позволяет легко использовать одну и ту же ломаную линию в разных местах кода,
# если она не требует отдельного экземпляра.
LINES_THIN: Final[LinesThin] = LinesThin()

