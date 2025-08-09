# Документация модуля Shapes

## Обзор

Модуль `Shapes` предоставляет комплексную систему работы с геометрическими фигурами в библиотеке PySGL. Он обеспечивает полный набор инструментов для создания, манипуляции и отрисовки различных форм с высокой производительностью.

**Версия:** 1.0.0  
**Автор:** Павлов Иван (Pavlov Ivan)  
**Лицензия:** MIT  
**Реализация:** 100%

## Основные возможности

- ✅ **Базовые геометрические фигуры** - прямоугольники, круги, линии различных типов
- ✅ **Высокопроизводительная отрисовка** - нативная реализация на C++ с Python API
- ✅ **Полные преобразования** - позиционирование, поворот, масштабирование, точка отсчета
- ✅ **Визуальные эффекты** - цвета заливки, контуры, прозрачность
- ✅ **Специализированные линии** - толстые линии, тонкие линии, полилинии, скругленные концы
- ✅ **Сложные фигуры** - полигоны с автоматической триангуляцией

## Требования

- Python 3.8+
- Нативная библиотека PySGL.dll
- Модули: `ctypes`, `os`, `typing`
- Зависимости: `PySGL.python.Types`, `PySGL.python.Colors`, `PySGL.python.Vectors`
- Внешняя библиотека: `tripy` (для триангуляции полигонов)

---

## Архитектура модуля

### Нативная интеграция
Модуль использует прямую интеграцию с C++ библиотекой через `ctypes` для максимальной производительности. Все графические операции выполняются на стороне нативного кода.

### Типы указателей
```python
RectanglePtr: Final[ctypes.c_void_p] = ctypes.c_void_p
LinesThinPtr = ctypes.c_void_p
```

### Загрузка библиотеки
```python
def _find_library() -> str
```
**Описание:** Автоматически находит и загружает нативную библиотеку PySGL.dll.

**Исключения:**
- `LibraryLoadError` - если библиотека не найдена

---

## Класс RectangleShape

Базовый класс для работы с прямоугольными фигурами с полной поддержкой преобразований.

### Конструктор
```python
def __init__(self, width: float, height: float)
```
**Описание:** Создает новый прямоугольник с заданными размерами.

**Параметры:**
- `width` - ширина прямоугольника (>0)
- `height` - высота прямоугольника (>0)

**Исключения:**
- `ValueError` - при недопустимых размерах

**Пример:**
```python
rect = RectangleShape(100.0, 50.0)
```

---

### Методы позиционирования

#### set_position()
```python
@overload
def set_position(self, x: Number, y: Number) -> Self: ...
@overload
def set_position(self, vector: Vector2f) -> Self: ...
```
**Описание:** Устанавливает позицию прямоугольника.

**Параметры:**
- `x, y` - координаты или
- `vector` - вектор позиции

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
rect.set_position(150.5, 200.0)
rect.set_position(Vector2f(150.5, 200.0))
```

#### get_position()
```python
def get_position(self) -> Vector2f
```
**Описание:** Возвращает текущую позицию прямоугольника.

**Возвращает:** Вектор позиции {x, y}

---

### Методы размеров

#### set_size()
```python
@overload
def set_size(self, width: float, height: float) -> Self: ...
@overload
def set_size(self, size: Vector2f) -> Self: ...
```
**Описание:** Устанавливает размеры прямоугольника.

**Параметры:**
- `width, height` - размеры или
- `size` - вектор размеров

**Возвращает:** Текущий объект для цепочки вызовов

#### get_size()
```python
def get_size(self) -> Vector2f
```
**Описание:** Возвращает текущие размеры прямоугольника.

**Возвращает:** Вектор размеров {width, height}

---

### Методы визуального оформления

#### set_color()
```python
def set_color(self, color: Color) -> Self
```
**Описание:** Устанавливает цвет заливки прямоугольника.

**Параметры:**
- `color` - цвет в формате RGBA

**Возвращает:** Текущий объект для цепочки вызовов

#### set_outline_color() / set_outline_thickness()
```python
def set_outline_color(self, color: Color) -> Self
def set_outline_thickness(self, thickness: float) -> Self
```
**Описание:** Настройка контура прямоугольника.

**Параметры:**
- `color` - цвет контура
- `thickness` - толщина контура (≥0)

---

### Методы преобразований

#### set_angle()
```python
def set_angle(self, angle: float) -> Self
```
**Описание:** Устанавливает угол поворота в градусах.

**Параметры:**
- `angle` - угол поворота (0-360)

#### set_scale()
```python
@overload
def set_scale(self, scale: float) -> Self: ...
@overload
def set_scale(self, scale_x: float, scale_y: float) -> Self: ...
```
**Описание:** Устанавливает масштаб прямоугольника.

**Параметры:**
- `scale` - равномерный масштаб или
- `scale_x, scale_y` - масштаб по осям

#### set_origin()
```python
@overload
def set_origin(self, x: float, y: float) -> Self: ...
@overload
def set_origin(self, vector: Vector2f) -> Self: ...
```
**Описание:** Устанавливает точку отсчета для преобразований.

**Параметры:**
- `x, y` - координаты точки отсчета или
- `vector` - вектор точки отсчета

---

### Утилитарные методы

#### move()
```python
def move(self, offset: Vector2f) -> Self
```
**Описание:** Перемещает прямоугольник на заданный вектор.

#### copy()
```python
def copy(self) -> "RectangleShape"
```
**Описание:** Создает полную независимую копию прямоугольника.

**Возвращает:** Новый объект RectangleShape с идентичными параметрами

**Пример:**
```python
original = RectangleShape(100, 50).set_color(Color.RED)
duplicate = original.copy()
duplicate.set_color(Color.BLUE)  # Не влияет на оригинал
```

---

## Класс CircleShape

Базовый класс для работы с круговыми фигурами с настраиваемой точностью аппроксимации.

### Конструктор
```python
def __init__(self, approximation: int = 30)
```
**Описание:** Создает новый круг с заданным количеством точек аппроксимации.

**Параметры:**
- `approximation` - количество точек контура (≥3)

**Исключения:**
- `ValueError` - при approximation < 3

**Пример:**
```python
circle = CircleShape(50)  # Высокое качество
simple_circle = CircleShape(10)  # Низкое качество (многоугольник)
```

---

### Методы управления радиусом

#### set_radius()
```python
def set_radius(self, radius: float) -> Self
```
**Описание:** Устанавливает радиус круга.

**Параметры:**
- `radius` - новый радиус (>0)

#### set_origin_radius()
```python
def set_origin_radius(self, radius: float) -> Self
```
**Описание:** Устанавливает радиус с автоматической центровкой точки отсчета.

**Параметры:**
- `radius` - новый радиус (>0)

**Пример:**
```python
circle.set_origin_radius(50)  # Радиус 50 с центром в середине
```

#### get_radius()
```python
def get_radius(self) -> float
```
**Описание:** Возвращает текущий радиус круга.

---

### Методы позиционирования и преобразований

CircleShape поддерживает все те же методы преобразований, что и RectangleShape:
- `set_position()` / `get_position()`
- `set_angle()` / `get_angle()`
- `set_scale()` / `get_scale()`
- `set_origin()` / `get_origin()`
- `set_color()` / `get_color()`
- `set_outline_color()` / `set_outline_thickness()`
- `move()`, `copy()`

---

## Класс BaseLineShape

Базовый класс для работы с толстыми линиями с поддержкой скругленных концов.

### Конструктор
```python
def __init__(self, color: Color = COLOR_GRAY) -> None
```
**Описание:** Создает линию с базовыми параметрами.

**Параметры:**
- `color` - начальный цвет линии

**Особенности:**
- Не рекомендуется использовать цвета с alpha каналом (артефакты отрисовки)
- Реализована как комбинация прямоугольника и кругов

---

### Методы настройки точек

#### set_points()
```python
@overload
def set_points(self, start: Vector2f, end: Vector2f) -> Self: ...
@overload
def set_points(self, x1: float, y1: float, x2: float, y2: float) -> Self: ...
```
**Описание:** Устанавливает начальную и конечную точки линии.

**Пример:**
```python
line.set_points(0, 0, 100, 100)
line.set_points(Vector2f(0, 0), Vector2f(100, 100))
```

#### set_start_point() / set_end_point()
```python
@overload
def set_start_point(self, point: Vector2f) -> Self: ...
@overload
def set_start_point(self, x: float, y: float) -> Self: ...
```
**Описание:** Устанавливает начальную/конечную точку линии.

---

### Методы настройки внешнего вида

#### set_width()
```python
def set_width(self, width: float) -> Self
```
**Описание:** Устанавливает толщину линии.

**Параметры:**
- `width` - толщина линии (>0)

#### set_rounded()
```python
def set_rounded(self, round: bool = True) -> Self
```
**Описание:** Включает/выключает скругление концов линии.

**Параметры:**
- `round` - флаг скругления

**Пример:**
```python
line.set_rounded(True)   # Скругленные концы
line.set_rounded(False)  # Прямые концы
```

#### set_color()
```python
def set_color(self, color: Color) -> Self
```
**Описание:** Устанавливает цвет всей линии (тело + концы).

---

### Методы перемещения точек

#### move_start_point() / move_end_point()
```python
@overload
def move_start_point(self, vector: Vector2f) -> Self: ...
@overload
def move_start_point(self, dx: float, dy: float) -> Self: ...
```
**Описание:** Перемещает начальную/конечную точку на заданное смещение.

**Пример:**
```python
line.move_start_point(Vector2f(10, 5))
line.move_end_point(5.0, -10.0)
```

---

### Методы отрисовки и обновления

#### update()
```python
def update(self) -> None
```
**Описание:** Пересчитывает геометрию линии на основе текущих параметров.

#### special_draw()
```python
def special_draw(self, window)
```
**Описание:** Выполняет отрисовку линии с автоматическим обновлением геометрии.

**Параметры:**
- `window` - целевое окно для отрисовки

**Пример:**
```python
line = BaseLineShape(COLOR_RED)
line.set_points(0, 0, 100, 100).set_width(5).set_rounded(True)

# В цикле отрисовки
line.special_draw(window)
```

---

## Класс LineShape

Расширенная линия с поддержкой контурной обводки, наследует от BaseLineShape.

### Конструктор
```python
def __init__(self) -> None
```
**Описание:** Создает линию с поддержкой контура.

---

### Методы контура

#### set_outline_thickness()
```python
def set_outline_thickness(self, value: float) -> Self
```
**Описание:** Устанавливает толщину контурной обводки.

**Параметры:**
- `value` - толщина контура (≥0)

#### set_outline_color()
```python
def set_outline_color(self, color: Color) -> Self
```
**Описание:** Устанавливает цвет контурной обводки.

**Пример:**
```python
line = LineShape()
line.set_points(0, 0, 100, 100)
    .set_width(5)
    .set_color(COLOR_RED)
    .set_outline_thickness(2)
    .set_outline_color(COLOR_BLUE)
```

---

## Класс LineThinShape

Высокопроизводительный класс для отрисовки тонких линий через вершинные массивы.

### Конструктор
```python
def __init__(self) -> None
```
**Описание:** Создает тонкую линию с минимальными накладными расходами.

**Особенности:**
- Оптимизирован для массовой отрисовки
- Не поддерживает толстые линии и скругленные концы
- Использует вершинные массивы напрямую

---

### Методы настройки

#### set_points()
```python
@overload
def set_points(self, start: Vector2f, end: Vector2f) -> Self: ...
@overload
def set_points(self, x1: float, y1: float, x2: float, y2: float) -> Self: ...
```

#### set_color()
```python
def set_color(self, color: Color) -> Self
```
**Описание:** Устанавливает цвет для всей линии.

#### set_start_color() / set_end_color()
```python
def set_start_color(self, color: Color) -> Self
def set_end_color(self, color: Color) -> Self
```
**Описание:** Устанавливает цвет начальной/конечной точки для создания градиентов.

**Пример:**
```python
line = LineThinShape()
line.set_points(0, 0, 100, 100)
    .set_start_color(Color(255, 0, 0))  # Красный
    .set_end_color(Color(0, 0, 255))    # Синий
```

---

### Методы доступа к данным

#### get_colors()
```python
def get_colors(self) -> tuple[Color, Color]
```
**Описание:** Возвращает цвета обеих точек линии.

**Возвращает:** Кортеж (начальный_цвет, конечный_цвет)

#### get_vertex()
```python
def get_vertex(self, index: int) -> Vertex
```
**Описание:** Возвращает вершину линии по индексу (0 или 1).

---

## Класс LinesThinShape

Класс для работы с полилиниями (ломаными линиями) с высокой производительностью.

### Конструктор
```python
def __init__(self) -> None
```
**Описание:** Создает пустую полилинию.

---

### Методы управления точками

#### append_point_to_end()
```python
@overload
def append_point_to_end(self, point: Vector2f, color: Color = COLOR_BLACK) -> Self: ...
@overload
def append_point_to_end(self, x: float, y: float, color: Color = COLOR_BLACK) -> Self: ...
```
**Описание:** Добавляет точку в конец полилинии (O(1) операция).

#### append_point_to_begin()
```python
@overload
def append_point_to_begin(self, point: Vector2f, color: Color = COLOR_BLACK) -> Self: ...
@overload
def append_point_to_begin(self, x: float, y: float, color: Color = COLOR_BLACK) -> Self: ...
```
**Описание:** Добавляет точку в начало полилинии (O(n) операция).

#### remove_last_point() / remove_first_point()
```python
def remove_last_point(self) -> Self
def remove_first_point(self) -> Self
```
**Описание:** Удаляет последнюю/первую точку полилинии.

---

### Методы модификации точек

#### set_point_position()
```python
@overload
def set_point_position(self, index: int, position: Vector2f) -> Self: ...
@overload
def set_point_position(self, index: int, x: float, y: float) -> Self: ...
```
**Описание:** Устанавливает новую позицию существующей точки.

#### set_point_color()
```python
def set_point_color(self, index: int, color: Color) -> Self
```
**Описание:** Устанавливает цвет конкретной точки.

#### move_point()
```python
def move_point(self, index: int, vector: Vector2f) -> Self
```
**Описание:** Сдвигает точку на заданный вектор.

---

### Утилитарные методы

#### clear()
```python
def clear(self) -> Self
```
**Описание:** Полностью очищает полилинию.

#### __len__()
```python
def __len__(self) -> int
```
**Описание:** Возвращает количество точек в полилинии.

#### __getitem__()
```python
def __getitem__(self, index: int) -> tuple[Vector2f, Color]
```
**Описание:** Получает точку и ее цвет по индексу.

**Пример:**
```python
polyline = LinesThinShape()
polyline.append_point_to_end(0, 0, COLOR_RED)
        .append_point_to_end(100, 50, COLOR_GREEN)
        .append_point_to_end(200, 0, COLOR_BLUE)

print(f"Количество точек: {len(polyline)}")
pos, color = polyline[1]  # Получить вторую точку
```

---

## Класс PolygoneShape

Класс для работы с произвольными полигонами с автоматической триангуляцией.

### Конструктор
```python
def __init__(self, points: list[Vector2f], color: Color = COLOR_WHITE)
```
**Описание:** Создает полигон из списка точек.

**Параметры:**
- `points` - список вершин полигона
- `color` - цвет заливки

**Пример:**
```python
# Треугольник
triangle = PolygoneShape([
    Vector2f(0, 0),
    Vector2f(100, 0),
    Vector2f(50, 100)
], COLOR_RED)
```

---

### Методы управления точками

#### append_point_to_end() / append_point_to_begin()
```python
def append_point_to_end(self, point: Vector2f) -> Self
def append_point_to_begin(self, point: Vector2f) -> Self
```
**Описание:** Добавляет точку в конец/начало полигона с автоматической ретриангуляцией.

#### clear()
```python
def clear(self) -> Self
```
**Описание:** Очищает все точки полигона.

---

### Методы визуального оформления

#### set_color() / get_color()
```python
def set_color(self, color: Color) -> Self
def get_color(self) -> Color
```
**Описание:** Устанавливает/возвращает цвет полигона.

---

## Предустановленные объекты

Модуль предоставляет готовые экземпляры фигур для быстрого использования:

```python
CIRCLE_SHAPE: Final[CircleShape] = CircleShape(30)
RECTANGLE_SHAPE: Final[RectangleShape] = RectangleShape(100, 100)
BASE_LINE_SHAPE: Final[BaseLineShape] = BaseLineShape()
LINE_SHAPE: Final[LineShape] = LineShape()
LINE_THIN_SHAPE: Final[LineThinShape] = LineThinShape()
LINES_THIN_SHAPE: Final[LinesThinShape] = LinesThinShape()
POLYGONE_SHAPE: Final[PolygoneShape] = PolygoneShape([], COLOR_RED)
```

---

## Примеры использования

### Базовые фигуры

```python
from PySGL.python.Rendering.Shapes import *
from PySGL.python.Colors import *

# Прямоугольник с настройками
rect = RectangleShape(200, 100)
rect.set_position(100, 50)
    .set_color(COLOR_BLUE)
    .set_outline_color(COLOR_BLACK)
    .set_outline_thickness(2)
    .set_angle(45)

# Круг с центровкой
circle = CircleShape(50)
circle.set_origin_radius(75)
      .set_position(300, 200)
      .set_color(COLOR_RED)
```

### Работа с линиями

```python
# Толстая линия со скругленными концами
thick_line = BaseLineShape(COLOR_GREEN)
thick_line.set_points(0, 0, 200, 100)
          .set_width(10)
          .set_rounded(True)

# Линия с контуром
outlined_line = LineShape()
outlined_line.set_points(50, 50, 250, 150)
             .set_width(8)
             .set_color(COLOR_YELLOW)
             .set_outline_thickness(3)
             .set_outline_color(COLOR_BLACK)

# Градиентная тонкая линия
gradient_line = LineThinShape()
gradient_line.set_points(0, 100, 300, 100)
             .set_start_color(COLOR_RED)
             .set_end_color(COLOR_BLUE)
```

### Полилинии и полигоны

```python
# Создание ломаной линии
polyline = LinesThinShape()
points = [(0, 0), (50, 100), (100, 50), (150, 150), (200, 0)]
colors = [COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE]

for (x, y), color in zip(points, colors):
    polyline.append_point_to_end(x, y, color)

# Создание многоугольника
pentagon_points = []
import math
for i in range(5):
    angle = i * 2 * math.pi / 5
    x = 100 + 50 * math.cos(angle)
    y = 100 + 50 * math.sin(angle)
    pentagon_points.append(Vector2f(x, y))

pentagon = PolygoneShape(pentagon_points, COLOR_PURPLE)
```

### Анимация и трансформации

```python
import time

class AnimatedShape:
    def __init__(self):
        self.rect = RectangleShape(50, 50)
        self.rect.set_color(COLOR_CYAN)
        self.rect.set_origin(25, 25)  # Центр для вращения
        
    def update(self, dt):
        # Вращение
        current_angle = self.rect.get_angle()
        self.rect.set_angle(current_angle + 90 * dt)
        
        # Пульсация
        scale = 1.0 + 0.3 * math.sin(time.time() * 2)
        self.rect.set_scale(scale)
        
        # Движение по кругу
        t = time.time()
        x = 200 + 100 * math.cos(t)
        y = 200 + 100 * math.sin(t)
        self.rect.set_position(x, y)

# Использование
animated = AnimatedShape()
# В игровом цикле:
# animated.update(delta_time)
# window.draw(animated.rect)
```

### Создание сложных фигур

```python
class Star:
    def __init__(self, center: Vector2f, outer_radius: float, inner_radius: float):
        points = []
        for i in range(10):  # 5 внешних + 5 внутренних точек
            angle = i * math.pi / 5
            if i % 2 == 0:  # Внешние точки
                radius = outer_radius
            else:  # Внутренние точки
                radius = inner_radius
            
            x = center.x + radius * math.cos(angle - math.pi/2)
            y = center.y + radius * math.sin(angle - math.pi/2)
            points.append(Vector2f(x, y))
        
        self.shape = PolygoneShape(points, COLOR_GOLD)
    
    def draw(self, window):
        window.draw(self.shape)

# Создание звезды
star = Star(Vector2f(200, 200), 50, 25)
```

### Оптимизация производительности

```python
# Для массовой отрисовки используйте тонкие линии
class Grid:
    def __init__(self, width, height, cell_size):
        self.lines = []
        
        # Вертикальные линии
        for x in range(0, width, cell_size):
            line = LineThinShape()
            line.set_points(x, 0, x, height)
            line.set_color(COLOR_LIGHT_GRAY)
            self.lines.append(line)
        
        # Горизонтальные линии
        for y in range(0, height, cell_size):
            line = LineThinShape()
            line.set_points(0, y, width, y)
            line.set_color(COLOR_LIGHT_GRAY)
            self.lines.append(line)
    
    def draw(self, window):
        for line in self.lines:
            window.draw(line)

# Переиспользование объектов
class ShapePool:
    def __init__(self):
        self.rectangles = [RectangleShape(10, 10) for _ in range(100)]
        self.circles = [CircleShape(20) for _ in range(50)]
        self.used_rects = 0
        self.used_circles = 0
    
    def get_rectangle(self):
        if self.used_rects < len(self.rectangles):
            rect = self.rectangles[self.used_rects]
            self.used_rects += 1
            return rect
        return None
    
    def reset(self):
        self.used_rects = 0
        self.used_circles = 0
```

---

## Рекомендации по использованию

### Производительность

> **🚀 Оптимизация:** Используйте LineThinShape для массовой отрисовки простых линий вместо BaseLineShape.

> **💾 Память:** Переиспользуйте объекты фигур через пулы объектов для избежания частых аллокаций.

> **⚡ Батчинг:** Группируйте однотипные фигуры для более эффективной отрисовки.

### Выбор типа фигуры

> **📏 Линии:** 
> - LineThinShape - для простых линий и сеток
> - BaseLineShape - для декоративных линий с эффектами
> - LineShape - когда нужен контур
> - LinesThinShape - для сложных ломаных линий

> **🔺 Полигоны:** PolygoneShape автоматически триангулирует сложные формы, но для простых фигур предпочтительнее базовые классы.

### Преобразования

> **🎯 Точка отсчета:** Всегда устанавливайте origin перед применением поворотов и масштабирования.

> **🔄 Порядок операций:** Применяйте преобразования в порядке: origin → scale → rotation → position.

### Визуальные эффекты

> **🎨 Цвета:** Избегайте альфа-канала в BaseLineShape и LineShape для предотвращения артефактов.

> **🖼️ Контуры:** Используйте контуры умеренно - они увеличивают нагрузку на отрисовку.

### Архитектура

> **🏗️ Композиция:** Создавайте сложные объекты из простых фигур для лучшей гибкости.

> **🔧 Фабрики:** Используйте фабричные методы для создания стандартных конфигураций фигур.

### Отладка

> **🐛 Отладка:** Используйте контуры и яркие цвета для визуализации границ фигур при отладке.

> **📊 Профилирование:** Мониторьте количество создаваемых объектов и вызовов отрисовки.

---

## Лицензия

MIT License - Copyright (c) 2025 Pavlov Ivan

Разрешается свободное использование, копирование, изменение и распространение при условии сохранения уведомления об авторских правах.