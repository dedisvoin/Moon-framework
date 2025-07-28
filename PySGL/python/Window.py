"""
#### *Модуль работы с окнами в PySGL*

---

##### Версия: 1.1.8

*Автор: Павлов Иван (Pavlov Ivan)*

*Лицензия: MIT*
##### Реализованно на 98% 

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


LIB_PYSGL.createWindow.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
LIB_PYSGL.createWindow.restype = ctypes.c_void_p
LIB_PYSGL.destroyWindow.argtypes = [ctypes.c_void_p]
LIB_PYSGL.destroyWindow.restype = None
LIB_PYSGL.clearWindow.argtypes = [ctypes.c_void_p, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte]
LIB_PYSGL.clearWindow.restype = None
LIB_PYSGL.displayWindow.argtypes = [ctypes.c_void_p]
LIB_PYSGL.displayWindow.restype = None
LIB_PYSGL.isWindowOpen.argtypes = [ctypes.c_void_p]
LIB_PYSGL.isWindowOpen.restype = ctypes.c_bool
LIB_PYSGL.drawWindow.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.drawWindow.restype = None
LIB_PYSGL.getView.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getView.restype = ctypes.c_void_p
LIB_PYSGL.setWaitFps.argtypes = [ctypes.c_void_p, ctypes.c_uint]
LIB_PYSGL.setWaitFps.restype = None
LIB_PYSGL.setWindowTitle.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
LIB_PYSGL.setWindowTitle.restype = None
LIB_PYSGL.SetVerticalSync.argtypes = [ctypes.c_void_p, ctypes.c_bool]
LIB_PYSGL.SetVerticalSync.restype = None
LIB_PYSGL.createEvent.argtypes = []
LIB_PYSGL.createEvent.restype = ctypes.c_void_p
LIB_PYSGL.destroyEvent.argtypes = [ctypes.c_void_p]
LIB_PYSGL.destroyEvent.restype = None
LIB_PYSGL.getWindowEvent.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.getWindowEvent.restype = ctypes.c_int
LIB_PYSGL.getEventType.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventType.restype = ctypes.c_int
LIB_PYSGL.getEventKey.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventKey.restype = ctypes.c_int
LIB_PYSGL.getEventMouseButton.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventMouseButton.restype = ctypes.c_int
LIB_PYSGL.getEventMouseX.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventMouseX.restype = ctypes.c_int
LIB_PYSGL.getEventMouseY.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventMouseY.restype = ctypes.c_int
LIB_PYSGL.getEventSizeWidth.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventSizeWidth.restype = ctypes.c_int
LIB_PYSGL.getEventSizeHeight.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventSizeHeight.restype = ctypes.c_int
LIB_PYSGL.getEventMouseWheel.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getEventMouseWheel.restype = ctypes.c_int
LIB_PYSGL.setViewCenter.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL.setViewCenter.restype = None
LIB_PYSGL.setViewSize.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float]
LIB_PYSGL.setViewSize.restype = None
LIB_PYSGL.setView.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.setView.restype = None
LIB_PYSGL.getWindowSizeWidth.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getWindowSizeWidth.restype = ctypes.c_int
LIB_PYSGL.getWindowSizeHeight.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getWindowSizeHeight.restype = ctypes.c_int
LIB_PYSGL.getWindowPositionX.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getWindowPositionX.restype = ctypes.c_int
LIB_PYSGL.getWindowPositionY.argtypes = [ctypes.c_void_p]
LIB_PYSGL.getWindowPositionY.restype = ctypes.c_int
LIB_PYSGL.setWindowPosition.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
LIB_PYSGL.setWindowPosition.restype = None
LIB_PYSGL.setWindowSize.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
LIB_PYSGL.setWindowSize.restype = None
LIB_PYSGL.zoomView.argtypes = [ctypes.c_void_p, ctypes.c_float]
LIB_PYSGL.zoomView.restype = None
LIB_PYSGL.mapPixelToCoordsX.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_void_p]
LIB_PYSGL.mapPixelToCoordsX.restype = ctypes.c_float
LIB_PYSGL.mapPixelToCoordsY.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_void_p]
LIB_PYSGL.mapPixelToCoordsY.restype = ctypes.c_float
LIB_PYSGL.mapCoordsToPixelX.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_void_p]
LIB_PYSGL.mapCoordsToPixelX.restype = ctypes.c_float
LIB_PYSGL.mapCoordsToPixelY.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_void_p]
LIB_PYSGL.mapCoordsToPixelY.restype = ctypes.c_float
LIB_PYSGL.drawWindowWithStates.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.drawWindowWithStates.restype = None
LIB_PYSGL.drawWindowWithShader.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
LIB_PYSGL.drawWindowWithShader.restype = None
LIB_PYSGL.setMouseCursorVisible.argtypes = [ctypes.c_void_p, ctypes.c_bool]
LIB_PYSGL.setMouseCursorVisible.restype = None
LIB_PYSGL.closeWindow.argtypes = [ctypes.c_void_p]
LIB_PYSGL.closeWindow.restype = None
LIB_PYSGL.setSystemCursor.argtypes = [ctypes.c_void_p, ctypes.c_int]
LIB_PYSGL.setSystemCursor.restype = None
  
class WindowEvents:
    """
    #### Класс для обработки событий окна
    
    ---
    
    :Description:
    - Обеспечивает интерфейс для работы с событиями окна (клавиатура, мышь, джойстик и др.)
    - Получает события из системной очереди сообщений
    - Преобразует нативные события в удобный Python-интерфейс
    
    ---
    
    :Features:
    - Поддержка событий клавиатуры, мыши, джойстика
    - Обработка сенсорного ввода и событий окна
    - Получение детальной информации о каждом событии
    """
    
    class Type:
        """
        #### Перечисление типов событий окна
        
        ---
        
        :Values:
        - Closed: Окно было закрыто
        - Resized: Изменен размер окна
        - Focus: События изменения фокуса окна
        - Input: События ввода (клавиатура, мышь, джойстик)
        - Touch: События сенсорного ввода
        - Sensor: События датчиков устройства
        """
    ########################################################################### 
        Closed = 0                     # Окно запросило закрытие (крестик/Alt+F4)
        Resized = 1                    # Окно изменило размер (width/height доступны)
        LostFocus = 2                  # Окно потеряло фокус ввода
        GainedFocus = 3                # Окно получило фокус ввода
        TextEntered = 4                # Введен Unicode-символ (поддержка IME)

        KeyPressed = 5                 # Нажата клавиша клавиатуры
        KeyReleased = 6                # Отпущена клавиша клавиатуры

        MouseWheelMoved = 7            # Прокручено колесо мыши (устаревший формат)
        MouseWheelScrolled = 8         # Прокручено колесо мыши (новый формат)
        MouseButtonPressed = 9         # Нажата кнопка мыши
        MouseButtonReleased = 10       # Отпущена кнопка мыши
        MouseMoved = 11                # Перемещен курсор мыши
        MouseEntered = 12              # Курсор вошел в область окна
        MouseLeft = 13                 # Курсор покинул область окна

        JoystickButtonPressed = 14     # Нажата кнопка джойстика
        JoystickButtonReleased = 15    # Отпущена кнопка джойстика
        JoystickMoved = 16             # Изменено положение оси джойстика
        JoystickConnected = 17         # Джойстик подключен
        JoystickDisconnected = 18      # Джойстик отключен

        TouchBegan = 19                # Начало касания сенсорного экрана
        TouchMoved = 20                # Перемещение касания
        TouchEnded = 21                # Окончание касания
        SensorChanged = 22             # Изменение показаний датчика устройства
    ###########################################################################

    def __init__(self):
        """
        #### Инициализация обработчика событий
        
        ---
        
        :Actions:
        - Создает нативный объект для хранения событий
        - Подготавливает внутренние структуры данных
        
        ---
        
        :Raises:
        - RuntimeError: При ошибке создания нативного объекта
        """
        self.__event_ptr = LIB_PYSGL.createEvent()

    def __del__(self):
        """
        #### Освобождение ресурсов обработчика событий
        
        ---
        
        :Actions:
        - Удаляет нативный объект событий
        - Гарантирует корректное завершение работы
        """
        LIB_PYSGL.destroyEvent(self.__event_ptr)

    def get_ptr(self) -> ctypes.c_void_p:
        """
        #### Получение указателя на нативный объект событий
        
        ---
        
        :Returns:
        - ctypes.c_void_p: Указатель на внутренний объект событий
        
        ---
        
        :Note:
        - Для внутреннего использования в PySGL
        """
        return self.__event_ptr

    def poll(self, window) -> bool:
        """
        #### Проверка наличия событий в очереди
        
        ---
        
        :Args:
        - window: Объект окна для проверки событий
        
        ---
        
        :Returns:
        - bool: True если есть непрочитанные события, иначе False
        
        ---
        
        :Example:
        ```python
        while events.poll(window):
            handle_event(events)
        ```
        """
        return LIB_PYSGL.getWindowEvent(window.get_ptr(), self.__event_ptr)

    def get_type(self) -> int:
        """
        #### Получение типа текущего события
        
        ---
        
        :Returns:
        - int: Код события из WindowEvents.Type
        
        ---
        
        :Example:
        ```python
        if events.get_type() == WindowEvents.Type.KeyPressed:
            handle_key_press()
        ```
        """
        return LIB_PYSGL.getEventType(self.__event_ptr)

    def get_key(self) -> int:
        """
        #### Получение кода клавиши для событий клавиатуры
        
        ---
        
        :Returns:
        - int: Код клавиши (соответствует KeyCode)
        
        ---
        
        :Note:
        - Только для KeyPressed/KeyReleased событий
        """
        return LIB_PYSGL.getEventKey(self.__event_ptr)

    def get_mouse_button(self) -> int:
        """
        #### Получение кода кнопки мыши
        
        ---
        
        :Returns:
        - int: Код кнопки (0-левая, 1-правая, 2-средняя)
        
        ---
        
        :Note:
        - Для MouseButtonPressed/MouseButtonReleased
        """
        return LIB_PYSGL.getEventMouseButton(self.__event_ptr)
    
    def get_mouse_wheel(self) -> int:
        """
        #### Получение значения прокрутки колеса мыши
        
        ---
        
        :Returns:
        - int: Шаги прокрутки (>0 - вверх, <0 - вниз)
        
        ---
        
        :Note:
        - Для MouseWheelMoved/MouseWheelScrolled
        """
        return LIB_PYSGL.getEventMouseWheel(self.__event_ptr)

    def get_mouse_x(self) -> int:
        """
        #### Получение X-координаты курсора мыши
        
        ---
        
        :Returns:
        - int: Координата X в пикселях относительно окна
        
        ---
        
        :Note:
        - Для событий связанных с положением мыши
        """
        return LIB_PYSGL.getEventMouseX(self.__event_ptr)

    def get_mouse_y(self) -> int:
        """
        #### Получение Y-координаты курсора мыши
        
        ---
        
        :Returns:
        - int: Координата Y в пикселях относительно окна
        
        ---
        
        :Note:
        - Для событий связанных с положением мыши
        """
        return LIB_PYSGL.getEventMouseY(self.__event_ptr)
    
    def get_size_width(self) -> int:
        """
        #### Получение новой ширины окна
        
        ---
        
        :Returns:
        - int: Ширина окна после изменения (в пикселях)
        
        ---
        
        :Note:
        - Только для Resized события
        """
        return LIB_PYSGL.getEventSizeWidth(self.__event_ptr)
    
    def get_size_height(self) -> int:
        """
        #### Получение новой высоты окна
        
        ---
        
        :Returns:
        - int: Высота окна после изменения (в пикселях)
        
        ---
        
        :Note:
        - Только для Resized события
        """
        return LIB_PYSGL.getEventSizeHeight(self.__event_ptr)


# Тип для хранения указателя на объект окна ===== +
type WindowPtr = ctypes.c_void_p
# =============================================== +

# Константа для обозначения неограниченного FPS (представляется большим числом)
FPS_UNLIMIT_CONST: Final[float] = 1000000

class SystemCursors:
    """Класс, представляющий системные курсоры. Каждая константа соответствует определенному типу курсора."""
    
    Arrow = 0                     # Стандартный курсор (стрелка)
    ArrowWait = 1                 # Стрелка с индикатором ожидания (например, при занятости системы)
    Wait = 2                      # Курсор ожидания (обычно песочные часы или круговой индикатор)
    Text = 3                      # Текстовый курсор (вертикальная черта, используется в полях ввода)
    Hand = 4                      # Указатель в виде руки (обычно для кликабельных ссылок)
    
    # Курсоры изменения размера
    SizeHorizontal = 5             # Двунаправленная горизонтальная стрелка (изменение ширины)
    SizeVertical = 6               # Двунаправленная вертикальная стрелка (изменение высоты)
    SizeTopLeftBottomRight = 7     # Диагональная двунаправленная стрелка (↖↘, изменение размера по диагонали)
    SizeBottomLeftTopRight = 8     # Диагональная двунаправленная стрелка (↙↗, изменение размера по диагонали)
    
    # Курсоры изменения размера (альтернативные варианты)
    SizeLeft = 9                  # Курсор изменения размера влево (горизонтальная стрелка ←)
    SizeRight = 10                # Курсор изменения размера вправо (горизонтальная стрелка →)
    SizeTop = 11                  # Курсор изменения размера вверх (вертикальная стрелка ↑)
    SizeBottom = 12               # Курсор изменения размера вниз (вертикальная стрелка ↓)
    
    # Угловые курсоры изменения размера
    SizeTopLeft = 13              # Курсор изменения размера в верхний левый угол (↖)
    SizeBottomRight = 14          # Курсор изменения размера в нижний правый угол (↘)
    SizeBottomLeft = 15           # Курсор изменения размера в нижний левый угол (↙)
    SizeTopRight = 16             # Курсор изменения размера в верхний правый угол (↗)
    
    SizeAll = 17                  # Курсор перемещения (четырехнаправленная стрелка)
    Cross = 18                    # Перекрестие (используется для точного выбора, например в графических редакторах)
    Help = 19                     # Курсор со знаком вопроса (указывает на справку или подсказку)
    NotAllowed = 20               # Курсор "Действие запрещено" (перечеркнутый круг, например при drag-and-drop)


DWMWA_WINDOW_CORNER_PREFERENCE = 33

DWM_API = ctypes.WinDLL("dwmapi")

class Window:
    """
    #### Класс для создания и управления окном приложения
    
    ---
    
    :Description:
    - Создает графическое окно для отображения контента
    - Управляет параметрами окна (размер, заголовок, стиль)
    - Обеспечивает рендеринг графики и обработку событий
    
    ---
    
    :Features:
    - Поддержка различных стилей оформления окна
    - Настройка вертикальной синхронизации
    - Управление прозрачностью окна
    - Полноэкранные режимы работы
    """
    
    class Style:
        """
        #### Перечисление стилей окна
        
        ---
        
        :Values:
        - No: Окно без рамки и элементов управления
        - Titlebar: Окно с заголовком
        - Resize: Окно с возможностью изменения размера
        - Close: Окно с кнопкой закрытия
        - FullScreen: Настоящий полноэкранный режим
        - FullScreenDesktop: Псевдо-полноэкранный режим (окно под разрешение рабочего стола)
        - Default: Стандартный набор стилей (Titlebar | Resize | Close)
        
        ---
        
        :Note:
        - Стили можно комбинировать через побитовое OR (|)
        - Пример: `Style.Titlebar | Style.Close`
        """
        No = 0                        # Просто окно без каких-либо декораций
        Titlebar = 1 << 0             # Окно с заголовком и кнопкой свернуть
        Resize = 1 << 1               # Окно с изменяемым размером и рамкой
        Close = 1 << 2                # Окно с кнопкой закрытия
        FullScreen = 1 << 3           # Полноэкранный режим с собственным разрешением
        FullScreenDesktop = 1 << 4    # Полноэкранный режим с разрешением рабочего стола
        Default = Titlebar | Resize | Close  # Стандартный набор стилей окон

    def __init__(self, width: int = 800, height: int = 600, 
                 title: str = "PySGL Window", style: int = Style.Default, 
                 vsync: bool = False, alpha: float = 255):
        """
        #### Инициализация нового окна приложения
        
        ---
        
        :Args:
        - width (int): Начальная ширина окна в пикселях (по умолчанию 800)
        - height (int): Начальная высота окна в пикселях (по умолчанию 600)
        - title (str): Заголовок окна (по умолчанию "PySGL Window")
        - style (int): Комбинация стилей из Window.Style (по умолчанию Style.Default)
        - vsync (bool): Включение вертикальной синхронизации (по умолчанию False)
        - alpha (float): Уровень прозрачности окна (0-255, по умолчанию 255 - непрозрачное)
        
        ---
        
        :Raises:
        - RuntimeError: При невозможности создать графическое окно
        
        ---
        
        :Note:
        - Вертикальная синхронизация (vsync) устраняет артефакты разрыва кадров
        - Прозрачность (alpha) поддерживается не на всех платформах
        
        ---
        
        :Example:
        ```python
        # Создание окна со стандартными параметрами
        window = Window()
        
        # Создание полноэкранного окна
        fullscreen = Window(style=Window.Style.FullScreen)
        ```
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

        self.__start_time = time()              # Время открытия окна (для get_global_timer)

        self.__cursor_visibility: bool = True   # Флаг видимости курсора мыши

        self.set_vertical_sync(vsync)           # Устанавливает вертикальную синхронизацию при инициализации

        self.__ghosting: bool = False
        self.__ghosting_min_value: int = 30
        self.__ghosting_at_value: int = 255
        self.__ghosting_interpolation: float = 0.1

        self.__active: bool = True
        self.__actve_text = Text(self.__info_font)
        self.__cursor: SystemCursors = SystemCursors.Arrow

        # Флаг который будет реализован в будщем 
        self.__using_custom_window: bool = False


    def enable_rounded_corners(self) -> Self:
        """
        #### Включает скругленные углы для окна (Windows 11+)
        
        ---
        
        :Description:
        - Применяет современный стиль с закругленными углами к окну
        - Работает только в Windows 11 и новее
        - Для других ОС или версий Windows эффекта не будет
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        window.enable_rounded_corners()
        ```
        """
        DWM_API.DwmSetWindowAttribute(
            self.__window_descriptor, 
            DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(ctypes.c_int(2)), 
            ctypes.sizeof(ctypes.c_int(2)))
        return self

    def set_system_cursor(self, cursor: SystemCursors) -> Self:
        """
        #### Устанавливает системный курсор для окна
        
        ---
        
        :Args:
        - cursor (SystemCursors): Тип курсора из перечисления SystemCursors
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        window.set_system_cursor(SystemCursors.Hand)  # Курсор в виде руки
        ```
        """
        self.__cursor = cursor
        LIB_PYSGL.setSystemCursor(self.__window_ptr, cursor)
        return self

    def get_cursor(self) -> SystemCursors:
        """
        #### Возвращает текущий системный курсор окна
        
        ---
        
        :Returns:
        - SystemCursors: Текущий установленный курсор
        
        ---
        
        :Example:
        ```python
        if window.get_cursor() == SystemCursors.Wait:
            print("Сейчас установлен курсор ожидания")
        ```
        """
        return self.__cursor

    def get_active(self) -> bool:
        """
        #### Проверяет, является ли окно активным
        
        ---
        
        :Description:
        - Возвращает True, если окно в данный момент окное не заблокированно 
        - Возвращает False, если окно заблокированно програмно
        - Для окон верхнего уровня также учитывает видимость
        
        ---
        
        :Returns:
        - bool: True если окно активно, False в противном случае
        
        ---
        
        :Example:
        ```python
        # Обновлять содержимое только для активного окна
        if window.get_active():
            ...
        ```
        """
        return self.__active

    def enable_ghosting(self, value: bool = True) -> Self:
        """
        #### Включает/выключает эффект "призрачного" окна
        
        ---
        
        :Description:
        - При включении делает окно полупрозрачным при потере фокуса
        - Эффект автоматически регулирует прозрачность между минимальным и максимальным значениями

        ---
        
        :Args:
        - value (bool): True - включить эффект, False - выключить (по умолчанию True)

        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов

        ---
        
        :Example:
        ```python
        # Включить эффект призрачного окна
        window.enable_ghosting()
        
        # Выключить эффект
        window.enable_ghosting(False)
        ```
        """
        self.__ghosting = value
        return self

    def get_ghosting(self) -> bool:
        """
        #### Проверяет, включен ли эффект призрачного окна

        ---
        
        :Returns:
        - bool: True если эффект включен, False если выключен

        ---
        
        :Example:
        ```python
        if window.get_ghosting():
            print("Эффект призрачного окна активен")
        ```
        """
        return self.__ghosting
        
    def set_ghosting_min_alpha(self, alpha: int) -> Self:
        """
        #### Устанавливает минимальную прозрачность для эффекта призрачного окна

        ---
        
        :Args:
        - alpha (int): Значение прозрачности (0-255), где 0 - полностью прозрачное
        
        ---

        :Returns:
        - Self: Возвращает self для цепочки вызовов

        ---
        
        :Note:
        - Действует только при включенном эффекте ghosting

        ---
        
        :Example:
        ```python
        # Установить минимальную прозрачность 50%
        window.set_ghosting_min_alpha(128)
        ```
        """
        self.__ghosting_min_value = alpha
        return self
        
    def get_ghosting_min_alpha(self) -> int:
        """
        #### Возвращает текущее минимальное значение прозрачности для эффекта призрачного окна
        
        ---

        :Returns:
        - int: Текущее значение минимальной прозрачности (0-255)
        
        ---
        
        :Example:
        ```python
        print(f"Текущая минимальная прозрачность: {window.get_ghosting_min_alpha()}")
        ```
        """
        return self.__ghosting_min_value

    def set_alpha(self, alpha: int):
        """
        #### Устанавливает глобальную прозрачность окна
        
        ---
        
        :Args:
        - alpha (int): Уровень прозрачности (0 - полностью прозрачное, 255 - непрозрачное)
        
        ---
        
        :Note:
        - Работает только на Windows через WinAPI
        - Требует стиль WS_EX_LAYERED
        - `! Кроссплатформенные решения еще не реализованы !`
        
        ---
        
        :Example:
        ```python
        window.set_alpha(100)
        ```
        """
        self.__window_descriptor = ctypes.windll.user32.FindWindowW(None, self.__title)
        self.__window_alpha = alpha  # Конвертируем в диапазон 0-255

        # Устанавливаем стиль слоистого окна
        style = ctypes.windll.user32.GetWindowLongW(self.__window_descriptor, -20)  # GWL_EXSTYLE = -20
        ctypes.windll.user32.SetWindowLongW(self.__window_descriptor, -20, style | 0x00080000)  # WS_EX_LAYERED = 0x00080000
        
        # Применяем прозрачность
        ctypes.windll.user32.SetLayeredWindowAttributes(
            self.__window_descriptor, 
            0,  # Ключ цвета (не используется)
            int(self.__window_alpha),  # Значение альфа-канала
            2  # LWA_ALPHA = 2
        )

    def get_alpha(self) -> float:
        """
        #### Возвращает текущий уровень прозрачности окна
        
        ---
        
        :Description:
        - Возвращает значение в диапазоне от 0 (полная прозрачность) до 255 (полная непрозрачность)
        - Соответствует последнему установленному значению через set_alpha()
        
        ---
        
        :Returns:
        - float: Текущий уровень прозрачности окна
        
        ---
        
        :Example:
        ```python
        # Проверить текущую прозрачность
        transparency = window.get_alpha()
        print(f"Текущая прозрачность: {transparency}")
        ```
        """
        return self.__window_alpha

    def close(self) -> None:
        """
        #### Полностью закрывает окно и освобождает ресурсы
        
        ---
        
        :Description:
        - Завершает работу графического контекста
        - Освобождает системные ресурсы
        - Удаляет все связанные с окном объекты
        
        ---
        
        :Note:
        - После вызова этого метода окно нельзя использовать повторно
        - Рекомендуется вызывать в конце работы приложения
        
        ---
        
        :Example:
        ```python
        # Стандартный цикл закрытия
        window.close()
        ```
        """
        LIB_PYSGL.closeWindow(self.__window_ptr)

    def hide_cursor(self) -> Self:
        """
        #### Скрывает системный курсор в области окна
        
        ---
        
        :Description:
        - Делает курсор невидимым при наведении на окно
        - Сохраняет состояние для последующего восстановления
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Для режима полноэкранной игры
        window.hide_cursor().set_fullscreen(True)
        ```
        """
        LIB_PYSGL.setMouseCursorVisible(self.__window_ptr, False)
        self.__cursor_visibility = False
        return self
        
    def show_cursor(self) -> Self:
        """
        #### Восстанавливает видимость курсора в области окна
        
        ---
        
        :Description:
        - Показывает стандартный курсор при наведении на окно
        - Восстанавливает предыдущее состояние курсора
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Для обычного оконного режима
        window.show_cursor().set_fullscreen(False)
        ```
        """
        LIB_PYSGL.setMouseCursorVisible(self.__window_ptr, True)
        self.__cursor_visibility = True
        return self

    def get_cursor_visibility(self) -> bool:
        """
        #### Проверяет видимость курсора мыши в окне
        
        ---
        
        :Description:
        - Возвращает текущее состояние видимости курсора
        - Соответствует последнему установленному значению через show_cursor()/hide_cursor()
        
        ---
        
        :Returns:
        - bool: True если курсор видим, False если скрыт
        
        ---
        
        :Example:
        ```python
        if window.get_cursor_visibility():
            print("Курсор в настоящее время виден")
        else:
            print("Курсор скрыт")
        ```
        """
        return self.__cursor_visibility

    def set_max_fps_history(self, number: int) -> Self:
        """
        #### Устанавливает глубину истории значений FPS
        
        ---
        
        :Description:
        - Определяет сколько последних значений FPS сохраняется для анализа
        - Используется для построения графиков производительности
        - Большие значения требуют больше памяти, но дают более точную статистику
        
        ---
        
        :Args:
        - number (int): Максимальное количество сохраняемых значений (должно быть > 0)
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Raises:
        - ValueError: Если передано неположительное число
        
        ---
        
        :Example:
        ```python
        # Сохранять последние 120 значений FPS (2 секунды при 60 FPS)
        window.set_max_fps_history(120)
        ```
        """
        if number <= 0:
            raise ValueError("History size must be positive")
        self.__max_history = number
        return self

    def get_max_fps_history(self) -> int:
        """
        #### Возвращает текущий размер истории FPS
        
        ---
        
        :Description:
        - Показывает сколько последних значений FPS сохраняется в памяти
        - Значение по умолчанию обычно составляет 60 (1 секунда при 60 FPS)
        
        ---
        
        :Returns:
        - int: Текущая глубина истории значений FPS
        
        ---
        
        :Example:
        ```python
        print(f"Текущий размер истории FPS: {window.get_max_fps_history()}")
        ```
        """
        return self.__max_history

    def convert_window_coords_to_view_coords(self, x: float, y: float, view: View) -> Vector2f:
        """
        #### Преобразует экранные координаты в мировые относительно камеры
        
        ---
        
        :Description:
        - Конвертирует координаты из пикселей экрана в мировые координаты игры
        - Учитывает текущее положение, масштаб и поворот камеры (View)
        - Полезно для обработки ввода (мышь/тач) в игровом пространстве
        
        ---
        
        :Args:
        - x (float): Горизонтальная позиция в пикселях (от левого края окна)
        - y (float): Вертикальная позиция в пикселях (от верхнего края окна)
        - view (View): Камера/вид, относительно которой выполняется преобразование
        
        ---
        
        :Returns:
        - Vector2f: Преобразованные координаты в игровом пространстве
        
        ---
        
        :Example:
        ```python
        # Получить мировые координаты клика мыши
        mouse_pos = window.convert_window_coords_to_view_coords(mouse_x, mouse_y, game_view)
        print(f"Клик в мире игры: {mouse_pos.x}, {mouse_pos.y}")
        ```
        """
        return Vector2f(
            LIB_PYSGL.mapPixelToCoordsX(self.__window_ptr, x, y, view.get_ptr()),
            LIB_PYSGL.mapPixelToCoordsY(self.__window_ptr, x, y, view.get_ptr()),
        )
        
    def convert_view_coords_to_window_coords(self, x: float, y: float, view: View) -> Vector2f:
        """
        #### Преобразует мировые координаты в экранные относительно камеры
        
        ---
        
        :Description:
        - Конвертирует координаты из игрового пространства в пиксели экрана
        - Учитывает текущее положение, масштаб и поворот камеры (View)
        - Полезно для позиционирования UI элементов в мировых координатах
        
        ---
        
        :Args:
        - x (float): Горизонтальная позиция в игровом пространстве
        - y (float): Вертикальная позиция в игровом пространстве
        - view (View): Камера/вид, относительно которой выполняется преобразование
        
        ---
        
        :Returns:
        - Vector2f: Преобразованные экранные координаты в пикселях
        
        ---
        
        :Example:
        ```python
        # Получить экранные координаты игрового объекта
        screen_pos = window.convert_view_coords_to_window_coords(object_x, object_y, game_view)
        print(f"Объект на экране: {screen_pos.x}, {screen_pos.y}")
        ```
        """
        return Vector2f(
            LIB_PYSGL.mapCoordsToPixelX(self.__window_ptr, x, y, view.get_ptr()),
            LIB_PYSGL.mapCoordsToPixelY(self.__window_ptr, x, y, view.get_ptr()),
        )

    def get_default_view(self) -> View:
        """
        #### Возвращает стандартное представление (View) окна
        
        ---
        
        :Description:
        - Возвращает View, соответствующее полному размеру окна
        - Начало координат (0,0) в левом верхнем углу
        - Не содержит трансформаций (масштаб=1, поворот=0)
        - Автоматически обновляется при изменении размера окна
        
        ---
        
        :Returns:
        - View: Объект стандартного представления
        
        ---
        
        :Example:
        ```python
        # Сброс камеры к стандартному виду (это просто пример)
        camera = window.get_default_view()
        ```
        """
        return View.from_view_ptr(LIB_PYSGL.getView(self.__window_ptr))

    def set_position(self, x: int, y: int) -> Self:
        """
        #### Устанавливает позицию окна на экране
        
        ---
        
        :Description:
        - Позиционирует окно относительно верхнего левого угла экрана
        - Координаты указываются в пикселях
        
        ---
        
        :Args:
        - x (int): Горизонтальная позиция (X координата)
        - y (int): Вертикальная позиция (Y координата)
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Позиционировать окно в точке (100, 200)
        window.set_position(100, 200)
        ```
        """
        LIB_PYSGL.setWindowPosition(self.__window_ptr, x, y)
        return self

    def set_size(self, width: int, height: int) -> Self:
        """
        #### Изменяет размер окна
        
        ---
        
        :Description:
        - Устанавливает новые размеры клиентской области окна
        - Минимальный/максимальный размер зависит от системы
        - Может вызвать событие `Resized`
        
        ---
        
        :Args:
        - width (int): Новая ширина в пикселях (>0)
        - height (int): Новая высота в пикселях (>0)
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Raises:
        - ValueError: При недопустимых размерах
        
        ---
        
        :Example:
        ```python
        # Установить размер 800x600
        window.set_size(800, 600)
        ```
        """
        if width <= 0 or height <= 0:
            raise ValueError("Window dimensions must be positive")
        LIB_PYSGL.setWindowSize(self.__window_ptr, width, height)
        return self

    def get_ptr(self) -> WindowPtr:
        """
        #### Возвращает нативный указатель на окно
        
        ---
        
        :Description:
        - Предоставляет доступ к низкоуровневому объекту окна
        - Используется для интеграции с нативным кодом
        
        ---
        
        :Returns:
        - WindowPtr: Указатель на внутренний объект окна
        
        ---
        
        :Note:
        - Только для продвинутого использования
        - Не изменяйте объект напрямую
        
        ---
        
        :Example:
        ```python
        # Передать указатель в нативную функцию
        native_function(window.get_ptr())
        ```
        """
        return self.__window_ptr
    
    def get_size(self) -> Vector2i:
        """
        #### Возвращает текущий размер клиентской области окна
        
        ---
        
        :Description:
        - Возвращает размеры в пикселях
        - Учитывает только рабочую область (без рамок и заголовка)
        - Размеры обновляются при изменении окна
        
        ---
        
        :Returns:
        - Vector2i: Вектор с шириной (x) и высотой (y) окна
        
        ---
        
        :Example:
        ```python
        # Получить текущий размер окна
        size = window.get_size()
        print(f"Ширина: {size.x}, Высота: {size.y}")
        ```
        """
        return Vector2i(
            LIB_PYSGL.getWindowSizeWidth(self.__window_ptr),
            LIB_PYSGL.getWindowSizeHeight(self.__window_ptr)
        )
        
    def get_center(self) -> Vector2f:
        """
        #### Возвращает координаты центра окна
        
        ---
        
        :Description:
        - Вычисляет центр относительно клиентской области
        - Возвращает координаты в пикселях
        - Полезно для центрирования элементов
        
        ---
        
        :Returns:
        - Vector2f: Вектор с координатами центра (x, y)
        
        ---
        
        :Example:
        ```python
        # Поместить спрайт в центр окна
        sprite.position = window.get_center()
        ```
        """
        size = self.get_size()
        return Vector2f(
            size.x / 2,
            size.y / 2
        )

    def get_position(self) -> Vector2i:
        """
        #### Возвращает позицию окна на экране
        
        ---
        
        :Description:
        - Координаты относительно верхнего левого угла экрана
        - Учитывает системные рамки окна
        - Позиция в пикселях
        
        ---
        
        :Returns:
        - Vector2i: Вектор с координатами (x, y) верхнего левого угла
        
        ---
        
        :Example:
        ```python
        # Проверить положение окна
        pos = window.get_position()
        print(f"Окно расположено в ({pos.x}, {pos.y})")
        ```
        """
        return Vector2i(
            LIB_PYSGL.getWindowPositionX(self.__window_ptr),
            LIB_PYSGL.getWindowPositionY(self.__window_ptr)
        )

    def view_info(self) -> None:
        """
        #### Отображает отладочную информацию о производительности
        
        ---
        
        :Description:
        - Показывает FPS, время рендеринга и дельта-тайм
        - Включает график изменения FPS за последние кадры
        - Адаптивная прозрачность при наведении курсора
        - Требует включения флага __view_info
        
        ---
        
        :Features:
        - Динамический график FPS с цветовой индикацией
        - Подсветка при наведении в область информации
        - Подробная текстовая статистика
        - Индикатор активности окна
        
        ---
        
        :Note:
        - Для активации установите window.set_view_info()
        - Автоматически использует стандартный View
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
        #### Управляет вертикальной синхронизацией (VSync)
        
        ---
        
        :Description:
        - Синхронизирует частоту кадров с частотой обновления монитора
        - Устраняет артефакты разрыва изображения
        - Может уменьшить нагрузку на GPU
        
        ---
        
        :Args:
        - value (bool): True - включить VSync, False - выключить
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Включить вертикальную синхронизацию
        window.set_vertical_sync(True)
        ```
        """
        self.__vsync = value
        LIB_PYSGL.SetVerticalSync(self.__window_ptr, value)
        return self

    def set_exit_key(self, key: str) -> Self:
        """
        #### Устанавливает клавишу для закрытия окна
        
        ---
        
        :Description:
        - Определяет клавишу, которая будет закрывать окно при нажатии
        - Использует системное отслеживание клавиатуры
        - По умолчанию `esc`
        
        ---
        
        :Args:
        - key (str): Идентификатор клавиши в формате 
                    (например: "esc", "space", "ctrl+c")
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Закрывать окно по Escape
        window.set_exit_key("esc")
        
        # Закрывать по комбинации Ctrl+Q
        window.set_exit_key("ctrl+q")
        ```
        """
        self.__exit_key = key
        return self

    def get_exit_key(self) -> str:
        """
        #### Возвращает текущую клавишу для закрытия окна
        
        ---
        
        :Description:
        - Возвращает None если клавиша не установлена
        - Значение соответствует последнему set_exit_key()
        
        ---
        
        :Returns:
        - str: Текущая установленная клавиша или None
        
        ---
        
        :Example:
        ```python
        if window.get_exit_key() == "esc":
            print("Окно закрывается по Escape")
        ```
        """
        return self.__exit_key
        
    def set_view_info(self, value: bool = True) -> Self:
        """
        #### Управляет отображением отладочной информации
        
        ---
        
        :Description:
        - Включает/выключает панель с FPS и статистикой рендеринга
        - Отображается в верхнем левом углу окна
        - Полезно для отладки производительности
        
        ---
        
        :Args:
        - value (bool): Флаг отображения (True - показать, False - скрыть)
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Показать информацию
        window.set_view_info(True)
        
        # Скрыть информацию
        window.set_view_info(False)
        ```
        """
        self.__view_info = value
        return self

    def get_delta(self) -> float:
        """
        #### Возвращает коэффициент дельта-тайм
        
        ---
        
        :Description:
        - Показывает отношение реального FPS к целевому
        - Значение 1.0 означает идеальное соответствие
        - <1.0 - рендеринг медленнее целевого
        - >1.0 - рендеринг быстрее целевого
        - Используется для нормализации игрового времени
        
        ---
        
        :Returns:
        - float: Коэффициент дельта-тайм
        
        ---
        
        :Example:
        ```python
        # Нормализовать движение относительно FPS
        distance = speed * window.get_delta()
        ```
        """
        return self.__delta

    def set_target_fps(self, fps: int) -> Self:
        """
        #### Устанавливает эталонный FPS для расчетов
        
        ---
        
        :Description:
        - Определяет целевую частоту кадров для расчета delta-time
        - Не ограничивает фактический FPS рендеринга
        - Используется для нормализации игрового времени
        
        ---
        
        :Args:
        - fps (int): Целевые кадры в секунду (>0)
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Установить 60 FPS как эталон для расчетов
        window.set_target_fps(60)
        ```
        """
        self.__target_fps = fps
        return self

    def get_target_fps(self) -> int:
        """
        #### Возвращает текущий эталонный FPS
        
        ---
        
        :Description:
        - Показывает значение, установленное set_target_fps()
        - По умолчанию обычно 60 FPS
        
        ---
        
        :Returns:
        - int: Текущее целевое значение FPS
        
        ---
        
        :Example:
        ```python
        print(f"Эталонная частота: {window.get_target_fps()} FPS")
        ```
        """
        return self.__target_fps

    def set_wait_fps(self, fps: int) -> Self:
        """
        #### Устанавливает ограничение частоты кадров
        
        ---
        
        :Description:
        - Ограничивает максимальный FPS рендеринга
        - Реальное значение может отличаться из-за:
        - Ограничений системы
        - Сложности сцены
        - Нагрузки на GPU/CPU
        
        ---
        
        :Args:
        - fps (int): Максимальные кадры в секунду (FPS_UNLIMIT_CONST = без ограничений)
        - `! Снятие ограничения может привести к перегереву устройства и последующего сбрасывания частот !`
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Ограничить 60 FPS для экономии батареи
        window.set_wait_fps(60)
        
        # Снять ограничение FPS
        window.set_wait_fps(FPS_UNLIMIT_CONST)
        ```
        """
        LIB_PYSGL.setWaitFps(self.__window_ptr, int(fps))
        self.__wait_fps = fps
        return self

    def get_wait_fps(self) -> int:
        """
        #### Возвращает текущее ограничение FPS
        
        ---
        
        :Description:
        - Показывает значение, установленное set_wait_fps()
        - 0 означает отсутствие ограничений
        
        ---
        
        :Returns:
        - int: Текущее ограничение FPS (FPS_UNLIMIT_CONST = без лимита)
        
        ---
        
        :Example:
        ```python
        if window.get_wait_fps() == FPS_UNLIMIT_CONST:
            print("Ограничение FPS отключено")
        ```
        """
        return self.__wait_fps
    
    def get_render_time(self, factor: float = 1) -> float:
        """
        #### Возвращает время рендеринга последнего кадра
        
        ---
        
        :Description:
        - Измеряет только время отрисовки (рендеринг)
        - Не включает время логики и ожидания
        - Полезно для оптимизации производительности
        
        ---
        
        :Args:
        - factor (float): Множитель для преобразования единиц (по умолчанию 1 = секунды)
        
        ---
        
        :Returns:
        - float: Время в секундах (или других единицах при factor != 1)
        
        ---
        
        :Example:
        ```python
        # Получить время в секундах
        render_sec = window.get_render_time()
        
        # Получить время в миллисекундах
        render_ms = window.get_render_time(1000)
        ```
        """
        return self.__render_time * factor

    def get_fps(self) -> float:
        """
        #### Возвращает текущую частоту кадров
        
        ---
        
        :Description:
        - Рассчитывается как среднее за последние N кадров
        - Учитывает только время рендеринга
        - Может колебаться в зависимости от нагрузки
        
        ---
        
        :Returns:
        - float: Текущее значение FPS
        
        ---
        
        :Example:
        ```python
        # Адаптивное качество при падении FPS
        if window.get_fps() < 30:
            decrease_quality()
        ```
        """
        return self.__fps

    def get_global_timer(self, factor: float = 1.0) -> float:
        """
        #### Возвращает время работы приложения
        
        ---
        
        :Description:
        - Отсчет начинается при создании окна
        - Независит от пауз/остановок
        - Полезно для анимаций и таймеров
        
        ---
        
        :Args:
        - factor (float): Множитель времени (1.0 = реальное время)
        
        ---
        
        :Returns:
        - float: Время в секундах × factor
        
        ---
        
        :Example:
        ```python
        # Простое измерение времени
        run_time = window.get_global_timer()
        
        # Ускоренное время для эффектов
        fast_time = window.get_global_timer(2.0)
        ```
        """
        return (time() - self.__start_time) * factor
    
    def set_view(self, view: View) -> Self:
        """
        #### Устанавливает активную камеру/область просмотра
        
        ---
        
        :Description:
        - Определяет систему координат для всех последующих операций отрисовки
        - Влияет на позиционирование, масштабирование и поворот графики
        - По умолчанию используется стандартный View (охватывает все окно)
        
        ---
        
        :Args:
        - view (View): Объект камеры/вида для установки
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        """
        LIB_PYSGL.setView(self.__window_ptr, view.get_ptr())
        return self
        
    def disable(self) -> None:
        """
        #### Деактивирует окно (Windows-only)
        
        ---
        
        :Description:
        - Блокирует ввод и взаимодействие с окном
        - Затемняет заголовок окна (визуальный индикатор неактивности)
        - Автоматически устанавливает флаг __active в False
        
        ---
        
        :Note:
        - Работает только на платформе Windows

        """
        self.__window_descriptor = ctypes.windll.user32.FindWindowW(None, self.__title)
        ctypes.windll.user32.EnableWindow(self.__window_descriptor, False)
        self.__active = False
                
    def enable(self) -> None:
        """
        #### Активирует окно (Windows-only)
        
        ---
        
        :Description:
        - Восстанавливает возможность взаимодействия с окном
        - Возвращает нормальный вид заголовка окна
        - Автоматически устанавливает флаг __active в True
        
        ---
        
        :Note:
        - Работает только на платформе Windows

        """
        self.__window_descriptor = ctypes.windll.user32.FindWindowW(None, self.__title)
        ctypes.windll.user32.EnableWindow(self.__window_descriptor, True)
        self.__active = True
            

    def update(self, events: WindowEvents) -> bool:
        """
        #### Основной метод обновления состояния окна
        
        ---
        
        :Description:
        - Обрабатывает все события окна (ввод, изменение размера и т.д.)
        - Вычисляет метрики производительности (FPS, время рендеринга)
        - Управляет эффектом "призрачности" окна
        - Должен вызываться каждый кадр в основном цикле приложения
        
        ---
        
        :Args:
        - events (WindowEvents): Объект для работы с событиями окна
        
        ---
        
        :Returns:
        - bool: True если окно должно продолжать работу, False если требуется закрытие
        
        ---
        
        :Workflow:
        1. Обновление эффекта "призрачности" (если включен)
        2. Расчет метрик производительности
        3. Обработка событий окна
        4. Проверка условий закрытия
        5. Обновление состояния окна
        """
        
        # Реализация эффекта "призрачности" окна
        if self.__ghosting:
            # Прозрачность зависит от нахождения курсора в окне
            target_alpha = 255 if MouseInterface.in_window(self) else self.__ghosting_min_value
            # Плавное изменение прозрачности
            self.__window_alpha += (target_alpha - self.__window_alpha) * self.__ghosting_interpolation
            self.set_alpha(self.__window_alpha)
        
        # =============================================
        # Расчет метрик производительности
        # =============================================
        
        # Замер времени рендеринга предыдущего кадра
        self.__render_time = self.__clock.get_elapsed_time()
        self.__clock.restart()
        
        # Расчет текущего FPS (с защитой от деления на ноль)
        self.__fps = 1 / self.__render_time if self.__render_time > 0 else 0
        
        # Расчет delta-time (нормализованного времени кадра)
        self.__delta = self.__target_fps / self.__fps if self.__fps > 0 else 1
        
        # Обновление истории FPS для графика производительности
        self.__update_fps_history()
        
        # =============================================
        # Обработка событий окна
        # =============================================
        
        # Опрос событий из системной очереди
        event_type = events.poll(self)
        
        # Проверка условий закрытия окна
        if self.__should_close_window(event_type, events):
            return False
        
        # Обработка изменения размера окна
        if event_type == WindowEvents.Type.Resized:
            self.__handle_window_resize(events)
        
        # Обновление флага изменения размера
        self.__update_resize_status()
        
        return True

    def __update_fps_history(self):
        """
        #### Обновляет историю значений FPS
        
        ---
        :Description:
        - Сохраняет значения FPS для построения графика
        - Обновляется каждые 0.1 секунды
        - Поддерживает ограниченный размер истории
        """
        self.__fps_update_timer += self.__render_time
        if self.__fps_update_timer >= 0.1:
            self.__fps_history.append(self.__fps)
            self.__min_fps_in_fps_history = min(self.__fps_history)
            self.__max_fps_in_fps_history = max(self.__fps_history)
            
            # Ограничение размера истории
            if len(self.__fps_history) > self.__max_history:
                self.__fps_history.pop(0)
                
            self.__fps_update_timer = 0

    def __should_close_window(self, event_type: int, events: WindowEvents) -> bool:
        """
        #### Проверяет условия закрытия окна
        
        ---
        :Args:
        - event_type: Тип последнего события
        - events: Объект событий окна
        
        :Returns:
        - bool: True если окно должно закрыться
        """
        return (event_type == WindowEvents.Type.Closed or 
                keyboard.is_pressed(self.__exit_key))

    def __handle_window_resize(self, events: WindowEvents):
        """
        #### Обрабатывает изменение размера окна
        
        ---
        :Description:
        - Обновляет внутренние размеры окна
        - Корректирует стандартную область просмотра
        """
        self.__width = events.get_size_width()
        self.__height = events.get_size_height()
        
        # Обновление стандартного View под новый размер
        self.__view.set_size(self.__width, self.__height)
        self.__view.set_center(self.__width / 2, self.__height / 2)
        self.set_view(self.__view)

    def __update_resize_status(self):
        """
        #### Обновляет флаг изменения размера окна
        
        ---
        :Description:
        - Сравнивает текущие размеры с предыдущими
        - Устанавливает флаг __resized
        - Сохраняет текущие размеры для следующего сравнения
        """
        self.__resized = (self.__end_height != self.__height or 
                        self.__end_width != self.__width)
        self.__end_height = self.__height
        self.__end_width = self.__width
    
    def get_resized(self) -> bool:
        """
        #### Проверяет изменение размера окна в текущем кадре
        
        ---
        
        :Description:
        - Возвращает True, если в этом кадре произошло изменение размера окна
        - Автоматически сбрасывается при следующем вызове update()
        - Полезно для адаптации интерфейса к новому размеру
        
        ---
        
        :Returns:
        - bool: Флаг изменения размера
        
        ---
        
        :Example:
        ```python
        if window.get_resized():
            # Пересчитать позиции элементов при изменении размера
            resize_ui_elements()
        ```
        """
        return self.__resized
        
    def clear(self, color: Color | None = None) -> None:
        """
        #### Очищает буфер рисования окна
        
        ---
        
        :Description:
        - Заполняет окно указанным цветом
        - Если цвет не указан, используется цвет по умолчанию
        - Должен вызываться перед началом рисования каждого кадра
        
        ---
        
        :Args:
        - color (Color | None): Цвет очистки или None для цвета по умолчанию
        
        ---
        
        :Raises:
        - TypeError: Если передан недопустимый тип цвета
        
        ---
        
        :Example:
        ```python
        # Очистить черным цветом
        window.clear(Color(0, 0, 0))
        
        # Очистить цветом по умолчанию
        window.clear()
        ```
        """
        if isinstance(color, Color):
            LIB_PYSGL.clearWindow(self.__window_ptr, color.r, color.g, color.b, color.a)
        elif color is None:
            LIB_PYSGL.clearWindow(
                self.__window_ptr, 
                self.__clear_color.r, 
                self.__clear_color.g, 
                self.__clear_color.b, 
                self.__clear_color.a
            )
        else:
            raise TypeError(f"Expected Color or None, got {type(color).__name__}")

    def display(self) -> None:
        """
        #### Отображает нарисованное содержимое
        
        ---
        
        :Description:
        - Выводит все нарисованные объекты на экран
        - Выполняет переключение буферов (double buffering)
        - Должен вызываться после завершения рисования кадра
        
        ---
        
        :Note:
        - Все операции рисования между clear() и display() будут показаны одновременно
        
        ---
        
        :Example:
        ```python
        # Стандартный цикл рендеринга
        window.clear()
        # ... рисование объектов ...
        window.display()
        ```
        """
        LIB_PYSGL.displayWindow(self.__window_ptr)

    def set_title(self, title: str) -> Self:
        """
        #### Устанавливает заголовок окна
        
        ---
        
        :Description:
        - Изменяет текст в заголовке окна
        - Поддерживает Unicode символы
        - Влияет на отображение в панели задач и заголовке окна
        
        ---
        
        :Args:
        - title (str): Новый заголовок окна
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Установить заголовок с FPS счетчиком
        window.set_title(f"My Game - {window.get_fps():.0f} FPS")
        ```
        """
        self.__title = title
        LIB_PYSGL.setWindowTitle(self.__window_ptr, title.encode('utf-8'))
        return self
    
    def get_title(self) -> str:
        """
        #### Возвращает текущий заголовок окна
        
        ---
        
        :Description:
        - Возвращает текст, отображаемый в заголовке окна
        - Соответствует последнему значению, установленному через set_title()
        
        ---
        
        :Returns:
        - str: Текущий заголовок окна
        
        ---
        
        :Example:
        ```python
        print(f"Текущий заголовок: {window.get_title()}")
        ```
        """
        return self.__title

    def set_clear_color(self, color: Color) -> Self:
        """
        #### Устанавливает цвет очистки по умолчанию
        
        ---
        
        :Description:
        - Определяет цвет, которым будет заполняться окно при clear()
        - Используется, когда clear() вызывается без параметров
        - Начальное значение обычно черный цвет (0, 0, 0)
        
        ---
        
        :Args:
        - color (Color): Цвет для очистки (должен быть объектом Color)
        
        ---
        
        :Returns:
        - Self: Возвращает self для цепочки вызовов
        
        ---
        
        :Example:
        ```python
        # Установить синий цвет фона
        window.set_clear_color(Color(0, 0, 255))
        ```
        """
        self.__clear_color = color
        return self

    def get_clear_color(self) -> Color:
        """
        #### Возвращает текущий цвет очистки
        
        ---
        
        :Description:
        - Показывает цвет, установленный через set_clear_color()
        - Может отличаться от фактического цвета окна, если используется clear() с параметром
        
        ---
        
        :Returns:
        - Color: Текущий цвет очистки по умолчанию
        
        ---
        
        :Example:
        ```python
        # Проверить текущий цвет фона
        bg_color = window.get_clear_color()
        print(f"Фон: R={bg_color.r}, G={bg_color.g}, B={bg_color.b}")
        ```
        """
        return self.__clear_color
        
    def is_open(self) -> bool:
        """
        #### Проверяет состояние окна
        
        ---
        
        :Description:
        - Возвращает True, если окно создано и не закрыто
        - False означает, что окно было закрыто и больше не может использоваться
        
        ---
        
        :Returns:
        - bool: Состояние окна (открыто/закрыто)
        
        ---
        
        :Example:
        ```python
        # Основной цикл приложения
        while window.is_open():
            if not window.update(events): window.close()
            ... 
        ```
        """
        return LIB_PYSGL.isWindowOpen(self.__window_ptr)
    
    @overload
    def draw(self, shape, render_states: RenderStates) -> None:
        """
        #### Отрисовывает объект с пользовательскими параметрами рендеринга
        
        ---
        
        :Description:
        - Позволяет указать точные параметры отрисовки через RenderStates
        - Поддерживает кастомные трансформации, blending modes и текстуры
        
        ---
        
        :Args:
        - shape (Drawable): Отрисовываемый объект (Shape, Sprite, Text)
        - render_states (RenderStates): Параметры рендеринга
        
        ---
        
        :Example:
        ```python
        states = RenderStates(blend_mode=BlendMode.ADD)
        window.draw(sprite, states)
        ```
        """
        ...

    @overload
    def draw(self, shape, shader: Shader) -> None:
        """
        #### Отрисовывает объект с пользовательским шейдером
        
        ---
        
        :Description:
        - Применяет указанный шейдер к объекту
        - Позволяет создавать сложные визуальные эффекты
        
        ---
        
        :Args:
        - shape (Drawable): Отрисовываемый объект
        - shader (Shader): Шейдер для применения
        
        ---
        
        :Example:
        ```python
        shader = Shader.from_file("blur.frag")
        window.draw(sprite, shader)
        ```
        """
        ...

    @overload 
    def draw(self, shape) -> None:
        """
        #### Отрисовывает объект с параметрами по умолчанию
        
        ---
        
        :Description:
        - Использует стандартные настройки рендеринга
        - Подходит для большинства случаев
        
        ---
        
        :Args:
        - shape (Drawable): Отрисовываемый объект
        
        ---
        
        :Example:
        ```python
        window.draw(sprite)  # Простая отрисовка
        ```
        """
        ...

    def draw(self, shape, render_states: RenderStates | Shader | None = None) -> None:
        """
        #### Основной метод отрисовки объектов
        
        ---
        
        :Description:
        - Поддерживает три режима отрисовки:
            - Стандартный (без параметров)
            - С пользовательскими RenderStates
            - С шейдером
        - Автоматически определяет тип объекта и способ его отрисовки
        
        ---
        
        :Args:
        - shape (Drawable): Объект для отрисовки (должен иметь get_ptr())
        - render_states (RenderStates|Shader|None): Параметры отрисовки
        
        ---
        
        :Workflow:
        1. Проверяет тип объекта (специальный или стандартный)
        2. Для специальных объектов вызывает их метод отрисовки
        3. Для стандартных объектов выбирает подходящий метод C++
        
        ---
        
        :Note:
        - Специальные объекты (LineThin и др.) обрабатываются в Python
        - Стандартные объекты передаются в нативный код
        
        ---
        
        :Example:
        ```python
        # Все три варианта использования:
        window.draw(sprite)  # По умолчанию
        window.draw(sprite, RenderStates(...))
        window.draw(sprite, shader)
        ```
        """
        if not isinstance(shape.get_ptr(), int):
            # Специальные объекты с собственной логикой отрисовки
            shape.special_draw(self)
        else:
            # Стандартные объекты
            if render_states is None:
                LIB_PYSGL.drawWindow(self.__window_ptr, shape.get_ptr())
            elif isinstance(render_states, RenderStates):
                LIB_PYSGL.drawWindowWithStates(
                    self.__window_ptr, 
                    render_states.get_ptr(), 
                    shape.get_ptr()
                )
            elif isinstance(render_states, Shader):
                LIB_PYSGL.drawWindowWithShader(
                    self.__window_ptr,
                    render_states.get_ptr(),
                    shape.get_ptr()
                )

