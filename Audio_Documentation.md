# Документация модуля Audio

## Обзор

Модуль `Audio` предоставляет комплексную систему работы со звуком в библиотеке PySGL. Он обеспечивает полный набор инструментов для загрузки, управления и воспроизведения аудиоконтента с поддержкой 3D позиционирования и многоканального воспроизведения.

**Версия:** 1.0.6  
**Автор:** Павлов Иван (Pavlov Ivan)  
**Лицензия:** MIT  
**Реализация:** 99%

## Основные возможности

- ✅ **Полноценная система аудио** - загрузка и управление звуковыми буферами, поддержка WAV/OGG/MP3
- ✅ **Расширенные возможности** - 3D позиционирование звука, многоканальное воспроизведение
- ✅ **Гибкая система событий** - отслеживание состояния воспроизведения с callback-функциями
- ✅ **Оптимизированная работа** - минимальные задержки, эффективное использование ресурсов
- ✅ **Готовые интерфейсы** - SoundBuffer, Sound, MultiSound, SoundEventListener

## Требования

- Python 3.8+
- Библиотека `ctypes` (для работы с DLL)
- PySGL.dll (нативная аудио библиотека)

---

## Исключения

### LibraryLoadError
```python
class LibraryLoadError(Exception)
```
**Описание:** Ошибка загрузки нативной библиотеки PySGL.dll.

---

## Перечисления

### AudioStatus
```python
class AudioStatus(Enum):
    STOPPED = 0   # Звук остановлен
    PAUSED = 1    # Звук приостановлен
    PLAYING = 2   # Звук воспроизводится
```
**Описание:** Перечисление статусов воспроизведения звука для контроля состояния аудиообъектов.

---

## Класс SoundBuffer

Основной класс для работы со звуковыми буферами, обеспечивающий загрузку и хранение аудиоданных.

### Конструктор
```python
def __init__(self, path: str) -> Self
```
**Описание:** Инициализирует звуковой буфер из файла с автоматическим определением формата.

**Параметры:**
- `path` - путь к аудиофайлу (поддерживаются форматы WAV, OGG, MP3)

**Исключения:**
- `RuntimeError` - при ошибке загрузки файла или неподдерживаемом формате

**Пример:**
```python
buffer = SoundBuffer("sounds/explosion.wav")
music_buffer = SoundBuffer("music/background.ogg")
```

---

### Методы SoundBuffer

#### get_sample_rate()
```python
def get_sample_rate(self) -> int
```
**Описание:** Возвращает частоту дискретизации звука в герцах.

**Возвращает:** Частота дискретизации (обычно 44100, 48000 Гц)

**Пример:**
```python
rate = buffer.get_sample_rate()  # 44100
print(f"Sample rate: {rate} Hz")
```

---

#### get_channels_count()
```python
def get_channels_count(self) -> int
```
**Описание:** Возвращает количество аудиоканалов в буфере.

**Возвращает:** Количество каналов (1 - моно, 2 - стерео)

**Пример:**
```python
channels = buffer.get_channels_count()  # 2 для стерео
if channels == 1:
    print("Mono audio")
elif channels == 2:
    print("Stereo audio")
```

---

#### get_path()
```python
def get_path(self) -> str
```
**Описание:** Возвращает путь к исходному файлу, из которого был загружен буфер.

**Возвращает:** Строка с путем к файлу

---

#### get_ptr()
```python
def get_ptr(self) -> SoundBufferPtr
```
**Описание:** Возвращает указатель на нативный буфер для внутреннего использования в PySGL.

**Возвращает:** Указатель на внутренний объект

> **⚠️ Внимание:** Метод предназначен для внутреннего использования библиотекой.

---

#### destroy()
```python
def destroy(self) -> None
```
**Описание:** Освобождает ресурсы звукового буфера.

> **💡 Примечание:** Вызывается автоматически при удалении объекта через деструктор.

---

## Класс Sound

Основной класс для управления воспроизведением звука с полным контролем параметров воспроизведения.

### Конструктор
```python
def __init__(self, sound_buffer: SoundBuffer) -> Self
```
**Описание:** Инициализирует звук из буфера с возможностью хеширования для использования в коллекциях.

**Параметры:**
- `sound_buffer` - буфер с аудиоданными

**Исключения:**
- `RuntimeError` - при ошибке создания звука

**Пример:**
```python
buffer = SoundBuffer("sound.wav")
sound = Sound(buffer)
```

---

### Методы управления воспроизведением

#### play()
```python
def play(self) -> Self
```
**Описание:** Начинает воспроизведение звука с текущей позиции.

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
sound.play()
# Или в цепочке
sound.set_volume(0.8).play()
```

---

#### pause()
```python
def pause(self) -> Self
```
**Описание:** Приостанавливает воспроизведение звука с сохранением текущей позиции.

**Возвращает:** Текущий объект для цепочки вызовов

---

#### stop()
```python
def stop(self) -> Self
```
**Описание:** Останавливает воспроизведение звука и сбрасывает позицию в начало.

**Возвращает:** Текущий объект для цепочки вызовов

---

#### reset()
```python
def reset(self) -> Self
```
**Описание:** Сбрасывает звук в начальное состояние без остановки воспроизведения.

**Возвращает:** Текущий объект для цепочки вызовов

---

### Методы проверки состояния

#### get_status()
```python
def get_status(self) -> AudioStatus
```
**Описание:** Возвращает текущий статус воспроизведения звука.

**Возвращает:** Элемент перечисления `AudioStatus`

**Пример:**
```python
if sound.get_status() == AudioStatus.PLAYING:
    print("Sound is currently playing")
elif sound.get_status() == AudioStatus.PAUSED:
    print("Sound is paused")
```

---

#### is_playing()
```python
def is_playing(self) -> bool
```
**Описание:** Проверяет, воспроизводится ли звук в данный момент.

**Возвращает:** `True` если звук воспроизводится

**Пример:**
```python
if sound.is_playing():
    print("Audio is active")
```

---

#### is_paused()
```python
def is_paused(self) -> bool
```
**Описание:** Проверяет, приостановлен ли звук.

**Возвращает:** `True` если звук приостановлен

---

### Методы настройки параметров

#### set_volume()
```python
def set_volume(self, volume: float) -> Self
```
**Описание:** Устанавливает громкость звука.

**Параметры:**
- `volume` - уровень громкости (0.0 - бесконечность, зависит от мощности динамиков)

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
sound.set_volume(0.5)  # 50% громкости
sound.set_volume(1.5)  # 150% громкости (усиление)
```

---

#### get_volume()
```python
def get_volume(self) -> float
```
**Описание:** Возвращает текущую громкость звука.

**Возвращает:** Текущий уровень громкости

---

#### set_pitch()
```python
def set_pitch(self, pitch: float) -> Self
```
**Описание:** Устанавливает высоту тона звука, влияя на скорость воспроизведения.

**Параметры:**
- `pitch` - высота тона (0.0-1.0, где 1.0 - нормальная высота)

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
sound.set_pitch(0.5)  # Низкий тон, медленное воспроизведение
sound.set_pitch(2.0)  # Высокий тон, быстрое воспроизведение
```

---

#### get_pitch()
```python
def get_pitch(self) -> float
```
**Описание:** Возвращает текущую высоту тона звука.

**Возвращает:** Текущая высота тона

---

#### set_loop()
```python
def set_loop(self, loop: bool) -> Self
```
**Описание:** Устанавливает зацикливание звука.

**Параметры:**
- `loop` - флаг зацикливания (`True` для бесконечного повтора)

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
background_music.set_loop(True).play()  # Фоновая музыка на повторе
```

---

#### get_loop()
```python
def get_loop(self) -> bool
```
**Описание:** Проверяет, зациклен ли звук.

**Возвращает:** `True` если звук зациклен

---

#### set_attenuation()
```python
def set_attenuation(self, attenuation: float) -> Self
```
**Описание:** Устанавливает коэффициент затухания звука с расстоянием.

**Параметры:**
- `attenuation` - коэффициент затухания (0.0-1.0)

**Возвращает:** Текущий объект для цепочки вызовов

> **🎯 Применение:** Полезно для 3D звука, где громкость зависит от расстояния до источника.

---

#### get_attenuation()
```python
def get_attenuation(self) -> float
```
**Описание:** Возвращает текущий коэффициент затухания звука.

**Возвращает:** Текущий коэффициент затухания

---

### Методы 3D позиционирования

#### set_position()
```python
def set_position(self, x: float, y: float, z: float) -> Self
```
**Описание:** Устанавливает позицию звука в 3D пространстве для пространственного аудио.

**Параметры:**
- `x` - координата X в 3D пространстве
- `y` - координата Y в 3D пространстве
- `z` - координата Z в 3D пространстве

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
sound.set_position(0, 0, 0)    # Центр
sound.set_position(-5, 0, 0)   # Слева от слушателя
sound.set_position(5, 0, 0)    # Справа от слушателя
```

---

#### set_relative_to_listener()
```python
def set_relative_to_listener(self, relative: bool) -> Self
```
**Описание:** Устанавливает, будет ли звук воспроизводиться относительно позиции слушателя.

**Параметры:**
- `relative` - флаг относительности (`True` для привязки к слушателю)

**Возвращает:** Текущий объект для цепочки вызовов

---

#### play_left()
```python
def play_left(self) -> Self
```
**Описание:** Воспроизводит звук слева от слушателя (быстрый способ).

**Возвращает:** Текущий объект для цепочки вызовов

---

#### play_right()
```python
def play_right(self) -> Self
```
**Описание:** Воспроизводит звук справа от слушателя (быстрый способ).

**Возвращает:** Текущий объект для цепочки вызовов

---

### Служебные методы

#### copy()
```python
def copy(self) -> "Sound"
```
**Описание:** Создает копию текущего звука с теми же параметрами.

**Возвращает:** Новый объект `Sound` с идентичными настройками

**Пример:**
```python
original = Sound(buffer).set_volume(0.8).set_pitch(1.2)
copy = original.copy()  # Копия со всеми настройками
```

---

#### get_identifier()
```python
def get_identifier(self) -> Identifier
```
**Описание:** Возвращает уникальный идентификатор звука для хеширования и сравнения.

**Возвращает:** Объект `Identifier`

---

#### get_path()
```python
def get_path(self) -> str
```
**Описание:** Возвращает путь к исходному файлу звука.

**Возвращает:** Строка с путем к файлу

---

## Класс SoundEventListener

Продвинутый обработчик событий состояния звука с поддержкой callback-функций.

### Конструктор
```python
def __init__(self, sound: Sound) -> None
```
**Описание:** Инициализирует обработчик событий для отслеживания изменений состояния звука.

**Параметры:**
- `sound` - звуковой объект для отслеживания

**Пример:**
```python
listener = SoundEventListener(sound)
```

---

### Методы SoundEventListener

#### set_on_play()
```python
def set_on_play(self, callback: Callable[[], None]) -> Self
```
**Описание:** Устанавливает обработчик события начала воспроизведения.

**Параметры:**
- `callback` - функция без параметров, вызываемая при начале воспроизведения

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
listener.set_on_play(lambda: print("Playback started"))
```

---

#### set_on_pause()
```python
def set_on_pause(self, callback: Callable[[], None]) -> Self
```
**Описание:** Устанавливает обработчик события паузы.

**Параметры:**
- `callback` - функция без параметров, вызываемая при паузе

**Возвращает:** Текущий объект для цепочки вызовов

---

#### set_on_stop()
```python
def set_on_stop(self, callback: Callable[[], None]) -> Self
```
**Описание:** Устанавливает обработчик события остановки.

**Параметры:**
- `callback` - функция без параметров, вызываемая при остановке

**Возвращает:** Текущий объект для цепочки вызовов

---

#### get_event()
```python
def get_event(self, type: Literal['play', 'stop', 'pause'] = 'play') -> bool
```
**Описание:** Проверяет наличие события указанного типа в текущем кадре.

**Параметры:**
- `type` - тип события для проверки ('play', 'stop', 'pause')

**Возвращает:** `True` если событие произошло

**Исключения:**
- `ValueError` - при передаче недопустимого типа события

**Пример:**
```python
if listener.get_event('play'):
    print("Sound just started playing")
```

---

#### update()
```python
def update(self) -> None
```
**Описание:** Проверяет состояние звука и вызывает соответствующие обработчики событий.

> **⚠️ Критично:** Должен вызываться регулярно (каждый кадр) для корректной работы системы событий.

**Пример:**
```python
# В основном игровом цикле
while running:
    listener.update()  # Обязательно!
    # Остальная логика...
```

---

#### get_last_status()
```python
def get_last_status(self) -> AudioStatus
```
**Описание:** Возвращает последнее зафиксированное состояние звука.

**Возвращает:** Элемент перечисления `AudioStatus`

---

## Класс MultiSound

Класс для одновременного воспроизведения нескольких экземпляров одного звука без перекрытия.

### Конструктор
```python
def __init__(self, sound: Sound, number_of_channels: int = 3) -> Self
```
**Описание:** Инициализирует мультизвук с указанным количеством каналов воспроизведения.

**Параметры:**
- `sound` - исходный звук для копирования
- `number_of_channels` - количество звуковых каналов (по умолчанию 3)

**Исключения:**
- `ValueError` - если количество каналов меньше 1

**Пример:**
```python
# Создание мультизвука для частых звуков (выстрелы, шаги)
gunshot = MultiSound(Sound(SoundBuffer("gunshot.wav")), 5)
```

---

### Методы управления воспроизведением

#### auto_play()
```python
def auto_play(self) -> Self
```
**Описание:** Автоматически воспроизводит звук и переключается на следующий канал.

**Возвращает:** Текущий объект для цепочки вызовов

> **🎯 Применение:** Идеально для частых звуков, которые должны накладываться друг на друга.

**Пример:**
```python
# В игровом цикле при стрельбе
if player.shooting:
    gunshot.auto_play()  # Каждый выстрел на новом канале
```

---

#### play()
```python
def play(self) -> Self
```
**Описание:** Воспроизводит звук на текущем канале без автоматического переключения.

**Возвращает:** Текущий объект для цепочки вызовов

---

#### next()
```python
def next(self) -> Self
```
**Описание:** Переключает на следующий звуковой канал без воспроизведения.

**Возвращает:** Текущий объект для цепочки вызовов

---

#### stop() / pause()
```python
def stop(self) -> Self
def pause(self) -> Self
```
**Описание:** Останавливает/приостанавливает только текущий активный канал.

**Возвращает:** Текущий объект для цепочки вызовов

---

#### stop_all() / pause_all()
```python
def stop_all(self) -> Self
def pause_all(self) -> Self
```
**Описание:** Останавливает/приостанавливает все каналы одновременно.

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
# Остановка всех звуков при паузе игры
all_sounds.stop_all()
```

---

### Методы управления каналами

#### add_chanel()
```python
def add_chanel(self, count: int = 1) -> Self
```
**Описание:** Добавляет новые каналы для воспроизведения.

**Параметры:**
- `count` - количество добавляемых каналов (по умолчанию 1)

**Возвращает:** Текущий объект для цепочки вызовов

---

#### remove_chanel()
```python
def remove_chanel(self, index: int) -> Self
```
**Описание:** Удаляет канал по указанному индексу.

**Параметры:**
- `index` - индекс канала для удаления (начиная с 0)

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `ValueError` - если указан недопустимый индекс

---

### Методы настройки параметров

#### set_volume_all() / set_volume_current() / set_volume_at()
```python
def set_volume_all(self, volume: float) -> Self
def set_volume_current(self, volume: float) -> None
def set_volume_at(self, index: int, volume: float) -> None
```
**Описание:** Устанавливает громкость для всех каналов/текущего канала/конкретного канала.

**Параметры:**
- `volume` - уровень громкости (0.0-1.0)
- `index` - индекс канала (только для `set_volume_at`)

**Исключения:**
- `ValueError` - если указан недопустимый индекс (только для `set_volume_at`)

---

#### set_pitch_all() / set_pitch_current() / set_pitch_at()
```python
def set_pitch_all(self, pitch: float) -> None
def set_pitch_current(self, pitch: float) -> None
def set_pitch_at(self, index: int, pitch: float) -> None
```
**Описание:** Устанавливает высоту тона для всех каналов/текущего канала/конкретного канала.

**Параметры:**
- `pitch` - высота тона (1.0 - нормальная)
- `index` - индекс канала (только для `set_pitch_at`)

---

#### set_loop_all() / set_loop_current() / set_loop_at()
```python
def set_loop_all(self, loop: bool) -> None
def set_loop_current(self, loop: bool) -> None
def set_loop_at(self, index: int, loop: bool) -> None
```
**Описание:** Устанавливает цикличность воспроизведения для всех каналов/текущего канала/конкретного канала.

**Параметры:**
- `loop` - флаг цикличности (`True` - зациклить)
- `index` - индекс канала (только для `set_loop_at`)

---

### Методы 3D позиционирования

#### set_position_all()
```python
def set_position_all(self, x: float, y: float, z: float) -> None
```
**Описание:** Устанавливает позицию для всех звуков в 3D пространстве.

**Параметры:**
- `x`, `y`, `z` - координаты в 3D пространстве

---

#### set_position_current() / set_position_at()
```python
def set_position_current(self, x: float, y: float, z: float) -> None
def set_position_at(self, index: int, x: float, y: float, z: float) -> None
```
**Описание:** Устанавливает позицию для текущего канала/конкретного канала.

**Параметры:**
- `x`, `y`, `z` - координаты в 3D пространстве
- `index` - индекс канала (только для `set_position_at`)

---

### Методы получения информации

#### get_current_sound() / get_current_sound_index()
```python
def get_current_sound(self) -> Sound
def get_current_sound_index(self) -> int
```
**Описание:** Возвращает текущий активный звук/его индекс.

**Возвращает:** Объект `Sound` или индекс текущего канала

---

#### get_number_of_channels()
```python
def get_number_of_channels(self) -> int
```
**Описание:** Возвращает общее количество каналов.

**Возвращает:** Количество доступных каналов воспроизведения

---

#### get_sound() / get_sounds()
```python
def get_sound(self, index: int) -> Sound
def get_sounds(self) -> list[Sound]
```
**Описание:** Возвращает звук по индексу/список всех звуков.

**Параметры:**
- `index` - индекс канала (только для `get_sound`)

**Возвращает:** Объект `Sound` или список всех звуков

**Исключения:**
- `ValueError` - если указан недопустимый индекс (только для `get_sound`)

---

## Примеры использования

### Базовая работа со звуком

```python
from PySGL.Audio import SoundBuffer, Sound, AudioStatus

# Загрузка звука
buffer = SoundBuffer("sounds/explosion.wav")
sound = Sound(buffer)

# Настройка параметров
sound.set_volume(0.8).set_pitch(1.2).set_loop(False)

# Воспроизведение
sound.play()

# Проверка состояния
if sound.get_status() == AudioStatus.PLAYING:
    print("Sound is playing")
```

### Работа с событиями

```python
from PySGL.Audio import SoundEventListener

# Создание обработчика событий
listener = SoundEventListener(sound)

# Настройка callback-функций
listener.set_on_play(lambda: print("Started playing"))
listener.set_on_pause(lambda: print("Paused"))
listener.set_on_stop(lambda: print("Stopped"))

# В основном цикле
def game_loop():
    listener.update()  # Обязательно!
    
    # Проверка событий
    if listener.get_event('play'):
        show_sound_indicator()
    
    if listener.get_event('stop'):
        hide_sound_indicator()
```

### Многоканальное воспроизведение

```python
from PySGL.Audio import MultiSound

# Создание мультизвука для частых звуков
gunshot_buffer = SoundBuffer("sounds/gunshot.wav")
gunshot_sound = Sound(gunshot_buffer)
multi_gunshot = MultiSound(gunshot_sound, 5)  # 5 каналов

# Настройка всех каналов
multi_gunshot.set_volume_all(0.7)
multi_gunshot.set_pitch_all(1.0)

# Использование в игре
def player_shoot():
    multi_gunshot.auto_play()  # Автоматическое переключение каналов

# Управление отдельными каналами
multi_gunshot.set_volume_at(0, 0.5)  # Первый канал тише
multi_gunshot.set_pitch_at(1, 1.5)   # Второй канал выше тоном
```

### 3D позиционирование звука

```python
# Настройка 3D звука
engine_sound = Sound(SoundBuffer("sounds/engine.wav"))
engine_sound.set_loop(True)
engine_sound.set_attenuation(0.8)  # Затухание с расстоянием

# Позиционирование относительно игрока
def update_engine_sound(car_position, player_position):
    relative_x = car_position.x - player_position.x
    relative_y = car_position.y - player_position.y
    
    engine_sound.set_position(relative_x, relative_y, 0)
    
    # Громкость зависит от расстояния
    distance = math.sqrt(relative_x**2 + relative_y**2)
    volume = max(0.0, 1.0 - distance / 100.0)
    engine_sound.set_volume(volume)

# Быстрое позиционирование
footstep_sound.play_left()   # Шаги слева
explosion_sound.play_right() # Взрыв справа
```

### Система управления аудио

```python
class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.music = {}
        self.listeners = {}
        
        # Загрузка звуков
        self.load_sounds()
    
    def load_sounds(self):
        sound_files = {
            'jump': 'sounds/jump.wav',
            'coin': 'sounds/coin.wav',
            'explosion': 'sounds/explosion.wav'
        }
        
        for name, path in sound_files.items():
            buffer = SoundBuffer(path)
            self.sounds[name] = MultiSound(Sound(buffer), 3)
    
    def play_sound(self, name: str, volume: float = 1.0):
        if name in self.sounds:
            self.sounds[name].set_volume_current(volume)
            self.sounds[name].auto_play()
    
    def play_music(self, name: str, loop: bool = True):
        if name in self.music:
            self.music[name].set_loop(loop).play()
    
    def stop_all_sounds(self):
        for sound in self.sounds.values():
            sound.stop_all()
    
    def set_master_volume(self, volume: float):
        for sound in self.sounds.values():
            sound.set_volume_all(volume)

# Использование
audio = AudioManager()
audio.play_sound('jump', 0.8)
audio.play_music('background')
```

### Продвинутые техники

```python
# Динамическое изменение параметров
class DynamicSound:
    def __init__(self, sound: Sound):
        self.sound = sound
        self.base_pitch = 1.0
        self.base_volume = 1.0
    
    def update_by_speed(self, speed: float):
        # Изменение тона в зависимости от скорости
        pitch = self.base_pitch + (speed / 100.0) * 0.5
        self.sound.set_pitch(min(2.0, max(0.5, pitch)))
    
    def update_by_health(self, health: float):
        # Изменение громкости в зависимости от здоровья
        volume = self.base_volume * (health / 100.0)
        self.sound.set_volume(max(0.1, volume))

# Система fade-in/fade-out
class FadeSound:
    def __init__(self, sound: Sound):
        self.sound = sound
        self.target_volume = 1.0
        self.current_volume = 0.0
        self.fade_speed = 0.02
    
    def fade_in(self, target: float = 1.0):
        self.target_volume = target
        self.sound.play()
    
    def fade_out(self):
        self.target_volume = 0.0
    
    def update(self):
        if abs(self.current_volume - self.target_volume) > 0.01:
            if self.current_volume < self.target_volume:
                self.current_volume += self.fade_speed
            else:
                self.current_volume -= self.fade_speed
            
            self.sound.set_volume(self.current_volume)
            
            if self.current_volume <= 0.01 and self.target_volume == 0.0:
                self.sound.stop()
```

---

## Рекомендации по использованию

### Производительность

> **🚀 Оптимизация:** Используйте `MultiSound` для часто воспроизводимых звуков (выстрелы, шаги) вместо создания множественных объектов `Sound`.

> **💾 Память:** Переиспользуйте `SoundBuffer` объекты для одинаковых звуков - создавайте буфер один раз и используйте для нескольких `Sound` объектов.

### Архитектура

> **🏗️ Структура:** Создавайте централизованный `AudioManager` для управления всеми звуками в приложении.

> **🔄 Обновления:** Всегда вызывайте `update()` для `SoundEventListener` в основном игровом цикле.

### 3D Аудио

> **🎯 Позиционирование:** Используйте `set_attenuation()` для реалистичного затухания звука с расстоянием в 3D играх.

> **🌍 Координаты:** Устанавливайте позицию звуков относительно слушателя для корректного пространственного аудио.

### Отладка

> **🐛 Отладка:** Используйте `get_status()` и `SoundEventListener` для отслеживания состояния звуков при отладке.

> **📊 Мониторинг:** Проверяйте `get_path()` для идентификации источников звуков в логах.

### Безопасность

> **⚠️ Исключения:** Всегда обрабатывайте `RuntimeError` при загрузке звуковых файлов и создании звуков.

> **🔒 Валидация:** Проверяйте существование файлов перед созданием `SoundBuffer` для избежания ошибок времени выполнения.

---

## Лицензия

MIT License - Copyright (c) 2025 Pavlov Ivan

Разрешается свободное использование, копирование, изменение и распространение при условии сохранения уведомления об авторских правах.