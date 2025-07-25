import ctypes
import os
from typing import Self

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
            print("Library not found at", lib_path)
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

# Тип указателя на нативный FloatRect
FloatRectPtr = ctypes.c_void_p

# Регистрация функций для работы с FloatRect в нативной библиотеке
LIB_PYSGL._FloatRect_Create.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._FloatRect_Create.restype = ctypes.c_void_p
LIB_PYSGL._FloatRect_Delete.argtypes = [ctypes.c_void_p]
LIB_PYSGL._FloatRect_Delete.restype = None
LIB_PYSGL._FloatRect_GetPositionX.argtypes = [ctypes.c_void_p]
LIB_PYSGL._FloatRect_GetPositionX.restype = ctypes.c_float
LIB_PYSGL._FloatRect_GetPositionY.argtypes = [ctypes.c_void_p]
LIB_PYSGL._FloatRect_GetPositionY.restype = ctypes.c_float
LIB_PYSGL._FloatRect_GetWidth.argtypes = [ctypes.c_void_p]
LIB_PYSGL._FloatRect_GetWidth.restype = ctypes.c_float
LIB_PYSGL._FloatRect_GetHeight.argtypes = [ctypes.c_void_p]
LIB_PYSGL._FloatRect_GetHeight.restype = ctypes.c_float
LIB_PYSGL._FloatRect_SetPosition.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._FloatRect_SetPosition.restype = None
LIB_PYSGL._FloatRect_SetSize.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._FloatRect_SetSize.restype = None


class FloatRect:
    """
    Класс прямоугольной области с плавающей точкой.
    Соответствует sf::FloatRect в SFML.
    
    Атрибуты:
        _ptr: Указатель на нативный объект FloatRect
    
    Методы:
        get_ptr(): Получить указатель на нативный объект
        get_postion(): Получить позицию (x, y)
        get_size(): Получить размеры (width, height)
        set_position(): Установить позицию
        set_size(): Установить размеры
    """
    
    def __init__(self, x: float, y: float, w: float, h: float) -> Self:
        """
        Создает новый FloatRect с указанными параметрами.
        
        Аргументы:
            x: Позиция по X
            y: Позиция по Y
            w: Ширина
            h: Высота
        """
        self._ptr = LIB_PYSGL._FloatRect_Create(x, y, w, h)

    def get_ptr(self) -> FloatRectPtr:
        """Возвращает указатель на нативный объект FloatRect"""
        return self._ptr

    def __del__(self) -> None:
        """Освобождает ресурсы нативного объекта"""
        LIB_PYSGL._FloatRect_Delete(self._ptr)

    def get_postion(self) -> tuple[float, float]:
        """
        Возвращает текущую позицию прямоугольника.
        
        Возвращает:
            Кортеж (x, y)
        """
        return (
            LIB_PYSGL._FloatRect_GetPositionX(self._ptr),
            LIB_PYSGL._FloatRect_GetPositionY(self._ptr),
        )
    
    def get_size(self) -> tuple[float, float]:
        """
        Возвращает текущие размеры прямоугольника.
        
        Возвращает:
            Кортеж (width, height)
        """
        return (
            LIB_PYSGL._FloatRect_GetWidth(self._ptr),
            LIB_PYSGL._FloatRect_GetHeight(self._ptr),
        )
    
    def set_position(self, x: float | None = None, y: float | None = None) -> "FloatRect":
        """
        Устанавливает новую позицию прямоугольника.
        Поддерживает частичное обновление (только X или только Y).
        
        Аргументы:
            x: Новая позиция X (None - не изменять)
            y: Новая позиция Y (None - не изменять)
            
        Возвращает:
            self для цепных вызовов
        """
        if x is not None:
            LIB_PYSGL._FloatRect_SetPosition(self._ptr, x, self.get_postion()[1])
        if y is not None:
            LIB_PYSGL._FloatRect_SetPosition(self._ptr, self.get_postion()[0], y)
        return self
    
    def set_size(self, w: float | None = None, h: float | None = None) -> "FloatRect":
        """
        Устанавливает новые размеры прямоугольника.
        Поддерживает частичное обновление (только width или только height).
        
        Аргументы:
            w: Новая ширина (None - не изменять)
            h: Новая высота (None - не изменять)
            
        Возвращает:
            self для цепных вызовов
        """
        if w is not None:
            LIB_PYSGL._FloatRect_SetSize(self._ptr, w, self.get_size()[1])
        if h is not None:
            LIB_PYSGL._FloatRect_SetSize(self._ptr, self.get_size()[0], h)
        return self


# Тип указателя на нативный View
ViewPtr = ctypes.c_void_p

# Регистрация функций для работы с View в нативной библиотеке
LIB_PYSGL._View_Create.argtypes = [FloatRectPtr]
LIB_PYSGL._View_Create.restype = ViewPtr
LIB_PYSGL._View_GetCenterX.argtypes = [ViewPtr]
LIB_PYSGL._View_GetCenterX.restype = ctypes.c_float
LIB_PYSGL._View_GetCenterY.argtypes = [ViewPtr]
LIB_PYSGL._View_GetCenterY.restype = ctypes.c_float
LIB_PYSGL._View_GetPositionX.argtypes = [ViewPtr]
LIB_PYSGL._View_GetPositionX.restype = ctypes.c_float
LIB_PYSGL._View_GetPositionY.argtypes = [ViewPtr]
LIB_PYSGL._View_GetPositionY.restype = ctypes.c_float
LIB_PYSGL._View_GetAngle.argtypes = [ViewPtr]
LIB_PYSGL._View_GetAngle.restype = ctypes.c_float
LIB_PYSGL._View_GetWidth.argtypes = [ViewPtr]
LIB_PYSGL._View_GetWidth.restype = ctypes.c_float
LIB_PYSGL._View_GetHeight.argtypes = [ViewPtr]
LIB_PYSGL._View_GetHeight.restype = ctypes.c_float 
LIB_PYSGL._View_Rotate.argtypes = [ViewPtr, ctypes.c_float]
LIB_PYSGL._View_Rotate.restype = None
LIB_PYSGL._View_Reset.argtypes = [ViewPtr, FloatRectPtr]
LIB_PYSGL._View_Reset.restype = None
LIB_PYSGL._View_Move.argtypes = [ViewPtr, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._View_Move.restype = None
LIB_PYSGL._View_SetCenter.argtypes = [ViewPtr, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._View_SetCenter.restype = None
LIB_PYSGL._View_SetAngle.argtypes = [ViewPtr, ctypes.c_float]
LIB_PYSGL._View_SetAngle.restype = None
LIB_PYSGL._View_SetViewport.argtypes = [ViewPtr, FloatRectPtr]
LIB_PYSGL._View_SetViewport.restype = None
LIB_PYSGL._View_SetSize.argtypes = [ViewPtr, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._View_SetSize.restype = None
LIB_PYSGL._View_Zoom.argtypes = [ViewPtr, ctypes.c_float]
LIB_PYSGL._View_Zoom.restype = None


class View:
    """
    Класс камеры/вида (соответствует sf::View в SFML).
    Позволяет управлять областью просмотра, поворотом и масштабом.
    
    Атрибуты:
        _ptr: Указатель на нативный объект View
        __float_rect: Базовый прямоугольник вида
    
    Методы:
        from_view_ptr(): Создает View из существующего указателя
        set_center(): Устанавливает центр вида
        set_size(): Устанавливает размер вида
        set_viewport(): Устанавливает вьюпорт
        set_zoom(): Устанавливает масштаб
        set_angle(): Устанавливает угол поворота
        move(): Перемещает вид
        get_center(): Возвращает центр вида
        get_angle(): Возвращает угол поворота
        get_size(): Возвращает размер вида
        rotate(): Поворачивает вид
        reset(): Сбрасывает параметры вида
    """
    
    @classmethod
    def from_view_ptr(self, view_ptr: ViewPtr) -> "View":
        """
        Создает объект View из существующего указателя на нативный View.
        
        Аргументы:
            view_ptr: Указатель на нативный View
            
        Возвращает:
            Новый экземпляр View
        """
        size = [
            LIB_PYSGL._View_GetWidth(view_ptr),
            LIB_PYSGL._View_GetHeight(view_ptr)
        ]
        pos = [
            LIB_PYSGL._View_GetPositionX(view_ptr),
            LIB_PYSGL._View_GetPositionY(view_ptr)
        ]

        view = View(FloatRect(*pos, *size))
        view.set_ptr(view_ptr)
        return view

    def __del__(self):
        """Освобождает ресурсы (в текущей реализации просто удаляет ссылку)"""
        del self

    def __init__(self, float_rect: FloatRect) -> Self:
        """
        Создает новый View на основе FloatRect.
        
        Аргументы:
            float_rect: Базовый прямоугольник для вида
        """
        self.__float_rect = float_rect
        self._ptr = LIB_PYSGL._View_Create(self.__float_rect.get_ptr())

    def set_ptr(self, view_ptr: ViewPtr):
        """Устанавливает указатель на нативный View"""
        self.__del__()
        self._ptr = view_ptr

    def get_ptr(self) -> ViewPtr:
        """Возвращает указатель на нативный View"""
        return self._ptr
    
    def get_float_rect(self) -> FloatRect:
        """Возвращает базовый FloatRect вида"""
        return self.__float_rect
    
    def set_center(self, x: float | None = None, y: float | None = None) -> "View":
        """
        Устанавливает центр вида.
        Поддерживает частичное обновление (только X или только Y).
        
        Аргументы:
            x: Координата X центра (None - не изменять)
            y: Координата Y центра (None - не изменять)
            
        Возвращает:
            self для цепных вызовов
        """
        center = list(self.get_center())
        if x is not None: center[0] = x
        if y is not None: center[1] = y
        LIB_PYSGL._View_SetCenter(self._ptr, *center)
        return self
    
    def set_size(self, w: float | None = None, h: float | None = None) -> "View":
        """
        Устанавливает размер вида.
        Поддерживает частичное обновление (только width или только height).
        
        Аргументы:
            w: Ширина (None - не изменять)
            h: Высота (None - не изменять)
            
        Возвращает:
            self для цепных вызовов
        """
        size = list(self.get_size())
        if w is not None: size[0] = w
        if h is not None: size[1] = h
        LIB_PYSGL._View_SetSize(self._ptr, *size)
        return self
    
    def set_viewport(self, rect: FloatRect) -> "View":
        """
        Устанавливает вьюпорт вида.
        
        Аргументы:
            rect: FloatRect определяющий область вьюпорта
            
        Возвращает:
            self для цепных вызовов
        """
        LIB_PYSGL._View_SetViewport(self._ptr, rect.get_ptr())
        return self

    def set_zoom(self, zoom: float) -> "View":
        """
        Устанавливает масштаб вида.
        
        Аргументы:
            zoom: Коэффициент масштабирования
            
        Возвращает:
            self для цепных вызовов
        """
        LIB_PYSGL._View_Zoom(self._ptr, zoom)
        return self

    def set_angle(self, angle: float) -> "View":
        """
        Устанавливает угол поворота вида.
        
        Аргументы:
            angle: Угол поворота в градусах
            
        Возвращает:
            self для цепных вызовов
        """
        LIB_PYSGL._View_SetAngle(self._ptr, angle)    
        return self
    
    def move(self, x: float | None = 0, y: float | None = 0) -> None:
        """
        Перемещает вид на указанное смещение.
        
        Аргументы:
            x: Смещение по X
            y: Смещение по Y
        """
        LIB_PYSGL._View_Move(self._ptr, x, y)
    
    def get_center(self) -> tuple[float, float]:
        """
        Возвращает текущий центр вида.
        
        Возвращает:
            Кортеж (center_x, center_y)
        """
        return (
            LIB_PYSGL._View_GetCenterX(self._ptr),
            LIB_PYSGL._View_GetCenterY(self._ptr)
        )
    
    def get_angle(self) -> float:
        """Возвращает текущий угол поворота вида в градусах"""
        return LIB_PYSGL._View_GetAngle(self._ptr)
    
    def get_size(self) -> tuple[float, float]:
        """
        Возвращает текущий размер вида.
        
        Возвращает:
            Кортеж (width, height)
        """
        return (
            LIB_PYSGL._View_GetWidth(self._ptr),
            LIB_PYSGL._View_GetHeight(self._ptr)
        )
    
    def rotate(self, angle: float) -> None:
        """
        Поворачивает вид на указанный угол.
        
        Аргументы:
            angle: Угол поворота в градусах
        """
        LIB_PYSGL._View_Rotate(self._ptr, angle)

    def reset(self, rect: FloatRect) -> None:
        """
        Сбрасывает параметры вида к указанному прямоугольнику.
        
        Аргументы:
            rect: FloatRect для сброса параметров
        """
        LIB_PYSGL._View_Reset(self._ptr, rect.get_ptr())