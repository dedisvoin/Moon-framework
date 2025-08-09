# Документация модуля Colors

## Обзор

Модуль `Colors` предоставляет комплексную систему работы с цветами в библиотеке PySGL. Он обеспечивает полный набор инструментов для создания, манипуляции, преобразования цветов и создания градиентов.

**Версия:** 1.0.3  
**Автор:** Павлов Иван (Pavlov Ivan)  
**Лицензия:** MIT  
**Реализация:** 100%

## Основные возможности

- ✅ **Полноценная работа с цветами** - RGB/RGBA форматы, преобразования между цветовыми пространствами
- ✅ **Расширенные возможности** - гармоничные цветовые палитры, плавные градиенты
- ✅ **Математические операции** - смешивание, осветление, затемнение, инверсия цветов
- ✅ **Оптимизированные алгоритмы** - быстрые преобразования и эффективные методы смешивания
- ✅ **Готовые интерфейсы** - предустановленные цвета и градиенты для быстрого использования

## Требования

- Python 3.8+
- Стандартная библиотека `math`
- Стандартная библиотека `random`
- Стандартная библиотека `colorsys`

---

## Типы данных

### RGBAColorAsArrayType
```python
type RGBAColorAsArrayType = tuple[int, int, int, int]
```
**Описание:** Тип для представления цвета в виде кортежа RGBA.

### RGBColorAsArrayType
```python
type RGBColorAsArrayType = tuple[int, int, int]
```
**Описание:** Тип для представления цвета в виде кортежа RGB.

### ColorArrayType
```python
type ColorArrayType = list[Color] | tuple[Color, ...]
```
**Описание:** Тип для представления массива объектов Color.

---

## Класс Color

Основной класс для хранения и манипуляции с цветами в формате RGBA.

### Конструктор
```python
def __init__(self, r: int, g: int, b: int, a: int = 255)
```
**Описание:** Инициализирует цвет в формате RGBA с проверкой диапазона значений.

**Параметры:**
- `r` - красный компонент (0-255)
- `g` - зеленый компонент (0-255)
- `b` - синий компонент (0-255)
- `a` - альфа-канал/прозрачность (0-255, по умолчанию 255)

**Исключения:**
- `ValueError` - если компоненты выходят за допустимый диапазон 0-255

**Пример:**
```python
red = Color(255, 0, 0)  # Красный цвет
semi_transparent = Color(0, 255, 0, 128)  # Полупрозрачный зеленый
```

---

### Статические методы класса Color

#### random()
```python
@classmethod
def random(cls) -> 'Color'
```
**Описание:** Генерирует полностью непрозрачный случайный цвет с альфа-каналом 255.

**Возвращает:** Новый объект `Color` со случайными RGB компонентами

**Пример:**
```python
random_color = Color.random()  # Например: Color(123, 45, 67, 255)
```

---

#### random_alpha()
```python
@classmethod
def random_alpha(cls) -> 'Color'
```
**Описание:** Генерирует случайный цвет со случайной прозрачностью.

**Возвращает:** Новый объект `Color` со случайными RGBA компонентами

**Пример:**
```python
transparent_color = Color.random_alpha()  # Например: Color(123, 45, 67, 128)
```

---

### Методы трансформации

#### lighten()
```python
def lighten(self, factor: float) -> "Color"
```
**Описание:** Осветляет цвет, смешивая его с белым цветом.

**Параметры:**
- `factor` - коэффициент осветления (0.0 - исходный цвет, 1.0 - полностью белый)

**Возвращает:** Новый осветленный объект `Color`

**Исключения:**
- `ValueError` - если factor вне диапазона [0, 1]

**Пример:**
```python
blue = Color(0, 0, 255)
light_blue = blue.lighten(0.3)  # Осветленный на 30% синий
```

---

#### darken()
```python
def darken(self, factor: float) -> "Color"
```
**Описание:** Затемняет цвет, смешивая его с черным цветом.

**Параметры:**
- `factor` - коэффициент затемнения (0.0 - исходный цвет, 1.0 - полностью черный)

**Возвращает:** Новый затемненный объект `Color`

**Исключения:**
- `ValueError` - если factor вне диапазона [0, 1]

**Пример:**
```python
red = Color(255, 0, 0)
dark_red = red.darken(0.4)  # Затемненный на 40% красный
```

---

#### lighten_hsv()
```python
def lighten_hsv(self, factor: float) -> "Color"
```
**Описание:** Осветляет цвет через увеличение Value компонента в HSV цветовом пространстве.

**Параметры:**
- `factor` - коэффициент осветления (0.0 - без изменений, 1.0 - максимальное осветление)

**Возвращает:** Новый цвет с увеличенной яркостью

**Исключения:**
- `ValueError` - если factor вне диапазона [0, 1]

> **💡 Применение:** Более естественное осветление по сравнению с обычным `lighten()`.

---

#### darken_hsv()
```python
def darken_hsv(self, factor: float) -> "Color"
```
**Описание:** Затемняет цвет через уменьшение Value компонента в HSV цветовом пространстве.

**Параметры:**
- `factor` - коэффициент затемнения (0.0 - без изменений, 1.0 - полное затемнение)

**Возвращает:** Новый цвет с уменьшенной яркостью

**Исключения:**
- `ValueError` - если factor вне диапазона [0, 1]

---

#### invert()
```python
def invert(self) -> "Color"
```
**Описание:** Инвертирует RGB компоненты цвета и возвращает новый объект Color.

**Возвращает:** Новый инвертированный объект `Color`

**Пример:**
```python
white = Color(255, 255, 255)
black = white.invert()  # Color(0, 0, 0, 255)
```

---

#### invert_this()
```python
def invert_this(self) -> "Color"
```
**Описание:** Инвертирует RGB компоненты данного цвета (изменяет текущий объект).

**Возвращает:** Текущий объект `Color` для цепочки вызовов

**Пример:**
```python
color = Color(255, 255, 255)
color.invert_this()  # Теперь color = Color(0, 0, 0, 255)
```

---

### Методы настройки альфа-канала

#### set_alpha()
```python
def set_alpha(self, a: int | float) -> "Color"
```
**Описание:** Устанавливает значение альфа-канала в диапазоне 0-255.

**Параметры:**
- `a` - новое значение альфа-канала (0-255)

**Возвращает:** Текущий объект `Color` для цепочки вызовов

**Исключения:**
- `ValueError` - если значение вне диапазона [0, 255]

**Пример:**
```python
color = Color(255, 0, 0).set_alpha(128)  # Полупрозрачный красный
```

---

#### set_alpha_float()
```python
def set_alpha_float(self, a: float) -> "Color"
```
**Описание:** Устанавливает альфа-канал в диапазоне 0.0-1.0.

**Параметры:**
- `a` - новое значение альфа-канала (0.0-1.0)

**Возвращает:** Текущий объект `Color` для цепочки вызовов

**Исключения:**
- `ValueError` - если значение вне диапазона [0.0, 1.0]

**Пример:**
```python
color = Color(0, 0, 255).set_alpha_float(0.5)  # 50% прозрачности
```

---

### Математические операции

#### __mul__() / mul()
```python
def __mul__(self, number: float | int) -> "Color"
def mul(self, number: float | int) -> "Color"
```
**Описание:** Умножает цвет на коэффициент. Положительные значения затемняют цвет, отрицательные - осветляют.

**Параметры:**
- `number` - коэффициент умножения (-1.0 до 1.0)

**Возвращает:** Новый объект `Color` - результат умножения

**Исключения:**
- `TypeError` - если коэффициент вне диапазона [-1.0, 1.0]

**Пример:**
```python
color = Color(100, 100, 100)
darker = color * 0.5      # Color(50, 50, 50, 100)
lighter = color * (-0.5)  # Color(178, 178, 178, 100)
```

---

### Свойства

#### rgb
```python
@property
def rgb(self) -> RGBColorAsArrayType
```
**Описание:** Возвращает RGB компоненты цвета в виде кортежа.

**Возвращает:** Кортеж `(r, g, b)`

**Пример:**
```python
color = Color(255, 128, 0)
print(color.rgb)  # (255, 128, 0)
```

---

#### rgba
```python
@property
def rgba(self) -> RGBAColorAsArrayType
```
**Описание:** Возвращает RGBA компоненты цвета в виде кортежа.

**Возвращает:** Кортеж `(r, g, b, a)`

**Пример:**
```python
color = Color(255, 0, 0, 128)
print(color.rgba)  # (255, 0, 0, 128)
```

---

#### hex
```python
@property
def hex(self) -> str
```
**Описание:** Возвращает HEX представление цвета в формате "#RRGGBB".

**Возвращает:** Строка в HEX формате

**Пример:**
```python
color = Color(255, 0, 0)
print(color.hex)  # "#ff0000"
```

---

## Класс BaseColorGradient

Простой градиент между двумя цветами для создания плавных переходов.

### Конструктор
```python
def __init__(self, color_1: Color, color_2: Color)
```
**Описание:** Создает базовый градиент между двумя цветами.

**Параметры:**
- `color_1` - начальный цвет градиента
- `color_2` - конечный цвет градиента

**Пример:**
```python
gradient = BaseColorGradient(COLOR_RED, COLOR_BLUE)
```

---

### Методы BaseColorGradient

#### get()
```python
def get(self, amount: float | int) -> Color
```
**Описание:** Возвращает промежуточный цвет градиента в указанной позиции.

**Параметры:**
- `amount` - позиция в градиенте (0.0 - начальный цвет, 1.0 - конечный цвет)

**Возвращает:** Промежуточный объект `Color`

**Исключения:**
- `ValueError` - если amount вне диапазона [0, 1]

**Пример:**
```python
gradient = BaseColorGradient(COLOR_RED, COLOR_BLUE)
middle_color = gradient.get(0.5)  # Цвет посередине градиента
```

---

#### get_color_1() / get_color_2()
```python
def get_color_1(self) -> Color
def get_color_2(self) -> Color
```
**Описание:** Возвращает начальный/конечный цвет градиента.

**Возвращает:** Объект `Color` - первый/второй цвет градиента

---

#### set_color_1() / set_color_2()
```python
def set_color_1(self, color: Color) -> "BaseColorGradient"
def set_color_2(self, color: Color) -> "BaseColorGradient"
```
**Описание:** Устанавливает начальный/конечный цвет градиента.

**Параметры:**
- `color` - новый цвет для установки

**Возвращает:** Текущий объект для цепочки вызовов

---

## Класс ColorGradient

Многоцветный градиент с равномерным распределением цветов.

### Конструктор
```python
def __init__(self, colors: ColorArrayType)
```
**Описание:** Создает многоцветный градиент из списка цветов.

**Параметры:**
- `colors` - список цветов для создания градиента (минимум 2 цвета)

**Исключения:**
- `ValueError` - если передано меньше 2 цветов

**Пример:**
```python
gradient = ColorGradient([COLOR_RED, COLOR_GREEN, COLOR_BLUE])
```

---

### Методы ColorGradient

#### get()
```python
def get(self, amount: float | int) -> Color
```
**Описание:** Возвращает цвет в указанной позиции многоцветного градиента.

**Параметры:**
- `amount` - позиция в градиенте (0.0 - начало, 1.0 - конец)

**Возвращает:** Цвет в указанной позиции

**Пример:**
```python
gradient = ColorGradient([COLOR_RED, COLOR_GREEN, COLOR_BLUE])
mid_color = gradient.get(0.5)  # Цвет в середине градиента
```

---

#### add_color()
```python
def add_color(self, color: Color) -> Self
```
**Описание:** Добавляет цвет в конец градиента.

**Параметры:**
- `color` - цвет для добавления

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
gradient.add_color(COLOR_PURPLE)
```

---

#### insert_color()
```python
def insert_color(self, index: int, color: Color) -> Self
```
**Описание:** Вставляет цвет в указанную позицию градиента.

**Параметры:**
- `index` - позиция для вставки
- `color` - цвет для вставки

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `IndexError` - если индекс вне допустимого диапазона

---

#### remove_color()
```python
def remove_color(self, index: int) -> Self
```
**Описание:** Удаляет цвет из градиента по индексу.

**Параметры:**
- `index` - индекс цвета для удаления

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `IndexError` - если индекс вне допустимого диапазона
- `ValueError` - если после удаления останется меньше 2 цветов

---

#### reverse()
```python
def reverse(self) -> Self
```
**Описание:** Обращает порядок цветов в градиенте.

**Возвращает:** Текущий объект для цепочки вызовов

---

#### to_list_rgba() / to_list_rgb()
```python
def to_list_rgba(self) -> RGBAColorsArrayType
def to_list_rgb(self) -> RGBColorsArrayType
```
**Описание:** Возвращает цвета градиента в формате RGBA/RGB.

**Возвращает:** Список кортежей с компонентами цветов

---

## Класс ColorGradientEx

Расширенный градиент с настраиваемыми длинами участков между цветами.

### Конструкторы

#### __init__()
```python
def __init__(self, colors: list[Color], lengths: list[float])
```
**Описание:** Инициализирует расширенный градиент с настраиваемыми длинами участков.

**Параметры:**
- `colors` - список цветов (минимум 2)
- `lengths` - список длин участков между цветами (сумма должна равняться 1.0)

**Исключения:**
- `ValueError` - если нарушены условия создания градиента

**Пример:**
```python
gradient = ColorGradientEx(
    [COLOR_RED, COLOR_GREEN, COLOR_BLUE],
    [0.3, 0.7]  # 30% красный->зеленый, 70% зеленый->синий
)
```

---

#### from_colors()
```python
@classmethod
def from_colors(cls, colors: list[Color]) -> "ColorGradientEx"
```
**Описание:** Создает градиент с равномерным распределением цветов.

**Параметры:**
- `colors` - список цветов Color

**Возвращает:** Градиент с равными промежутками между цветами

---

#### from_integers()
```python
@classmethod
def from_integers(cls, colors: list[int], lengths: list[int | float]) -> "ColorGradientEx"
```
**Описание:** Создает градиент из цветов с длинами участков, заданных в виде целых чисел.

**Параметры:**
- `colors` - список целочисленных значений цветов
- `lengths` - список длин участков между цветами

**Возвращает:** Новый экземпляр градиента

---

#### rainbow_gradient()
```python
@classmethod
def rainbow_gradient(cls) -> "ColorGradientEx"
```
**Описание:** Создает плавный радужный градиент с 13 цветами.

**Возвращает:** Градиент, содержащий все цвета радуги

**Пример:**
```python
rainbow = ColorGradientEx.rainbow_gradient()
```

---

## Функции модуля

### Работа с цветами

#### mix()
```python
def mix(color_1: Color, color_2: Color, amount: float | int) -> Color
```
**Описание:** Смешивает два цвета в заданной пропорции.

**Параметры:**
- `color_1` - первый цвет для смешивания
- `color_2` - второй цвет для смешивания
- `amount` - доля второго цвета (0.0 - color_1, 1.0 - color_2)

**Возвращает:** Новый цвет - результат смешивания

**Исключения:**
- `ValueError` - если amount вне диапазона [0, 1]

**Пример:**
```python
red = Color(255, 0, 0)
blue = Color(0, 0, 255)
purple = mix(red, blue, 0.5)  # Фиолетовый цвет
```

---

#### middle()
```python
def middle(color_1: Color, color_2: Color) -> Color
```
**Описание:** Находит средний цвет между двумя цветами.

**Параметры:**
- `color_1` - первый цвет
- `color_2` - второй цвет

**Возвращает:** Цвет, находящийся посередине между color_1 и color_2

**Пример:**
```python
black = Color(0, 0, 0)
white = Color(255, 255, 255)
gray = middle(black, white)  # Color(127, 127, 127, 255)
```

---

#### random_color_with_alpha()
```python
def random_color_with_alpha(alpha: int) -> Color
```
**Описание:** Возвращает случайный цвет с указанным альфа-каналом.

**Параметры:**
- `alpha` - значение альфа-канала (0-255)

**Возвращает:** Случайный цвет с заданной прозрачностью

**Исключения:**
- `ValueError` - если alpha вне диапазона [0, 255]

---

### Генерация палитр

#### generate_palette()
```python
def generate_palette(
    color: Color,
    scheme: Literal[...] = "complementary",
    num_colors: int = 5,
    saturation_range: tuple[float, float] = (0.7, 1.0),
    brightness_range: tuple[float, float] = (0.6, 0.9)
) -> ColorArrayType
```
**Описание:** Генерирует гармоничную цветовую палитру на основе базового цвета.

**Параметры:**
- `color` - базовый цвет для генерации палитры
- `scheme` - схема генерации (по умолчанию 'complementary')
- `num_colors` - количество цветов в палитре (2-5)
- `saturation_range` - диапазон насыщенности (0.0-1.0)
- `brightness_range` - диапазон яркости (0.0-1.0)

**Доступные схемы:**
- `"analogous"` - соседние цвета в цветовом круге (±30°)
- `"monochromatic"` - оттенки одного цвета
- `"complementary"` - основной цвет + его дополнение
- `"split_complementary"` - основной цвет + два соседних к дополнению
- `"triadic"` - три равноудаленных цвета (120°)
- `"tetradic"` - четыре цвета (две комплементарные пары)
- `"square"` - четыре цвета через 90°

**Возвращает:** Список сгенерированных цветов

**Исключения:**
- `ValueError` - если параметры выходят за допустимые диапазоны

**Пример:**
```python
# Триадная палитра из синего цвета
blue = Color(0, 0, 255)
palette = generate_palette(blue, scheme='triadic', num_colors=3)

# Монохроматическая палитра с 5 оттенками
red_palette = generate_palette(Color(255, 0, 0), 'monochromatic', 5)
```

---

### Анимационные функции

#### get_rainbow_with_time()
```python
def get_rainbow_with_time(time: float | int) -> Color
```
**Описание:** Возвращает цвет радуги, зависящий от времени для создания анимированных эффектов.

**Параметры:**
- `time` - временная координата

**Возвращает:** Цвет из радужного градиента

**Пример:**
```python
import time
animated_color = get_rainbow_with_time(time.time())
```

---

## Предустановленные цвета

### Основные цвета
```python
COLOR_RED: Final[Color] = Color(255, 0, 0)
COLOR_GREEN: Final[Color] = Color(0, 255, 0)
COLOR_BLUE: Final[Color] = Color(0, 0, 255)
COLOR_YELLOW: Final[Color] = Color(255, 255, 0)
COLOR_CYAN: Final[Color] = Color(0, 255, 255)
COLOR_MAGENTA: Final[Color] = Color(255, 0, 255)
COLOR_WHITE: Final[Color] = Color(255, 255, 255)
COLOR_BLACK: Final[Color] = Color(0, 0, 0)
```

### Дополнительные базовые цвета
```python
COLOR_ORANGE: Final[Color] = Color(255, 165, 0)
COLOR_PURPLE: Final[Color] = Color(128, 0, 128)
COLOR_PINK: Final[Color] = Color(255, 192, 203)
COLOR_BROWN: Final[Color] = Color(165, 42, 42)
COLOR_GRAY: Final[Color] = Color(128, 128, 128)
COLOR_LIGHT_GRAY: Final[Color] = Color(211, 211, 211)
COLOR_DARK_GRAY: Final[Color] = Color(169, 169, 169)
```

### Металлические цвета
```python
COLOR_GOLD: Final[Color] = Color(255, 215, 0)
COLOR_SILVER: Final[Color] = Color(192, 192, 192)
COLOR_BRONZE: Final[Color] = Color(205, 127, 50)
COLOR_ROSE_GOLD: Final[Color] = Color(183, 110, 121)
```

### Специальные цвета
```python
COLOR_ALPHA: Final[Color] = Color(0, 0, 0, 0)  # Полностью прозрачный
RAINBOW_GRADIENT: Final[ColorGradientEx] = ColorGradientEx.rainbow_gradient()
```

> **📚 Полный список:** Модуль содержит более 50 предустановленных цветов, включая оттенки синего, зеленого, красного, фиолетовые, коричневые тона, веб-безопасные и современные UI цвета.

---

## Примеры использования

### Базовая работа с цветами

```python
from PySGL.Colors import Color, COLOR_RED, COLOR_BLUE

# Создание цветов
red = Color(255, 0, 0)
semi_red = Color(255, 0, 0, 128)  # Полупрозрачный

# Трансформации
light_red = red.lighten(0.3)
dark_red = red.darken(0.5)
inverted = red.invert()

# Случайные цвета
random1 = Color.random()
random2 = Color.random_alpha()

# Цепочки вызовов
color = Color(100, 100, 100).lighten(0.2).set_alpha(200)
```

### Работа с градиентами

```python
from PySGL.Colors import BaseColorGradient, ColorGradient, ColorGradientEx

# Простой градиент
gradient = BaseColorGradient(COLOR_RED, COLOR_BLUE)
middle = gradient.get(0.5)

# Многоцветный градиент
multi_gradient = ColorGradient([COLOR_RED, COLOR_GREEN, COLOR_BLUE])
color_at_75 = multi_gradient.get(0.75)

# Расширенный градиент с настройкой длин
custom_gradient = ColorGradientEx(
    [COLOR_RED, COLOR_YELLOW, COLOR_GREEN],
    [0.2, 0.8]  # 20% красный->желтый, 80% желтый->зеленый
)

# Радужный градиент
rainbow = ColorGradientEx.rainbow_gradient()
rainbow_color = rainbow.get(0.33)
```

### Генерация палитр

```python
from PySGL.Colors import generate_palette

# Комплементарная палитра
base_color = Color(100, 150, 200)
complementary = generate_palette(
    base_color, 
    scheme='complementary', 
    num_colors=2
)

# Триадная палитра
triadic = generate_palette(
    base_color,
    scheme='triadic',
    num_colors=3
)

# Монохроматическая палитра с настройками
monochrome = generate_palette(
    base_color,
    scheme='monochromatic',
    num_colors=5,
    saturation_range=(0.5, 1.0),
    brightness_range=(0.3, 0.9)
)
```

### Смешивание и анимация

```python
from PySGL.Colors import mix, middle, get_rainbow_with_time
import time

# Смешивание цветов
color1 = Color(255, 0, 0)
color2 = Color(0, 0, 255)
mixed = mix(color1, color2, 0.3)  # 30% синего, 70% красного

# Средний цвет
average = middle(color1, color2)

# Анимированные цвета
animated_rainbow = get_rainbow_with_time(time.time())

# Создание анимированного градиента
def animate_gradient(t):
    return ColorGradient([
        get_rainbow_with_time(t),
        get_rainbow_with_time(t + 1),
        get_rainbow_with_time(t + 2)
    ])
```

### Практические применения

```python
# Создание темы интерфейса
primary = Color(52, 152, 219)    # Синий
secondary = primary.lighten(0.2)  # Светлее
accent = generate_palette(primary, 'complementary')[1]
background = Color(248, 249, 250)
text = Color(33, 37, 41)

# Градиент для кнопки
button_gradient = BaseColorGradient(
    primary,
    primary.darken(0.1)
)

# Статусные цвета
success = COLOR_GREEN.darken(0.2)
warning = COLOR_ORANGE
error = COLOR_RED.lighten(0.1)
info = COLOR_BLUE.lighten(0.3)

# Комбинированная обработка цветов
class ColorTheme:
    def __init__(self, base_color: Color):
        self.primary = base_color
        self.secondary = base_color.lighten(0.3)
        self.accent = generate_palette(base_color, 'complementary')[1]
        self.gradient = BaseColorGradient(self.primary, self.secondary)
    
    def get_variant(self, lightness: float) -> Color:
        if lightness > 0:
            return self.primary.lighten(lightness)
        else:
            return self.primary.darken(abs(lightness))
```

---

## Рекомендации по использованию

### Производительность

> **🚀 Оптимизация:** Используйте предустановленные цвета (COLOR_RED, COLOR_BLUE и т.д.) вместо создания новых объектов для базовых цветов.

> **💾 Память:** Создавайте градиенты заранее и переиспользуйте их, особенно для сложных ColorGradientEx.

### Цветовые схемы

> **🎨 Гармония:** Используйте `generate_palette()` для создания гармоничных цветовых схем вместо случайного подбора цветов.

> **🌈 Градиенты:** Для плавных переходов предпочитайте HSV методы (`lighten_hsv`, `darken_hsv`) обычным RGB трансформациям.

### Архитектура

> **🏗️ Структура:** Создавайте цветовые темы как отдельные классы для лучшей организации кода.

> **🔄 Анимация:** Используйте `get_rainbow_with_time()` для создания динамических цветовых эффектов.

### Отладка

> **🐛 Отладка:** Используйте свойство `hex` для вывода цветов в читаемом формате при отладке.

> **📊 Анализ:** Свойства `rgb` и `rgba` удобны для передачи цветов в другие библиотеки.

### Безопасность

> **⚠️ Исключения:** Всегда обрабатывайте `ValueError` при работе с пользовательским вводом цветовых параметров.

> **🔒 Валидация:** Проверяйте диапазоны значений перед передачей в методы трансформации цветов.

---

## Лицензия

MIT License - Copyright (c) 2025 Pavlov Ivan

Разрешается свободное использование, копирование, изменение и распространение при условии сохранения уведомления об авторских правах.