import os
import ctypes
from time import time
from typing import Generator
from .Types import OptionalIdentifier, Identifier, NoReturn, FunctionOrMethod

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


LIB_PYSGL.createClock.argtypes = [] 
LIB_PYSGL.createClock.restype = ctypes.c_void_p  
LIB_PYSGL.clockRestart.argtypes = [ctypes.c_void_p] 
LIB_PYSGL.clockRestart.restype = None  
LIB_PYSGL.getClockElapsedTime.argtypes = [ctypes.c_void_p] 
LIB_PYSGL.getClockElapsedTime.restype = ctypes.c_double  


class Clock:
    """
    Высокоточный таймер на основе C++ реализации из DLL.
    
    Используется для измерения временных интервалов с максимальной точностью.
    Особенно полезен для:
    - Измерения времени рендеринга кадров
    - Профилирования производительности
    - Синхронизации игрового цикла
    """
    
    def __init__(self):
        """
        Инициализирует новый экземпляр таймера.
        Создает внутренний таймер в DLL.
        """
        self.__clock_ptr = LIB_PYSGL.createClock()  # Указатель на C++ объект таймера

    def restart(self) -> None:
        """
        Сбрасывает и немедленно перезапускает таймер.
        Обнуляет счетчик прошедшего времени.
        """
        LIB_PYSGL.clockRestart(self.__clock_ptr)

    def get_elapsed_time(self) -> float:
        """
        Возвращает время в секундах, прошедшее с последнего вызова restart().
        
        Возвращает:
            float: Количество секунд с высокой точностью (дробное число)
        """
        return LIB_PYSGL.getClockElapsedTime(self.__clock_ptr)


class Timer:
    """
    Простой таймер на основе системного времени.
    
    Позволяет проверять, истек ли заданный временной интервал.
    Полезен для:
    - Периодического выполнения действий
    - Ограничения частоты обновлений
    - Реализации задержек
    """
    
    def __init__(self, name: OptionalIdentifier = 'dummy', wait_time: float = 1):
        """
        Создает новый таймер с указанным именем и интервалом.
        
        Аргументы:
            name (str): Уникальное имя для идентификации таймера
            wait_time (float): Интервал срабатывания в секундах
        """
        self.__name = name
        self.__wait_time = wait_time
        self.__saved_time = time()  # Запоминаем текущее время
        self.__delta: float = 0

    def get_name(self) -> OptionalIdentifier:
        """
        Возвращает имя таймера.
        
        Возвращает:
            str: Текущее имя таймера
        """
        return self.__name
    
    def set_name(self, name: Identifier) -> None:
        """
        Устанавливает новое имя таймера.
        
        Аргументы:
            name (str): Новое имя таймера
        """
        self.__name = name
        

    def get_wait_time(self) -> float:
        """
        Возвращает текущий установленный интервал срабатывания.
        
        Возвращает:
            float: Интервал в секундах
        """
        return self.__wait_time
    
    def set_wait_time(self, time: float) -> None:
        """
        Устанавливает новый интервал срабатывания.
        
        Аргументы:
            time (float): Новый интервал в секундах
        """
        self.__wait_time = time

    def timing(self) -> bool:
        """
        Проверяет, истек ли установленный интервал.
        Если интервал истек, сбрасывает таймер.
        
        Возвращает:
            bool: True если интервал истек, False если нет
        """
        self.__delta = time() - self.__saved_time  # Вычисляем прошедшее время
        if self.__delta >= self.__wait_time:
            self.__saved_time = time()  # Сбрасываем таймер
            return True
        return False
    
    def get_delta(self) -> float:
        return self.__delta


# Глобальный буфер для хранения именованных таймеров
TIMER_BUFFER: dict[OptionalIdentifier, Timer] = {}

def wait(timer_name: OptionalIdentifier = 'dummy', wait_time: float = 0) -> bool:
    """
    Удобная обертка для работы с глобальными таймерами.
    Создает таймер при первом вызове, затем проверяет его состояние.
    
    Аргументы:
        timer_name (str): Имя таймера (по умолчанию "dummy")
        wait_time (float): Интервал срабатывания в секундах (по умолчанию 0)
        
    Возвращает:
        bool: True если интервал истек, False если нет
    """
    if timer_name not in TIMER_BUFFER:
        # Создаем новый таймер если он не существует
        TIMER_BUFFER[timer_name] = Timer(timer_name, wait_time)
    return TIMER_BUFFER[timer_name].timing()
    
def wait_call(timer_name: OptionalIdentifier, wait_time: float, func: FunctionOrMethod, *args, **kvargs) -> None:
    """
    Вызывает функцию только если истек указанный интервал для заданного таймера.
    
    Аргументы:
        timer_name (str): Имя таймера
        wait_time (float): Интервал между вызовами в секундах
        func (callable): Функция для вызова
        *args: Позиционные аргументы для функции
        **kvargs: Именованные аргументы для функции
    """
    if wait(timer_name, wait_time):
        func(*args, **kvargs)


# Мощный, но не очень то уж и полезный декоратор (используйте с умом)
def throttle(wait_time: float):
    """
    Декоратор для ограничения частоты вызовов функции
    
    Аргументы:
        wait_time (float): Минимальный интервал между вызовами в секундах
    """
    def decorator(func: FunctionOrMethod):
        last_called = 0
        
        def wrapper(*args, **kwargs):
            nonlocal last_called
            current_time = time()
            if current_time - last_called >= wait_time:
                last_called = current_time
                return func(*args, **kwargs)
        return wrapper
    return decorator

def every(interval: float) -> Generator[bool]:
    """
    Возвращает генератор, который возвращает True каждые interval секунд
    
    Аргументы:
        interval (float): Интервал в секундах
        
    Пример:
    for ready in every(1.0):
        if ready:
            print("Прошла секунда")
    """
    last_time = time()
    while True:
        current_time = time()
        if current_time - last_time >= interval:
            last_time = current_time
            yield True
        else:
            yield False