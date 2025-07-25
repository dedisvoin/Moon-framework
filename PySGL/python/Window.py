"""
#### *Модуль работы с окнами в PySGL*

---

##### Версия: 1.1.8

*Автор: Павлов Иван (Pavlov Ivan)*

*Лицензия: MIT*
##### Реализованно на 100% 

---

✓ Полноценное управление окнами:
  - Создание/уничтожение окон
  - Управление размером, позицией и стилями
  - Настройка заголовка и прозрачности

✓ Комплексная система рендеринга:
  - Поддержка View и мировых координат
  - Отрисовка примитивов с состояниями рендеринга
  - Гибкая система преобразования координат

✓ Производительность и контроль:
  - Управление FPS и вертикальной синхронизацией
  - Детальная статистика рендеринга
  - Встроенный профилировщик производительности

✓ Готовые интерфейсы:
  - Window - основной класс работы с окном
  - WindowEvents - система обработки событий
  - Window.Style - перечисление стилей окна

---

:Requires:

• Python 3.8+

• Библиотека keyboard (для обработки клавиатуры)

• Библиотека ctypes (для работы с DLL)

• PySGL.dll (нативная библиотека рендеринга)

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
import keyboard
from time import time
from typing import overload, Final

from .Colors import *
from .Time import Clock 
from .Views import View
from .Types import TwoIntegerList
from .Inputs import MouseInterface
from .Vectors import Vector2i, Vector2f

from .Rendering.Text import *
from .Rendering.Shapes import *
from .Rendering.Shaders import Shader
from .Rendering.RenderStates import RenderStates



from .Inputs import MouseInterface

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

def get_screen_resolution() -> TwoIntegerList:
    """
    #### Получает разрешение основного монитора с использованием Windows API.

    ---

    :Returns:
    - tuple: Кортеж, содержащий ширину и высоту экрана в пикселях (ширина, высота).
    """
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)  # SM_CXSCREEN
    screen_height = user32.GetSystemMetrics(1) # SM_CYSCREEN
    return [screen_width, screen_height]


##################################################################
#                   `C / C++` Bindings                           #
#   Определение аргументов и возвращаемых типов для функций      #
#   из нативной DLL библиотеки PySGL, используемых через ctypes. #
##################################################################

# Определение сигнатуры для функции createWindow: (int, int, char*, int) -> void*
LIB_PYSGL.createWindow.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
LIB_PYSGL.createWindow.restype = ctypes.c_void_p
# Определение сигнатуры для функции destroyWindow: (void*) -> None
LIB_PYSGL.destroyWindow.argtypes = [ctypes.c_void_p]
LIB_PYSGL.destroyWindow.restype = None
# Определение сигнатуры для функции clearWindow: (void*, ubyte, ubyte, ubyte, ubyte) -> None
LIB_PYSGL.clearWindow.argtypes = [ctypes.c_void_p, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte]
LIB_PYSGL.clearWindow.restype = None
# Определение сигнатуры для функции displayWindow: (void*) -> None
LIB_PYSGL.displayWindow.argtypes = [ctypes.c_void_p]
LIB_PYSGL.displayWindow.restype = None
# Определение сигнатуры для функции isWindowOpen: (void*) -> bool
LIB_PYSGL.isWindowOpen.argtypes = [ctypes.c_void_p]
LIB_PYSGL.isWindowOpen.restype = ctypes.c_bool
# Определение сигнатуры для функции drawWindow: (void*, void*) -> None
LIB_PYSGL.drawWindow.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.drawWindow.restype = None
# Определение сигнатуры для функции getView: (void*) -> void*
LIB_PYSGL.getView.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getView.restype = ctypes.c_void_p
# Определение сигнатуры для функции setWaitFps: (void*, uint) -> None
LIB_PYSGL.setWaitFps.argtypes = [ctypes.c_void_p, ctypes.c_uint]
LIB_PYSGL.setWaitFps.restype = None
# Определение сигнатуры для функции setWindowTitle: (void*, char*) -> None
LIB_PYSGL.setWindowTitle.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
LIB_PYSGL.setWindowTitle.restype = None
# Определение сигнатуры для функции SetVerticalSync: (void*, bool) -> None
LIB_PYSGL.SetVerticalSync.argtypes = [ctypes.c_void_p, ctypes.c_bool]
LIB_PYSGL.SetVerticalSync.restype = None
# Определение сигнатуры для функции createEvent: () -> void*
LIB_PYSGL.createEvent.argtypes = []
LIB_PYSGL.createEvent.restype = ctypes.c_void_p
# Определение сигнатуры для функции destroyEvent: (void*) -> None
LIB_PYSGL.destroyEvent.argtypes = [ctypes.c_void_p]
LIB_PYSGL.destroyEvent.restype = None
# Определение сигнатуры для функции getWindowEvent: (void*, void*) -> int
LIB_PYSGL.getWindowEvent.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.getWindowEvent.restype = ctypes.c_int
# Определение сигнатуры для функции getEventType: (void*) -> int
LIB_PYSGL.getEventType.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventType.restype = ctypes.c_int
# Определение сигнатуры для функции getEventKey: (void*) -> int
LIB_PYSGL.getEventKey.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventKey.restype = ctypes.c_int
# Определение сигнатуры для функции getEventMouseButton: (void*) -> int
LIB_PYSGL.getEventMouseButton.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventMouseButton.restype = ctypes.c_int
# Определение сигнатуры для функции getEventMouseX: (void*) -> int
LIB_PYSGL.getEventMouseX.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventMouseX.restype = ctypes.c_int
# Определение сигнатуры для функции getEventMouseY: (void*) -> int
LIB_PYSGL.getEventMouseY.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventMouseY.restype = ctypes.c_int
# Определение сигнатуры для функции getEventSizeWidth: (void*) -> int
LIB_PYSGL.getEventSizeWidth.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventSizeWidth.restype = ctypes.c_int
# Определение сигнатуры для функции getEventSizeHeight: (void*) -> int
LIB_PYSGL.getEventSizeHeight.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventSizeHeight.restype = ctypes.c_int
# Определение сигнатуры для функции getEventMouseWheel: (void*) -> int
LIB_PYSGL.getEventMouseWheel.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventMouseWheel.restype = ctypes.c_int
# Определение сигнатуры для функции setViewCenter: (void*, float, float) -> None
LIB_PYSGL.setViewCenter.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL.setViewCenter.restype = None
# Определение сигнатуры для функции setViewSize: (void*, float, float) -> None
LIB_PYSGL.setViewSize.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL.setViewSize.restype = None
# Определение сигнатуры для функции setView: (void*, void*) -> None
LIB_PYSGL.setView.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.setView.restype = None
# Определение сигнатуры для функции getWindowSizeWidth: (void*) -> int
LIB_PYSGL.getWindowSizeWidth.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getWindowSizeWidth.restype = ctypes.c_int
# Определение сигнатуры для функции getWindowSizeHeight: (void*) -> int
LIB_PYSGL.getWindowSizeHeight.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getWindowSizeHeight.restype = ctypes.c_int
# Определение сигнатуры для функции getWindowPositionX: (void*) -> int
LIB_PYSGL.getWindowPositionX.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getWindowPositionX.restype = ctypes.c_int
# Определение сигнатуры для функции getWindowPositionY: (void*) -> int
LIB_PYSGL.getWindowPositionY.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getWindowPositionY.restype = ctypes.c_int
# Определение сигнатуры для функции setWindowPosition: (void*, int, int) -> None
LIB_PYSGL.setWindowPosition.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
LIB_PYSGL.setWindowPosition.restype = None
# Определение сигнатуры для функции setWindowSize: (void*, int, int) -> None
LIB_PYSGL.setWindowSize.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
LIB_PYSGL.setWindowSize.restype = None
# Определение сигнатуры для функции zoomView: (void*, float) -> None
LIB_PYSGL.zoomView.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_PYSGL.zoomView.restype = None
# Определение сигнатуры для функции mapPixelToCoordsX: (void*, double, double, void*) -> float
LIB_PYSGL.mapPixelToCoordsX.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_void_p]
LIB_PYSGL.mapPixelToCoordsX.restype = ctypes.c_float
# Определение сигнатуры для функции mapPixelToCoordsY: (void*, double, double, void*) -> float
LIB_PYSGL.mapPixelToCoordsY.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_void_p]
LIB_PYSGL.mapPixelToCoordsY.restype = ctypes.c_float

LIB_PYSGL.mapCoordsToPixelX.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_void_p]
LIB_PYSGL.mapCoordsToPixelX.restype = ctypes.c_float

LIB_PYSGL.mapCoordsToPixelY.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_void_p]
LIB_PYSGL.mapCoordsToPixelY.restype = ctypes.c_float
# Определение сигнатуры для функции drawWindowWithStates: (void*, void*, void*) -> None
LIB_PYSGL.drawWindowWithStates.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.drawWindowWithStates.restype = None
# Определение сигнатуры для функции drawWindowWithShader: (void*, void*, void*) -> None
LIB_PYSGL.drawWindowWithShader.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.drawWindowWithShader.restype = None
# Определение сигнатуры для функции setMouseCursorVisible: (void*, bool) -> None
LIB_PYSGL.setMouseCursorVisible.argtypes = [ctypes.c_void_p, ctypes.c_bool]
LIB_PYSGL.setMouseCursorVisible.restype = None
# Определение сигнатуры для функции closeWindow: (void*) -> None
LIB_PYSGL.closeWindow.argtypes = [ctypes.c_void_p]
LIB_PYSGL.closeWindow.restype = None


class WindowEvents:
    """
    Класс для работы с событиями окна (клавиатура, мышь, изменение размера и т.д.).
    Обеспечивает интерфейс для обработки событий из очереди сообщений операционной системы.
    """
    
    class Type:
        """
        Перечисление типов событий, которые может генерировать окно.
        Соответствует типам событий в нативной библиотеке PySGL.
        """
    ################################################################################################## 
        Closed = 0                       # Событие закрытия окна (пользователь запросил закрытие).
        Resized = 1                      # Событие изменения размера окна (данные в event.size).
        LostFocus = 2                    # Событие потери фокуса окном.
        GainedFocus = 3                  # Событие получения фокуса окном.         
        TextEntered = 4                  # Событие ввода символа (данные в event.text).

        KeyPressed = 5                   # Событие нажатия клавиши (данные в event.key).
        KeyReleased = 6                  # Событие отпускания клавиши (данные в event.key).

        MouseWheelMoved = 7              # Событие прокрутки колесика мыши (старый тип, данные в event.mouseWheel).
        MouseWheelScrolled = 8           # Событие прокрутки колесика мыши (новый тип, данные в event.mouseWheelScroll).
        MouseButtonPressed = 9           # Событие нажатия кнопки мыши (данные в event.mouseButton). 
        MouseButtonReleased = 10         # Событие отпускания кнопки мыши (данные в event.mouseButton).
        MouseMoved = 11                  # Событие перемещения курсора мыши (данные в event.mouseMove).  
        MouseEntered = 12                # Событие входа курсора мыши в область окна.
        MouseLeft = 13                   # Событие выхода курсора мыши из области окна.

        JoystickButtonPressed = 14       # Событие нажатия кнопки джойстика (данные в event.joystickButton).
        JoystickButtonReleased = 15      # Событие отпускания кнопки джойстика (данные в event.joystickButton).
        JoystickMoved = 16               # Событие перемещения джойстика по оси (данные в event.joystickMove).
        JoystickConnected = 17           # Событие подключения джойстика (данные в event.joystickConnect).
        JoystickDisconnected = 18        # Событие отключения джойстика (данные в event.joystickConnect).

        TouchBegan = 19                  # Событие начала касания (для сенсорных экранов, данные в event.touch).
        TouchMoved = 20                  # Событие перемещения касания (для сенсорных экранов, данные в event.touch).
        TouchEnded = 21                  # Событие окончания касания (для сенсорных экранов, данные в event.touch).
        SensorChanged = 22               # Событие изменения значения датчика (данные в event.sensor).
    ################################################################################################## 

    def __init__(self):
        """
        Инициализирует объект Events.
        Создает внутренний указатель на объект прослушивателя событий в нативной библиотеке.
        """
        self.__event_ptr = LIB_PYSGL.createEvent()

    def __del__(self):
        """
        Деструктор класса Events.
        Освобождает ресурсы, связанные с объектом прослушивателя событий в нативной библиотеке.
        """
        LIB_PYSGL.destroyEvent(self.__event_ptr)

    def get_ptr(self):
        """
        Возвращает указатель на внутренний объект прослушивателя событий в памяти.

        Returns:
            ctypes.c_void_p: Указатель на объект события.
        """
        return self.__event_ptr

    def poll(self, window) -> bool:
        """
        Извлекает следующее событие из очереди событий окна.
        Возвращает True, если в очереди есть событие, и False, если очередь пуста.
        
        Args:
            window: Объект окна, для которого происходит опрос событий.

        Returns:
            bool: True, если событие было получено, False иначе.
        """
        return LIB_PYSGL.getWindowEvent(window.get_ptr(), self.__event_ptr)

    def get_type(self) -> int:
        """
        Возвращает тип текущего события, находящегося в очереди.

        Returns:
            int: Целочисленное значение, соответствующее типу события (см. Events.Type).
        """
        return LIB_PYSGL.getEventType(self.__event_ptr)

    def get_key(self) -> int:
        """
        Возвращает код нажатой/отпущенной клавиши для событий KeyPressed/KeyReleased.

        Returns:
            int: Целочисленный код клавиши.
        """
        return LIB_PYSGL.getEventKey(self.__event_ptr)

    def get_mouse_button(self) -> int:
        """
        Возвращает код нажатой/отпущенной кнопки мыши для событий MouseButtonPressed/MouseButtonReleased.

        Returns:
            int: Целочисленный код кнопки мыши.
        """
        return LIB_PYSGL.getEventMouseButton(self.__event_ptr)
    
    def get_mouse_wheel(self) -> int:
        """
        Возвращает значение прокрутки колесика мыши для событий MouseWheelMoved/MouseWheelScrolled.
        Положительное значение означает прокрутку вверх, отрицательное - вниз.

        Returns:
            int: Значение прокрутки колесика мыши.
        """
        return LIB_PYSGL.getEventMouseWheel(self.__event_ptr)

    def get_mouse_x(self) -> int:
        """
        Возвращает координату X курсора мыши для событий, связанных с мышью.

        Returns:
            int: Координата X курсора мыши в пикселях.
        """
        return LIB_PYSGL.getEventMouseX(self.__event_ptr)

    def get_mouse_y(self) -> int:
        """
        Возвращает координату Y курсора мыши для событий, связанных с мышью.

        Returns:
            int: Координата Y курсора мыши в пикселях.
        """
        return LIB_PYSGL.getEventMouseY(self.__event_ptr)
    
    def get_size_width(self) -> int:
        """
        Возвращает новую ширину окна для события Resized.

        Returns:
            int: Ширина окна в пикселях.
        """
        return LIB_PYSGL.getEventSizeWidth(self.__event_ptr)
    
    def get_size_height(self) -> int:
        """
        Возвращает новую высоту окна для события Resized.

        Returns:
            int: Высота окна в пикселях.
        """
        return LIB_PYSGL.getEventSizeHeight(self.__event_ptr)


# Тип для хранения указателя на объект окна ===== +
type WindowPtr = ctypes.c_void_p
# =============================================== +

# Константа для обозначения неограниченного FPS
FPS_UNLIMIT_CONST: Final[float] = 1000000

class Window:
    """
    Класс для работы с окном приложения PySGL.
    Позволяет создавать окна, управлять их размерами, заголовком, стилем,
    а также предоставляет методы для отрисовки графических объектов и управления циклом обновления.
    """
    class Style:
        """
        Перечисление стилей окна, определяющих его внешний вид и поведение.
        Эти стили можно комбинировать с использованием побитовых операций.
        """
        No = 0                       # Окно без каких-либо декораций.
        Titlebar = 1 << 0            # Окно с заголовком.
        Resize = 1 << 1              # Окно, которое можно изменять в размере.
        Close = 1 << 2               # Окно с кнопкой закрытия.
        FullScreen = 1 << 3          # Окно в полноэкранном режиме.
        FullScreenDesktop = 1 << 4   # Окно в полноэкранном режиме, использующее разрешение рабочего стола.
        Default = Titlebar | Resize | Close # Стиль окна по умолчанию (заголовок, изменение размера, кнопка закрытия).

    def __init__(self, width: int = 800, height: int = 600, 
                 title: str = "PySGL Window", style: int = Style.Default, 
                 vsync: bool = False,
                 alpha: float = 255):
        """
        Инициализирует окно с заданными параметрами.
        
        Args:
            width (int): Начальная ширина окна в пикселях (по умолчанию 800).
            height (int): Начальная высота окна в пикселях (по умолчанию 600).
            title (str): Заголовок окна (по умолчанию "PySGL Window").
            style (int): Стиль окна (по умолчанию Style.Default).
            vsync (bool): Включение вертикальной синхронизации (по умолчанию False).
                          Вертикальная синхронизация синхронизирует частоту кадров с частотой обновления монитора,
                          что помогает избежать "разрывов" изображения.
        """

        # Обработка кастомного стиля FullScreenDesktop:
        # Если стиль FullScreenDesktop, ширина и высота окна будут равны разрешению экрана.
        if style == Window.Style.FullScreenDesktop:
            width, height = get_screen_resolution() # Получаем максимальное разрешение экрана монитора
            style = Window.Style.No # Переключаем на режим без ничего

        # Создаем окно через нативную библиотеку и сохраняем указатель на него
        self.__window_ptr: WindowPtr = LIB_PYSGL.createWindow(width, height, title.encode('utf-8'), style)
        self.__title = title
        self.__window_descriptor = ctypes.windll.user32.FindWindowW(None, self.__title)
        self.__window_alpha: int = alpha

        self.set_alpha(self.__window_alpha)
        # Получаем стандартную область отображения (View) и сохраняем указатель на нее
        self.__view = self.get_default_view()
        
        # __wait_fps - ожидание кадров в секунду (максимальное число кадров в секунду, установленное пользователем)
        self.__wait_fps = 60 

        # __target_fps - целевое число кадров в секунду (используется для вычисления delta-time)
        self.__target_fps = 60

        # Истинные значения текущего FPS и delta-time
        self.__fps = 0.0
        self.__delta = 0.0

        # render_time - время, затраченное на рендер одного кадра
        self.__render_time = 0.0

        # Инициализация переменных для отслеживания FPS (максимальное и минимальное значения)
        self.__min_fps_in_fps_history: float = 0
        self.__max_fps_in_fps_history: float = 0
        LIB_PYSGL.setWaitFps(self.__window_ptr, int(self.__wait_fps))

        #////////////////////////////////////////////////////////////////////////////////
        # (             Переменные, необходимые для генерации графика фрейм-тайма            )
        #////////////////////////////////////////////////////////////////////////////////
        self.__info_alpha = 0
        self.__target_info_alpha = 100
        self.__fps_update_timer = 0.0
        self.__fps_history = [] # История значений FPS для построения графика
        self.__max_history = 40 # Максимальное количество точек в истории FPS

        # Настройка шрифта и текстовых элементов для отображения отладочной информации
        self.__info_font = Font.SystemFont("calibri")
        self.__info_text = BaseText(self.__info_font).\
            set_outline_thickness(2).set_outline_color(COLOR_GHOST_WHITE)
        self.__info_text_color_ghost_white = Color(248, 248, 255, 100)
        self.__info_text_color_black = Color(0, 0, 0, 100)
        self.__info_text_color_gray = Color(100, 100, 100, 100)

        # Настройка фонового прямоугольника и линий для графика FPS
        self.__info_bg_color = Color(200, 200, 220, 100)
        self.__info_bg = BaseRectangleShape(100, 200)
        self.__info_line_color = Color(200, 200, 250, 100)
        self.__info_line = LineThin()
        self.__fps_line_color_red = Color(200, 0, 0, 100)
        self.__fps_line_color_green = Color(0, 200, 0, 100)
        self.__fps_line = LinesThin()
        self.__info_text_fps_color = Color(0, 0, 0, 180)
        self.__info_text_fps = BaseText(self.__info_font)
        


        #////////////////////////////////////////////////////////////////////////////////

        # Внутренняя переменная для вычисления FPS, render_time, delta-time и т.д.
        self.__clock = Clock()          

        # Флаги и константы состояния окна
        self.__view_info = False            # Флаг отображения информации о рендере (FPS, дельта и т.д.)
        self.__exit_key = "esc"             # Клавиша для закрытия окна (по умолчанию Esc)
        self.__vsync = vsync                # Флаг вертикальной синхронизации
        self.__clear_color = COLOR_WHITE    # Цвет по умолчанию для очистки окна

        # Текущий размер окна и флаг для отслеживания изменения размера
        self.__width = width                # Ширина окна в текущем кадре
        self.__height = height              # Высота окна в текущем кадре
        self.__end_width = width            # Ширина окна в прошлом кадре (для отслеживания изменений)
        self.__end_height = height          # Высота окна в прошлом кадре (для отслеживания изменений)
        self.__resized: bool = False        # Флаг, указывающий, был ли изменен размер окна в текущем кадре

        self.__start_time = time()          # Время открытия окна (для get_global_timer)

        self.__cursor_visibility: bool = True # Флаг видимости курсора мыши

        self.set_vertical_sync(vsync) # Устанавливает вертикальную синхронизацию при инициализации


        self.__ghosting: bool = False
        self.__ghosting_min_value: int = 30
        self.__ghosting_at_value: int = 255
        self.__ghosting_interpolation: float = 0.1

        self.__active: bool = True
        self.__actve_text = Text(self.__info_font)

    def get_active(self) -> float:
        return self.__active

    def set_ghosting(self, value: bool = True) -> Self:
        self.__ghosting = value
        return self

    def get_ghosting(self) -> bool:
        return self.__ghosting
    
    def set_ghosting_min_alpha(self, alpha: int) -> Self:
        self.__ghosting_min_value = alpha
        return self
    
    def get_ghosting_min_alpha(self) -> int:
        return self.__ghosting_min_value

    def set_alpha(self, alpha: float):
        self.__window_descriptor = ctypes.windll.user32.FindWindowW(None, self.__title)
        self.__window_alpha = alpha

        style = ctypes.windll.user32.GetWindowLongW(self.__window_descriptor, -20)  # GWL_EXSTYLE = -20
        ctypes.windll.user32.SetWindowLongW(self.__window_descriptor, -20, style | 0x00080000)  # WS_EX_LAYERED = 0x00080000
        
        # Установить прозрачность (0 = полностью прозрачное, 255 = полностью непрозрачное)
        ctypes.windll.user32.SetLayeredWindowAttributes(self.__window_descriptor, 0, int(self.__window_alpha), 2)  # 150 ~ 60% прозрачности

    def get_alpha(self) -> float:
        return self.__window_alpha

    def close(self) -> None:
        """
        Закрывает окно. Рекомендуется вызывать этот метод после того, как цикл приложения прекратился.
        Освобождает ресурсы, связанные с окном в нативной библиотеке.
        """
        LIB_PYSGL.closeWindow(self.__window_ptr)

    def hide_cursor(self) -> Self:
        """
        Скрывает курсор мыши, когда он находится над окном.
        """
        LIB_PYSGL.setMouseCursorVisible(self.__window_ptr, False)
        self.__cursor_visibility = False
        return self
    
    def show_cursor(self) -> Self:
        """
        Отображает курсор мыши, когда он находится над окном.
        """
        LIB_PYSGL.setMouseCursorVisible(self.__window_ptr, True)
        self.__cursor_visibility = True
        return self

    def get_cursor_visibility(self) -> bool:
        """
        Возвращает текущее состояние видимости курсора мыши.

        Returns:
            bool: True, если курсор виден, False, если скрыт.
        """
        return self.__cursor_visibility

    def set_max_fps_history(self, number: int) -> Self:
        """
        Устанавливает максимальное количество сохраняемых значений FPS для истории.
        История FPS используется для построения графика производительности.
        
        Args:
            number (int): Максимальное количество значений в истории FPS. Должно быть положительным.
            
        Returns:
            Window: Возвращает текущий объект Window для цепочки вызовов (fluent interface).
        """
        self.__max_history = number  
        return self  

    def get_max_fps_history(self) -> int:
        """
        Возвращает максимальное количество сохраняемых значений FPS.
        
        Returns:
            int: Максимальное количество значений в истории FPS.
        """
        return self.__max_history

    def convert_window_coords_to_view_coords(self, x: float, y: float, view: View) -> Vector2f:
        """
        Преобразует координаты пикселей (экранные координаты) в мировые координаты
        относительно заданной области просмотра (View).
        
        Args:
            x (float): Координата X в пикселях.
            y (float): Координата Y в пикселях.
            view (View): Объект View, определяющий область просмотра для преобразования.
            
        Returns:
            Vector2f: Вектор с преобразованными мировыми координатами (x, y).
        """
        return Vector2f(
            LIB_PYSGL.mapPixelToCoordsX(self.__window_ptr, x, y, view.get_ptr()),
            LIB_PYSGL.mapPixelToCoordsY(self.__window_ptr, x, y, view.get_ptr()),
        )
    
    def convert_view_coords_to_window_coords(self, x: float, y: float, view: View) -> Vector2f:
        """
        Преобразует мировые координаты в координаты пикселей (экранные координаты)
        относительно заданной области просмотра (View).
        
        Args:
            x (float): Координата X в пикселях.
            y (float): Координата Y в пикселях.
            view (View): Объект View, определяющий область просмотра для преобразования.
            
        Returns:
            Vector2f: Вектор с преобразованными мировыми координатами (x, y).
        """
        return Vector2f(
            LIB_PYSGL.mapCoordsToPixelX(self.__window_ptr, x, y, view.get_ptr()),
            LIB_PYSGL.mapCoordsToPixelY(self.__window_ptr, x, y, view.get_ptr()),
        )

    def get_default_view(self) -> View:
        """
        Возвращает стандартную (дефолтную) область просмотра окна.
        Эта область просмотра соответствует полному размеру окна и не имеет смещений.
        
        Returns:
            View: Объект стандартной области просмотра.
        """
        return View.from_view_ptr(LIB_PYSGL.getView(self.__window_ptr))

    def set_position(self, x: int, y: int) -> Self:
        """
        Устанавливает позицию окна на экране в пикселях.
        Координаты (x, y) соответствуют верхнему левому углу окна.
        
        Args:
            x (int): Координата X верхнего левого угла окна.
            y (int): Координата Y верхнего левого угла окна.
        """
        LIB_PYSGL.setWindowPosition(self.__window_ptr, x, y)
        return self

    def set_size(self, width: int, height: int) -> Self:
        """
        Устанавливает новый размер окна в пикселях.
        
        Args:
            width (int): Новая ширина окна.
            height (int): Новая высота окна.
        """
        LIB_PYSGL.setWindowSize(self.__window_ptr, width, height)
        return self


    def get_ptr(self) -> WindowPtr:
        """
        Возвращает указатель на внутренний объект окна в памяти,
        используемый нативной библиотекой PySGL.
        
        Returns:
            ctypes.c_void_p: Указатель на окно.
        """
        return self.__window_ptr
    
    def get_size(self) -> Vector2i:
        """
        Возвращает текущий размер окна в пикселях.
        
        Returns:
            Vector2i: Вектор, содержащий ширину (x) и высоту (y) окна.
        """
        return Vector2i(LIB_PYSGL.getWindowSizeWidth(self.__window_ptr), LIB_PYSGL.getWindowSizeHeight(self.__window_ptr))
    
    def get_center(self) -> Vector2f:
        """
        Возвращает координаты центра окна в мировых координатах.
        
        Returns:
            Vector2f: Вектор с координатами X и Y центра окна.
        """
        size = self.get_size()
        center = [
            size.x / 2,
            size.y / 2
        ]
        return Vector2f(*center)

    def get_position(self) -> Vector2i:
        """
        Возвращает текущую позицию окна на экране в пикселях.
        
        Returns:
            Vector2i: Вектор, содержащий координату X и Y верхнего левого угла окна.
        """
        return Vector2i(LIB_PYSGL.getWindowPositionX(self.__window_ptr), LIB_PYSGL.getWindowPositionY(self.__window_ptr))

    def view_info(self) -> None:
        """
        Отображает отладочную информацию об окне, такую как текущий FPS, время рендеринга и дельта-тайм.
        Также включает простой график изменения FPS.
        Требует, чтобы флаг '__view_info' был установлен в True для отображения.
        """
        
        if not self.__view_info:
            return
            
        # Устанавливаем представление по умолчанию, чтобы информация отображалась в экранных координатах
        self.set_view(self.get_default_view().set_size(*self.get_size().xy).set_center(*self.get_center().xy))

        # Изменяем прозрачность информационного блока в зависимости от положения курсора
        mp = MouseInterface.get_position_in_window(self)

        if mp.x < 250 and mp.y < 200: # Если курсор в верхнем левом углу
            self.__target_info_alpha = 200
        else:
            self.__target_info_alpha = 50

        # Анимируем прозрачность информационного блока
        self.__info_alpha += (self.__target_info_alpha - self.__info_alpha) * 0.3 * self.get_render_time() * 10
        self.__info_bg_color.set_alpha(int(self.__info_alpha))
        self.__info_line_color.set_alpha(int(self.__info_alpha))
        self.__info_text_fps_color.set_alpha(int(self.__info_alpha))
        self.__fps_line_color_green.set_alpha(int(self.__info_alpha))
        self.__fps_line_color_red.set_alpha(int(self.__info_alpha))
        self.__info_text_color_black.set_alpha(int(self.__info_alpha))
        self.__info_text_color_gray.set_alpha(int(self.__info_alpha))
        self.__info_text_color_ghost_white.set_alpha(int(self.__info_alpha))

        # Основная информация: FPS
        self.__info_text.set_size(30)
        self.__info_text.set_outline_color(self.__info_text_color_ghost_white)
        self.__info_text.set_style(TextStyle.BOLD)
        if self.get_wait_fps() >= FPS_UNLIMIT_CONST:
            self.__info_text.set_text(f"FPS: {self.get_fps():.0f} / unlimit")
        else:
            self.__info_text.set_text(f"FPS: {self.get_fps():.0f} / {self.get_wait_fps():.0f}")
        self.__info_text.set_position(10, 5)
        self.__info_text.set_color(self.__info_text_color_black)
        self.draw(self.__info_text)

        
        width =  self.__info_text.get_text_width()
        self.__info_text.set_position(width + 15, 9)
        self.__info_text.set_size(14)
        self.__info_text.set_style(TextStyle.REGULAR)
        self.__info_text.set_text(f"max: {self.__max_fps_in_fps_history:.0f}")
        self.draw(self.__info_text)

        self.__info_text.set_position(width + 15, 20)
        self.__info_text.set_size(14)
        self.__info_text.set_text(f"min: {self.__min_fps_in_fps_history:.0f}")
        self.draw(self.__info_text)

        
        # Дополнительная информация: время рендеринга
        self.__info_text.set_style(TextStyle.REGULAR)
        self.__info_text.set_size(18)
        self.__info_text.set_text(f"Render time: {self.get_render_time()*1000:.1f}ms")
        self.__info_text.set_position(10, 35)
        self.__info_text.set_color(self.__info_text_color_gray)
        self.draw(self.__info_text)

        # Дополнительная информация: дельта-тайм
        self.__info_text.set_text(f"Delta: {self.get_delta():.3f}")
        self.__info_text.set_position(10, 55)
        self.draw(self.__info_text)

        # Дополнительная информация: вертикальная синхронизация
        self.__info_text.set_text(f"Vsync: {self.__vsync}")
        self.__info_text.set_position(10, 75)
        # Цвет текста Vsync зависит от ее состояния (красный - выключена, зеленый - включена)
        self.__info_text.set_color(self.__fps_line_color_red if not self.__vsync else self.__fps_line_color_green)
        self.draw(self.__info_text)


        self.__actve_text.set_typed_origin(OriginTypes.TOP_RIGHT)
        self.__actve_text.set_position(self.get_size()[0]-8, 0)
        self.__actve_text.set_text(f"Active: {self.__active}").set_size(17)
        self.draw(self.__actve_text)

        # График фреймтайма
        graph_width = 200
        graph_height = 100
        graph_x = 10
        graph_y = 100

        # Фон графика
        self.__info_bg.set_size(graph_width, graph_height)
        self.__info_bg.set_position(graph_x, graph_y)
        self.__info_bg.set_color(self.__info_bg_color)
        self.draw(self.__info_bg)

        # Сетка графика
        # Максимальное значение FPS для масштабирования графика
        max_fps = max(self.__fps_history) if self.__fps_history else self.__wait_fps
        for i in range(5): # Рисуем 5 горизонтальных линий сетки
            y_pos = graph_y + i * (graph_height / 4)
            self.__info_line.set_start_pos(graph_x, y_pos)
            self.__info_line.set_end_pos(graph_x + graph_width, y_pos)
            self.__info_line.set_color(self.__info_line_color)
            self.draw(self.__info_line)
            
            # Отображаем числовые значения FPS по оси Y
            fps_value = max_fps - (i * (max_fps / 4))
            self.__info_text_fps.set_size(10)
            self.__info_text_fps.set_text(f"{fps_value:.0f}")
            self.__info_text_fps.set_position(graph_x + graph_width + 3, y_pos - 7)
            self.__info_text_fps.set_color(self.__info_text_fps_color)
            self.draw(self.__info_text_fps)

        # Линия графика FPS
        if len(self.__fps_history) > 1: # Рисуем линию только если есть хотя бы 2 точки в истории
            self.__fps_line.clear() # Очищаем предыдущие точки линии
            
            for i, fps in enumerate(self.__fps_history):
                # Вычисляем координаты точки на графике
                x = graph_x + (i * graph_width / (self.__max_history - 1))
                y = graph_y + graph_height - (fps * graph_height / max_fps)
                # Выбираем цвет линии в зависимости от производительности
                color = self.__fps_line_color_green if fps >= max_fps * 0.5 else self.__fps_line_color_red
                self.__fps_line.append_point_to_end(x, y, color) # Добавляем точку к линии
            
            self.draw(self.__fps_line) # Отрисовываем линию

    def set_vertical_sync(self, value: bool) -> Self:
        """
        Включает или выключает вертикальную синхронизацию.
        Вертикальная синхронизация синхронизирует частоту кадров приложения с частотой обновления монитора,
        чтобы избежать визуальных артефактов, таких как "разрывы" изображения.
        
        Args:
            value (bool): True для включения вертикальной синхронизации, False для выключения.
        """
        self.__vsync = value
        LIB_PYSGL.SetVerticalSync(self.__window_ptr, value)
        return self

    def set_exit_key(self, key: str) -> Self:
        """
        Устанавливает клавишу, нажатие которой приведет к закрытию окна.
        
        Args:
            key (str): Название клавиши (например, "esc", "q", "delete").
                       Используется библиотека `keyboard` для отслеживания нажатий.
        """
        self.__exit_key = key
        return self

    def get_exit_key(self) -> str:
        """
        Возвращает установленную клавишу для закрытия окна.
        
        Returns:
            str: Название клавиши.
        """
        return self.__exit_key
    
    def set_view_info(self, value: bool = True) -> Self:
        """
        Включает или выключает отображение отладочной информации (FPS, время рендеринга) на окне.
        
        Args:
            value (bool): True для включения отображения, False для выключения (по умолчанию True).
        """
        self.__view_info = value
        return self

    def get_delta(self) -> float:
        """
        Возвращает дельта-тайм (delta-time) - отношение целевого FPS к текущему FPS.
        Дельта-тайм используется для обеспечения независимости скорости игрового процесса
        от частоты кадров.
        
        Returns:
            float: Значение дельта-тайма.
        """
        return self.__delta

    def set_target_fps(self, fps: int) -> Self:
        """
        Устанавливает целевой FPS (количество кадров в секунду) для расчета дельта-тайма.
        Это не ограничивает фактический FPS, а используется как эталон для масштабирования времени.
        
        Args:
            fps (int): Целевое количество кадров в секунду.
        """
        self.__target_fps = fps
        return self

    def get_target_fps(self) -> int:
        """
        Возвращает установленный целевой FPS.
        
        Returns:
            int: Целевое количество кадров в секунду.
        """
        return self.__target_fps

    def set_wait_fps(self, fps: int) -> Self:
        """
        Устанавливает ограничение на максимальное количество кадров в секунду (FPS).
        Это функция, которая пытается ограничить фактический FPS отрисовки.
        Возможна неточность установки, так как фактический FPS может зависеть от операционной системы и оборудования.
        
        Args:
            fps (int): Максимальное количество кадров в секунду.
        """
        LIB_PYSGL.setWaitFps(self.__window_ptr, int(fps))
        self.__wait_fps = fps
        return self

    def get_wait_fps(self) -> int:
        """
        Возвращает установленное ограничение на FPS.
        
        Returns:
            int: Максимальное количество кадров в секунду.
        """
        return self.__wait_fps
    
    def get_render_time(self, factor: float = 1) -> float:
        """
        Возвращает время, затраченное на рендеринг последнего кадра, в секундах.
        
        Returns:
            float: Время рендеринга в секундах.
        """
        return self.__render_time * factor
    
    def get_fps(self) -> float:
        """
        Возвращает текущее количество кадров в секунду (FPS).
        
        Returns:
            float: Текущий FPS.
        """
        return self.__fps
    
    def get_global_timer(self, factor: float = 1.0) -> float:
        """
        Возвращает время работы приложения с момента открытия окна, умноженное на заданный множитель.
        
        Args:
            delta (float): Множитель времени (по умолчанию 1.0). Используется для ускорения/замедления времени.
            
        Returns:
            float: Время работы приложения, умноженное на delta.
        """
        return (time() - self.__start_time) * factor
    
    def set_view(self, view: View) -> Self:
        """
        Устанавливает текущую область просмотра для окна.
        Все последующие отрисовки будут выполняться относительно этой области просмотра.
        
        Args:
            view (View): Объект области просмотра (View).
        """
        LIB_PYSGL.setView(self.__window_ptr, view.get_ptr())
        return self
    
    def disable(self):
        self.__window_descriptor = ctypes.windll.user32.FindWindowW(None, self.__title)
        ctypes.windll.user32.EnableWindow(self.__window_descriptor, False)
        self.__active = False
            
    def enable(self):
        self.__window_descriptor = ctypes.windll.user32.FindWindowW(None, self.__title)
        ctypes.windll.user32.EnableWindow(self.__window_descriptor, True)
        self.__active = True
            

    def update(self, events: WindowEvents) -> bool:
        """
        Обновляет состояние окна и обрабатывает события из очереди.
        Этот метод должен вызываться в каждом кадре основного цикла приложения.
        Он также рассчитывает FPS, дельта-тайм и время рендеринга.
        
        Args:
            events (Events): Объект для работы с событиями.
            
        Returns:
            bool: False, если окно должно быть закрыто (например, пользователь нажал кнопку закрытия
                  или установленную клавишу выхода), иначе True.
        """

        if self.__ghosting:
            if MouseInterface.in_window(self):
                self.__ghosting_at_value = 255
            else:
                self.__ghosting_at_value = self.__ghosting_min_value
            self.__window_alpha += (self.__ghosting_at_value - self.__window_alpha) * self.__ghosting_interpolation
            self.set_alpha(self.__window_alpha)
        
        # Измерение времени рендеринга предыдущего кадра и перезапуск счетчика
        self.__render_time = self.__clock.get_elapsed_time()
        self.__clock.restart()
        # Расчет текущего FPS
        self.__fps = 1 / self.__render_time if self.__render_time > 0 else 0
        # Расчет дельта-тайма
        self.__delta = self.__target_fps / self.__fps if self.__fps > 0 else 1
        
        # Обновление истории FPS для графика
        self.__fps_update_timer += self.__render_time
        if self.__fps_update_timer >= 0.1: # Обновляем историю каждые 0.1 секунды
            self.__fps_history.append(self.__fps)
            self.__min_fps_in_fps_history = min(self.__fps_history)
            self.__max_fps_in_fps_history = max(self.__fps_history)
            if len(self.__fps_history) >= self.__max_history:
                self.__fps_history.pop(0) # Удаляем старейшее значение, если история переполняется
                
            self.__fps_update_timer = 0

        # Опрос событий окна
        event_type = events.poll(self)
        # Проверка условий закрытия окна (пользователь закрыл окно или нажал клавишу выхода)
        if event_type == WindowEvents.Type.Closed or keyboard.is_pressed(self.__exit_key):
            return False
        
        # Обработка события изменения размера окна
        if event_type == WindowEvents.Type.Resized:
            self.__width = events.get_size_width()
            self.__height = events.get_size_height()
            # Обновление размера и центра стандартной области просмотра
            self.__view.set_size(self.__width, self.__height)
            self.__view.set_center(self.__width / 2, self.__height / 2)
            self.set_view(self.__view) # Применяем обновленную область просмотра

        # Установка флага, если размер окна изменился по сравнению с прошлым кадром
        if self.__end_height != self.__height or self.__end_width != self.__width:
            self.__resized = True
        else:
            self.__resized = False

        # Сохранение текущих размеров для следующего кадра
        self.__end_height = self.__height
        self.__end_width = self.__width

        return True
    
    def get_resized(self) -> bool:
        """
        Возвращает True, если размер окна был изменен в текущем кадре, иначе False.
        
        Returns:
            bool: True, если размер окна изменился.
        """
        return self.__resized
    
    def clear(self, color: Color | None = None) -> None:
        """
        Очищает содержимое окна заданным цветом.
        Если цвет не указан, используется цвет очистки по умолчанию, установленный через `set_clear_color`.
        
        Args:
            color (Color | None): Объект Color для заливки, или None для использования цвета по умолчанию.
        
        Raises:
            TypeError: Если переданный аргумент 'color' не является объектом Color или None.
        """
        if isinstance(color, Color):
            LIB_PYSGL.clearWindow(self.__window_ptr, color.r, color.g, color.b, color.a)
        elif color is None:
            LIB_PYSGL.clearWindow(self.__window_ptr, self.__clear_color.r, self.__clear_color.g, self.__clear_color.b, self.__clear_color.a)
        else:
            raise TypeError("Color or None expected, got " + type(color).__name__)
    
    def display(self) -> None:
        """
        Отображает нарисованное содержимое (все объекты, отрисованные с момента последнего `clear()` и `display()`)
        на экране. Это вызывает переключение буферов кадра.
        """
        LIB_PYSGL.displayWindow(self.__window_ptr)

    def set_title(self, title: str) -> Self:
        """
        Устанавливает заголовок окна.
        
        Args:
            title (str): Новый заголовок окна.
        """
        self.__title = title
        LIB_PYSGL.setWindowTitle(self.__window_ptr, title.encode('utf-8'))
        return self
    
    def get_title(self) -> str:
        return self.__title

    def set_clear_color(self, color: Color) -> Self:
        """
        Устанавливает цвет, который будет использоваться для очистки окна по умолчанию
        при вызове метода `clear()` без аргументов.
        
        Args:
            color (Color): Новый объект Color для очистки.
        """
        self.__clear_color = color
        return self

    def get_clear_color(self) -> Color:
        """
        Возвращает текущий цвет очистки окна по умолчанию.
        
        Returns:
            Color: Текущий объект Color, используемый для очистки.
        """
        return self.__clear_color
    
    def is_open(self) -> bool:
        """
        Проверяет, открыто ли окно.
        
        Returns:
            bool: True, если окно открыто и активно, False, если оно было закрыто.
        """
        return LIB_PYSGL.isWindowOpen(self.__window_ptr)
    
    @overload
    def draw(self, shape, render_states: RenderStates) -> None:
        """
        Отрисовывает объект с указанными параметрами рендеринга.
        
        Args:
            shape: Объект для отрисовки (например, Shape, Text). Должен иметь метод `get_ptr()`.
            render_states (RenderStates): Объект RenderStates, определяющий такие параметры, как смешивание,
                                         матрица преобразования, текстура и шейдер.
        """
        ...

    @overload
    def draw(self, shape, shader: Shader) -> None:
        """
        Отрисовывает объект с указанным шейдером.
        
        Args:
            shape: Объект для отрисовки (например, Shape, Text).
            shader (Shader): Объект Shader, который будет использоваться для рендеринга объекта.
        """
        ...

    @overload
    def draw(self, shape) -> None:
        """
        Отрисовывает объект с параметрами рендеринга по умолчанию.
        
        Args:
            shape: Объект для отрисовки (например, Shape, Text).
        """
        ...
    
    def draw(self, shape, render_states: RenderStates | Shader | None = None) -> None:
        """
        Основной метод для отрисовки объектов в окне.
        Поддерживает отрисовку с параметрами по умолчанию, с пользовательскими RenderStates или с шейдером.
        
        Args:
            shape: Объект для отрисовки. Он должен предоставлять метод `get_ptr()`
                   для получения указателя на его нативное представление,
                   кроме некоторых специфичных для Python объектов отрисовки (например, LineThin, LinesThin).
            render_states (RenderStates | Shader | None): Необязательный аргумент, который может быть
                                                          объектом RenderStates для продвинутого управления рендерингом,
                                                          объектом Shader для применения пользовательского шейдера,
                                                          или None для использования параметров по умолчанию.
        """
        # Проверяем, является ли shape "особым" объектом, который требует специальной обработки в Python
        # (например, многосегментные линии, которые не имеют прямого указателя на один объект в C++).
        # В данном случае, это относится к некоторым классам линий, которые могут агрегировать несколько
        # примитивов C++ или иметь более сложную логику отрисовки.
        
        if not isinstance(shape.get_ptr(), int):    
            shape.special_draw(self) # Вызов специального метода отрисовки, реализованного в Python
        else:
            # Для стандартных объектов, которые имеют указатель на C++ объект
            if render_states is None:
                # Отрисовка с параметрами по умолчанию
                LIB_PYSGL.drawWindow(self.__window_ptr, shape.get_ptr())
            else:    
                # Отрисовка с пользовательскими RenderStates или шейдером
                if isinstance(render_states, RenderStates):
                    LIB_PYSGL.drawWindowWithStates(self.__window_ptr, render_states.get_ptr(), shape.get_ptr())
                elif isinstance(render_states, Shader):
                    LIB_PYSGL.drawWindowWithShader(self.__window_ptr, render_states.get_ptr(), shape.get_ptr())
        

