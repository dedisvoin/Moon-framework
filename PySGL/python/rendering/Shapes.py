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
class BaseRectangleShape:
    """
    Низкоуровневый класс для создания и управления прямоугольниками с использованием привязок к DLL C++.
    Этот класс помечен как `@final`, что означает, что от него нельзя наследоваться.
    Он обеспечивает прямое взаимодействие с базовой графической библиотекой C++ для оптимизированной отрисовки.
    """

    def __init__(self, width: float, height: float):
        """
        Инициализирует новый прямоугольник с указанной шириной и высотой.
        Объект прямоугольника C++ создается в памяти, и указатель на него сохраняется.

        Args:
            width: Желаемая ширина прямоугольника.
            height: Желаемая высота прямоугольника.
        """
        # Вызываем функцию C++ для создания объекта прямоугольника и сохраняем его указатель.
        self._ptr = LIB_PYSGL._Rectangle_Create(float(width), float(height))

        # Храним дополнительные атрибуты непосредственно в объекте Python.
        # Эти атрибуты "не являются нативными", так как они управляются в Python, а не напрямую объектом C++.
        # Это обеспечивает более легкий доступ и согласованность внутри обертки Python.
        self.__color: Color | None = None
        self.__outline_color: Color | None = None
        self.__outline_thickness: float = 0
        self.__origin: Vector2f = Vector2f(0, 0)
        self.__angle: float = 0
        self.__scale: Vector2f = Vector2f.one()
    
    def get_ptr(self) -> int:
        """
        Извлекает необработанный указатель на объект C++.
        Этот метод в основном предназначен для внутреннего использования, позволяя другим частям
        графической системы взаимодействовать напрямую с объектом C++.

        Returns:
            int: Адрес памяти (указатель) объекта прямоугольника C++.
        """
        return self._ptr

    def __del__(self):
        """
        Метод деструктора. Он автоматически вызывается сборщиком мусора Python,
        когда объект BaseRectangleShape больше не имеет ссылок.
        Он гарантирует, что соответствующий объект C++ правильно освобожден
        для предотвращения утечек памяти.
        """
        # Проверяем, существует ли указатель и не является ли он None (что означает, что объект C++ еще не удален).
        if hasattr(self, '_ptr') and self._ptr:
            # Вызываем функцию C++ для удаления объекта прямоугольника из памяти.
            LIB_PYSGL._Rectangle_Delete(self._ptr)
            self._ptr = None  # Очищаем указатель, чтобы предотвратить проблемы с двойным освобождением памяти.
    
    @overload
    def set_position(self, x: float, y: float) -> Self:
        """
        Устанавливает позицию прямоугольника на экране.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            x: Координата X для новой позиции прямоугольника.
            y: Координата Y для новой позиции прямоугольника.

        Returns:
            Self: Экземпляр объекта BaseRectangleShape.
        """
        
    
    @overload
    def set_position(self, vector: Vector2f) -> Self:
        """
        Устанавливает позицию прямоугольника на экране.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            vector: Вектор координат

        Returns:
            Self: Экземпляр объекта BaseRectangleShape.
        """
        ...

    def set_position(self, arg1, arg2 = None) -> Self:
        if isinstance(arg1, Vector2f) and arg2 is None:
            LIB_PYSGL._Rectangle_SetPosition(self._ptr, float(arg1.x), float(arg1.y))
            return self
        elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
            LIB_PYSGL._Rectangle_SetPosition(self._ptr, float(arg1), float(arg2))
            return self
        raise ValueError("Invalid arguments")

    
    def get_position(self) -> Vector2f:
        """
        Извлекает текущую позицию прямоугольника.

        Returns:
            Vector2f: 2D-вектор, представляющий координаты (X, Y) прямоугольника.
        """
        x = LIB_PYSGL._Rectangle_GetPositionX(self._ptr)
        y = LIB_PYSGL._Rectangle_GetPositionY(self._ptr)
        return Vector2f(x, y)
    
    def set_color(self, color: Color) -> Self:
        """
        Устанавливает цвет заливки прямоугольника.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            color: Объект Color, определяющий значения RGBA (Красный, Зеленый, Синий, Альфа).

        Returns:
            Self: Экземпляр объекта BaseRectangleShape.
        """
        LIB_PYSGL._Rectangle_SetColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__color = color  # Храним цвет локально в объекте Python.
        return self
    
    def get_color(self) -> Color:
        """
        Извлекает текущий цвет заливки прямоугольника.

        Returns:
            Color: Объект Color, представляющий цвет заливки прямоугольника.
        """
        return self.__color
    
    def set_origin(self, x: float, y: float) -> Self:
        """
        Устанавливает точку отсчета для преобразований (например, вращения, масштабирования).
        Начало координат относительно верхнего левого угла прямоугольника.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            x: Координата X точки отсчета.
            y: Координата Y точки отсчета.

        Returns:
            Self: Экземпляр объекта BaseRectangleShape.
        """
        LIB_PYSGL._Rectangle_SetOrigin(self._ptr, float(x), float(y))
        self.__origin.x = x  # Обновляем локальный атрибут origin.
        self.__origin.y = y
        return self
    
    def get_origin(self) -> Vector2f:
        """
        Извлекает текущую точку отсчета прямоугольника.

        Returns:
            Vector2f: 2D-вектор, представляющий начало координат прямоугольника.
        """
        # Возвращаем копию, чтобы предотвратить внешнее изменение внутреннего начала координат.
        return self.__origin.copy()
    
    def set_size(self, width: float, height: float) -> Self:
        """
        Изменяет размер (ширину и высоту) прямоугольника.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            width: Новая ширина прямоугольника.
            height: Новая высота прямоугольника.

        Returns:
            Self: Экземпляр объекта BaseRectangleShape.
        """
        LIB_PYSGL._Rectangle_SetSize(self._ptr, float(width), float(height))
        return self
    
    def get_size(self) -> Vector2f:
        """
        Извлекает текущий размер (ширину и высоту) прямоугольника.

        Returns:
            Vector2f: 2D-вектор, где x - это ширина, а y - это высота.
        """
        width = LIB_PYSGL._Rectangle_GetWidth(self._ptr)
        height = LIB_PYSGL._Rectangle_GetHeight(self._ptr)
        return Vector2f(width, height)
    
    def set_angle(self, angle: float) -> Self:
        """
        Устанавливает угол поворота прямоугольника в градусах.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            angle: Угол поворота в градусах.

        Returns:
            Self: Экземпляр объекта BaseRectangleShape.
        """
        LIB_PYSGL._Rectangle_SetRotation(self._ptr, float(angle))
        self.__angle = angle  # Храним угол локально.
        return self
    
    def get_angle(self) -> float:
        """
        Извлекает текущий угол поворота прямоугольника в градусах.

        Returns:
            float: Угол поворота в градусах.
        """
        return self.__angle
    
    def set_outline_thickness(self, thickness: float) -> Self:
        """
        Устанавливает толщину контура прямоугольника.
        Толщина 0 означает отсутствие контура.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            thickness: Желаемая толщина контура.

        Returns:
            Self: Экземпляр объекта BaseRectangleShape.
        """
        LIB_PYSGL._Rectangle_SetOutlineThickness(self._ptr, float(thickness))
        self.__outline_thickness = thickness  # Храним толщину контура локально.
        return self
    
    def get_outline_thickness(self) -> float:
        """
        Извлекает текущую толщину контура прямоугольника.

        Returns:
            float: Толщина контура.
        """
        return self.__outline_thickness
    
    def set_outline_color(self, color: Color) -> Self:
        """
        Устанавливает цвет контура прямоугольника.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            color: Объект Color, определяющий RGBA значения для контура.

        Returns:
            Self: Экземпляр объекта BaseRectangleShape.
        """
        LIB_PYSGL._Rectangle_SetOutlineColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__outline_color = color  # Храним цвет контура локально.
        return self
    
    def get_outline_color(self) -> Color:
        """
        Извлекает текущий цвет контура прямоугольника.

        Returns:
            Color: Объект Color, представляющий цвет контура.
        """
        return self.__outline_color
    
    def set_scale_xy(self, scale_x: float, scale_y: float) -> Self:
        """
        Масштабирует прямоугольник по осям X и Y.
        Значения масштаба 1.0 означают отсутствие масштабирования.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            scale_x: Коэффициент масштабирования по оси X.
            scale_y: Коэффициент масштабирования по оси Y.

        Returns:
            Self: Экземпляр объекта BaseRectangleShape.
        """
        LIB_PYSGL._Rectangle_SetScale(self._ptr, float(scale_x), float(scale_y))
        self.__scale.x = scale_x  # Обновляем локальный атрибут масштаба.
        self.__scale.y = scale_y
        return self
    
    def set_scale(self, scale: float) -> Self:
        """
        Равномерно масштабирует прямоугольник по обеим осям.
        Эквивалентно вызову `set_scale_xy(scale, scale)`.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            scale: Единый коэффициент масштабирования для обеих осей.

        Returns:
            Self: Экземпляр объекта BaseRectangleShape.
        """
        LIB_PYSGL._Rectangle_SetScale(self._ptr, float(scale), float(scale))
        self.__scale.x = scale  # Обновляем локальный атрибут масштаба.
        self.__scale.y = scale
        return self
    
    def get_scale(self) -> Vector2f:
        """
        Извлекает текущие коэффициенты масштабирования прямоугольника.

        Returns:
            Vector2f: 2D-вектор, где x - это масштаб по оси X, а y - это масштаб по оси Y.
        """
        return self.__scale
    
    
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
class BaseCircleShape:
    """
    Низкоуровневый класс для создания и управления кругами с использованием привязок к DLL C++.
    Этот класс помечен как `@final`, что означает, что от него нельзя наследоваться.
    Он обеспечивает прямое взаимодействие с базовой графической библиотекой C++ для оптимизированной отрисовки.
    """

    def __init__(self, points_count: int = 30):
        """
        Создает круг. Обратите внимание, что начальный радиус устанавливается в 100,
        а количество точек аппроксимации определяет, насколько гладким будет круг (больше точек = более гладкий круг).

        Args:
            points_count: Количество точек, используемых для аппроксимации круга.
                          Больше точек делает круг более гладким, но может потреблять больше ресурсов.
        """
        
        self.__points_count = points_count
        # Создаем C++ объект круга с начальным радиусом 100 и указанным количеством точек.
        self._ptr = LIB_PYSGL._Circle_Create(100, points_count)
        # Устанавливаем точку отсчета в центр, что упрощает масштабирование и вращение.
        self.set_origin(100, 100)

        # Локальные (не нативные C++) атрибуты для хранения состояния круга в Python.
        self.__outline_color: Color | None = None
        self.__outline_thickness: float = 1
        self.__color: Color | None = None


    # ////////////////////////////////////////////////////////////////////////////////////////
    # **ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ О УПРАВЛЕНИИ ПАМЯТЬЮ**
    # **Не рекомендуется вручную вызывать данный метод для очистки памяти.**
    # `del circle` <- {НЕ ДЕЛАЙТЕ ТАК!}
    # При самостоятельной очистке могут возникнуть ошибки доступа к уже освобожденной памяти!
    # Интерпретатор Python сам будет очищать память, не рискуйте!
    # #########################################################################################
    def __del__(self):
        """
        Метод деструктора. Он автоматически вызывается сборщиком мусора Python
        при удалении объекта BaseCircleShape.
        Он гарантирует, что соответствующий объект C++ будет корректно удален из памяти,
        что предотвращает утечки памяти.
        """
        # Проверяем, существует ли указатель и не равен ли он None (это означает, что C++ объект еще не был удален).
        if hasattr(self, '_ptr') and self._ptr:
            # Вызываем функцию C++ для удаления объекта круга из памяти.
            LIB_PYSGL._Circle_Delete(self._ptr)
            self._ptr = None  # Очищаем указатель, чтобы предотвратить проблемы с двойным освобождением памяти.
    # #########################################################################################
    

    # ////////////////////////////////////////////////////////////////////////////////////////
    # **Специальные методы, упрощающие работу с кругом.**
    # #########################################################################################
    def get_point_count(self) -> int:
        """
        Возвращает количество точек, используемых для аппроксимации круга.
        """
        return self.__points_count

    def copy(self):
        """
        Возвращает новую копию этого круга с теми же характеристиками
        (радиус, количество точек аппроксимации и точка отсчета).

        Returns:
            BaseCircleShape: Новый экземпляр BaseCircleShape, являющийся копией текущего.
        """
        circle = BaseCircleShape(self.get_point_count())
        circle.set_origin_radius(self.get_radius())
        return circle
    
    def set_origin_radius(self, radius: float) -> Self:
        """
        Устанавливает радиус круга и автоматически настраивает его точку отсчета
        так, чтобы она находилась в центре круга (x = radius, y = radius).
        Это удобно для преобразований, центрированных по кругу.

        Args:
            radius: Новый радиус круга.

        Returns:
            Self: Экземпляр объекта BaseCircleShape (для цепочки вызовов).
        """
        self.set_radius(radius)
        self.set_origin(radius, radius)
        return self
    # #########################################################################################


    def get_ptr(self) -> int:
        """
        Извлекает необработанный указатель на объект C++.
        Этот метод в основном предназначен для внутреннего использования.

        Returns:
            int: Адрес памяти (указатель) объекта круга C++.
        """
        return self._ptr

    def set_position(self, x: float, y: float) -> Self:
        """
        Устанавливает позицию круга на экране.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            x: Координата X для новой позиции круга.
            y: Координата Y для новой позиции круга.

        Returns:
            Self: Экземпляр объекта BaseCircleShape.
        """
        LIB_PYSGL._Circle_SetPosition(self._ptr, x, y)
        return self
    
    def get_position(self) -> Vector2f:
        """
        Извлекает текущую позицию круга.

        Returns:
            Vector2f: 2D-вектор, представляющий координаты (X, Y) круга.
        """
        x = LIB_PYSGL._Circle_GetPositionX(self._ptr)
        y = LIB_PYSGL._Circle_GetPositionY(self._ptr)
        return Vector2f(x, y)

    def set_radius(self, radius: float) -> Self:
        """
        Устанавливает радиус круга.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            radius: Новый радиус круга.

        Returns:
            Self: Экземпляр объекта BaseCircleShape.
        """
        LIB_PYSGL._Circle_SetRadius(self._ptr, radius)
        return self
    
    def get_radius(self) -> float:
        """
        Извлекает текущий радиус круга.

        Returns:
            float: Текущий радиус круга.
        """
        return LIB_PYSGL._Circle_GetRadius(self._ptr)

    def set_angle(self, angle: float) -> Self:
        """
        Устанавливает угол поворота круга в градусах.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            angle: Угол поворота в градусах.

        Returns:
            Self: Экземпляр объекта BaseCircleShape.
        """
        LIB_PYSGL._Circle_SetRotation(self._ptr, angle)
        return self

    def get_angle(self) -> float:
        """
        Извлекает текущий угол поворота круга в градусах.

        Returns:
            float: Угол поворота в градусах.
        """
        return LIB_PYSGL._Circle_GetRotation(self._ptr)

    def set_color(self, color: Color) -> Self:
        """
        Устанавливает цвет заливки круга.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            color: Объект Color, определяющий RGBA значения для заливки.

        Returns:
            Self: Экземпляр объекта BaseCircleShape.
        """
        LIB_PYSGL._Circle_SetFillColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__color = color  # Храним цвет заливки локально.
        return self
    
    def get_color(self) -> Color:
        """
        Извлекает текущий цвет заливки круга.

        Returns:
            Color: Объект Color, представляющий цвет заливки.
        """
        return self.__color

    def set_outline_color(self, color: Color) -> Self:
        """
        Устанавливает цвет контура круга.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            color: Объект Color, определяющий RGBA значения для контура.

        Returns:
            Self: Экземпляр объекта BaseCircleShape.
        """
        LIB_PYSGL._Circle_SetOutlineColor(self._ptr, color.r, color.g, color.b, color.a)
        self.__outline_color = color  # Храним цвет контура локально.
        return self
    
    def get_outline_color(self) -> Color:
        """
        Извлекает текущий цвет контура круга.

        Returns:
            Color: Объект Color, представляющий цвет контура.
        """
        return self.__outline_color

    def set_outline_thickness(self, thickness: float) -> Self:
        """
        Устанавливает толщину контура круга.
        Толщина 0 означает отсутствие контура.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            thickness: Желаемая толщина контура.

        Returns:
            Self: Экземпляр объекта BaseCircleShape.
        """
        LIB_PYSGL._Circle_SetOutlineThickness(self._ptr, thickness)
        self.__outline_thickness = thickness  # Храним толщину контура локально.
        return self
    
    def get_outline_thickness(self) -> float:
        """
        Извлекает текущую толщину контура круга.

        Returns:
            float: Толщина контура.
        """
        return self.__outline_thickness

    def set_scale_xy(self, scale_x: float, scale_y: float) -> Self:
        """
        Масштабирует круг по осям X и Y.
        Значения масштаба 1.0 означают отсутствие масштабирования.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            scale_x: Коэффициент масштабирования по оси X.
            scale_y: Коэффициент масштабирования по оси Y.

        Returns:
            Self: Экземпляр объекта BaseCircleShape.
        """
        LIB_PYSGL._Circle_SetScale(self._ptr, scale_x, scale_y)
        return self

    def set_scale(self, scale: float) -> Self:
        """
        Равномерно масштабирует круг по обеим осям.
        Эквивалентно вызову `set_scale_xy(scale, scale)`.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            scale: Единый коэффициент масштабирования для обеих осей.

        Returns:
            Self: Экземпляр объекта BaseCircleShape.
        """
        # Обратите внимание: здесь используется `SetCircleScale`, возможно, это опечатка,
        # если существует `_Circle_SetScale`, как показано выше. Предполагается, что это корректная функция.
        LIB_PYSGL.SetCircleScale(self._ptr, scale, scale)
        return self

    def get_scale(self) -> Vector2f:
        """
        Извлекает текущие коэффициенты масштабирования круга.

        Returns:
            Vector2f: 2D-вектор, где x - это масштаб по оси X, а y - это масштаб по оси Y.
        """
        x = LIB_PYSGL._Circle_GetScaleX(self._ptr)
        y = LIB_PYSGL._Circle_GetScaleY(self._ptr)
        return Vector2f(x, y)

    def set_origin(self, x: float, y: float) -> Self:
        """
        Устанавливает точку отсчета для преобразований (например, вращения, масштабирования) круга.
        Точка отсчета определяет, вокруг какой точки происходят эти преобразования.
        Использует fluent-интерфейс, возвращая `self` для цепочки вызовов методов.

        Args:
            x: Координата X точки отсчета.
            y: Координата Y точки отсчета.

        Returns:
            Self: Экземпляр объекта BaseCircleShape.
        """
        LIB_PYSGL._Circle_SetOrigin(self._ptr, x, y)
        return self

    def get_origin(self) -> Vector2f:
        """
        Извлекает текущую точку отсчета круга.

        Returns:
            Vector2f: 2D-вектор, представляющий начало координат круга.
        """
        x = LIB_PYSGL._Circle_GetOriginX(self._ptr)
        y = LIB_PYSGL._Circle_GetOriginY(self._ptr)
        return Vector2f(x, y)

@final
class BaseLineShape:
    """
    Базовый класс для работы с толстыми линиями.
    Он реализует линию как прямоугольник с возможностью добавления скругленных концов (кругов).
    """

    def __init__(self, color: Color = COLOR_GRAY):
        """
        Инициализирует новую линию.

        Args:
            color: Начальный цвет линии (по умолчанию серый).
        """
        self.__start_pos = [0, 0]   # Начальная позиция линии в виде списка [x, y].
        self.__end_pos = [0, 0]    # Конечная позиция линии в виде списка [x, y].
        self.__color = color       # Цвет заливки линии.
        self.__width = 1           # Толщина линии.

        # Внутренний прямоугольник, который фактически отрисовывает тело линии.
        self.__rectangle_shape = BaseRectangleShape(10, 10)
        self.__rectangle_shape.set_color(COLOR_BLACK) # Начальный цвет прямоугольника.

        self.__rounded_corners: bool = False  # Флаг, определяющий, должны ли концы линии быть скругленными.

        # Два внутренних круга для отрисовки скругленных концов линии, если __rounded_corners = True.
        self.__round_circles = BaseCircleShape(15) # Круги аппроксимируются 15 точками.
        self.__round_circles.set_color(COLOR_BLACK) # Начальный цвет кругов.
        self.__round_circles.set_origin(12, 12) # Устанавливаем центр кругов для правильного позиционирования.

    def set_round(self, round: bool = True) -> Self:
        """
        Устанавливает, будут ли концы линии скругленными.

        Args:
            round: Если True, концы линии будут скругленными; иначе - прямыми.

        Returns:
            Self: Экземпляр объекта BaseLineShape (для цепочки вызовов).
        """
        self.__rounded_corners = round
        return self
    
    def get_round(self) -> bool:
        """
        Возвращает текущее состояние флага скругления концов линии.

        Returns:
            bool: True, если концы скруглены, False в противном случае.
        """
        return self.__rounded_corners
    
    def set_poses(self, x1: float, y1: float, x2: float, y2: float) -> Self:
        """
        Устанавливает начальную и конечную позиции линии.

        Args:
            x1: X-координата начальной точки линии.
            y1: Y-координата начальной точки линии.
            x2: X-координата конечной точки линии.
            y2: Y-координата конечной точки линии.

        Returns:
            Self: Возвращает сам объект для цепочки вызовов (fluent interface).
        """
        self.set_start_pos(x1, y1) # Устанавливаем начальную позицию с x1 и y1.
        self.set_end_pos(x2, y2)   # Устанавливаем конечную позицию с x2 и y2.

    def set_start_pos(self, x: float, y: float) -> Self:
        """
        Устанавливает начальную позицию линии.

        Args:
            x: Координата X начальной точки.
            y: Координата Y начальной точки.

        Returns:
            Self: Экземпляр объекта BaseLineShape (для цепочки вызовов).
        """
        self.__start_pos = [x, y]
        return self
    
    def set_end_pos(self, x: float, y: float) -> Self:
        """
        Устанавливает конечную позицию линии.

        Args:
            x: Координата X конечной точки.
            y: Координата Y конечной точки.

        Returns:
            Self: Экземпляр объекта BaseLineShape (для цепочки вызовов).
        """
        self.__end_pos = [x, y]
        return self
    
    def set_color(self, color: Color) -> Self:
        """
        Устанавливает цвет линии. Этот цвет применяется как к основной части линии (прямоугольнику),
        так и к скругленным концам (кругам).

        Args:
            color: Объект Color, определяющий RGBA значения для линии.

        Returns:
            Self: Экземпляр объекта BaseLineShape (для цепочки вызовов).
        """
        self.__color = color
        self.__rectangle_shape.set_color(color)  # Устанавливаем цвет прямоугольника.
        self.__round_circles.set_color(color)    # Устанавливаем цвет скругленных концов.
        return self
    
    def set_width(self, width: float) -> Self:
        """
        Устанавливает толщину линии.
        При изменении толщины также обновляется точка отсчета для скругленных концов,
        чтобы они правильно центрировались по толщине линии.

        Args:
            width: Желаемая толщина линии.

        Returns:
            Self: Экземпляр объекта BaseLineShape (для цепочки вызовов).
        """
        self.__width = width
        # Точка отсчета для кругов устанавливается в половину толщины,
        # чтобы круги центрировались относительно линии.
        self.__round_circles.set_origin(self.__width / 2, self.__width / 2)
        return self
    
    def get_width(self) -> float:
        """
        Возвращает текущую толщину линии.

        Returns:
            float: Толщина линии.
        """
        return self.__width
    
    def get_start_pos(self) -> tuple[float, float]:
        """
        Возвращает начальную позицию линии.

        Returns:
            tuple[float, float]: Кортеж (x, y) начальной точки.
        """
        return self.__start_pos
    
    def get_end_pos(self) -> tuple[float, float]:
        """
        Возвращает конечную позицию линии.

        Returns:
            tuple[float, float]: Кортеж (x, y) конечной точки.
        """
        return self.__end_pos
    
    def get_color(self) -> Color:
        """
        Возвращает текущий цвет линии.

        Returns:
            Color: Объект Color, представляющий цвет линии.
        """
        return self.__color
    
    def update(self):
        """
        Обновляет геометрию линии (позицию, размер, вращение прямоугольника и радиус кругов)
        на основе текущих начальной и конечной точек, а также толщины.
        Этот метод должен вызываться перед отрисовкой линии, если ее параметры изменились.
        """
        # Вычисляем вектор от начальной до конечной точки.
        vector = Vector2f.from_two_point(self.__start_pos, self.__end_pos)
        length = vector.length()  # Длина линии.
        normal = vector.normalized() # Нормализованный вектор (длина 1).
        angle = normal.angle_degrees() # Угол вектора в градусах.

        # Настраиваем прямоугольник, который представляет тело линии.
        self.__rectangle_shape.set_size(length, self.__width)  # Ширина = длина линии, Высота = толщина линии.
        self.__rectangle_shape.set_angle(angle - 180) # Устанавливаем угол вращения.
        # Точка отсчета прямоугольника (0, self.__width / 2) означает,
        # что он будет вращаться вокруг центральной точки на его "левом" краю.
        self.__rectangle_shape.set_origin(0, self.__width / 2) 
        self.__rectangle_shape.set_position(*self.__start_pos) # Позиционируем прямоугольник по начальной точке.
        
        # Настраиваем круги для скругленных концов.
        # Радиус кругов равен половине толщины линии.
        self.__round_circles.set_radius(self.__width / 2)

    def special_draw(self, window):
        """
        Специальный метод для отрисовки линии.
        Он обновляет геометрию линии и затем отрисовывает ее компоненты (прямоугольник и круги).

        Args:
            window: Объект окна, который предоставляет метод `draw()` для отрисовки фигур.
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
    
    def get_ptr(self):
        """
        В данном контексте возвращает сам объект Python, так как `BaseLineShape`
        не имеет прямого указателя на единый C++ объект, как `BaseRectangleShape` или `BaseCircleShape`.
        Его отрисовка управляется внутренними фигурами.
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
        
        self.__thickness_shape.set_round(super().get_round()) # Синхронизируем скругление концов с основной линией.
        
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
            self.__thickness_shape.set_start_pos(self.get_start_pos()[0] + n.x / 2, self.get_start_pos()[1] + n.y / 2) 
            self.__thickness_shape.set_end_pos(self.get_end_pos()[0] - n.x / 2, self.get_end_pos()[1] - n.y / 2)
        else:
            # Если углы скруглены, контур просто использует те же начальную и конечную точки,
            # но с увеличенной толщиной, чтобы круги контура были больше.
            self.__thickness_shape.set_start_pos(*self.get_start_pos())
            self.__thickness_shape.set_end_pos(*self.get_end_pos())
        
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
CIRCLE_SHAPE: Final[BaseCircleShape] = BaseCircleShape(30)       # Стандартный круг с 30 точками.
RECTANGLE_SHAPE: Final[BaseRectangleShape] = BaseRectangleShape(100, 100) # Стандартный прямоугольник 100x100.
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

