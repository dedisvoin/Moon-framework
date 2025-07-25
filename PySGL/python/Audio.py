import ctypes
import os

from .Types import *

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

# Тип указателя на звуковой буфер ====== +
SoundBufferPtr = ctypes.c_void_p
# ====================================== +

# Определение типов аргументов и возвращаемых значений для функций DLL
LIB_PYSGL._SoundBuffer_loadFromFile.argtypes = [ctypes.c_char_p]
LIB_PYSGL._SoundBuffer_loadFromFile.restype = SoundBufferPtr
LIB_PYSGL._SoundBuffer_Destroy.argtypes = [SoundBufferPtr]
LIB_PYSGL._SoundBuffer_Destroy.restype = None
LIB_PYSGL._SoundBuffer_GetChannelsCount.argtypes = [SoundBufferPtr]
LIB_PYSGL._SoundBuffer_GetChannelsCount.restype = ctypes.c_int
LIB_PYSGL._SoundBuffer_GetSampleRate.argtypes = [SoundBufferPtr]
LIB_PYSGL._SoundBuffer_GetSampleRate.restype = ctypes.c_int

class SoundBuffer:
    """
    #### Класс для работы со звуковыми буферами
    
    ---
    
    :Description:
    - Загружает и хранит аудиоданные из файлов
    - Предоставляет доступ к параметрам звука
    - Управляет жизненным циклом звукового буфера
    
    ---
    
    :Formats:
    - WAV
    - OGG
    - MP3

    """
    __slots__ = ("__path", "__ptr")

    def __init__(self, path: str) -> Self:
        """
        #### Инициализирует звуковой буфер из файла
        
        ---
        
        :Args:
        - path (str): Путь к файлу с расширением .wav
        
        ---
        
        :Raises:
        - RuntimeError: При ошибке загрузки файла
        
        ---
        
        :Example:
        ```python
        buffer = SoundBuffer("sound.wav")
        ```
        """
        self.__path = path
        self.__ptr: SoundBufferPtr = LIB_PYSGL._SoundBuffer_loadFromFile(path.encode('utf-8'))
        
    def destroy(self) -> None:
        """
        #### Освобождает ресурсы звукового буфера
        
        ---
        
        :Note:
        - Вызывается автоматически при удалении объекта
        """
        LIB_PYSGL._SoundBuffer_Destroy(self.__ptr)
        self.__ptr = None

    def __del__(self) -> None:
        """
        #### Деструктор, освобождающий ресурсы
        
        ---
        
        :Note:
        - Гарантирует корректное удаление нативного объекта
        """
        self.destroy()

    def get_sample_rate(self) -> int:
        """
        #### Возвращает частоту дискретизации звука
        
        ---
        
        :Returns:
        - int: Частота дискретизации в Гц
        
        ---
        
        :Example:
        ```python
        rate = buffer.get_sample_rate()  # 44100
        ```
        """
        return LIB_PYSGL._SoundBuffer_GetSampleRate(self.__ptr)

    def get_ptr(self) -> SoundBufferPtr:
        """
        #### Возвращает указатель на нативный буфер
        
        ---
        
        :Returns:
        - SoundBufferPtr: Указатель на внутренний объект
        
        ---
        
        :Note:
        - Для внутреннего использования в PySGL
        """
        return self.__ptr
    
    def get_channels_count(self) -> int:
        """
        #### Возвращает количество аудиоканалов
        
        ---
        
        :Returns:
        - int: Количество каналов (1 - моно, 2 - стерео)
        
        ---
        
        :Example:
        ```python
        channels = buffer.get_channels_count()  # 2
        ```
        """
        return LIB_PYSGL._SoundBuffer_GetChannelsCount(self.__ptr)
    
    def get_path(self) -> str:
        """
        #### Возвращает путь к исходному файлу
        
        ---
        
        :Returns:
        - str: Путь к файлу, из которого загружен буфер
        """
        return self.__path

# Тип указателя на звук ========= +
SoundPtr = ctypes.c_void_p
# =============================== +

# Определение типов аргументов и возвращаемых значений для функций DLL
LIB_PYSGL._Sound_Create.argtypes = [SoundBufferPtr]
LIB_PYSGL._Sound_Create.restype = SoundPtr
LIB_PYSGL._Sound_Play.argtypes = [SoundPtr]
LIB_PYSGL._Sound_Play.restype = None
LIB_PYSGL._Sound_Pause.argtypes = [SoundPtr]
LIB_PYSGL._Sound_Pause.restype = None
LIB_PYSGL._Sound_Stop.argtypes = [SoundPtr]
LIB_PYSGL._Sound_Stop.restype = None
LIB_PYSGL._Sound_Destroy.argtypes = [SoundPtr]
LIB_PYSGL._Sound_Destroy.restype = None
LIB_PYSGL._Sound_SetLoop.argtypes = [SoundPtr, ctypes.c_bool]
LIB_PYSGL._Sound_SetLoop.restype = None
LIB_PYSGL._Sound_SetVolume.argtypes = [SoundPtr, ctypes.c_float]
LIB_PYSGL._Sound_SetVolume.restype = None
LIB_PYSGL._Sound_SetPitch.argtypes = [SoundPtr, ctypes.c_float]
LIB_PYSGL._Sound_SetPitch.restype = None
LIB_PYSGL._Sound_SetAttenuation.argtypes = [SoundPtr, ctypes.c_float]
LIB_PYSGL._Sound_SetAttenuation.restype = None
LIB_PYSGL._Sound_ResetBuffer.argtypes = [SoundPtr]
LIB_PYSGL._Sound_ResetBuffer.restype = None
LIB_PYSGL._Sound_SetPosition.argtypes = [SoundPtr, ctypes.c_float, ctypes.c_float, ctypes.c_float]
LIB_PYSGL._Sound_SetPosition.restype = None
LIB_PYSGL._Sound_SetRelativeToListener.argtypes = [SoundPtr, ctypes.c_bool]
LIB_PYSGL._Sound_SetRelativeToListener.restype = None
LIB_PYSGL._Sound_GetStatus.argtypes = [SoundPtr]
LIB_PYSGL._Sound_GetStatus.restype = ctypes.c_int

class AudioStatus(Enum):
    """
    #### Перечисление статусов воспроизведения звука
    
    ---
    
    :Values:
    - STOPPED: Звук остановлен
    - PAUSED: Звук приостановлен
    - PLAYING: Звук воспроизводится
    """
    STOPED = auto(0)
    PAUSED = auto()
    PLAYING = auto()

class Sound:
    """
    #### Класс для управления воспроизведением звука
    
    ---
    
    :Description:
    - Контролирует воспроизведение, паузу, остановку звука
    - Позволяет настраивать параметры воспроизведения
    - Поддерживает 3D-позиционирование
    """
    __slots__ = ("__sound_buffer", "__ptr", "__played", "__paused", "__volume", "__pitch", "__attenuation", "__looped", "__id")

    def __init__(self, sound_buffer: SoundBuffer) -> Self:
        """
        #### Инициализирует звук из буфера

        ---

        Есть возможность хеширования.
        
        ---
        
        :Args:
        - sound_buffer (SoundBuffer): Буфер с аудиоданными
        
        ---
        
        :Raises:
        - RuntimeError: При ошибке создания звука
        """
        self.__sound_buffer = sound_buffer

        try:
            self.__ptr: SoundPtr = LIB_PYSGL._Sound_Create(self.__sound_buffer.get_ptr())
        except:
            raise RuntimeError("Failed to create sound")
        
        self.__played: bool = False
        self.__paused: bool = False
        self.__volume: float = 1.0
        self.__pitch: float = 1.0
        self.__attenuation: float = 1.0
        self.__looped: bool = False
        self.__id: Identifier = AutoIdentifier()

    def get_identifier(self) -> Identifier:
        """
        #### Возвращает идентификатор звука

        ---

        :Returns:
        - Identifier: Идентификатор звука

        ---

        :Example:
        ```python
        sound_id = sound.get_identifier()
        ```
        """
        return self.__id

    def __eq__(self, other: "Sound") -> bool:
        """
        #### Сравнивает два звука по идентификатору
        """
        return  self.__id == other.get_identifier()
    
    def __ne__(self, other: "Sound") -> bool:
        """
        #### Сравнивает два звука по идентификатору
        """
        return  self.__id != other.get_identifier()
        
    def __hash__(self) -> int:
        """
        #### Возвращает хэш-код звука
        """
        return hash(self.__id)
    
    def get_path(self) -> str:
        """
        #### Возвращает путь к исходному файлу

        ---

        :Returns:
        - str: Путь к файлу, из которого загружен звук
        """
        return self.__sound_buffer.get_path()

    def get_status(self) -> AudioStatus:
        """
        #### Возвращает текущий статус воспроизведения
        
        ---
        
        :Returns:
        - AudioStatus: Текущее состояние звука
        
        ---
        
        :Example:
        ```python
        if sound.get_status() == AudioStatus.PLAYING:
            print("Sound is playing")
        ```
        """
        return AudioStatus(LIB_PYSGL._Sound_GetStatus(self.__ptr))

    def set_relative_to_listener(self, relative: bool) -> Self:
        """
        #### Устанавливает, будет ли звук воспроизводиться относительно слушателя.

        ---

        :Args:
        - relative (bool): True, если звук должен воспроизводиться относительно слушателя

        ---

        :Returns:
        - self: Для цепных вызовов

        ---

        :Example:
        ```python
        sound.set_relative_to_listener(True)
        ```
        """
        LIB_PYSGL._Sound_SetRelativeToListener(self.__ptr, relative)
        return self

    def set_position(self, x: float, y: float, z: float) -> Self:
        """
        Устанавливает позицию звука в 3D пространстве.

        ---

        :Args:
        - x (float): Координата X
        - y (float): Координата Y 
        - z (float): Координата Z

        ---

        :Returns:
        - self: Для цепных вызовов

        ---

        :Example:
        ```python
        sound.set_position(0, 0, 0) # Устанавливает звук в центр экрана
        ```
        """
        LIB_PYSGL._Sound_SetPosition(self.__ptr, float(x), float(y), float(z))
        return self
    
    def play_left(self) -> Self:
        """
        #### Воспроизводит звук слева от слушателя.

        ---

        :Returns:
        - self: Для цепных вызовов
        """
        self.set_position(-1, 0, 0)
        self.play()
        return self
    
    def play_right(self) -> Self:
        """
        #### Воспроизводит звук справа от слушателя.

        ---

        :Returns:
        - self: Для цепных вызовов
        """
        self.set_position(1, 0, 0)
        self.play()
        return self

    def copy(self) -> "Sound":
        """
        #### Создает копию текущего звука с теми же параметрами.

        ---

        :Returns:
            Sound: Новая копия звука

        ---

        :Example:
        ```python
        sound_buffer = SoundBuffer("path/to/sound.wav")
        sound = Sound(sound_buffer)
        sound_copy = sound.copy()
        ```
        """
        sound = Sound(self.__sound_buffer)
        sound.set_attenuation(self.__attenuation)
        sound.set_pitch(self.__pitch)
        sound.set_volume(self.__volume)
        sound.set_loop(self.__looped)
        return sound

    def get_ptr(self) -> SoundPtr:
        """
        #### Возвращает указатель на звук.

        ---

        :Returns:
        - SoundPtr: Указатель на звук

        ---

        :Example:
        ```python
        sound_ptr = sound.get_ptr()
        print(sound_ptr) # Выведет адрес звука в памяти
        ```
        """
        return self.__ptr
    
    def get_sound_buffer(self) -> SoundBuffer:
        """
        #### Возвращает звуковой буфер.

        ---

        :Returns:
        - SoundBuffer: Звуковый буфер

        ---

        :Example:
        ```python
        sound_buffer = sound.get_sound_buffer()
        print(sound_buffer) # Выведет звуковый буфер
        ```
        """
        return self.__sound_buffer
    
    def play(self) -> Self:
        """
        #### Начинает воспроизведение звука.

        ---

        :Returns:
        - self: Для цепных вызовов

        ---

        :Example:
        ```python
        sound = Sound(SoundBuffer("path/to/sound.wav"))
        sound.play()
        ```
        """
        self.__played = True
        self.__paused = False
        LIB_PYSGL._Sound_Play(self.__ptr)
        return self
    
    def pause(self) -> Self:
        """
        #### Приостанавливает воспроизведение звука.

        :Returns:
        - self: Для цепных вызовов
        """
        self.__paused = True
        LIB_PYSGL._Sound_Pause(self.__ptr)
        return self
    
    def stop(self) -> Self:
        """
        #### Останавливает воспроизведение звука.

        :Returns:
        - self: Для цепных вызовов
        """
        self.__played = False
        LIB_PYSGL._Sound_Stop(self.__ptr)
        return self
    
    def is_playing(self) -> bool:
        """
        #### Проверяет, воспроизводится ли звук.

        ---

        :Returns:
            bool: True если звук воспроизводится

        ---

        :Example:
        ```python
        if sound.is_playing():
            print("Sound is playing")
        ```
        """
        return self.__played
    
    def is_paused(self) -> bool:
        """
        #### Проверяет, приостановлен ли звук.

        ---

        :Returns:
        - bool: True если звук приостановлен
        """
        return self.__paused
    
    def set_loop(self, loop: bool) -> Self:
        """
        #### Устанавливает зацикливание звука.

        ---

        :Args:
        - loop (bool): True для зацикливания

        :Returns:
        - self: Для цепных вызовов

        ---

        :Example:
        ```python
        sound.set_loop(True)
        ```
        """
        self.__looped = loop
        LIB_PYSGL._Sound_SetLoop(self.__ptr, loop)
        return self

    def get_loop(self) -> bool:
        """
        #### Проверяет, зациклен ли звук.

        ---

        :Returns:
            bool: True если звук зациклен

        ---

        :Example:
        ```python
        if sound.get_loop():
            print("Sound is looped")
        ```
        """
        return self.__looped

    def set_volume(self, volume: float) -> Self:
        """
        #### Устанавливает громкость звука.

        ---

        :Args:
        - volume (float): Громкость (0.0 - infinity)

        Чем больше число тем громче звук, зависит на сколько мощные динамики у вас

        :Returns:
        - self: Для цепных вызовов
        """
        self.__volume = volume
        LIB_PYSGL._Sound_SetVolume(self.__ptr, volume)
        return self
    
    def get_volume(self) -> float:
        """
        #### Возвращает текущую громкость звука.

        ---

        :Returns:
        - float: Текущая громкость
        """
        return self.__volume
    
    def set_pitch(self, pitch: float) -> Self:
        """
        #### Устанавливает высоту тона звука.

        ---

        :Args:
        - pitch (float): Высота тона (0.0 - 1.0)
        
        :Returns:
        - self: Для цепных вызовов
        """
        self.__pitch = pitch
        LIB_PYSGL._Sound_SetPitch(self.__ptr, pitch)
        return self
    
    def get_pitch(self) -> float:
        """
        #### Возвращает текущую высоту тона звука.

        :Returns:
        - float: Текущая высота тона
        """
        return self.__pitch
    
    def set_attenuation(self, attenuation: float) -> Self:
        """
        #### Устанавливает затухание звука.

        ---

        :Args:
        - attenuation (float): Коэффициент затухания (0.0 - 1.0)

        :Returns:
        - self: Для цепных вызовов
        """
        self.__attenuation = attenuation
        LIB_PYSGL._Sound_SetAttenuation(self.__ptr, attenuation)
        return self
    
    def get_attenuation(self) -> float:
        """
        #### Возвращает текущее затухание звука.

        ---

        :Returns:
        - float: Текущее затухание
        """
        return self.__attenuation
    
    def destroy(self) -> None:
        """
        #### Освобождает ресурсы звука.
        """
        LIB_PYSGL._Sound_Destroy(self.__ptr)
        self.__ptr = None

    def __del__(self) -> None:
        """
        #### Деструктор, освобождающий ресурсы.
        """
        self.destroy()

    def reset(self) -> Self:
        """
        #### Сбрасывает звук в начальное состояние.

        --- 

        :Returns:
            self: Для цепных вызовов
        """
        LIB_PYSGL._Sound_ResetBuffer(self.__ptr)
        return self

class SoundEventListener:
    """
    #### Обработчик событий состояния звука
    
    ---
    
    :Description:
    - Отслеживает изменения состояния воспроизведения звука
    - Позволяет назначить callback-функции на события
    - Требует регулярного вызова update() в основном цикле
    
    ---
    
    :Events:
    - play: Начало воспроизведения
    - pause: Приостановка воспроизведения
    - stop: Остановка воспроизведения
    """
    __slots__ = ("__sound", "__last_status", "__on_play", "__on_pause", "__on_stop", 
                "__played", "__paused", "__stopped")

    def __init__(self, sound: Sound) -> None:
        """
        #### Инициализирует обработчик событий для звука
        
        ---
        
        :Args:
        - sound (Sound): Звуковой объект для отслеживания
        
        ---
        
        :Example:
        ```python
        listener = SoundEventListener(sound)
        ```
        """
        self.__sound: Sound = sound
        self.__last_status: AudioStatus = AudioStatus.STOPPED
        
        # Callback-функции
        self.__on_play: Optional[Callable[[], None]] = None
        self.__on_pause: Optional[Callable[[], None]] = None
        self.__on_stop: Optional[Callable[[], None]] = None

        # Флаги событий
        self.__played: bool = False
        self.__paused: bool = False
        self.__stopped: bool = False

    def get_event(self, type: Literal['play', 'stop', 'pause'] = 'play') -> bool:
        """
        #### Проверяет наличие события указанного типа
        
        ---
        
        :Args:
        - type (str): Тип события ('play', 'stop', 'pause')
        
        ---
        
        :Returns:
        - bool: True если событие произошло
        
        ---
        
        :Raises:
        - ValueError: При передаче недопустимого типа события
        
        ---
        
        :Example:
        ```python
        if listener.get_event('play'):
            print("Sound started playing")
        ```
        """
        match type:
            case 'play':
                return self.__played
            case 'pause':
                return self.__paused
            case 'stop':
                return self.__stopped
            case _:
                raise ValueError(f"Invalid event type: {type}")

    def _update_statuses(self) -> None:
        """
        #### Сбрасывает флаги событий
        
        ---
        
        :Note:
        - Внутренний метод, вызывается перед проверкой состояния
        """
        self.__played = False
        self.__paused = False
        self.__stopped = False

    def set_on_play(self, callback: Callable[[], None]) -> Self:
        """
        #### Устанавливает обработчик начала воспроизведения
        
        ---
        
        :Args:
        - callback (Callable[[], None]): Функция без параметров
        
        ---
        
        :Returns:
        - self: Для цепных вызовов
        
        ---
        
        :Example:
        ```python
        listener.set_on_play(lambda: print("Playback started"))
        ```
        """
        self.__on_play = callback
        return self

    def set_on_pause(self, callback: Callable[[], None]) -> Self:
        """
        #### Устанавливает обработчик паузы
        
        ---
        
        :Args:
        - callback (Callable[[], None]): Функция без параметров
        
        ---
        
        :Returns:
        - self: Для цепных вызовов
        """
        self.__on_pause = callback
        return self

    def set_on_stop(self, callback: Callable[[], None]) -> Self:
        """
        #### Устанавливает обработчик остановки
        
        ---
        
        :Args:
        - callback (Callable[[], None]): Функция без параметров
        
        ---
        
        :Returns:
        - self: Для цепных вызовов
        """
        self.__on_stop = callback
        return self

    def update(self) -> None:
        """
        #### Проверяет состояние звука и вызывает обработчики
        
        ---
        
        :Note:
        - Должен вызываться регулярно (например, в основном цикле приложения)
        - Автоматически определяет изменение состояния звука
        
        ---
        
        :Example:
        ```python
        while True:
            listener.update()
            # Другая логика...
        ```
        """
        current_status = self.__sound.get_status()
        self._update_statuses()
        
        if current_status == self.__last_status:
            return
            
        if current_status == AudioStatus.PLAYING:
            if self.__on_play is not None:
                self.__on_play()
            self.__played = True
                
        elif current_status == AudioStatus.PAUSED:
            if self.__on_pause is not None:
                self.__on_pause()
            self.__paused = True
                
        elif current_status == AudioStatus.STOPPED:
            if self.__on_stop is not None:
                self.__on_stop()
            self.__stopped = True
                
        self.__last_status = current_status

    def get_last_status(self) -> AudioStatus:
        """
        #### Возвращает последнее зафиксированное состояние
        
        ---
        
        :Returns:
        - AudioStatus: Текущий статус воспроизведения
        
        ---
        
        :Example:
        ```python
        status = listener.get_last_status()
        ```
        """
        return self.__last_status

class MultiSound:
    """
    Класс для одновременного воспроизведения нескольких экземпляров одного звука.
    Позволяет воспроизводить один звук многократно без перекрытия предыдущих воспроизведений.
    """
    
    def __init__(self, sound: Sound, number_of_channels: int = 3) -> Self:
        """
        Инициализирует мультизвук. Позволяет многоканально воспроизводить один звук.

        Аргументы:
            sound (Sound): Исходный звук для копирования
            number_of_channels (int): Количество звуковых каналов (по умолчанию 3)
        """
        if number_of_channels < 1:
            raise ValueError("Number of channels must be at least 1")

        self.__original_sound: Sound = sound
        self.__number_of_channels: int = number_of_channels
        self.__sounds: list[Sound] = [sound.copy() for _ in range(self.__number_of_channels)]
        self.__current_sound: int = 0
        self.__position: tuple[float, float, float] = (0, 0, 0)

    def auto_play(self) -> None:
        """
        Воспроизводит текущий звук.
        """
        self.__sounds[self.__current_sound].play()
        self.__current_sound = (self.__current_sound + 1) % self.__number_of_channels

    # //////////////////////////////////////////////////////////////////////////////////////////
    # Методы по отдельности для удобства контроля воспроизведения
    # //////////////////////////////////////////////////////////////////////////////////////////
    def play(self) -> None:
        """
        Воспроизводит текущий звук.
        """
        self.__sounds[self.__current_sound].play()

    def next(self) -> None:
        """
        Переключает на следующий звук.
        """
        self.__current_sound = (self.__current_sound + 1) % self.__number_of_channels

    # //////////////////////////////////////////////////////////////////////////////////////////

    def stop(self) -> None:
        """
        Останавливает текущий звук.
        """
        self.__sounds[self.__current_sound].stop()

    def pause(self) -> None:
        """
        Приостанавливает текущий звук.
        """
        self.__sounds[self.__current_sound].pause()

    def stop_all(self) -> None:
        """
        Останавливает все звуки.
        """
        for sound in self.__sounds:
            sound.stop()

    def pause_all(self) -> None:
        """
        Приостанавливает все звуки.
        """
        for sound in self.__sounds:
            sound.pause()

    def add_chanel(self) -> None:
        """
        Добавляет новый канал для воспроизведения.
        """
        self.__sounds.append(self.__original_sound.copy())
        self.__number_of_channels += 1

    def remove_chanel(self, index: int) -> None:
        """
        Удаляет канал по индексу.
        Аргументы:
            index (int): Индекс канала для удаления
        """
        if index >= self.__number_of_channels:
            raise ValueError("Invalid channel index")
        del self.__sounds[index]
        self.__number_of_channels -= 1

    def set_position_all(self, x: float, y: float, z: float) -> None:
        """
        Устанавливает позицию для всех звуков.
        """
        self.__position = (x, y, z)
        for sound in self.__sounds:
            sound.set_position(x, y, z)

    def get_position_all(self) -> tuple[float, float, float]:
        """
        Возвращает позицию для всех звуков.
        """
        return self.__position

    def set_position_current(self, x: float, y: float, z: float) -> None:
        """
        Устанавливает позицию текущего звука.
        """
        self.__sounds[self.__current_sound].set_position(x, y, z)

    def set_position_at(self, index: int, x: float, y: float, z: float) -> None:
        """
        Устанавливает позицию звука по индексу.
        Аргументы:
            index (int): Индекс звука
            x (float): Координата X
            y (float): Координата Y
            z (float): Координата Z
        """
        if index >= self.__number_of_channels:
            raise ValueError("Invalid channel index")
        self.__sounds[index].set_position(x, y, z)

    def set_volume_all(self, volume: float) -> None:
        """
        Устанавливает громкость всех звуков.
        """
        for sound in self.__sounds:
            sound.set_volume(volume)

    def set_volume_current(self, volume: float) -> None:
        """
        Устанавливает громкость текущего звука.
        """
        self.__sounds[self.__current_sound].set_volume(volume)

    def set_volume_at(self, index: int, volume: float) -> None:
        """
        Устанавливает громкость звука по индексу.
        Аргументы:
            index (int): Индекс звука
            volume (float): Громкость
        """
        if index >= self.__number_of_channels:
            raise ValueError("Invalid channel index")
        self.__sounds[index].set_volume(volume)

    def set_loop_all(self, loop: bool) -> None:
        """
        Устанавливает цикличность всех звуков.
        """
        for sound in self.__sounds:
            sound.set_loop(loop)

    def set_loop_current(self, loop: bool) -> None:
        """
        Устанавливает цикличность текущего звука.
        """
        self.__sounds[self.__current_sound].set_loop(loop)

    def set_loop_at(self, index: int, loop: bool) -> None:
        """
        Устанавливает цикличность звука по индексу.
        Аргументы:
            index (int): Индекс звука
            loop (bool): Флаг цикличности
        """
        if index >= self.__number_of_channels:
            raise ValueError("Invalid channel index")
        self.__sounds[index].set_loop(loop)

    def set_pitch_all(self, pitch: float) -> None:
        """
        Устанавливает высоту тона всех звуков.
        """
        for sound in self.__sounds:
            sound.set_pitch(pitch)

    def set_pitch_current(self, pitch: float) -> None:
        """
        Устанавливает высоту тона текущего звука.
        """
        self.__sounds[self.__current_sound].set_pitch(pitch)

    def set_pitch_at(self, index: int, pitch: float) -> None:
        """
        Устанавливает высоту тона звука по индексу.
        Аргументы:
            index (int): Индекс звука
            pitch (float): Высота тона
        """
        if index >= self.__number_of_channels:
            raise ValueError("Invalid channel index")
        self.__sounds[index].set_pitch(pitch)

    def get_current_sound(self) -> Sound:
        """
        Возвращает текущий звук.
        """
        return self.__sounds[self.__current_sound]
    
    def get_current_sound_index(self) -> int:
        """
        Возвращает индекс текущего звука.
        """
        return self.__current_sound
    
    def get_number_of_channels(self) -> int:
        """
        Возвращает количество каналов.
        """
        return self.__number_of_channels
    
    def get_original_sound(self) -> Sound:
        """
        Возвращает исходный звук.
        """
        return self.__original_sound
    
    def get_sound(self, index: int) -> Sound:
        """
        Возвращает звук по индексу.
        """
        if index >= self.__number_of_channels:
            raise ValueError("Invalid channel index")
        return self.__sounds[index]
    
    def get_sounds(self) -> list[Sound]:
        """
        Возвращает список звуков.
        """
        return self.__sounds
    