# 🎨 Документация модуля Colors

## 📋 Содержание
- [Обзор модуля](#обзор-модуля)
- [Основные классы](#основные-классы)
  - [Color](#color)
  - [BaseColorGradient](#basecolorgradient)
  - [ColorGradient](#colorgradient)
  - [ColorGradientEx](#colorgradientex)
- [Функции модуля](#функции-модуля)
- [Предустановленные цвета](#предустановленные-цвета)
- [Примеры использования](#примеры-использования)

---

## 🎯 Обзор модуля

**Colors** - это мощный модуль для работы с цветами в PySGL, предоставляющий полный набор инструментов для создания, манипуляции и преобразования цветов.

### ✨ Ключевые возможности:
- **🎨 Полноценная работа с цветами**: RGB/RGBA форматы, преобразования между цветовыми пространствами
- **🌈 Расширенные возможности**: Гармоничные палитры, плавные градиенты, математические операции
- **⚡ Оптимизированные алгоритмы**: Быстрые преобразования и эффективное смешивание цветов
- **🎭 Готовые интерфейсы**: Базовые и расширенные классы для всех потребностей
- **🎪 Встроенные палитры**: От базовых RGB до современных UI цветов

### 📦 Зависимости:
- Python 3.8+
- Стандартные библиотеки: `math`, `random`, `colorsys`

---

## 🏗️ Основные классы

### 🎨 Color

**Основной класс для работы с цветами в формате RGBA**

#### 🔧 Конструктор
```python
Color(r: int, g: int, b: int, a: int = 255)
```

**Параметры:**
- `r` - Красный компонент (0-255)
- `g` - Зеленый компонент (0-255) 
- `b` - Синий компонент (0-255)
- `a` - Альфа-канал/прозрачность (0-255, по умолчанию 255)

#### 🎲 Статические методы

##### `Color.random() -> Color`
**Генерирует случайный непрозрачный цвет**
```python
random_color = Color.random()  # Например: Color(123, 45, 67, 255)
```

##### `Color.random_alpha() -> Color`
**Генерирует случайный цвет со случайной прозрачностью**
```python
transparent_color = Color.random_alpha()  # Например: Color(123, 45, 67, 128)
```

#### 🎭 Методы трансформации

##### `lighten(factor: float) -> Color`
**Осветляет цвет смешиванием с белым**
- `factor` - Коэффициент осветления (0.0-1.0)
```python
blue = Color(0, 0, 255)
light_blue = blue.lighten(0.3)  # Осветленный на 30%
```

##### `darken(factor: float) -> Color`
**Затемняет цвет смешиванием с черным**
- `factor` - Коэффициент затемнения (0.0-1.0)
```python
red = Color(255, 0, 0)
dark_red = red.darken(0.4)  # Затемненный на 40%
```

##### `lighten_hsv(factor: float) -> Color`
**Осветляет через увеличение Value в HSV пространстве**
```python
green = Color(0, 128, 0)
bright_green = green.lighten_hsv(0.5)
```

##### `darken_hsv(factor: float) -> Color`
**Затемняет через уменьшение Value в HSV пространстве**
```python
yellow = Color(255, 255, 0)
dark_yellow = yellow.darken_hsv(0.6)
```

##### `invert() -> Color`
**Возвращает инвертированный цвет (новый объект)**
```python
white = Color(255, 255, 255)
black = white.invert()  # Color(0, 0, 0)
```

##### `invert_this() -> Color`
**Инвертирует текущий цвет (изменяет объект)**
```python
color = Color(255, 255, 255)
color.invert_this()  # Теперь color = Color(0, 0, 0)
```

#### 🔧 Методы настройки

##### `set_alpha(a: int | float) -> Color`
**Устанавливает альфа-канал (0-255)**
```python
color = Color(255, 0, 0).set_alpha(128)  # Полупрозрачный красный
```

##### `set_alpha_float(a: float) -> Color`
**Устанавливает альфа-канал в диапазоне 0.0-1.0**
```python
color = Color(0, 0, 255).set_alpha_float(0.5)  # 50% прозрачности
```

#### 🧮 Математические операции

##### `__mul__(number: float) -> Color` / `mul(number: float) -> Color`
**Умножение цвета на коэффициент (-1.0 до 1.0)**
- Положительные значения затемняют
- Отрицательные значения осветляют
```python
color = Color(100, 100, 100)
darker = color * 0.5      # Color(50, 50, 50)
lighter = color * (-0.5)  # Color(178, 178, 178)
```

#### 📊 Свойства

##### `rgb -> tuple[int, int, int]`
**Возвращает RGB компоненты**
```python
color = Color(255, 128, 0)
print(color.rgb)  # (255, 128, 0)
```

##### `rgba -> tuple[int, int, int, int]`
**Возвращает RGBA компоненты**
```python
color = Color(255, 0, 0, 128)
print(color.rgba)  # (255, 0, 0, 128)
```

##### `hex -> str`
**Возвращает HEX представление**
```python
color = Color(255, 0, 0)
print(color.hex)  # "#ff0000"
```

---

### 🌈 BaseColorGradient

**Простой градиент между двумя цветами**

#### 🔧 Конструктор
```python
BaseColorGradient(color_1: Color, color_2: Color)
```

#### 🎨 Основные методы

##### `get(amount: float) -> Color`
**Получает промежуточный цвет градиента**
- `amount` - Позиция в градиенте (0.0 - начало, 1.0 - конец)
```python
gradient = BaseColorGradient(COLOR_RED, COLOR_BLUE)
middle_color = gradient.get(0.5)  # Цвет посередине
```

##### `get_color_1() -> Color` / `get_color_2() -> Color`
**Получение начального/конечного цвета**

##### `set_color_1(color: Color)` / `set_color_2(color: Color)`
**Установка начального/конечного цвета**

---

### 🎭 ColorGradient

**Многоцветный градиент с равномерным распределением**

#### 🔧 Конструктор
```python
ColorGradient(colors: list[Color])
```
**Требует минимум 2 цвета**

#### 🎨 Основные методы

##### `get(amount: float) -> Color`
**Получает цвет в указанной позиции градиента**
```python
gradient = ColorGradient([COLOR_RED, COLOR_GREEN, COLOR_BLUE])
color = gradient.get(0.5)  # Цвет в середине градиента
```

##### `add_color(color: Color) -> ColorGradient`
**Добавляет цвет в конец градиента**
```python
gradient.add_color(COLOR_PURPLE)
```

##### `insert_color(index: int, color: Color) -> ColorGradient`
**Вставляет цвет в указанную позицию**
```python
gradient.insert_color(1, COLOR_YELLOW)
```

##### `remove_color(index: int) -> ColorGradient`
**Удаляет цвет по индексу**
```python
gradient.remove_color(0)  # Удаляет первый цвет
```

##### `reverse() -> ColorGradient`
**Обращает порядок цветов**
```python
gradient.reverse()
```

#### 📊 Методы экспорта

##### `to_list_rgba() -> list[tuple[int, int, int, int]]`
**Экспорт в формате RGBA**

##### `to_list_rgb() -> list[tuple[int, int, int]]`
**Экспорт в формате RGB**

---

### 🚀 ColorGradientEx

**Расширенный градиент с настраиваемыми длинами участков**

#### 🔧 Конструкторы

##### `__init__(colors: list[Color], lengths: list[float])`
**Создание с настраиваемыми длинами**
- `lengths` - Длины участков (сумма должна равняться 1.0)
```python
gradient = ColorGradientEx(
    [COLOR_RED, COLOR_GREEN, COLOR_BLUE],
    [0.3, 0.7]  # 30% красный->зеленый, 70% зеленый->синий
)
```

##### `from_colors(colors: list[Color]) -> ColorGradientEx`
**Создание с равномерным распределением**
```python
gradient = ColorGradientEx.from_colors([COLOR_RED, COLOR_GREEN, COLOR_BLUE])
```

##### `from_integers(colors: list[int], lengths: list[int]) -> ColorGradientEx`
**Создание из целочисленных значений**
```python
gradient = ColorGradientEx.from_integers(
    [COLOR_RED, COLOR_GREEN, COLOR_BLACK],
    [200, 100]  # Пропорциональные длины
)
```

##### `rainbow_gradient() -> ColorGradientEx`
**Создание радужного градиента**
```python
rainbow = ColorGradientEx.rainbow_gradient()
```

#### 🎨 Расширенные методы

##### `add_color(color: Color, length: float) -> ColorGradientEx`
**Добавляет цвет с указанной длиной участка**
```python
gradient.add_color(COLOR_PURPLE, 0.2)
```

##### `insert_color(index: int, color: Color, length: float) -> ColorGradientEx`
**Вставляет цвет с длиной в указанную позицию**
```python
gradient.insert_color(1, COLOR_YELLOW, 0.15)
```

##### `get_lengths() -> list[float]`
**Возвращает длины участков**

---

## 🛠️ Функции модуля

### 🎨 Работа с цветами

##### `mix(color_1: Color, color_2: Color, amount: float) -> Color`
**Смешивает два цвета в заданной пропорции**
- `amount` - Доля второго цвета (0.0-1.0)
```python
red = Color(255, 0, 0)
blue = Color(0, 0, 255)
purple = mix(red, blue, 0.5)  # Фиолетовый
```

##### `middle(color_1: Color, color_2: Color) -> Color`
**Находит средний цвет между двумя цветами**
```python
black = Color(0, 0, 0)
white = Color(255, 255, 255)
gray = middle(black, white)  # Color(127, 127, 127)
```

##### `random_color_with_alpha(alpha: int) -> Color`
**Генерирует случайный цвет с указанным альфа-каналом**
```python
semi_transparent = random_color_with_alpha(128)
```

### 🌈 Палитры и схемы

##### `generate_palette(color: Color, scheme: str, num_colors: int, ...) -> list[Color]`
**Генерирует гармоничную цветовую палитру**

**Доступные схемы:**
- `"analogous"` - Соседние цвета (±30°)
- `"monochromatic"` - Оттенки одного цвета
- `"complementary"` - Основной + дополнительный
- `"split_complementary"` - Основной + два соседних к дополнению
- `"triadic"` - Три равноудаленных цвета (120°)
- `"tetradic"` - Четыре цвета (две комплементарные пары)
- `"square"` - Четыре цвета через 90°

```python
# Триадная палитра из синего
blue = Color(0, 0, 255)
palette = generate_palette(blue, scheme='triadic', num_colors=3)

# Монохроматическая палитра
red_shades = generate_palette(Color(255, 0, 0), 'monochromatic', 5)
```

### ⏰ Анимационные функции

##### `get_rainbow_with_time(time: float) -> Color`
**Возвращает цвет радуги, зависящий от времени**
```python
import time
animated_color = get_rainbow_with_time(time.time())
```

---

## 🎨 Предустановленные цвета

### 🔴 Основные цвета
```python
COLOR_RED, COLOR_GREEN, COLOR_BLUE
COLOR_YELLOW, COLOR_CYAN, COLOR_MAGENTA
COLOR_WHITE, COLOR_BLACK
```

### 🟠 Дополнительные базовые
```python
COLOR_ORANGE, COLOR_PURPLE, COLOR_PINK
COLOR_BROWN, COLOR_GRAY, COLOR_LIGHT_GRAY, COLOR_DARK_GRAY
```

### ✨ Металлические
```python
COLOR_GOLD, COLOR_SILVER, COLOR_BRONZE, COLOR_ROSE_GOLD
```

### 🔵 Оттенки синего
```python
COLOR_NAVY, COLOR_DARK_BLUE, COLOR_MIDNIGHT_BLUE
COLOR_ROYAL_BLUE, COLOR_STEEL_BLUE, COLOR_SKY_BLUE, COLOR_LIGHT_BLUE
```

### 🟢 Оттенки зеленого
```python
COLOR_LIME, COLOR_FOREST_GREEN, COLOR_OLIVE, COLOR_DARK_GREEN
COLOR_SEA_GREEN, COLOR_SPRING_GREEN, COLOR_EMERALD
```

### 🔴 Оттенки красного
```python
COLOR_DARK_RED, COLOR_CRIMSON, COLOR_FIREBRICK
COLOR_TOMATO, COLOR_SALMON, COLOR_LIGHT_CORAL
```

### 🟣 Фиолетовые оттенки
```python
COLOR_INDIGO, COLOR_DARK_VIOLET, COLOR_ORCHID
COLOR_PLUM, COLOR_THISTLE
```

### 🟤 Коричневые тона
```python
COLOR_SIENNA, COLOR_CHOCOLATE, COLOR_SANDY_BROWN
COLOR_BURLYWOOD, COLOR_TAN, COLOR_BEIGE
```

### 🌊 Специальные цвета
```python
COLOR_TEAL, COLOR_AQUA, COLOR_TURQUOISE
COLOR_LAVENDER, COLOR_MINT, COLOR_IVORY
COLOR_SNOW, COLOR_HONEYDEW
```

### 🌐 Веб-безопасные
```python
COLOR_WEB_GRAY, COLOR_WEB_MAROON, COLOR_WEB_OLIVE
COLOR_WEB_GREEN, COLOR_WEB_PURPLE, COLOR_WEB_NAVY
```

### 💻 Современные UI
```python
COLOR_SLATE, COLOR_GHOST_WHITE, COLOR_ALICE_BLUE
COLOR_AZURE, COLOR_CORAL, COLOR_VIOLET_RED
```

### 👻 Специальные
```python
COLOR_ALPHA  # Полностью прозрачный цвет (0, 0, 0, 0)
RAINBOW_GRADIENT  # Готовый радужный градиент
```

---

## 💡 Примеры использования

### 🎨 Базовая работа с цветами
```python
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
```

### 🌈 Работа с градиентами
```python
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

### 🎭 Генерация палитр
```python
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

### 🎪 Смешивание и анимация
```python
# Смешивание цветов
color1 = Color(255, 0, 0)
color2 = Color(0, 0, 255)
mixed = mix(color1, color2, 0.3)  # 30% синего, 70% красного

# Анимированные цвета
import time
animated_rainbow = get_rainbow_with_time(time.time())

# Создание анимированного градиента
def animate_gradient(t):
    return ColorGradient([
        get_rainbow_with_time(t),
        get_rainbow_with_time(t + 1),
        get_rainbow_with_time(t + 2)
    ])
```

### 🔧 Практические применения
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
```

---

## ⚠️ Важные замечания

### 🎯 Диапазоны значений
- **RGB компоненты**: 0-255
- **Альфа-канал**: 0-255 (0 = прозрачный, 255 = непрозрачный)
- **Коэффициенты**: 0.0-1.0 для большинства операций
- **Умножение цвета**: -1.0 до 1.0

### 🔄 Цепочки вызовов
Многие методы возвращают `self`, позволяя создавать цепочки:
```python
color = Color(100, 100, 100).lighten(0.2).set_alpha(200)
```

### 🎨 Цветовые пространства
- Основная работа в **RGB**
- HSV преобразования для `lighten_hsv`/`darken_hsv`
- Поддержка **HEX** формата через свойство `hex`

### ⚡ Производительность
- Все операции оптимизированы для быстрого выполнения
- Градиенты кэшируют промежуточные вычисления
- Предустановленные цвета - константы для экономии памяти

---

*Документация модуля Colors v1.0.3 | PySGL Framework*