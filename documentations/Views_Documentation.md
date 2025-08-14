# Документация модуля Views

## Обзор

Модуль `Views` предоставляет комплексную систему работы с камерами и областями просмотра в библиотеке PySGL. Он обеспечивает полный набор инструментов для создания, управления и трансформации видов сцены с высокой производительностью.

**Версия:** 1.1.8  
**Автор:** Павлов Иван (Pavlov Ivan)  
**Лицензия:** MIT  
**Реализация:** 98%

## Основные возможности

- ✅ **Управление камерами** - создание, позиционирование, поворот и масштабирование областей просмотра
- ✅ **Высокопроизводительная обработка** - нативная реализация на C++ с Python API
- ✅ **Система координат** - поддержка FloatRect для точного позиционирования
- ✅ **Трансформации** - центрирование, масштабирование, поворот, перемещение
- ✅ **Вьюпорты** - настройка областей экрана для отображения
- ✅ **Временные изменения** - контекстные менеджеры для временных трансформаций

## Требования

- Python 3.8+
- Нативная библиотека PySGL.dll
- Модули: `ctypes`, `os`, `typing`, `contextlib`
- Зависимости: встроенные модули Python

---

## Архитектура модуля

### Нативная интеграция
Модуль использует прямую интеграцию с C++ библиотекой через `ctypes` для максимальной производительности. Все операции с камерами выполняются на стороне нативного кода.

### Типы указателей
```python
FloatRectPtr = ctypes.c_void_p
ViewPtr = ctypes.c_void_p
```

### Загрузка библиотеки
```python
def _find_library() -> str
```
**Описание:** Автоматически находит и загружает нативную библиотеку PySGL.dll.

**Исключения:**
- `LibraryLoadError` - если библиотека не найдена

---

## Исключения

### LibraryLoadError
```python
@final
class LibraryLoadError(Exception)
```
**Описание:** Ошибка загрузки нативной библиотеки PySGL.dll.

### ViewError
```python
@final
class ViewError(Exception)
```
**Описание:** Ошибка работы с объектами View и FloatRect.

---

## Класс FloatRect

Класс прямоугольной области с плавающей точкой для точного позиционирования.

### Конструктор
```python
def __init__(self, x: float, y: float, w: float, h: float) -> None
```
**Описание:** Создает новый FloatRect с указанными параметрами.

**Параметры:**
- `x` - позиция по X
- `y` - позиция по Y  
- `w` - ширина (должна быть >= 0)
- `h` - высота (должна быть >= 0)

**Исключения:**
- `ValueError` - при отрицательных размерах
- `ViewError` - если не удалось создать объект

**Пример:**
```python
# Создать прямоугольник 100x50 в позиции (10, 20)
rect = FloatRect(10.0, 20.0, 100.0, 50.0)
```

---

### Методы позиционирования

#### get_position()
```python
def get_position(self) -> tuple[float, float]
```
**Описание:** Возвращает текущую позицию прямоугольника.

**Возвращает:** Кортеж (x, y) с координатами левого верхнего угла

**Пример:**
```python
x, y = rect.get_position()
print(f"Позиция: ({x}, {y})")
```

#### set_position()
```python
def set_position(self, x: Optional[float] = None, y: Optional[float] = None) -> Self
```
**Описание:** Устанавливает новую позицию прямоугольника.

**Параметры:**
- `x` - новая позиция X (None - не изменять)
- `y` - новая позиция Y (None - не изменять)

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
# Установить только X координату
rect.set_position(x=100.0)

# Установить обе координаты
rect.set_position(50.0, 75.0)
```

---

### Методы размеров

#### get_size()
```python
def get_size(self) -> tuple[float, float]
```
**Описание:** Возвращает текущие размеры прямоугольника.

**Возвращает:** Кортеж (width, height) с размерами

**Пример:**
```python
width, height = rect.get_size()
print(f"Размер: {width}x{height}")
```

#### set_size()
```python
def set_size(self, w: Optional[float] = None, h: Optional[float] = None) -> Self
```
**Описание:** Устанавливает новые размеры прямоугольника.

**Параметры:**
- `w` - новая ширина (None - не изменять, должна быть >= 0)
- `h` - новая высота (None - не изменять, должна быть >= 0)

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `ValueError` - при отрицательных размерах

**Пример:**
```python
# Изменить только ширину
rect.set_size(w=200.0)

# Изменить оба размера
rect.set_size(150.0, 100.0)
```

---

### Утилитарные методы

#### get_ptr()
```python
def get_ptr(self) -> FloatRectPtr
```
**Описание:** Возвращает указатель на нативный объект для внутреннего использования в PySGL.

#### __repr__()
```python
def __repr__(self) -> str
```
**Описание:** Строковое представление для отладки.

**Пример:**
```python
print(rect)  # FloatRect(x=10.0, y=20.0, w=100.0, h=50.0)
```

---

## Класс View

Основной класс камеры/области просмотра для управления отображением сцены.

### Конструктор
```python
def __init__(self, float_rect: FloatRect) -> None
```
**Описание:** Создает новый View с указанным прямоугольником.

**Параметры:**
- `float_rect` - прямоугольник области просмотра

**Исключения:**
- `TypeError` - если float_rect не является экземпляром FloatRect
- `ViewError` - если не удалось создать View

**Пример:**
```python
# Создать область просмотра 800x600
rect = FloatRect(0, 0, 800, 600)
view = View(rect)
```

---

### Альтернативный конструктор

#### from_view_ptr()
```python
@classmethod
def from_view_ptr(cls, view_ptr: ViewPtr) -> "View"
```
**Описание:** Создает объект View из существующего указателя на нативный View.

**Параметры:**
- `view_ptr` - указатель на нативный View

**Возвращает:** Новый экземпляр View

**Исключения:**
- `ViewError` - если указатель невалиден

**Примечание:** Создаваемый объект не владеет указателем

**Пример:**
```python
# Создать View из нативного указателя
view = View.from_view_ptr(native_view_ptr)
```

---

### Методы управления центром

#### set_center()
```python
def set_center(self, x: float, y: float) -> Self
```
**Описание:** Устанавливает центр области просмотра.

**Параметры:**
- `x` - координата X центра
- `y` - координата Y центра

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
# Центрировать камеру на точке (400, 300)
view.set_center(400.0, 300.0)
```

#### get_center()
```python
def get_center(self) -> tuple[float, float]
```
**Описание:** Возвращает центр области просмотра.

**Возвращает:** Кортеж (center_x, center_y) с координатами центра

**Пример:**
```python
center_x, center_y = view.get_center()
print(f"Центр камеры: ({center_x}, {center_y})")
```

---

### Методы управления размером

#### set_size()
```python
def set_size(self, width: float, height: float) -> Self
```
**Описание:** Устанавливает размер области просмотра.

**Параметры:**
- `width` - ширина (должна быть > 0)
- `height` - высота (должна быть > 0)

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `ValueError` - если размеры неположительные

**Пример:**
```python
# Установить размер области просмотра 1024x768
view.set_size(1024.0, 768.0)
```

#### get_size()
```python
def get_size(self) -> tuple[float, float]
```
**Описание:** Возвращает размер области просмотра.

**Возвращает:** Кортеж (width, height) с размерами

**Пример:**
```python
width, height = view.get_size()
print(f"Размер области просмотра: {width}x{height}")
```

---

### Методы управления поворотом

#### set_angle()
```python
def set_angle(self, angle: float) -> Self
```
**Описание:** Устанавливает угол поворота области просмотра.

**Параметры:**
- `angle` - угол поворота в градусах

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
# Повернуть камеру на 45 градусов
view.set_angle(45.0)
```

#### get_angle()
```python
def get_angle(self) -> float
```
**Описание:** Возвращает угол поворота области просмотра.

**Возвращает:** Угол поворота в градусах

**Пример:**
```python
angle = view.get_angle()
print(f"Угол поворота: {angle}°")
```

#### rotate()
```python
def rotate(self, angle: float) -> Self
```
**Описание:** Поворачивает область просмотра на указанный угол.

**Параметры:**
- `angle` - угол поворота в градусах (добавляется к текущему углу)

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
# Повернуть камеру на дополнительные 90 градусов
view.rotate(90.0)
```

---

### Методы перемещения

#### move()
```python
def move(self, offset_x: float, offset_y: float) -> Self
```
**Описание:** Перемещает область просмотра на указанное смещение.

**Параметры:**
- `offset_x` - смещение по оси X
- `offset_y` - смещение по оси Y

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
# Сдвинуть камеру вправо на 50 пикселей
view.move(50.0, 0.0)
```

#### get_position()
```python
def get_position(self) -> tuple[float, float]
```
**Описание:** Возвращает позицию области просмотра.

**Возвращает:** Кортеж (position_x, position_y) с координатами левого верхнего угла

**Пример:**
```python
pos_x, pos_y = view.get_position()
print(f"Позиция камеры: ({pos_x}, {pos_y})")
```

---

### Методы масштабирования

#### zoom()
```python
def zoom(self, factor: float) -> Self
```
**Описание:** Масштабирует область просмотра.

**Параметры:**
- `factor` - коэффициент масштабирования (должен быть > 0)
  - 1.0 - без изменений
  - <1.0 - приближение (увеличение)
  - >1.0 - отдаление (уменьшение)

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `ValueError` - если factor <= 0

**Пример:**
```python
# Приблизить в 2 раза
view.zoom(0.5)

# Отдалить в 1.5 раза
view.zoom(1.5)
```

---

### Методы управления вьюпортом

#### set_viewport()
```python
def set_viewport(self, float_rect: FloatRect) -> Self
```
**Описание:** Устанавливает область экрана для отображения (viewport).

**Параметры:**
- `float_rect` - прямоугольник области экрана (координаты от 0.0 до 1.0)

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `TypeError` - если float_rect не является экземпляром FloatRect

**Пример:**
```python
# Левая половина экрана
viewport = FloatRect(0.0, 0.0, 0.5, 1.0)
view.set_viewport(viewport)

# Правый верхний квадрант
viewport = FloatRect(0.5, 0.0, 0.5, 0.5)
view.set_viewport(viewport)
```

#### get_viewport()
```python
def get_viewport(self) -> FloatRect
```
**Описание:** Возвращает текущий viewport области просмотра.

**Возвращает:** FloatRect с координатами viewport

**Пример:**
```python
viewport = view.get_viewport()
print(f"Viewport: {viewport.get_position()}, {viewport.get_size()}")
```

---

### Утилитарные методы

#### get_ptr()
```python
def get_ptr(self) -> ViewPtr
```
**Описание:** Возвращает указатель на нативный объект для внутреннего использования в PySGL.

#### reset()
```python
def reset(self, float_rect: FloatRect) -> Self
```
**Описание:** Сбрасывает все параметры View к исходным значениям.

**Параметры:**
- `float_rect` - новый базовый прямоугольник области просмотра

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
# Сброс к исходному состоянию
original_rect = FloatRect(0, 0, 800, 600)
view.reset(original_rect)
```

#### copy()
```python
def copy(self) -> "View"
```
**Описание:** Создает полную независимую копию области просмотра.

**Возвращает:** Новый объект View с идентичными параметрами

**Пример:**
```python
original_view = View(FloatRect(0, 0, 800, 600))
original_view.set_center(400, 300).zoom(0.5)

duplicate_view = original_view.copy()
duplicate_view.set_angle(45)  # Не влияет на оригинал
```

#### __repr__()
```python
def __repr__(self) -> str
```
**Описание:** Строковое представление для отладки.

**Пример:**
```python
print(view)  # View(center=(400.0, 300.0), size=(800.0, 600.0), angle=0.0)
```

---

## Контекстные менеджеры

Модуль предоставляет контекстные менеджеры для временных изменений области просмотра.

### TemporaryViewChange
```python
@contextmanager
def temporary_view_change(view: View, **kwargs) -> Generator[View, None, None]
```
**Описание:** Контекстный менеджер для временного изменения параметров View.

**Параметры:**
- `view` - объект View для изменения
- `**kwargs` - параметры для временного изменения:
  - `center` - tuple[float, float] - временный центр
  - `size` - tuple[float, float] - временный размер
  - `angle` - float - временный угол поворота
  - `zoom_factor` - float - временный коэффициент масштабирования

**Возвращает:** Измененный View, который автоматически восстанавливается

**Пример:**
```python
from PySGL.python.Rendering.Views import temporary_view_change

# Временное приближение для детального отображения
with temporary_view_change(view, center=(player_x, player_y), zoom_factor=0.3) as temp_view:
    # Отрисовка с приближенным видом
    window.set_view(temp_view)
    draw_detailed_objects(window)
    
# View автоматически восстанавливается к исходному состоянию
window.set_view(view)
```

### TemporaryViewport
```python
@contextmanager
def temporary_viewport(view: View, viewport: FloatRect) -> Generator[View, None, None]
```
**Описание:** Контекстный менеджер для временного изменения viewport.

**Параметры:**
- `view` - объект View для изменения
- `viewport` - временный viewport

**Пример:**
```python
# Временное отображение в мини-карте
minimap_viewport = FloatRect(0.7, 0.0, 0.3, 0.3)
with temporary_viewport(view, minimap_viewport) as minimap_view:
    window.set_view(minimap_view)
    draw_minimap(window)
```

---

## Предустановленные объекты

Модуль предоставляет готовые экземпляры для быстрого использования:

```python
DEFAULT_VIEW: Final[View] = View(FloatRect(0, 0, 800, 600))
FULLSCREEN_VIEWPORT: Final[FloatRect] = FloatRect(0.0, 0.0, 1.0, 1.0)
LEFT_HALF_VIEWPORT: Final[FloatRect] = FloatRect(0.0, 0.0, 0.5, 1.0)
RIGHT_HALF_VIEWPORT: Final[FloatRect] = FloatRect(0.5, 0.0, 0.5, 1.0)
TOP_HALF_VIEWPORT: Final[FloatRect] = FloatRect(0.0, 0.0, 1.0, 0.5)
BOTTOM_HALF_VIEWPORT: Final[FloatRect] = FloatRect(0.0, 0.5, 1.0, 0.5)
```

---

## Примеры использования

### Базовая настройка камеры

```python
from PySGL.python.Rendering.Views import *

# Создание основной камеры
main_camera = View(FloatRect(0, 0, 1920, 1080))
main_camera.set_center(960, 540)  # Центр экрана

# Настройка для игрока
player_x, player_y = 1000, 500
main_camera.set_center(player_x, player_y)
main_camera.zoom(0.8)  # Небольшое приближение

# Применение к окну
window.set_view(main_camera)
```

### Система следования за игроком

```python
class CameraController:
    def __init__(self, view: View, target_smoothing: float = 0.1):
        self.view = view
        self.target_pos = [0.0, 0.0]
        self.current_pos = [0.0, 0.0]
        self.smoothing = target_smoothing
        self.zoom_level = 1.0
        self.target_zoom = 1.0
    
    def set_target(self, x: float, y: float) -> None:
        """Устанавливает целевую позицию для камеры"""
        self.target_pos[0] = x
        self.target_pos[1] = y
    
    def set_zoom_target(self, zoom: float) -> None:
        """Устанавливает целевой уровень масштабирования"""
        self.target_zoom = max(0.1, min(5.0, zoom))
    
    def update(self, dt: float) -> None:
        """Обновляет позицию камеры с плавным следованием"""
        # Плавное следование за целью
        lerp_factor = 1.0 - pow(0.5, dt / self.smoothing)
        
        self.current_pos[0] += (self.target_pos[0] - self.current_pos[0]) * lerp_factor
        self.current_pos[1] += (self.target_pos[1] - self.current_pos[1]) * lerp_factor
        
        # Плавное изменение масштаба
        self.zoom_level += (self.target_zoom - self.zoom_level) * lerp_factor
        
        # Применение к камере
        self.view.set_center(self.current_pos[0], self.current_pos[1])
        
        # Установка масштаба через размер
        base_width, base_height = 1920, 1080
        new_width = base_width * self.zoom_level
        new_height = base_height * self.zoom_level
        self.view.set_size(new_width, new_height)
    
    def shake(self, intensity: float, duration: float) -> None:
        """Добавляет эффект тряски камеры"""
        import random
        import time
        
        shake_x = random.uniform(-intensity, intensity)
        shake_y = random.uniform(-intensity, intensity)
        
        # Временное смещение
        current_center = self.view.get_center()
        self.view.set_center(current_center[0] + shake_x, current_center[1] + shake_y)

# Использование
camera_controller = CameraController(main_camera, target_smoothing=0.05)

# В игровом цикле
player_pos = get_player_position()
camera_controller.set_target(player_pos.x, player_pos.y)
camera_controller.update(delta_time)

# При взрыве
camera_controller.shake(intensity=20.0, duration=0.5)
```

### Разделение экрана (Split Screen)

```python
class SplitScreenManager:
    def __init__(self, window_width: float, window_height: float):
        self.window_size = (window_width, window_height)
        
        # Создание двух камер
        self.player1_view = View(FloatRect(0, 0, window_width, window_height))
        self.player2_view = View(FloatRect(0, 0, window_width, window_height))
        
        # Настройка вьюпортов для вертикального разделения
        self.player1_view.set_viewport(LEFT_HALF_VIEWPORT)
        self.player2_view.set_viewport(RIGHT_HALF_VIEWPORT)
    
    def update_cameras(self, player1_pos: tuple, player2_pos: tuple) -> None:
        """Обновляет позиции обеих камер"""
        self.player1_view.set_center(player1_pos[0], player1_pos[1])
        self.player2_view.set_center(player2_pos[0], player2_pos[1])
    
    def render_split_screen(self, window, render_func) -> None:
        """Отрисовывает сцену для обеих камер"""
        # Отрисовка для первого игрока
        window.set_view(self.player1_view)
        render_func(window, player_id=1)
        
        # Отрисовка для второго игрока
        window.set_view(self.player2_view)
        render_func(window, player_id=2)
    
    def switch_to_horizontal(self) -> None:
        """Переключает на горизонтальное разделение"""
        self.player1_view.set_viewport(TOP_HALF_VIEWPORT)
        self.player2_view.set_viewport(BOTTOM_HALF_VIEWPORT)
    
    def switch_to_vertical(self) -> None:
        """Переключает на вертикальное разделение"""
        self.player1_view.set_viewport(LEFT_HALF_VIEWPORT)
        self.player2_view.set_viewport(RIGHT_HALF_VIEWPORT)

# Использование
split_manager = SplitScreenManager(1920, 1080)

# В игровом цикле
player1_pos = get_player_position(1)
player2_pos = get_player_position(2)
split_manager.update_cameras(player1_pos, player2_pos)
split_manager.render_split_screen(window, render_game_world)
```

### Мини-карта и UI камеры

```python
class MultiCameraSystem:
    def __init__(self):
        # Основная игровая камера
        self.main_camera = View(FloatRect(0, 0, 1920, 1080))
        
        # Камера для мини-карты (показывает большую область)
        self.minimap_camera = View(FloatRect(0, 0, 1920, 1080))
        self.minimap_camera.set_viewport(FloatRect(0.75, 0.05, 0.2, 0.2))
        self.minimap_camera.zoom(3.0)  # Отдаленный вид
        
        # Камера для UI (фиксированная)
        self.ui_camera = View(FloatRect(0, 0, 1920, 1080))
        self.ui_camera.set_center(960, 540)
    
    def update(self, player_pos: tuple) -> None:
        """Обновляет все камеры"""
        # Основная камера следует за игроком
        self.main_camera.set_center(player_pos[0], player_pos[1])
        
        # Мини-карта тоже центрируется на игроке
        self.minimap_camera.set_center(player_pos[0], player_pos[1])
    
    def render_all(self, window, world_renderer, ui_renderer) -> None:
        """Отрисовывает все слои"""
        # Основной игровой мир
        window.set_view(self.main_camera)
        world_renderer.render_main_world(window)
        
        # Мини-карта
        window.set_view(self.minimap_camera)
        world_renderer.render_minimap(window)
        
        # UI поверх всего
        window.set_view(self.ui_camera)
        ui_renderer.render_ui(window)

# Использование
camera_system = MultiCameraSystem()

# В игровом цикле
player_pos = get_player_position()
camera_system.update(player_pos)
camera_system.render_all(window, world_renderer, ui_renderer)
```

### Кинематографические эффекты

```python
class CinematicCamera:
    def __init__(self, view: View):
        self.view = view
        self.keyframes = []
        self.current_time = 0.0
        self.duration = 0.0
        self.is_playing = False
    
    def add_keyframe(self, time: float, center: tuple, zoom: float = 1.0, angle: float = 0.0) -> None:
        """Добавляет ключевой кадр анимации"""
        self.keyframes.append({
            'time': time,
            'center': center,
            'zoom': zoom,
            'angle': angle
        })
        self.keyframes.sort(key=lambda k: k['time'])
        self.duration = max(self.duration, time)
    
    def play(self) -> None:
        """Запускает воспроизведение анимации"""
        self.current_time = 0.0
        self.is_playing = True
    
    def update(self, dt: float) -> bool:
        """Обновляет анимацию камеры"""
        if not self.is_playing or len(self.keyframes) < 2:
            return False
        
        self.current_time += dt
        
        if self.current_time >= self.duration:
            self.is_playing = False
            return False
        
        # Найти текущие ключевые кадры для интерполяции
        prev_frame = None
        next_frame = None
        
        for frame in self.keyframes:
            if frame['time'] <= self.current_time:
                prev_frame = frame
            elif frame['time'] > self.current_time and next_frame is None:
                next_frame = frame
                break
        
        if prev_frame and next_frame:
            # Интерполяция между кадрами
            t = (self.current_time - prev_frame['time']) / (next_frame['time'] - prev_frame['time'])
            t = self._smooth_step(t)  # Плавная интерполяция
            
            # Интерполяция позиции
            center_x = self._lerp(prev_frame['center'][0], next_frame['center'][0], t)
            center_y = self._lerp(prev_frame['center'][1], next_frame['center'][1], t)
            
            # Интерполяция масштаба и угла
            zoom = self._lerp(prev_frame['zoom'], next_frame['zoom'], t)
            angle = self._lerp(prev_frame['angle'], next_frame['angle'], t)
            
            # Применение к камере
            self.view.set_center(center_x, center_y)
            base_size = self.view.get_size()
            self.view.set_size(base_size[0] * zoom, base_size[1] * zoom)
            self.view.set_angle(angle)
        
        return True
    
    def _lerp(self, a: float, b: float, t: float) -> float:
        """Линейная интерполяция"""
        return a + (b - a) * t
    
    def _smooth_step(self, t: float) -> float:
        """Плавная интерполяция (ease-in-out)"""
        return t * t * (3.0 - 2.0 * t)

# Создание кинематографической сцены
cinematic = CinematicCamera(main_camera)

# Добавление ключевых кадров
cinematic.add_keyframe(0.0, center=(0, 0), zoom=2.0, angle=0)
cinematic.add_keyframe(2.0, center=(500, 300), zoom=1.0, angle=15)
cinematic.add_keyframe(4.0, center=(1000, 600), zoom=0.5, angle=-10)
cinematic.add_keyframe(6.0, center=(1500, 900), zoom=1.5, angle=0)

# Запуск анимации
cinematic.play()

# В игровом цикле
if cinematic.update(delta_time):
    # Анимация продолжается
    pass
else:
    # Анимация завершена, вернуться к обычному управлению
    pass
```

### Параллакс эффект

```python
class ParallaxLayer:
    def __init__(self, view: View, parallax_factor: float):
        self.base_view = view
        self.layer_view = view.copy()
        self.parallax_factor = parallax_factor  # 0.0 = статичный, 1.0 = движется с камерой
        self.base_center = view.get_center()
    
    def update(self) -> None:
        """Обновляет позицию слоя на основе основной камеры"""
        current_center = self.base_view.get_center()
        
        # Вычисление смещения от базовой позиции
        offset_x = (current_center[0] - self.base_center[0]) * self.parallax_factor
        offset_y = (current_center[1] - self.base_center[1]) * self.parallax_factor
        
        # Применение смещения к слою
        self.layer_view.set_center(
            self.base_center[0] + offset_x,
            self.base_center[1] + offset_y
        )
    
    def get_view(self) -> View:
        return self.layer_view

class ParallaxRenderer:
    def __init__(self, main_camera: View):
        self.main_camera = main_camera
        self.layers = []
    
    def add_layer(self, parallax_factor: float) -> ParallaxLayer:
        """Добавляет новый слой параллакса"""
        layer = ParallaxLayer(self.main_camera, parallax_factor)
        self.layers.append(layer)
        return layer
    
    def render(self, window, render_functions: list) -> None:
        """Отрисовывает все слои параллакса"""
        # Обновление всех слоев
        for layer in self.layers:
            layer.update()
        
        # Отрисовка слоев от дальних к ближним
        for i, (layer, render_func) in enumerate(zip(self.layers, render_functions)):
            window.set_view(layer.get_view())
            render_func(window)
        
        # Основной слой
        window.set_view(self.main_camera)

# Использование параллакса
parallax = ParallaxRenderer(main_camera)

# Добавление слоев (от дальних к ближним)
background_layer = parallax.add_layer(0.1)    # Медленный фон
midground_layer = parallax.add_layer(0.5)     # Средний план
foreground_layer = parallax.add_layer(0.8)    # Передний план

# Функции отрисовки для каждого слоя
def render_background(window):
    # Отрисовка далекого фона (горы, небо)
    pass

def render_midground(window):
    # Отрисовка среднего плана (деревья, здания)
    pass

def render_foreground(window):
    # Отрисовка переднего плана (трава, детали)
    pass

# В игровом цикле
parallax.render(window, [render_background, render_midground, render_foreground])

# Отрисовка основного игрового слоя
render_main_game_objects(window)
```

### Адаптивное масштабирование

```python
class AdaptiveCamera:
    def __init__(self, view: View, min_zoom: float = 0.5, max_zoom: float = 2.0):
        self.view = view
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.target_objects = []
        self.padding = 100.0  # Отступ от краев экрана
    
    def add_target(self, position: tuple, priority: float = 1.0) -> None:
        """Добавляет объект для отслеживания"""
        self.target_objects.append({
            'position': position,
            'priority': priority
        })
    
    def clear_targets(self) -> None:
        """Очищает список отслеживаемых объектов"""
        self.target_objects.clear()
    
    def update(self) -> None:
        """Обновляет камеру для показа всех целей"""
        if not self.target_objects:
            return
        
        # Вычисление центра масс с учетом приоритетов
        total_weight = 0.0
        weighted_x = 0.0
        weighted_y = 0.0
        
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')
        
        for target in self.target_objects:
            pos = target['position']
            priority = target['priority']
            
            weighted_x += pos[0] * priority
            weighted_y += pos[1] * priority
            total_weight += priority
            
            min_x = min(min_x, pos[0])
            max_x = max(max_x, pos[0])
            min_y = min(min_y, pos[1])
            max_y = max(max_y, pos[1])
        
        # Центр камеры
        center_x = weighted_x / total_weight
        center_y = weighted_y / total_weight
        self.view.set_center(center_x, center_y)
        
        # Вычисление необходимого масштаба
        required_width = (max_x - min_x) + self.padding * 2
        required_height = (max_y - min_y) + self.padding * 2
        
        current_size = self.view.get_size()
        zoom_x = required_width / current_size[0] if required_width > 0 else 1.0
        zoom_y = required_height / current_size[1] if required_height > 0 else 1.0
        
        # Выбор максимального масштаба для показа всех объектов
        required_zoom = max(zoom_x, zoom_y)
        required_zoom = max(self.min_zoom, min(self.max_zoom, required_zoom))
        
        # Применение масштаба
        base_size = (1920, 1080)  # Базовый размер
        new_width = base_size[0] * required_zoom
        new_height = base_size[1] * required_zoom
        self.view.set_size(new_width, new_height)

# Использование адаптивной камеры
adaptive_camera = AdaptiveCamera(main_camera)

# В игровом цикле
adaptive_camera.clear_targets()

# Добавление игроков с разными приоритетами
for player in players:
    priority = 2.0 if player.is_local else 1.0
    adaptive_camera.add_target(player.position, priority)

# Добавление важных объектов
for objective in important_objectives:
    adaptive_camera.add_target(objective.position, 0.5)

adaptive_camera.update()
```

---

## Рекомендации по использованию

### Производительность

> **🚀 Оптимизация:** Избегайте частого создания новых объектов View - переиспользуйте существующие через методы set_*.

> **💾 Память:** Используйте copy() только когда необходимо сохранить состояние камеры, иначе работайте с одним экземпляром.

> **⚡ Вычисления:** Кэшируйте результаты сложных вычислений позиции камеры между кадрами.

### Выбор подхода к камере

> **🎮 Игровые жанры:**
> - Платформеры: фиксированное следование с зонами мертвого пространства
> - RTS: свободное перемещение с ограничениями границ
> - RPG: плавное следование с возможностью ручного управления
> - Шутеры: быстрое следование с предсказанием движения

### Масштабирование и размеры

> **📏 Пропорции:** Всегда учитывайте соотношение сторон экрана при установке размеров View.

> **🔍 Масштабирование:** Используйте zoom() для интерактивного масштабирования, set_size() для фиксированных размеров области.

> **📐 Координаты:** Помните, что FloatRect использует координаты левого верхнего угла, а View центрируется по set_center().

### Viewport и разделение экрана

> **📺 Координаты viewport:** Используйте нормализованные координаты (0.0-1.0) для viewport - они автоматически адаптируются к размеру окна.

> **🔄 Переключение режимов:** Создавайте предустановленные viewport'ы для быстрого переключения между режимами отображения.

### Анимация и эффекты

> **⏱️ Временные изменения:** Используйте контекстные менеджеры для временных эффектов - они гарантируют восстановление состояния.

> **🎬 Кинематограф:** Для сложных анимаций камеры создавайте отдельные классы-контроллеры с системой ключевых кадров.

> **📳 Эффекты тряски:** Применяйте тряску камеры умеренно и с затуханием для комфортного восприятия.

### Архитектура системы камер

> **🏗️ Разделение ответственности:** Создавайте отдельные классы для управления камерой, следования за объектами и эффектов.

> **🔧 Конфигурация:** Выносите параметры камеры (скорость следования, границы, масштабы) в конфигурационные файлы.

> **🎯 Приоритеты:** При множественных целях используйте систему весов для определения важности объектов.

### Отладка и тестирование

> **🐛 Визуализация:** Отрисовывайте границы области просмотра и центр камеры при отладке.

> **📊 Метрики:** Отслеживайте частоту изменений параметров камеры для оптимизации производительности.

> **🔍 Проверки:** Валидируйте границы камеры и предотвращайте выход за пределы игрового мира.

### Пользовательский опыт

> **👁️ Комфорт:** Избегайте резких изменений позиции и масштаба камеры - используйте плавные переходы.

> **🎮 Управление:** Предоставляйте игрокам возможность настройки чувствительности камеры и скорости следования.

> **⚙️ Доступность:** Добавляйте опции для отключения эффектов тряски и быстрых движений камеры.

---

## Лицензия

MIT License - Copyright (c) 2025 Pavlov Ivan

Разрешается свободное использование, копирование, изменение и распространение при условии сохранения уведомления об авторских правах.иближение
  - >1.0 - отдаление

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `ValueError` - если коэффициент неположительный

**Пример:**
```python
# Приблизить в 2 раза
view.zoom(0.5)

# Отдалить в 2 раза
view.zoom(2.0)
```

---

### Методы управления вьюпортом

#### set_viewport()
```python
def set_viewport(self, viewport: FloatRect) -> Self
```
**Описание:** Устанавливает вьюпорт (область экрана для отображения).

**Параметры:**
- `viewport` - прямоугольник вьюпорта в нормализованных координатах (0-1)

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `TypeError` - если viewport не является экземпляром FloatRect

**Пример:**
```python
# Установить вьюпорт на левую половину экрана
viewport = FloatRect(0.0, 0.0, 0.5, 1.0)
view.set_viewport(viewport)
```

---

### Методы сброса и доступа

#### reset()
```python
def reset(self, rectangle: FloatRect) -> Self
```
**Описание:** Сбрасывает параметры области просмотра к указанному прямоугольнику.

**Параметры:**
- `rectangle` - новый прямоугольник области просмотра

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `TypeError` - если rectangle не является экземпляром FloatRect

**Пример:**
```python
# Сбросить камеру к новой области
new_rect = FloatRect(0, 0, 1920, 1080)
view.reset(new_rect)
```

#### get_float_rect()
```python
def get_float_rect(self) -> FloatRect
```
**Описание:** Возвращает базовый прямоугольник вида.

**Возвращает:** Прямоугольник, определяющий область просмотра

**Пример:**
```python
rect = view.get_float_rect()
print(f"Область просмотра: {rect}")
```

---

### Контекстные менеджеры

#### temporary_transform()
```python
@contextmanager
def temporary_transform(self, center: Optional[tuple[float, float]] = None, 
                      size: Optional[tuple[float, float]] = None,
                      angle: Optional[float] = None)
```
**Описание:** Контекстный менеджер для временного изменения параметров области просмотра.

**Параметры:**
- `center` - временный центр (x, y)
- `size` - временный размер (width, height)
- `angle` - временный угол поворота в градусах

**Возвращает:** Текущий объект View с примененными временными параметрами

**Особенности:**
- Автоматически сохраняет текущие параметры
- Применяет временные изменения
- Восстанавливает исходные параметры при выходе из контекста

**Пример:**
```python
# Временно изменить центр и размер для специального рендеринга
with view.temporary_transform(center=(100, 100), size=(400, 300)):
    # Рендеринг с временными параметрами
    window.draw(special_object)
# Параметры автоматически восстановлены
```

---

### Утилитарные методы

#### get_ptr()
```python
def get_ptr(self) -> ViewPtr
```
**Описание:** Возвращает указатель на нативный объект для внутреннего использования в PySGL.

#### __repr__()
```python
def __repr__(self) -> str
```
**Описание:** Строковое представление для отладки.

**Пример:**
```python
print(view)  # View(center=(400.0, 300.0), size=(800.0, 600.0), angle=0.0°)
```

---

## Примеры использования

### Базовая настройка камеры

```python
from PySGL.python.Views import FloatRect, View

# Создание базовой области просмотра
rect = FloatRect(0, 0, 800, 600)
camera = View(rect)

# Центрирование камеры
camera.set_center(400, 300)

# Установка размера области просмотра
camera.set_size(1024, 768)
```

### Управление камерой в игре

```python
class GameCamera:
    def __init__(self, width: float, height: float):
        self.rect = FloatRect(0, 0, width, height)
        self.view = View(self.rect)
        self.target_x = 0.0
        self.target_y = 0.0
        self.follow_speed = 2.0
    
    def follow_player(self, player_x: float, player_y: float, dt: float):
        """Плавное следование за игроком"""
        current_x, current_y = self.view.get_center()
        
        # Интерполяция к цели
        dx = player_x - current_x
        dy = player_y - current_y
        
        move_x = dx * self.follow_speed * dt
        move_y = dy * self.follow_speed * dt
        
        self.view.move(move_x, move_y)
    
    def shake(self, intensity: float, duration: float):
        """Эффект тряски камеры"""
        import random
        import time
        
        start_time = time.time()
        original_center = self.view.get_center()
        
        while time.time() - start_time < duration:
            shake_x = random.uniform(-intensity, intensity)
            shake_y = random.uniform(-intensity, intensity)
            
            self.view.set_center(
                original_center[0] + shake_x,
                original_center[1] + shake_y
            )
            
            # В реальной игре здесь был бы yield или callback
            
        # Восстановить исходную позицию
        self.view.set_center(*original_center)

# Использование
camera = GameCamera(800, 600)
# В игровом цикле:
# camera.follow_player(player.x, player.y, delta_time)
```

### Разделение экрана

```python
class SplitScreenManager:
    def __init__(self, screen_width: float, screen_height: float):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Создаем две камеры для разделения экрана
        self.left_view = self._create_left_view()
        self.right_view = self._create_right_view()
    
    def _create_left_view(self) -> View:
        """Создает камеру для левой половины экрана"""
        rect = FloatRect(0, 0, self.screen_width, self.screen_height)
        view = View(rect)
        
        # Вьюпорт для левой половины экрана
        viewport = FloatRect(0.0, 0.0, 0.5, 1.0)
        view.set_viewport(viewport)
        
        return view
    
    def _create_right_view(self) -> View:
        """Создает камеру для правой половины экрана"""
        rect = FloatRect(0, 0, self.screen_width, self.screen_height)
        view = View(rect)
        
        # Вьюпорт для правой половины экрана
        viewport = FloatRect(0.5, 0.0, 0.5, 1.0)
        view.set_viewport(viewport)
        
        return view
    
    def update_cameras(self, player1_pos: tuple[float, float], 
                      player2_pos: tuple[float, float]):
        """Обновляет позиции камер для двух игроков"""
        self.left_view.set_center(*player1_pos)
        self.right_view.set_center(*player2_pos)

# Использование
split_screen = SplitScreenManager(1920, 1080)
# В игровом цикле:
# split_screen.update_cameras((player1.x, player1.y), (player2.x, player2.y))
```

### Система зумирования

```python
class ZoomController:
    def __init__(self, view: View):
        self.view = view
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        self.current_zoom = 1.0
        self.zoom_speed = 0.1
    
    def zoom_in(self, amount: float = None):
        """Приближение"""
        if amount is None:
            amount = self.zoom_speed
            
        new_zoom = self.current_zoom - amount
        if new_zoom >= self.min_zoom:
            self.view.zoom(1 - amount / self.current_zoom)
            self.current_zoom = new_zoom
    
    def zoom_out(self, amount: float = None):
        """Отдаление"""
        if amount is None:
            amount = self.zoom_speed
            
        new_zoom = self.current_zoom + amount
        if new_zoom <= self.max_zoom:
            self.view.zoom(1 + amount / self.current_zoom)
            self.current_zoom = new_zoom
    
    def set_zoom(self, zoom_level: float):
        """Установка конкретного уровня зума"""
        zoom_level = max(self.min_zoom, min(self.max_zoom, zoom_level))
        factor = zoom_level / self.current_zoom
        self.view.zoom(factor)
        self.current_zoom = zoom_level
    
    def reset_zoom(self):
        """Сброс зума к исходному уровню"""
        self.set_zoom(1.0)

# Использование
rect = FloatRect(0, 0, 800, 600)
view = View(rect)
zoom_controller = ZoomController(view)

# zoom_controller.zoom_in(0.2)  # Приблизить
# zoom_controller.zoom_out(0.1)  # Отдалить
# zoom_controller.set_zoom(2.0)  # Установить зум x2
```

### Анимированные переходы камеры

```python
import math
import time

class CameraAnimator:
    def __init__(self, view: View):
        self.view = view
        self.animations = []
    
    def animate_to_position(self, target_x: float, target_y: float, 
                          duration: float, easing="ease_out"):
        """Анимированный переход к позиции"""
        start_x, start_y = self.view.get_center()
        start_time = time.time()
        
        def update():
            elapsed = time.time() - start_time
            if elapsed >= duration:
                self.view.set_center(target_x, target_y)
                return True  # Анимация завершена
            
            # Применяем функцию сглаживания
            t = elapsed / duration
            if easing == "ease_out":
                t = 1 - (1 - t) ** 3
            elif easing == "ease_in":
                t = t ** 3
            elif easing == "ease_in_out":
                t = 3 * t**2 - 2 * t**3
            
            # Интерполяция позиции
            current_x = start_x + (target_x - start_x) * t
            current_y = start_y + (target_y - start_y) * t
            
            self.view.set_center(current_x, current_y)
            return False  # Анимация продолжается
        
        self.animations.append(update)
    
    def animate_zoom(self, target_zoom: float, duration: float):
        """Анимированное изменение зума"""
        start_size = self.view.get_size()
        target_width = start_size[0] / target_zoom
        target_height = start_size[1] / target_zoom
        start_time = time.time()
        
        def update():
            elapsed = time.time() - start_time
            if elapsed >= duration:
                self.view.set_size(target_width, target_height)
                return True
            
            t = elapsed / duration
            t = 1 - (1 - t) ** 2  # ease_out
            
            current_width = start_size[0] + (target_width - start_size[0]) * t
            current_height = start_size[1] + (target_height - start_size[1]) * t
            
            self.view.set_size(current_width, current_height)
            return False
        
        self.animations.append(update)
    
    def update(self):
        """Обновляет все активные анимации"""
        self.animations = [anim for anim in self.animations if not anim()]

# Использование
rect = FloatRect(0, 0, 800, 600)
view = View(rect)
animator = CameraAnimator(view)

# Анимированный переход к новой позиции
animator.animate_to_position(1000, 500, 2.0, "ease_out")

# В игровом цикле:
# animator.update()
```

### Временные эффекты с контекстными менеджерами

```python
def render_minimap(view: View, window, world_objects):
    """Рендеринг мини-карты с временным изменением камеры"""
    
    # Временно изменяем камеру для отображения всего мира
    with view.temporary_transform(
        center=(world_width/2, world_height/2),  # Центр мира
        size=(world_width, world_height),        # Весь мир
        angle=0                                  # Без поворота
    ):
        # Рендерим мини-карту
        for obj in world_objects:
            window.draw(obj)
    
    # Камера автоматически восстановлена к исходным параметрам

def render_zoom_effect(view: View, window, effect_objects, zoom_factor: float):
    """Временный эффект приближения"""
    
    current_size = view.get_size()
    zoomed_size = (current_size[0] / zoom_factor, current_size[1] / zoom_factor)
    
    with view.temporary_transform(size=zoomed_size):
        # Рендерим с эффектом приближения
        for obj in effect_objects:
            window.draw(obj)

# Использование в игровом цикле
def game_render_loop(view, window, objects):
    # Обычный рендеринг
    for obj in objects:
        window.draw(obj)
    
    # Рендеринг мини-карты без влияния на основную камеру
    render_minimap(view, window, objects)
    
    # Специальный эффект для определенных объектов
    render_zoom_effect(view, window, special_objects, 2.0)
```

---

## Рекомендации по использованию

### Производительность

> **🚀 Оптимизация:** Избегайте частых изменений параметров View в каждом кадре. Группируйте изменения и применяйте их за один вызов.

> **💾 Память:** Переиспользуйте объекты FloatRect для вьюпортов и областей просмотра.

> **⚡ Батчинг:** Используйте временные трансформации для специальных эффектов вместо создания новых View.

### Управление камерой

> **📐 Координаты:** 
> - Используйте центрирование для более интуитивного управления камерой
> - Помните, что позиция - это левый верхний угол, а центр - середина области

> **🔄 Трансформации:** Применяйте трансформации в логическом порядке: позиция → размер → поворот → масштабирование

### Вьюпорты

> **📱 Адаптивность:** Используйте нормализованные координаты (0-1) для вьюпортов для поддержки разных разрешений экрана.

> **🖼️ Разделение экрана:** Для многопользовательских игр создавайте отдельные View с разными вьюпортами.

### Анимации

> **⏱️ Плавность:** Используйте функции сглаживания (easing) для более естественных анимаций камеры.

> **🎯 Следование:** Реализуйте плавное следование за объектами с интерполяцией вместо мгновенного перемещения.

### Архитектура

> **🏗️ Инкапсуляция:** Создавайте классы-обертки для сложной логики управления камерой.

> **🔧 Контроллеры:** Используйте отдельные контроллеры для зума, следования и анимаций.

### Отладка

> **🐛 Визуализация:** Используйте временные трансформации для отладочного отображения границ камеры.

> **📊 Мониторинг:** Отслеживайте параметры камеры через __repr__ методы для диагностики проблем.

---

## Лицензия

MIT License - Copyright (c) 2025 Pavlov Ivan

Разрешается свободное использование, копирование, изменение и распространение при условии сохранения уведомления об авторских правах.