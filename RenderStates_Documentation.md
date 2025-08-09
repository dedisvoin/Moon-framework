# Документация модуля RenderStates

## Обзор

Модуль `RenderStates` предоставляет мощную систему управления состояниями рендеринга в библиотеке PySGL. Он позволяет контролировать способы смешивания пикселей, применение шейдеров и другие параметры отрисовки для создания разнообразных визуальных эффектов.

**Версия:** 1.0.0  
**Автор:** Павлов Иван (Pavlov Ivan)  
**Лицензия:** MIT  
**Реализация:** 100%

## Основные возможности

- ✅ **Режимы смешивания пикселей** - полный контроль над тем, как новые пиксели комбинируются с существующими
- ✅ **Готовые пресеты эффектов** - предустановленные режимы для популярных визуальных эффектов
- ✅ **Пользовательские режимы** - создание собственных алгоритмов смешивания
- ✅ **Интеграция с шейдерами** - применение пользовательских шейдеров к объектам
- ✅ **Высокая производительность** - оптимизированная работа с GPU через нативный код
- ✅ **Fluent API** - удобные цепочки вызовов для настройки состояний

## Требования

- Python 3.8+
- Нативная библиотека PySGL.dll
- Модули: `ctypes`, `os`, `typing`
- Зависимости: `PySGL.python.Rendering.Shaders`

---

## Архитектура модуля

### Нативная интеграция
Модуль использует прямую интеграцию с C++ библиотекой через `ctypes` для обеспечения максимальной производительности рендеринга на GPU.

### Загрузка библиотеки
```python
def _find_library() -> str
```
**Описание:** Автоматически находит и загружает нативную библиотеку PySGL.dll.

**Исключения:**
- `LibraryLoadError` - если библиотека не найдена

---

## Класс BlendMode

Основной класс для управления режимами смешивания пикселей с полной настройкой факторов и уравнений.

### Вложенные классы

#### Factor
```python
class Factor:
    Zero = 0             # (0, 0, 0, 0) - Полностью игнорировать компонент
    One = 1              # (1, 1, 1, 1) - Использовать компонент полностью
    SrcColor = 2         # (src.r, src.g, src.b, src.a) - Цвет источника
    OneMinusSrcColor = 3 # (1, 1, 1, 1) - (src.r, src.g, src.b, src.a) - Инверсия цвета источника
    DstColor = 4         # (dst.r, dst.g, dst.b, dst.a) - Цвет назначения
    OneMinusDstColor = 5 # (1, 1, 1, 1) - (dst.r, dst.g, dst.b, dst.a) - Инверсия цвета назначения
    SrcAlpha = 6         # (src.a, src.a, src.a, src.a) - Альфа источника
    OneMinusSrcAlpha = 7 # (1, 1, 1, 1) - (src.a, src.a, src.a, src.a) - Инверсия альфы источника
    DstAlpha = 8         # (dst.a, dst.a, dst.a, dst.a) - Альфа назначения
    OneMinusDstAlpha = 9 # (1, 1, 1, 1) - (dst.a, dst.a, dst.a, dst.a) - Инверсия альфы назначения
```
**Описание:** Факторы определяют, как исходный (src) и целевой (dst) цвета влияют на результат смешивания.

#### Equation
```python
class Equation:
    Add = 0             # Pixel = Src * SrcFactor + Dst * DstFactor - Сложение
    Subtract = 1        # Pixel = Src * SrcFactor - Dst * DstFactor - Вычитание
    ReverseSubtract = 2 # Pixel = Dst * DstFactor - Src * SrcFactor - Обратное вычитание
    Min = 3             # Pixel = min(Dst, Src) - Минимальное значение
    Max = 4             # Pixel = max(Dst, Src) - Максимальное значение
```
**Описание:** Уравнения определяют математическую операцию между исходным и целевым цветами после применения факторов.

---

### Конструктор
```python
def __init__(self, color_src_factor: Factor, color_dst_factor: Factor, color_eq: Equation,
             alpha_src_factor: Factor, alpha_dst_factor: Factor, alpha_eq: Equation)
```
**Описание:** Создает пользовательский режим смешивания с полным контролем над параметрами.

**Параметры:**
- `color_src_factor` - фактор для исходного цвета
- `color_dst_factor` - фактор для целевого цвета  
- `color_eq` - уравнение смешивания цветов
- `alpha_src_factor` - фактор для исходной альфы
- `alpha_dst_factor` - фактор для целевой альфы
- `alpha_eq` - уравнение смешивания альфы

**Пример:**
```python
# Пользовательский режим смешивания
custom_blend = BlendMode(
    BlendMode.Factor.SrcAlpha, BlendMode.Factor.OneMinusSrcAlpha, BlendMode.Equation.Add,
    BlendMode.Factor.One, BlendMode.Factor.Zero, BlendMode.Equation.Add
)
```

---

## Готовые пресеты BlendMode

### Alpha() - Стандартное альфа-смешивание
```python
@staticmethod
def Alpha() -> BlendMode
```
**Описание:** Самый распространенный режим смешивания для прозрачности.

**Формула:**
- Color: `Src * SrcAlpha + Dst * (1 - SrcAlpha)`
- Alpha: `SrcAlpha + DstAlpha * (1 - SrcAlpha)`

**Применение:**
- Обычная отрисовка спрайтов с прозрачностью
- UI элементы с полупрозрачным фоном
- Частицы и эффекты с плавным затуханием

**Пример:**
```python
states = RenderStates().set_blend_mode(BlendMode.Alpha())
window.draw(sprite, states)
```

---

### Add() - Аддитивное смешивание
```python
@staticmethod
def Add() -> BlendMode
```
**Описание:** Цвета складываются, создавая эффект свечения.

**Формула:**
- Color: `Src + Dst`
- Alpha: `SrcAlpha + DstAlpha`

**Применение:**
- Эффекты огня, взрывов, магии
- Световые лучи и блики
- Неоновые эффекты и голограммы
- Частицы искр и звезд

**Пример:**
```python
# Эффект огня
fire_states = RenderStates().set_blend_mode(BlendMode.Add())
window.draw(fire_particle, fire_states)
```

---

### Multiply() - Мультипликативное смешивание
```python
@staticmethod
def Multiply() -> BlendMode
```
**Описание:** Цвета перемножаются, создавая эффект затемнения.

**Формула:**
- Color: `Src * Dst`
- Alpha: `SrcAlpha * DstAlpha`

**Применение:**
- Эффекты теней и затемнения
- Наложение текстур освещения
- Создание силуэтов
- Эффекты дыма и тумана

**Пример:**
```python
# Эффект тени
shadow_states = RenderStates().set_blend_mode(BlendMode.Multiply())
window.draw(shadow_sprite, shadow_states)
```

---

### Screen() - Экранное смешивание
```python
@staticmethod
def Screen() -> BlendMode
```
**Описание:** Инверсия мультипликативного смешивания, осветляет изображение.

**Формула:**
- Color: `1 - (1 - Src) * (1 - Dst)` = `Src + Dst - Src * Dst`

**Применение:**
- Эффекты освещения и бликов
- Осветление темных областей
- Имитация передержки фотографии
- Мягкие световые эффекты

**Пример:**
```python
# Мягкое освещение
light_states = RenderStates().set_blend_mode(BlendMode.Screen())
window.draw(light_source, light_states)
```

---

### Lighten() / Darken() - Осветление/Затемнение
```python
@staticmethod
def Lighten() -> BlendMode
@staticmethod
def Darken() -> BlendMode
```
**Описание:** Выбирает более светлый/темный цвет из источника и назначения.

**Формула:**
- Lighten: `max(Src, Dst)`
- Darken: `min(Src, Dst)`

**Применение:**
- Наложение световых/теневых эффектов
- Сохранение ярких/темных деталей
- Эффекты молний/поглощения света

---

### Subtract() - Субтрактивное смешивание
```python
@staticmethod
def Subtract() -> BlendMode
```
**Описание:** Цвета вычитаются из существующих пикселей.

**Формула:**
- Color: `Dst - Src`
- Alpha: `DstAlpha - SrcAlpha`

**Применение:**
- Эффекты разрушения и коррозии
- Художественные фильтры
- Эффекты "выжигания" лазером
- Создание масок и вырезов

---

### None_() - Отсутствие смешивания
```python
@staticmethod
def None_() -> BlendMode
```
**Описание:** Новые пиксели полностью заменяют существующие.

**Формула:**
- Color: `Src`
- Alpha: `SrcAlpha`

**Применение:**
- Отрисовка непрозрачных объектов
- Фоновые изображения
- Оптимизация производительности
- Отладка рендеринга

---

## Класс RenderStates

Основной класс для управления состояниями рендеринга, объединяющий режимы смешивания и шейдеры.

### Конструктор
```python
def __init__(self)
```
**Описание:** Создает новый объект состояний рендеринга с параметрами по умолчанию.

**Пример:**
```python
states = RenderStates()
```

---

### Методы управления состояниями

#### set_blend_mode()
```python
def set_blend_mode(self, blend_mode: BlendMode) -> Self
```
**Описание:** Устанавливает режим смешивания для рендеринга.

**Параметры:**
- `blend_mode` - режим смешивания пикселей

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
# Использование готового пресета
states = RenderStates().set_blend_mode(BlendMode.Add())

# Создание пользовательского режима
custom_blend = BlendMode(
    BlendMode.Factor.SrcAlpha, BlendMode.Factor.One, BlendMode.Equation.Add,
    BlendMode.Factor.One, BlendMode.Factor.Zero, BlendMode.Equation.Add
)
states = RenderStates().set_blend_mode(custom_blend)
```

#### set_shader()
```python
def set_shader(self, shader: Shader) -> Self
```
**Описание:** Устанавливает шейдер для применения к объектам.

**Параметры:**
- `shader` - объект шейдера для применения

**Возвращает:** Текущий объект для цепочки вызовов

**Пример:**
```python
shader = Shader.FromFile("vertex.glsl", "fragment.glsl")
states = RenderStates().set_shader(shader)
```

---

### Методы доступа к данным

#### get_blend_mode() / get_shader()
```python
def get_blend_mode(self) -> BlendMode
def get_shader(self) -> Shader
```
**Описание:** Возвращают текущий режим смешивания/шейдер.

#### get_ptr()
```python
def get_ptr(self) -> RenderStatesPtr
```
**Описание:** Возвращает указатель на нативный объект для интеграции с C++.

---

## Примеры использования

### Базовые эффекты

```python
from PySGL.python.Rendering.RenderStates import *

# Стандартная прозрачность
alpha_states = RenderStates().set_blend_mode(BlendMode.Alpha())
window.draw(transparent_sprite, alpha_states)

# Эффект свечения
glow_states = RenderStates().set_blend_mode(BlendMode.Add())
window.draw(glow_effect, glow_states)

# Тени и затемнение
shadow_states = RenderStates().set_blend_mode(BlendMode.Multiply())
window.draw(shadow, shadow_states)
```

### Сложные визуальные эффекты

```python
class VisualEffects:
    def __init__(self):
        # Различные состояния для разных эффектов
        self.fire_states = RenderStates().set_blend_mode(BlendMode.Add())
        self.smoke_states = RenderStates().set_blend_mode(BlendMode.Multiply())
        self.light_states = RenderStates().set_blend_mode(BlendMode.Screen())
        self.magic_states = RenderStates().set_blend_mode(BlendMode.Lighten())
        
    def draw_fire_effect(self, window, particles):
        """Отрисовка эффекта огня с аддитивным смешиванием"""
        for particle in particles:
            window.draw(particle, self.fire_states)
    
    def draw_lighting(self, window, light_sources):
        """Отрисовка освещения с экранным смешиванием"""
        for light in light_sources:
            window.draw(light, self.light_states)
    
    def draw_shadows(self, window, shadow_casters):
        """Отрисовка теней с мультипликативным смешиванием"""
        for shadow in shadow_casters:
            window.draw(shadow, self.smoke_states)

# Использование
effects = VisualEffects()
effects.draw_fire_effect(window, fire_particles)
effects.draw_lighting(window, lights)
effects.draw_shadows(window, shadows)
```

### Пользовательские режимы смешивания

```python
class CustomBlendModes:
    @staticmethod
    def soft_light():
        """Мягкое освещение - комбинация Screen и Multiply"""
        return BlendMode(
            BlendMode.Factor.DstColor, BlendMode.Factor.SrcColor, BlendMode.Equation.Add,
            BlendMode.Factor.DstAlpha, BlendMode.Factor.SrcAlpha, BlendMode.Equation.Add
        )
    
    @staticmethod
    def color_dodge():
        """Осветление цвета - интенсивное осветление"""
        return BlendMode(
            BlendMode.Factor.One, BlendMode.Factor.OneMinusSrcColor, BlendMode.Equation.Add,
            BlendMode.Factor.One, BlendMode.Factor.OneMinusSrcAlpha, BlendMode.Equation.Add
        )
    
    @staticmethod
    def overlay():
        """Наложение - комбинация Screen и Multiply в зависимости от яркости"""
        return BlendMode(
            BlendMode.Factor.DstColor, BlendMode.Factor.SrcColor, BlendMode.Equation.Add,
            BlendMode.Factor.One, BlendMode.Factor.OneMinusSrcAlpha, BlendMode.Equation.Add
        )

# Использование пользовательских режимов
soft_light_states = RenderStates().set_blend_mode(CustomBlendModes.soft_light())
window.draw(soft_light_effect, soft_light_states)
```

### Комбинирование с шейдерами

```python
class ShaderEffects:
    def __init__(self):
        # Загрузка шейдеров
        self.distortion_shader = Shader.FromFile("distortion.vert", "distortion.frag")
        self.glow_shader = Shader.FromFile("glow.vert", "glow.frag")
        
        # Создание состояний с шейдерами и режимами смешивания
        self.distortion_states = RenderStates()\
            .set_shader(self.distortion_shader)\
            .set_blend_mode(BlendMode.Alpha())
            
        self.glow_states = RenderStates()\
            .set_shader(self.glow_shader)\
            .set_blend_mode(BlendMode.Add())
    
    def draw_distorted_sprite(self, window, sprite, time):
        """Отрисовка искаженного спрайта"""
        self.distortion_shader.set_uniform("time", time)
        window.draw(sprite, self.distortion_states)
    
    def draw_glowing_effect(self, window, effect, intensity):
        """Отрисовка светящегося эффекта"""
        self.glow_shader.set_uniform("intensity", intensity)
        window.draw(effect, self.glow_states)

# Использование
shader_effects = ShaderEffects()
shader_effects.draw_distorted_sprite(window, sprite, current_time)
shader_effects.draw_glowing_effect(window, glow_effect, 0.8)
```

### Оптимизация производительности

```python
class RenderStateManager:
    def __init__(self):
        # Предварительно созданные состояния для избежания аллокаций
        self.states_cache = {
            'alpha': RenderStates().set_blend_mode(BlendMode.Alpha()),
            'add': RenderStates().set_blend_mode(BlendMode.Add()),
            'multiply': RenderStates().set_blend_mode(BlendMode.Multiply()),
            'screen': RenderStates().set_blend_mode(BlendMode.Screen()),
            'none': RenderStates().set_blend_mode(BlendMode.None_())
        }
        
        self.current_state = None
    
    def get_states(self, blend_type: str) -> RenderStates:
        """Получение кэшированных состояний"""
        return self.states_cache.get(blend_type, self.states_cache['alpha'])
    
    def batch_draw_with_states(self, window, objects_by_blend):
        """Батчевая отрисовка с группировкой по состояниям"""
        for blend_type, objects in objects_by_blend.items():
            states = self.get_states(blend_type)
            for obj in objects:
                window.draw(obj, states)

# Использование для оптимизации
manager = RenderStateManager()

# Группировка объектов по типу смешивания
objects_by_blend = {
    'alpha': [ui_elements, transparent_sprites],
    'add': [fire_effects, light_beams],
    'multiply': [shadows, dark_overlays],
    'screen': [highlights, bright_effects]
}

manager.batch_draw_with_states(window, objects_by_blend)
```

### Создание анимированных эффектов

```python
import math
import time

class AnimatedBlendEffects:
    def __init__(self):
        self.time = 0
        self.base_states = RenderStates()
        
    def update(self, dt):
        self.time += dt
    
    def draw_pulsing_glow(self, window, sprite):
        """Пульсирующее свечение с изменяющейся интенсивностью"""
        # Создаем пульсирующий эффект через изменение режима смешивания
        pulse = (math.sin(self.time * 3) + 1) * 0.5  # 0..1
        
        if pulse > 0.5:
            # Яркая фаза - аддитивное смешивание
            states = RenderStates().set_blend_mode(BlendMode.Add())
        else:
            # Тусклая фаза - обычное альфа-смешивание
            states = RenderStates().set_blend_mode(BlendMode.Alpha())
        
        window.draw(sprite, states)
    
    def draw_dissolve_effect(self, window, sprite, dissolve_amount):
        """Эффект растворения через субтрактивное смешивание"""
        if dissolve_amount > 0:
            states = RenderStates().set_blend_mode(BlendMode.Subtract())
        else:
            states = RenderStates().set_blend_mode(BlendMode.Alpha())
        
        window.draw(sprite, states)

# Использование в игровом цикле
animated_effects = AnimatedBlendEffects()

while window.is_open():
    dt = clock.restart().as_seconds()
    animated_effects.update(dt)
    
    window.clear()
    animated_effects.draw_pulsing_glow(window, glow_sprite)
    animated_effects.draw_dissolve_effect(window, dissolving_sprite, dissolve_progress)
    window.display()
```

---

## Рекомендации по использованию

### Производительность

> **🚀 Оптимизация:** Группируйте объекты по типу состояний рендеринга для минимизации переключений GPU.

> **💾 Кэширование:** Создавайте состояния заранее и переиспользуйте их вместо создания новых в каждом кадре.

> **⚡ Батчинг:** Отрисовывайте объекты с одинаковыми состояниями последовательно для лучшей производительности.

### Выбор режимов смешивания

> **🎨 Эффекты:**
> - `Alpha()` - для обычных спрайтов и UI
> - `Add()` - для огня, света, магии
> - `Multiply()` - для теней, затемнения
> - `Screen()` - для мягкого освещения
> - `None_()` - для фонов и оптимизации

> **🔬 Эксперименты:** Комбинируйте разные режимы для создания уникальных эффектов.

### Интеграция с шейдерами

> **🎯 Комбинирование:** Используйте шейдеры совместно с режимами смешивания для максимального контроля над рендерингом.

> **🔄 Порядок применения:** Шейдеры применяются перед смешиванием пикселей.

### Отладка и тестирование

> **🐛 Отладка:** Используйте режим `None_()` для отладки проблем с прозрачностью.

> **📊 Профилирование:** Мониторьте количество переключений состояний рендеринга.

### Архитектура

> **🏗️ Менеджеры:** Создавайте менеджеры состояний для централизованного управления.

> **🎭 Эффекты:** Группируйте связанные эффекты в отдельные классы.

### Математика смешивания

> **📐 Понимание:** Изучите математику за режимами смешивания для создания пользовательских эффектов.

> **🧮 Формулы:** Экспериментируйте с различными комбинациями факторов и уравнений.

---

## Лицензия

MIT License - Copyright (c) 2025 Pavlov Ivan

Разрешается свободное использование, копирование, изменение и распространение при условии сохранения уведомления об авторских правах.