# Документация модуля Time

## Обзор

Модуль `Time` предоставляет комплексную систему работы со временем в библиотеке PySGL. Он обеспечивает высокоточные таймеры, гибкие интервальные таймеры и удобные утилиты для управления временными операциями.

**Версия:** 1.0.3  
**Автор:** Павлов Иван (Pavlov Ivan)  
**Лицензия:** MIT  
**Реализация:** 100%

## Основные возможности

- ✅ **Высокоточные таймеры** - наносекундная точность через C++ реализацию, кроссплатформенность
- ✅ **Гибкие интервальные таймеры** - именованные таймеры с глобальным менеджером
- ✅ **Удобные утилиты** - декораторы для ограничения частоты, генераторы интервалов
- ✅ **Оптимизированные алгоритмы** - минимальное потребление CPU, эффективное управление ресурсами

## Требования

- Python 3.8+
- Стандартная библиотека `time`
- Стандартная библиотека `typing`
- Нативная библиотека PySGL.dll

---

## Исключения

### LibraryLoadError
```python
class LibraryLoadError(Exception)
```
**Описание:** Ошибка загрузки нативной библиотеки PySGL.dll для высокоточных таймеров.

---

## Класс Clock

Высокоточный таймер на основе C++ реализации из DLL для максимальной точности измерений.

### Конструктор
```python
def __init__(self)
```
**Описание:** Инициализирует новый экземпляр высокоточного таймера с созданием внутреннего C++ объекта.

**Исключения:**
- `LibraryLoadError` - при ошибке загрузки нативной библиотеки

**Пример:**
```python
clock = Clock()  # Создание высокоточного таймера
```

> **🎯 Применение:** Особенно полезен для измерения времени рендеринга кадров, профилирования производительности и синхронизации игрового цикла.

---

### Методы Clock

#### restart()
```python
def restart(self) -> None
```
**Описание:** Сбрасывает и немедленно перезапускает таймер, обнуляя счетчик прошедшего времени.

**Пример:**
```python
clock = Clock()
# ... выполнение операций ...
clock.restart()  # Сброс таймера для нового измерения
```

---

#### get_elapsed_time()
```python
def get_elapsed_time(self) -> float
```
**Описание:** Возвращает время в секундах, прошедшее с последнего вызова `restart()` или создания объекта.

**Возвращает:** Количество секунд с высокой точностью (дробное число)

**Пример:**
```python
clock = Clock()
# ... выполнение операций ...
elapsed = clock.get_elapsed_time()
print(f"Операция заняла {elapsed:.6f} секунд")
```

> **⚡ Производительность:** Обеспечивает наносекундную точность благодаря нативной C++ реализации.

---

## Класс Timer

Простой таймер на основе системного времени для проверки истечения временных интервалов.

### Конструктор
```python
def __init__(self, name: OptionalIdentifier = 'dummy', wait_time: float = 1)
```
**Описание:** Создает новый таймер с указанным именем и интервалом срабатывания.

**Параметры:**
- `name` - уникальное имя для идентификации таймера (по умолчанию 'dummy')
- `wait_time` - интервал срабатывания в секундах (по умолчанию 1.0)

**Пример:**
```python
# Таймер для обновления UI каждые 0.5 секунды
ui_timer = Timer("ui_update", 0.5)

# Таймер для сохранения игры каждые 30 секунд
save_timer = Timer("auto_save", 30.0)
```

---

### Методы Timer

#### timing()
```python
def timing(self) -> bool
```
**Описание:** Проверяет, истек ли установленный интервал. Если интервал истек, автоматически сбрасывает таймер.

**Возвращает:** `True` если интервал истек, `False` если нет

**Пример:**
```python
timer = Timer("update", 1.0)

# В игровом цикле
if timer.timing():
    print("Прошла секунда!")
    update_game_state()
```

> **🔄 Важно:** Метод автоматически сбрасывает таймер при истечении интервала, поэтому следующий вызов начнет новый отсчет.

---

#### get_delta()
```python
def get_delta(self) -> float
```
**Описание:** Возвращает время, прошедшее с последнего сброса таймера.

**Возвращает:** Количество секунд с момента последнего сброса

**Пример:**
```python
timer = Timer("progress", 5.0)
delta = timer.get_delta()
progress = (delta / 5.0) * 100  # Прогресс в процентах
```

---

#### get_name() / set_name()
```python
def get_name(self) -> OptionalIdentifier
def set_name(self, name: Identifier) -> None
```
**Описание:** Получает/устанавливает имя таймера для идентификации.

**Параметры:**
- `name` - новое имя таймера (только для `set_name`)

**Возвращает:** Текущее имя таймера (только для `get_name`)

---

#### get_wait_time() / set_wait_time()
```python
def get_wait_time(self) -> float
def set_wait_time(self, time: float) -> None
```
**Описание:** Получает/устанавливает интервал срабатывания таймера.

**Параметры:**
- `time` - новый интервал в секундах (только для `set_wait_time`)

**Возвращает:** Текущий интервал в секундах (только для `get_wait_time`)

**Пример:**
```python
timer = Timer("dynamic", 1.0)
timer.set_wait_time(2.5)  # Изменение интервала на 2.5 секунды
current_interval = timer.get_wait_time()  # 2.5
```

---

## Глобальные функции

### wait()
```python
def wait(timer_name: OptionalIdentifier = 'dummy', wait_time: float = 0) -> bool
```
**Описание:** Удобная обертка для работы с глобальными таймерами. Создает таймер при первом вызове, затем проверяет его состояние.

**Параметры:**
- `timer_name` - имя таймера (по умолчанию 'dummy')
- `wait_time` - интервал срабатывания в секундах (по умолчанию 0)

**Возвращает:** `True` если интервал истек, `False` если нет

**Пример:**
```python
# В игровом цикле
if wait("enemy_spawn", 2.0):
    spawn_enemy()

if wait("ui_update", 0.1):
    update_ui()
```

> **💡 Удобство:** Автоматически создает и управляет таймерами в глобальном буфере `TIMER_BUFFER`.

---

### wait_call()
```python
def wait_call(timer_name: OptionalIdentifier, wait_time: float, func: FunctionOrMethod, *args, **kwargs) -> None
```
**Описание:** Вызывает функцию только если истек указанный интервал для заданного таймера.

**Параметры:**
- `timer_name` - имя таймера
- `wait_time` - интервал между вызовами в секундах
- `func` - функция для вызова
- `*args` - позиционные аргументы для функции
- `**kwargs` - именованные аргументы для функции

**Пример:**
```python
def save_game(filename):
    print(f"Сохранение игры в {filename}")

def update_stats(player_name, score):
    print(f"Обновление статистики: {player_name} - {score}")

# В игровом цикле
wait_call("auto_save", 30.0, save_game, "autosave.dat")
wait_call("stats_update", 5.0, update_stats, "Player1", score=1500)
```

---

### throttle()
```python
def throttle(wait_time: float)
```
**Описание:** Декоратор для ограничения частоты вызовов функции.

**Параметры:**
- `wait_time` - минимальный интервал между вызовами в секундах

**Возвращает:** Декорированную функцию с ограничением частоты

**Пример:**
```python
@throttle(0.5)  # Максимум один вызов в 0.5 секунды
def expensive_operation():
    print("Выполнение дорогой операции")
    # ... сложные вычисления ...

# Быстрые повторные вызовы будут игнорироваться
for i in range(10):
    expensive_operation()  # Выполнится только первый вызов
    time.sleep(0.1)
```

> **⚠️ Осторожно:** Декоратор может игнорировать вызовы, используйте с пониманием логики приложения.

---

### every()
```python
def every(interval: float) -> Generator[bool]
```
**Описание:** Возвращает генератор, который возвращает `True` каждые `interval` секунд.

**Параметры:**
- `interval` - интервал в секундах

**Возвращает:** Генератор, возвращающий `True` через заданные интервалы

**Пример:**
```python
# Выполнение действия каждую секунду
for ready in every(1.0):
    if ready:
        print("Прошла секунда")
        update_timer_display()
    
    # Другая логика игрового цикла
    render_frame()
    
    # Выход из цикла по условию
    if game_over:
        break
```

---

## Глобальные переменные

### TIMER_BUFFER
```python
TIMER_BUFFER: dict[OptionalIdentifier, Timer] = {}
```
**Описание:** Глобальный буфер для хранения именованных таймеров, используемый функцией `wait()`.

**Пример:**
```python
# Прямой доступ к глобальным таймерам
if "my_timer" in TIMER_BUFFER:
    timer = TIMER_BUFFER["my_timer"]
    print(f"Осталось времени: {timer.get_wait_time() - timer.get_delta():.2f}с")
```

---

## Примеры использования

### Измерение производительности

```python
from PySGL.Time import Clock

def benchmark_function():
    clock = Clock()
    
    # Тестируемая операция
    result = complex_calculation()
    
    elapsed = clock.get_elapsed_time()
    print(f"Операция заняла {elapsed*1000:.3f} мс")
    
    return result

# Профилирование нескольких операций
def profile_operations():
    clock = Clock()
    
    operations = [
        ("Загрузка данных", load_data),
        ("Обработка", process_data),
        ("Сохранение", save_data)
    ]
    
    for name, operation in operations:
        clock.restart()
        operation()
        elapsed = clock.get_elapsed_time()
        print(f"{name}: {elapsed*1000:.2f} мс")
```

### Игровой цикл с таймерами

```python
from PySGL.Time import Timer, wait, wait_call

class GameLoop:
    def __init__(self):
        self.fps_timer = Timer("fps", 1.0)  # Подсчет FPS каждую секунду
        self.frame_count = 0
        self.running = True
    
    def run(self):
        while self.running:
            self.update()
            self.render()
            self.frame_count += 1
    
    def update(self):
        # Обновление врагов каждые 0.1 секунды
        if wait("enemy_update", 0.1):
            self.update_enemies()
        
        # Автосохранение каждые 60 секунд
        wait_call("auto_save", 60.0, self.save_game, "autosave.dat")
        
        # Подсчет FPS
        if self.fps_timer.timing():
            fps = self.frame_count
            print(f"FPS: {fps}")
            self.frame_count = 0
    
    def update_enemies(self):
        print("Обновление врагов")
    
    def save_game(self, filename):
        print(f"Автосохранение: {filename}")
    
    def render(self):
        # Рендеринг кадра
        pass
```

### Система анимации

```python
from PySGL.Time import Clock, Timer

class Animation:
    def __init__(self, duration: float):
        self.duration = duration
        self.clock = Clock()
        self.is_playing = False
    
    def start(self):
        self.clock.restart()
        self.is_playing = True
    
    def get_progress(self) -> float:
        if not self.is_playing:
            return 0.0
        
        elapsed = self.clock.get_elapsed_time()
        progress = min(elapsed / self.duration, 1.0)
        
        if progress >= 1.0:
            self.is_playing = False
        
        return progress
    
    def is_finished(self) -> bool:
        return not self.is_playing and self.clock.get_elapsed_time() >= self.duration

# Использование
fade_animation = Animation(2.0)  # 2 секунды
fade_animation.start()

while not fade_animation.is_finished():
    progress = fade_animation.get_progress()
    alpha = int(255 * (1.0 - progress))  # Затухание от 255 до 0
    render_with_alpha(alpha)
```

### Система событий по времени

```python
from PySGL.Time import every, throttle

class TimeEventSystem:
    def __init__(self):
        self.events = []
    
    def add_recurring_event(self, interval: float, callback):
        """Добавляет событие, повторяющееся через интервал"""
        generator = every(interval)
        self.events.append((generator, callback))
    
    @throttle(0.1)  # Ограничение на обновление событий
    def update(self):
        for generator, callback in self.events:
            if next(generator):
                callback()

# Использование
event_system = TimeEventSystem()

# Добавление событий
event_system.add_recurring_event(1.0, lambda: print("Каждую секунду"))
event_system.add_recurring_event(5.0, lambda: print("Каждые 5 секунд"))
event_system.add_recurring_event(0.5, lambda: print("Дважды в секунду"))

# В игровом цикле
while running:
    event_system.update()
    # Другая логика...
```

### Продвинутое управление временем

```python
from PySGL.Time import Clock, Timer, wait

class TimeManager:
    def __init__(self):
        self.game_clock = Clock()
        self.pause_timer = Timer("pause_duration", 0)
        self.time_scale = 1.0
        self.is_paused = False
        self.total_game_time = 0.0
    
    def update(self):
        if not self.is_paused:
            frame_time = self.game_clock.get_elapsed_time()
            self.total_game_time += frame_time * self.time_scale
        
        self.game_clock.restart()
    
    def pause(self, duration: float = 0):
        """Пауза на указанное время (0 = бесконечно)"""
        self.is_paused = True
        if duration > 0:
            self.pause_timer.set_wait_time(duration)
    
    def resume(self):
        """Возобновление времени"""
        self.is_paused = False
    
    def set_time_scale(self, scale: float):
        """Изменение скорости времени (1.0 = нормально, 0.5 = медленно, 2.0 = быстро)"""
        self.time_scale = max(0.0, scale)
    
    def get_game_time(self) -> float:
        """Получение общего игрового времени"""
        return self.total_game_time
    
    def check_auto_resume(self):
        """Автоматическое возобновление после паузы"""
        if self.is_paused and self.pause_timer.timing():
            self.resume()

# Использование
time_manager = TimeManager()

# В игровом цикле
while running:
    time_manager.update()
    time_manager.check_auto_resume()
    
    if not time_manager.is_paused:
        # Обновление игровой логики
        update_game_logic()
    
    # Пауза на 3 секунды при нажатии клавиши
    if key_pressed('P'):
        time_manager.pause(3.0)
    
    # Замедление времени
    if key_pressed('S'):
        time_manager.set_time_scale(0.3)
    elif key_released('S'):
        time_manager.set_time_scale(1.0)
```

---

## Рекомендации по использованию

### Производительность

> **🚀 Оптимизация:** Используйте `Clock` для критичных по времени измерений (профилирование, FPS), а `Timer` для обычных игровых таймеров.

> **💾 Память:** Переиспользуйте объекты `Timer` вместо создания новых для повторяющихся операций.

### Архитектура

> **🏗️ Структура:** Используйте глобальную функцию `wait()` для простых случаев, создавайте собственные экземпляры `Timer` для сложной логики.

> **🔄 Управление:** Централизуйте управление временем через специальный класс `TimeManager` в больших проектах.

### Точность

> **⏱️ Точность:** `Clock` обеспечивает наносекундную точность благодаря C++ реализации, используйте для точных измерений.

> **🎯 Применение:** `Timer` подходит для игровой логики, где точность в миллисекундах не критична.

### Отладка

> **🐛 Отладка:** Используйте `get_delta()` для мониторинга состояния таймеров и отладки временной логики.

> **📊 Профилирование:** Комбинируйте `Clock` с логированием для анализа производительности различных частей приложения.

### Безопасность

> **⚠️ Исключения:** Обрабатывайте `LibraryLoadError` при создании объектов `Clock` для обеспечения стабильности.

> **🔒 Валидация:** Проверяйте корректность временных интервалов (положительные значения) перед установкой в таймеры.

---

## Лицензия

MIT License - Copyright (c) 2025 Pavlov Ivan

Разрешается свободное использование, копирование, изменение и распространение при условии сохранения уведомления об авторских правах.