# Документация модуля Shaders

## Обзор

Модуль `Shaders` предоставляет мощную систему работы с шейдерными программами в библиотеке PySGL. Он обеспечивает полный набор инструментов для загрузки, компиляции и управления шейдерами с высокой производительностью и простотой использования.

**Версия:** 1.0.0  
**Автор:** Павлов Иван (Pavlov Ivan)  
**Лицензия:** MIT  
**Реализация:** 100%

## Основные возможности

- ✅ **Полная поддержка OpenGL шейдеров** - вершинные, фрагментные и геометрические шейдеры
- ✅ **Высокопроизводительная компиляция** - нативная реализация на C++ с Python API
- ✅ **Гибкая загрузка** - из строк, файлов или по отдельным типам
- ✅ **Управление uniform переменными** - автоматическое определение типов данных
- ✅ **Поддержка всех типов данных** - скаляры, векторы, цвета, текстуры
- ✅ **Интеграция с системой рендеринга** - прямая совместимость с Window.draw()

## Требования

- Python 3.8+
- Нативная библиотека PySGL.dll
- Модули: `ctypes`, `typing`
- Зависимости: `PySGL.python.Types`, `PySGL.python.Colors`, `PySGL.python.Vectors`
- OpenGL 3.3+ совместимый драйвер

---

## Архитектура модуля

### Нативная интеграция
Модуль использует прямую интеграцию с C++ библиотекой через `ctypes` для максимальной производительности компиляции и выполнения шейдеров.

### Типы указателей
```python
ShaderPtr: Final[ctypes.c_void_p] = ctypes.c_void_p
```

### Загрузка библиотеки
```python
def _find_library() -> str
```
**Описание:** Автоматически находит и загружает нативную библиотеку PySGL.dll.

**Исключения:**
- `LibraryLoadError` - если библиотека не найдена

---

## Класс Shader

Основной класс для работы с шейдерными программами OpenGL.

### Вложенный класс Type

Перечисление типов шейдеров:

```python
class Type(Enum):
    VERTEX = 0      # Вершинный шейдер
    GEOMETRY = 1    # Геометрический шейдер  
    FRAGMENT = 2    # Фрагментный шейдер
```

**Описание:** Определяет тип шейдера для компиляции отдельных компонентов программы.

---

### Конструктор

```python
def __init__(self) -> None
```

**Описание:** Создает пустой объект шейдера с нативным указателем.

**Особенности:**
- Инициализирует внутренние переменные для хранения данных
- Шейдер готов к загрузке исходного кода
- После создания необходимо загрузить шейдерный код

**Пример:**
```python
shader = Shader()
```

---

### Методы управления uniform переменными

#### set_uniform()

```python
def set_uniform(self, name: str, value: int | float | bool | Vector2i | Vector2f | Color | ctypes.c_void_p) -> "Shader"
```

**Описание:** Устанавливает значение uniform переменной в шейдере.

**Параметры:**
- `name` - имя uniform переменной в шейдере
- `value` - значение для установки

**Поддерживаемые типы:**
- `int` - целое число (uniform int)
- `float` - дробное число (uniform float)  
- `bool` - логическое значение (uniform bool)
- `Vector2i` - вектор из двух целых чисел (uniform ivec2)
- `Vector2f` - вектор из двух дробных чисел (uniform vec2)
- `Color` - цвет RGBA (uniform vec4)
- `ctypes.c_void_p` - указатель на текстуру (uniform sampler2D)

**Возвращает:** Текущий объект для цепочки вызовов

**Исключения:**
- `TypeError` - при передаче неподдерживаемого типа данных

**Пример:**
```python
shader.set_uniform("u_time", 1.5)  # float
shader.set_uniform("u_resolution", Vector2f(800, 600))  # vec2
shader.set_uniform("u_color", Color(255, 0, 0))  # vec4
shader.set_uniform("u_texture", texture_ptr)  # sampler2D
shader.set_uniform("u_enabled", True)  # bool
```

---

### Методы доступа к указателю

#### get_ptr()

```python
def get_ptr(self) -> ShaderPtr
```

**Описание:** Возвращает указатель на нативный объект шейдера.

**Особенности:**
- Предоставляет доступ к внутреннему указателю для системы рендеринга
- Используется методом Window.draw() для применения шейдера
- Не предназначен для прямого использования пользователем

**Возвращает:** Указатель на нативный объект шейдера

#### set_ptr()

```python
def set_ptr(self, ptr: ShaderPtr) -> "Shader"
```

**Описание:** Устанавливает указатель на нативный объект шейдера.

**Параметры:**
- `ptr` - новый указатель на нативный объект

**Возвращает:** Текущий объект для цепочки вызовов

**Предупреждение:**
- Неправильное использование может привести к ошибкам
- Убедитесь, что указатель валиден

---

### Методы загрузки шейдеров

#### load_from_type()

```python
def load_from_type(self, type: Type, source: str) -> bool
```

**Описание:** Загружает шейдер определенного типа из строки.

**Параметры:**
- `type` - тип шейдера (VERTEX, GEOMETRY, FRAGMENT)
- `source` - исходный код шейдера на GLSL

**Возвращает:** True если компиляция успешна, False при ошибке

**Пример:**
```python
vertex_code = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos, 1.0);
}
"""

success = shader.load_from_type(Shader.Type.VERTEX, vertex_code)
if not success:
    print("Ошибка компиляции вершинного шейдера")
```

#### load_from_strings()

```python
def load_from_strings(self, fragment: str, vertex: str) -> "Shader"
```

**Описание:** Загружает шейдерную программу из строк с исходным кодом.

**Параметры:**
- `fragment` - исходный код фрагментного шейдера
- `vertex` - исходный код вершинного шейдера

**Возвращает:** Текущий объект для цепочки вызовов

**Особенности:**
- Компилирует и линкует полную шейдерную программу
- Сохраняет исходный код во внутренних переменных для отладки
- Автоматически создает готовую к использованию программу

**Пример:**
```python
shader = Shader()
shader.load_from_strings(fragment_code, vertex_code)

# Или через цепочку вызовов
shader = Shader().load_from_strings(fragment_code, vertex_code)
```

#### load_from_files()

```python
def load_from_files(self, fragment_path: str, vertex_path: str) -> "Shader"
```

**Описание:** Загружает шейдерную программу из файлов.

**Параметры:**
- `fragment_path` - путь к файлу фрагментного шейдера
- `vertex_path` - путь к файлу вершинного шейдера

**Возвращает:** Текущий объект для цепочки вызовов

**Особенности:**
- Читает исходный код шейдеров из указанных файлов
- Сохраняет пути к файлам и содержимое для отладки
- Компилирует и линкует полную шейдерную программу

**Исключения:**
- `FileNotFoundError` - если один из файлов не найден
- `IOError` - при ошибке чтения файлов
- `UnicodeDecodeError` - при проблемах с кодировкой файлов

**Пример:**
```python
shader = Shader()
shader.load_from_files("shaders/basic.frag", "shaders/basic.vert")

# Проверка загруженных путей
print(f"Fragment: {shader._Shader__fragment_path}")
print(f"Vertex: {shader._Shader__vertex_path}")
```

---

## Примеры использования

### Базовый шейдер

```python
from PySGL.python.Rendering.Shaders import Shader
from PySGL.python.Colors import Color
from PySGL.python.Vectors import Vector2f

# Простой вершинный шейдер
vertex_shader = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;

out vec2 TexCoord;

void main() {
    gl_Position = vec4(aPos, 1.0);
    TexCoord = aTexCoord;
}
"""

# Простой фрагментный шейдер
fragment_shader = """
#version 330 core
out vec4 FragColor;

in vec2 TexCoord;
uniform vec4 u_color;
uniform float u_time;

void main() {
    float pulse = sin(u_time * 2.0) * 0.5 + 0.5;
    FragColor = u_color * pulse;
}
"""

# Создание и загрузка шейдера
shader = Shader()
shader.load_from_strings(fragment_shader, vertex_shader)

# Установка uniform переменных
shader.set_uniform("u_color", Color(255, 100, 50))
shader.set_uniform("u_time", 0.0)
```

### Шейдер с текстурой

```python
# Фрагментный шейдер с текстурой
texture_fragment = """
#version 330 core
out vec4 FragColor;

in vec2 TexCoord;
uniform sampler2D u_texture;
uniform vec2 u_resolution;
uniform float u_time;

void main() {
    vec2 uv = TexCoord;
    
    // Волновой эффект
    uv.x += sin(uv.y * 10.0 + u_time) * 0.01;
    
    vec4 texColor = texture(u_texture, uv);
    FragColor = texColor;
}
"""

shader = Shader()
shader.load_from_strings(texture_fragment, vertex_shader)

# Установка текстуры и параметров
shader.set_uniform("u_texture", texture.get_ptr())
shader.set_uniform("u_resolution", Vector2f(800, 600))
shader.set_uniform("u_time", current_time)
```

### Загрузка из файлов

```python
# Создание файлов шейдеров
vertex_file_content = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec4 aColor;

out vec4 vertexColor;
uniform mat4 u_transform;

void main() {
    gl_Position = u_transform * vec4(aPos, 1.0);
    vertexColor = aColor;
}
"""

fragment_file_content = """
#version 330 core
out vec4 FragColor;

in vec4 vertexColor;
uniform float u_alpha;

void main() {
    FragColor = vec4(vertexColor.rgb, vertexColor.a * u_alpha);
}
"""

# Сохранение в файлы
with open("shaders/vertex.vert", "w") as f:
    f.write(vertex_file_content)

with open("shaders/fragment.frag", "w") as f:
    f.write(fragment_file_content)

# Загрузка из файлов
shader = Shader()
shader.load_from_files("shaders/fragment.frag", "shaders/vertex.vert")
shader.set_uniform("u_alpha", 0.8)
```

### Анимированный шейдер

```python
import time
import math

class AnimatedShader:
    def __init__(self):
        self.shader = Shader()
        
        # Анимированный фрагментный шейдер
        animated_fragment = """
        #version 330 core
        out vec4 FragColor;
        
        in vec2 TexCoord;
        uniform float u_time;
        uniform vec2 u_resolution;
        uniform vec3 u_color1;
        uniform vec3 u_color2;
        
        void main() {
            vec2 uv = TexCoord;
            
            // Создание градиента с анимацией
            float gradient = sin(uv.x * 3.14159 + u_time) * 0.5 + 0.5;
            
            // Интерполяция между цветами
            vec3 color = mix(u_color1, u_color2, gradient);
            
            // Пульсация яркости
            float pulse = sin(u_time * 2.0) * 0.3 + 0.7;
            
            FragColor = vec4(color * pulse, 1.0);
        }
        """
        
        self.shader.load_from_strings(animated_fragment, vertex_shader)
        
        # Установка базовых цветов
        self.shader.set_uniform("u_color1", Vector2f(1.0, 0.2, 0.3))  # Красный
        self.shader.set_uniform("u_color2", Vector2f(0.2, 0.3, 1.0))  # Синий
        
    def update(self, delta_time):
        current_time = time.time()
        self.shader.set_uniform("u_time", current_time)
        
    def get_shader(self):
        return self.shader

# Использование
animated = AnimatedShader()

# В игровом цикле
while running:
    animated.update(delta_time)
    
    # Применение шейдера при отрисовке
    window.draw(some_shape, shader=animated.get_shader())
```

### Постобработка

```python
class PostProcessShader:
    def __init__(self):
        self.shader = Shader()
        
        # Шейдер постобработки
        postprocess_fragment = """
        #version 330 core
        out vec4 FragColor;
        
        in vec2 TexCoord;
        uniform sampler2D u_screenTexture;
        uniform float u_brightness;
        uniform float u_contrast;
        uniform float u_saturation;
        
        vec3 rgb2hsv(vec3 c) {
            vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
            vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
            vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
            
            float d = q.x - min(q.w, q.y);
            float e = 1.0e-10;
            return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
        }
        
        vec3 hsv2rgb(vec3 c) {
            vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
            vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
            return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
        }
        
        void main() {
            vec4 texColor = texture(u_screenTexture, TexCoord);
            
            // Яркость
            texColor.rgb += u_brightness;
            
            // Контрастность
            texColor.rgb = (texColor.rgb - 0.5) * u_contrast + 0.5;
            
            // Насыщенность
            vec3 hsv = rgb2hsv(texColor.rgb);
            hsv.y *= u_saturation;
            texColor.rgb = hsv2rgb(hsv);
            
            FragColor = texColor;
        }
        """
        
        self.shader.load_from_strings(postprocess_fragment, vertex_shader)
        
        # Установка значений по умолчанию
        self.set_brightness(0.0)
        self.set_contrast(1.0)
        self.set_saturation(1.0)
    
    def set_brightness(self, brightness: float):
        self.shader.set_uniform("u_brightness", brightness)
        return self
    
    def set_contrast(self, contrast: float):
        self.shader.set_uniform("u_contrast", contrast)
        return self
    
    def set_saturation(self, saturation: float):
        self.shader.set_uniform("u_saturation", saturation)
        return self

# Использование
postprocess = PostProcessShader()
postprocess.set_brightness(0.1).set_contrast(1.2).set_saturation(1.3)
```

### Управление несколькими шейдерами

```python
class ShaderManager:
    def __init__(self):
        self.shaders = {}
        self.current_shader = None
        
    def load_shader(self, name: str, fragment_path: str, vertex_path: str):
        shader = Shader()
        shader.load_from_files(fragment_path, vertex_path)
        self.shaders[name] = shader
        return shader
    
    def load_shader_from_strings(self, name: str, fragment: str, vertex: str):
        shader = Shader()
        shader.load_from_strings(fragment, vertex)
        self.shaders[name] = shader
        return shader
    
    def get_shader(self, name: str) -> Shader:
        return self.shaders.get(name)
    
    def use_shader(self, name: str):
        self.current_shader = self.shaders.get(name)
        return self.current_shader
    
    def set_uniform_all(self, name: str, value):
        """Устанавливает uniform во всех шейдерах"""
        for shader in self.shaders.values():
            try:
                shader.set_uniform(name, value)
            except:
                pass  # Игнорируем шейдеры без этого uniform
    
    def reload_shader(self, name: str):
        """Перезагружает шейдер из файлов"""
        if name in self.shaders:
            shader = self.shaders[name]
            # Предполагаем, что пути сохранены
            if hasattr(shader, '_Shader__fragment_path'):
                shader.load_from_files(
                    shader._Shader__fragment_path,
                    shader._Shader__vertex_path
                )

# Использование
manager = ShaderManager()

# Загрузка различных шейдеров
manager.load_shader("basic", "shaders/basic.frag", "shaders/basic.vert")
manager.load_shader("textured", "shaders/texture.frag", "shaders/texture.vert")
manager.load_shader("animated", "shaders/animated.frag", "shaders/animated.vert")

# Установка общих uniform переменных
manager.set_uniform_all("u_resolution", Vector2f(800, 600))
manager.set_uniform_all("u_time", current_time)

# Использование конкретного шейдера
basic_shader = manager.use_shader("basic")
window.draw(rectangle, shader=basic_shader)
```

---

## Рекомендации по использованию

### Производительность

> **🚀 Компиляция:** Компилируйте шейдеры один раз при инициализации, избегайте повторной компиляции в игровом цикле.

> **💾 Uniform переменные:** Обновляйте только изменившиеся uniform переменные, избегайте установки одинаковых значений.

> **⚡ Кэширование:** Используйте менеджер шейдеров для кэширования и переиспользования шейдерных программ.

### Отладка шейдеров

> **🐛 Ошибки компиляции:** Проверяйте возвращаемое значение load_from_type() для обнаружения ошибок компиляции.

> **📝 Логирование:** Сохраняйте исходный код шейдеров для отладки и горячей перезагрузки.

> **🔍 Валидация:** Используйте простые тестовые шейдеры для проверки корректности uniform переменных.

### Архитектура

> **🏗️ Модульность:** Разделяйте сложные шейдеры на отдельные файлы для лучшей поддерживаемости.

> **🔧 Конфигурация:** Используйте #define директивы для создания вариантов шейдеров.

> **📦 Ресурсы:** Организуйте шейдеры в отдельной папке с понятной структурой.

### Совместимость

> **🎯 Версии OpenGL:** Указывайте корректную версию GLSL в директиве #version.

> **🔗 Атрибуты:** Используйте layout qualifiers для явного указания расположения атрибутов.

> **📊 Типы данных:** Соблюдайте соответствие между Python типами и GLSL uniform типами.

### Оптимизация шейдеров

> **⚡ Вычисления:** Выполняйте сложные вычисления в вершинном шейдере когда возможно.

> **🎨 Текстуры:** Используйте подходящие форматы текстур для uniform sampler2D.

> **🔄 Циклы:** Избегайте динамических циклов в фрагментных шейдерах.

---

## Лицензия

MIT License - Copyright (c) 2025 Pavlov Ivan

Разрешается свободное использование, копирование, изменение и распространение при условии сохранения уведомления об авторских правах.