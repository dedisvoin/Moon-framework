import ctypes
import os
from typing import Self, Optional
from contextlib import contextmanager

# Загрузка нативной библиотеки
class LibraryLoadError(Exception):
    """Ошибка загрузки нативной библиотеки"""
    pass

class ViewError(Exception):
    """Ошибка работы с View"""
    pass

def _find_library() -> str:
    """
    Поиск пути к нативной библиотеке PySGL.dll
    
    Returns:
        str: Абсолютный путь к библиотеке
        
    Raises:
        LibraryLoadError: Если библиотека не найдена
    """
    search_paths = [
        r"PySGL/dlls/PySGL.dll",
        "./dlls/PySGL.dll",
        os.path.join(os.path.dirname(__file__), "..", "dlls", "PySGL.dll")
    ]
    
    for lib_path in search_paths:
        if os.path.exists(lib_path):
            return os.path.abspath(lib_path)
    
    raise LibraryLoadError(f"PySGL library not found in paths: {search_paths}")

# Загружаем DLL библиотеку
try:
    LIB_PYSGL = ctypes.CDLL(_find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")

# Типы указателей
FloatRectPtr = ctypes.c_void_p
ViewPtr = ctypes.c_void_p

# Регистрация функций FloatRect
def _setup_floatrect_functions():
    """Настройка функций для работы с FloatRect"""
    functions = {
        '_FloatRect_Create': ([ctypes.c_float] * 4, ctypes.c_void_p),
        '_FloatRect_Delete': ([ctypes.c_void_p], None),
        '_FloatRect_GetPositionX': ([ctypes.c_void_p], ctypes.c_float),
        '_FloatRect_GetPositionY': ([ctypes.c_void_p], ctypes.c_float),
        '_FloatRect_GetWidth': ([ctypes.c_void_p], ctypes.c_float),
        '_FloatRect_GetHeight': ([ctypes.c_void_p], ctypes.c_float),
        '_FloatRect_SetPosition': ([ctypes.c_void_p, ctypes.c_float, ctypes.c_float], None),
        '_FloatRect_SetSize': ([ctypes.c_void_p, ctypes.c_float, ctypes.c_float], None),
    }
    
    for name, (argtypes, restype) in functions.items():
        func = getattr(LIB_PYSGL, name)
        func.argtypes = argtypes
        func.restype = restype

_setup_floatrect_functions()


class FloatRect:
    """
    Класс прямоугольной области с плавающей точкой.
    Соответствует sf::FloatRect в SFML.
    
    Атрибуты:
        _ptr: Указатель на нативный объект FloatRect
        _is_valid: Флаг валидности объекта
    """
    
    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        """
        Создает новый FloatRect с указанными параметрами.
        
        Args:
            x: Позиция по X
            y: Позиция по Y  
            w: Ширина (должна быть >= 0)
            h: Высота (должна быть >= 0)
            
        Raises:
            ValueError: Если размеры отрицательные
            ViewError: Если не удалось создать объект
        """
        if w < 0 or h < 0:
            raise ValueError(f"Размеры должны быть неотрицательными: w={w}, h={h}")
            
        self._ptr = LIB_PYSGL._FloatRect_Create(float(x), float(y), float(w), float(h))
        if not self._ptr:
            raise ViewError("Не удалось создать FloatRect")
        self._is_valid = True

    def _check_valid(self) -> None:
        """Проверяет валидность объекта"""
        if not self._is_valid:
            raise ViewError("FloatRect был удален")

    def get_ptr(self) -> FloatRectPtr:
        """Возвращает указатель на нативный объект"""
        self._check_valid()
        return self._ptr

    def __del__(self) -> None:
        """Освобождает ресурсы нативного объекта"""
        if hasattr(self, '_is_valid') and self._is_valid and hasattr(self, '_ptr'):
            try:
                LIB_PYSGL._FloatRect_Delete(self._ptr)
            except:
                pass  # Игнорируем ошибки при удалении
            finally:
                self._is_valid = False

    def get_position(self) -> tuple[float, float]:
        """
        Возвращает текущую позицию прямоугольника.
        
        Returns:
            Кортеж (x, y)
        """
        self._check_valid()
        return (
            LIB_PYSGL._FloatRect_GetPositionX(self._ptr),
            LIB_PYSGL._FloatRect_GetPositionY(self._ptr),
        )
    
    def get_size(self) -> tuple[float, float]:
        """
        Возвращает текущие размеры прямоугольника.
        
        Returns:
            Кортеж (width, height)
        """
        self._check_valid()
        return (
            LIB_PYSGL._FloatRect_GetWidth(self._ptr),
            LIB_PYSGL._FloatRect_GetHeight(self._ptr),
        )
    
    def set_position(self, x: Optional[float] = None, y: Optional[float] = None) -> Self:
        """
        Устанавливает новую позицию прямоугольника.
        
        Args:
            x: Новая позиция X (None - не изменять)
            y: Новая позиция Y (None - не изменять)
            
        Returns:
            self для цепных вызовов
        """
        self._check_valid()
        if x is None and y is None:
            return self
            
        current_x, current_y = self.get_position()
        new_x = float(x) if x is not None else current_x
        new_y = float(y) if y is not None else current_y
        
        LIB_PYSGL._FloatRect_SetPosition(self._ptr, new_x, new_y)
        return self
    
    def set_size(self, w: Optional[float] = None, h: Optional[float] = None) -> Self:
        """
        Устанавливает новые размеры прямоугольника.
        
        Args:
            w: Новая ширина (None - не изменять, должна быть >= 0)
            h: Новая высота (None - не изменять, должна быть >= 0)
            
        Returns:
            self для цепных вызовов
            
        Raises:
            ValueError: Если размеры отрицательные
        """
        self._check_valid()
        if w is None and h is None:
            return self
            
        if (w is not None and w < 0) or (h is not None and h < 0):
            raise ValueError(f"Размеры должны быть неотрицательными: w={w}, h={h}")
            
        current_w, current_h = self.get_size()
        new_w = float(w) if w is not None else current_w
        new_h = float(h) if h is not None else current_h
        
        LIB_PYSGL._FloatRect_SetSize(self._ptr, new_w, new_h)
        return self
        
    def __repr__(self) -> str:
        """Строковое представление для отладки"""
        if not self._is_valid:
            return "FloatRect(deleted)"
        try:
            x, y = self.get_position()
            w, h = self.get_size()
            return f"FloatRect(x={x}, y={y}, w={w}, h={h})"
        except:
            return "FloatRect(invalid)"


# Регистрация функций View
def _setup_view_functions():
    """Настройка функций для работы с View"""
    functions = {
        '_View_Create': ([FloatRectPtr], ViewPtr),
        '_View_Delete': ([ViewPtr], None),
        '_View_GetCenterX': ([ViewPtr], ctypes.c_float),
        '_View_GetCenterY': ([ViewPtr], ctypes.c_float),
        '_View_GetPositionX': ([ViewPtr], ctypes.c_float),
        '_View_GetPositionY': ([ViewPtr], ctypes.c_float),
        '_View_GetAngle': ([ViewPtr], ctypes.c_float),
        '_View_GetWidth': ([ViewPtr], ctypes.c_float),
        '_View_GetHeight': ([ViewPtr], ctypes.c_float),
        '_View_Rotate': ([ViewPtr, ctypes.c_float], None),
        '_View_Reset': ([ViewPtr, FloatRectPtr], None),
        '_View_Move': ([ViewPtr, ctypes.c_float, ctypes.c_float], None),
        '_View_SetCenter': ([ViewPtr, ctypes.c_float, ctypes.c_float], None),
        '_View_SetAngle': ([ViewPtr, ctypes.c_float], None),
        '_View_SetViewport': ([ViewPtr, FloatRectPtr], None),
        '_View_SetSize': ([ViewPtr, ctypes.c_float, ctypes.c_float], None),
        '_View_Zoom': ([ViewPtr, ctypes.c_float], None),
    }
    
    for name, (argtypes, restype) in functions.items():
        if hasattr(LIB_PYSGL, name):
            func = getattr(LIB_PYSGL, name)
            func.argtypes = argtypes
            func.restype = restype

_setup_view_functions()


class View:
    """
    Класс камеры/вида (соответствует sf::View в SFML).
    Позволяет управлять областью просмотра, поворотом и масштабом.
    
    Атрибуты:
        _ptr: Указатель на нативный объект View
        _float_rect: Базовый прямоугольник вида
        _is_valid: Флаг валидности объекта
        _owns_ptr: Флаг владения указателем
    """
    
    def __init__(self, float_rect: FloatRect) -> None:
        """
        Создает новый View с указанным прямоугольником.
        
        Args:
            float_rect: Прямоугольник области просмотра
            
        Raises:
            ViewError: Если не удалось создать View
        """
        if not isinstance(float_rect, FloatRect):
            raise TypeError("float_rect должен быть экземпляром FloatRect")
            
        self._float_rect = float_rect
        self._ptr = LIB_PYSGL._View_Create(float_rect.get_ptr())
        if not self._ptr:
            raise ViewError("Не удалось создать View")
        self._is_valid = True
        self._owns_ptr = True
    
    @classmethod
    def from_view_ptr(cls, view_ptr: ViewPtr) -> "View":
        """
        Создает объект View из существующего указателя на нативный View.
        
        Args:
            view_ptr: Указатель на нативный View
            
        Returns:
            Новый экземпляр View
            
        Raises:
            ViewError: Если указатель невалиден
        """
        if not view_ptr:
            raise ViewError("Невалидный указатель на View")
            
        # Получаем параметры из нативного View
        try:
            width = LIB_PYSGL._View_GetWidth(view_ptr)
            height = LIB_PYSGL._View_GetHeight(view_ptr)
            pos_x = LIB_PYSGL._View_GetPositionX(view_ptr)
            pos_y = LIB_PYSGL._View_GetPositionY(view_ptr)
        except Exception as e:
            raise ViewError(f"Не удалось получить параметры View: {e}")

        # Создаем FloatRect и View
        float_rect = FloatRect(pos_x, pos_y, width, height)
        view = cls.__new__(cls)
        view._float_rect = float_rect
        view._ptr = view_ptr
        view._is_valid = True
        view._owns_ptr = False  # Не владеем указателем
        return view
    
    def _check_valid(self) -> None:
        """Проверяет валидность объекта"""
        if not self._is_valid:
            raise ViewError("View был удален")

    def __del__(self) -> None:
        """Освобождает ресурсы нативного объекта"""
        if (hasattr(self, '_is_valid') and self._is_valid and 
            hasattr(self, '_owns_ptr') and self._owns_ptr and 
            hasattr(self, '_ptr') and hasattr(LIB_PYSGL, '_View_Delete')):
            try:
                LIB_PYSGL._View_Delete(self._ptr)
            except:
                pass  # Игнорируем ошибки при удалении
            finally:
                self._is_valid = False

    def get_ptr(self) -> ViewPtr:
        """Возвращает указатель на нативный объект"""
        self._check_valid()
        return self._ptr
        
    def get_float_rect(self) -> FloatRect:
        """Возвращает базовый прямоугольник вида"""
        return self._float_rect

    def set_center(self, x: float, y: float) -> Self:
        """
        Устанавливает центр вида.
        
        Args:
            x: Координата X центра
            y: Координата Y центра
            
        Returns:
            self для цепных вызовов
        """
        self._check_valid()
        LIB_PYSGL._View_SetCenter(self._ptr, float(x), float(y))
        return self

    def set_size(self, width: float, height: float) -> Self:
        """
        Устанавливает размер вида.
        
        Args:
            width: Ширина (должна быть > 0)
            height: Высота (должна быть > 0)
            
        Returns:
            self для цепных вызовов
            
        Raises:
            ValueError: Если размеры неположительные
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"Размеры должны быть положительными: width={width}, height={height}")
            
        self._check_valid()
        LIB_PYSGL._View_SetSize(self._ptr, float(width), float(height))
        return self

    def set_viewport(self, viewport: FloatRect) -> Self:
        """
        Устанавливает вьюпорт.
        
        Args:
            viewport: Прямоугольник вьюпорта
            
        Returns:
            self для цепных вызовов
        """
        if not isinstance(viewport, FloatRect):
            raise TypeError("viewport должен быть экземпляром FloatRect")
            
        self._check_valid()
        LIB_PYSGL._View_SetViewport(self._ptr, viewport.get_ptr())
        return self

    def set_angle(self, angle: float) -> Self:
        """
        Устанавливает угол поворота вида.
        
        Args:
            angle: Угол в градусах
            
        Returns:
            self для цепных вызовов
        """
        self._check_valid()
        LIB_PYSGL._View_SetAngle(self._ptr, float(angle))
        return self

    def move(self, offset_x: float, offset_y: float) -> Self:
        """
        Перемещает вид на указанное смещение.
        
        Args:
            offset_x: Смещение по X
            offset_y: Смещение по Y
            
        Returns:
            self для цепных вызовов
        """
        self._check_valid()
        LIB_PYSGL._View_Move(self._ptr, float(offset_x), float(offset_y))
        return self

    def get_center(self) -> tuple[float, float]:
        """
        Возвращает центр вида.
        
        Returns:
            Кортеж (center_x, center_y)
        """
        self._check_valid()
        return (
            LIB_PYSGL._View_GetCenterX(self._ptr),
            LIB_PYSGL._View_GetCenterY(self._ptr),
        )

    def get_position(self) -> tuple[float, float]:
        """
        Возвращает позицию вида.
        
        Returns:
            Кортеж (position_x, position_y)
        """
        self._check_valid()
        return (
            LIB_PYSGL._View_GetPositionX(self._ptr),
            LIB_PYSGL._View_GetPositionY(self._ptr),
        )

    def get_angle(self) -> float:
        """
        Возвращает угол поворота вида.
        
        Returns:
            Угол в градусах
        """
        self._check_valid()
        return LIB_PYSGL._View_GetAngle(self._ptr)

    def get_size(self) -> tuple[float, float]:
        """
        Возвращает размер вида.
        
        Returns:
            Кортеж (width, height)
        """
        self._check_valid()
        return (
            LIB_PYSGL._View_GetWidth(self._ptr),
            LIB_PYSGL._View_GetHeight(self._ptr),
        )

    def rotate(self, angle: float) -> Self:
        """
        Поворачивает вид на указанный угол.
        
        Args:
            angle: Угол поворота в градусах
            
        Returns:
            self для цепных вызовов
        """
        self._check_valid()
        LIB_PYSGL._View_Rotate(self._ptr, float(angle))
        return self

    def zoom(self, factor: float) -> Self:
        """
        Масштабирует вид.
        
        Args:
            factor: Коэффициент масштабирования (должен быть > 0)
            
        Returns:
            self для цепных вызовов
            
        Raises:
            ValueError: Если коэффициент неположительный
        """
        if factor <= 0:
            raise ValueError(f"Коэффициент масштабирования должен быть положительным: {factor}")
            
        self._check_valid()
        LIB_PYSGL._View_Zoom(self._ptr, float(factor))
        return self

    def reset(self, rectangle: FloatRect) -> Self:
        """
        Сбрасывает параметры вида к указанному прямоугольнику.
        
        Args:
            rectangle: Новый прямоугольник вида
            
        Returns:
            self для цепных вызовов
        """
        if not isinstance(rectangle, FloatRect):
            raise TypeError("rectangle должен быть экземпляром FloatRect")
            
        self._check_valid()
        LIB_PYSGL._View_Reset(self._ptr, rectangle.get_ptr())
        self._float_rect = rectangle
        return self
        
    def __repr__(self) -> str:
        """Строковое представление для отладки"""
        if not self._is_valid:
            return "View(deleted)"
        try:
            center = self.get_center()
            size = self.get_size()
            angle = self.get_angle()
            return f"View(center={center}, size={size}, angle={angle}°)"
        except:
            return "View(invalid)"
            
    @contextmanager
    def temporary_transform(self, center: Optional[tuple[float, float]] = None, 
                          size: Optional[tuple[float, float]] = None,
                          angle: Optional[float] = None):
        """
        Контекстный менеджер для временного изменения параметров вида.
        
        Args:
            center: Временный центр
            size: Временный размер
            angle: Временный угол
        """
        # Сохраняем текущие параметры
        old_center = self.get_center()
        old_size = self.get_size()
        old_angle = self.get_angle()
        
        try:
            # Применяем временные параметры
            if center is not None:
                self.set_center(*center)
            if size is not None:
                self.set_size(*size)
            if angle is not None:
                self.set_angle(angle)
            yield self
        finally:
            # Восстанавливаем старые параметры
            self.set_center(*old_center)
            self.set_size(*old_size)
            self.set_angle(old_angle)