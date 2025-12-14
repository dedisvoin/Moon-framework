import ctypes
from typing import Self, Final, final

from Moon.python.Types import *
from Moon.python.Colors import *
from Moon.python.Vectors import Vector2f, Vector2Type
from Moon.python.Rendering.Vertexes import Vertex2d, VertexList, VertexListTypes, NativeVertex2dPtr

from Moon.python.utils import find_library


# Загружаем DLL библиотеку
try:
    LIB_MOON: Final[ctypes.CDLL] = ctypes.CDLL(find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")


@final
class PolygonShape:
    """
    #### Класс для работы с многоугольниками

    ---

    :Description:
    - Представляет собой замкнутую фигуру из трех и более вершин
    - Использует примитив TriangleFan для заполнения многоугольника
    - Поддерживает динамическое добавление и удаление вершин
    - Автоматически генерирует треугольный веер для отрисовки

    ---

    :Features:
    - Добавление вершин в конец многоугольника
    - Вставка вершин в произвольную позицию
    - Удаление вершин по индексу
    - Установка цвета заполнения многоугольника
    - Проверка выпуклости многоугольника
    - Расчет площади и периметра
    """

    def __init__(self):
        """
        #### Инициализирует новый многоугольник

        ---

        :Description:
        - Создает пустой список вершин с типом примитива TriangleFan
        - Устанавливает начальный цвет заполнения
        - Инициализирует список вершин для отрисовки

        ---

        :Initial State:
        - Пустой список вершин
        - Тип примитива: TriangleFan (треугольный веер)
        - Цвет по умолчанию: белый
        """
        self.__vertex_list = VertexList()
        self.__vertex_list.set_primitive_type(VertexListTypes.TriangleFan)
        
        self.__fill_color = COLOR_WHITE
        
        self.__vertex_list.set_color(self.__fill_color)

    def get_ptr(self) -> ctypes.c_void_p:
        """
        #### Возвращает указатель на нативный объект вершин

        ---

        :Description:
        - Предоставляет доступ к низкоуровневому объекту вершин
        - Для внутреннего использования в системе рендеринга
        - Не предназначен для прямого манипулирования

        ---

        :Returns:
        - ctypes.c_void_p: Указатель на нативный VertexList

        ---

        :Note:
        - Используется системой рендеринга для отображения
        - Изменение указателя может привести к неопределенному поведению
        """
        return self.__vertex_list.get_ptr()

    def clear(self) -> Self:
        """
        #### Полностью очищает многоугольник

        ---

        :Description:
        - Удаляет все вершины из многоугольника
        - Сохраняет текущий цвет заполнения
        - Подготавливает объект для построения нового многоугольника

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.add_vertex(Vector2f(0, 0))
        polygon.add_vertex(Vector2f(100, 0))
        polygon.add_vertex(Vector2f(50, 100))
        # Многоугольник содержит 3 вершины

        polygon.clear()
        # Многоугольник полностью очищен
        ```
        """
        self.__vertex_list.clear()
        return self

    def add_vertex(self, point: Vector2Type) -> Self:
        """
        #### Добавляет вершину в конец многоугольника

        ---

        :Description:
        - Создает новую вершину в указанной позиции
        - Добавляет вершину в конец списка вершин
        - Автоматически обновляет треугольный веер для отрисовки
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - point (Vector2Type): Координаты новой вершины

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.add_vertex(Vector2f(0, 0))      # Вершина 1 (центр веера)
        polygon.add_vertex(Vector2f(100, 0))    # Вершина 2
        polygon.add_vertex(Vector2f(50, 100))   # Вершина 3
        # Создан треугольник
        ```

        :Note:
        - Первая добавленная вершина становится центром треугольного веера
        - Минимальное количество вершин для отрисовки - 3
        - Для корректного заполнения вершины должны добавляться по порядку обхода
        """
        self.__vertex_list.append(Vertex2d().FromPositionAndColor(point, self.__fill_color))
        return self

    def insert_vertex(self, index: int, point: Vector2Type) -> Self:
        """
        #### Вставляет вершину в указанную позицию

        ---

        :Description:
        - Создает новую вершину в указанной позиции
        - Вставляет вершину на указанный индекс
        - Сдвигает последующие вершины
        - Автоматически обновляет треугольный веер
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - index (int): Индекс для вставки (0-based)
        - point (Vector2Type): Координаты новой вершины

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.add_vertex(Vector2f(0, 0))
        polygon.add_vertex(Vector2f(100, 0))
        polygon.add_vertex(Vector2f(100, 100))
        # Многоугольник с тремя вершинами

        polygon.insert_vertex(1, Vector2f(50, 0))
        # Теперь вершина (50,0) на позиции 1
        ```

        :Raises:
        - IndexError: Если индекс вне диапазона [0, vertex_count]
        """
        self.__vertex_list.insert(index, Vertex2d().FromPositionAndColor(point, self.__fill_color))
        return self

    def remove_vertex(self, index: int) -> Self:
        """
        #### Удаляет вершину по индексу

        ---

        :Description:
        - Удаляет вершину с указанным индексом
        - Автоматически перестраивает треугольный веер
        - Сдвигает индексы последующих вершин
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - index (int): Индекс удаляемой вершины (0-based)

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.add_vertex(Vector2f(0, 0))
        polygon.add_vertex(Vector2f(100, 0))
        polygon.add_vertex(Vector2f(50, 100))
        polygon.add_vertex(Vector2f(0, 100))
        # Четырехугольник

        polygon.remove_vertex(2)
        # Теперь треугольник
        ```

        :Raises:
        - IndexError: Если индекс вне диапазона [0, vertex_count-1]
        """
        self.__vertex_list.remove(index)
        return self

    def set_global_color(self, color: Color) -> Self:
        """
        #### Устанавливает глобальный цвет заполнения многоугольника

        ---

        :Description:
        - Применяет указанный цвет ко всему многоугольнику
        - Немедленно обновляет отображение
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - color (Color): Новый цвет заполнения

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.add_vertex(Vector2f(0, 0))
        polygon.add_vertex(Vector2f(100, 0))
        polygon.add_vertex(Vector2f(50, 100))
        polygon.set_fill_color(Color.RED)  # Многоугольник становится красным
        ```

        ---

        :Note:
        - Цвет применяется ко всему многоугольнику равномерно
        - Для градиентной заливки нужно модифицировать отдельные вершины
        """
        self.__fill_color = color
        self.__vertex_list.set_color(color)
        return self

    def get_global_color(self) -> Color:
        """
        #### Возвращает глобальный цвет заполнения (не цвет вершин)

        ---

        :Description:
        - Возвращает цвет, установленный через set_fill_color()

        ---

        :Returns:
        - Color: Текущий цвет заполнения

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.set_fill_color(Color.BLUE)
        color = polygon.get_fill_color()  # Color.BLUE
        ```
        """
        return self.__fill_color

    def get_vertex_count(self) -> int:
        """
        #### Возвращает количество вершин в многоугольнике

        ---

        :Description:
        - Возвращает текущее количество вершин
        - Минимальное значение: 0 (пустой многоугольник)
        - Для отображения требуется минимум 3 вершины

        ---

        :Returns:
        - int: Количество вершин

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.add_vertex(Vector2f(0, 0))
        polygon.add_vertex(Vector2f(100, 0))
        polygon.add_vertex(Vector2f(50, 100))
        count = polygon.get_vertex_count()  # 3
        ```
        """
        return self.__vertex_list.length()

    def get_vertex(self, index: int) -> NativeVertex2dPtr:
        """
        #### Возвращает указатель на вершину по индексу

        ---

        :Description:
        - Предоставляет прямой доступ к вершине многоугольника
        - Позволяет модифицировать свойства вершины (позицию, цвет, текстурные координаты)
        - Возвращает NativeVertex2dPtr для низкоуровневого доступа
        - Поддерживает fluent-интерфейс при модификации

        ---

        :Args:
        - index (int): Индекс вершины (0-based)

        ---

        :Returns:
        - NativeVertex2dPtr: Указатель на вершину

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.add_vertex(Vector2f(0, 0))
        polygon.add_vertex(Vector2f(100, 0))
        
        # Изменяем позицию первой вершины
        polygon.get_vertex(0).position = Vector2f(50, 50)
        
        # Изменяем цвет второй вершины (для градиента)
        polygon.get_vertex(1).color = Color.RED
        ```

        ---

        :Raises:
        - IndexError: Если индекс вне диапазона [0, vertex_count-1]
        """
        return self.__vertex_list.get(index)

    def set_vertex_color(self, index: int, color: Color) -> Self:
        """
        #### Устанавливает цвет отдельной вершины

        ---

        :Description:
        - Устанавливает цвет для конкретной вершины многоугольника
        - Позволяет создавать градиентные заливки
        - Немедленно обновляет отображение
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - index (int): Индекс вершины (0-based)
        - color (Color): Новый цвет вершины

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.add_vertex(Vector2f(0, 0))
        polygon.add_vertex(Vector2f(100, 0))
        polygon.add_vertex(Vector2f(50, 100))
        
        # Создаем градиент от красного к синему
        polygon.set_vertex_color(0, Color.RED)
        polygon.set_vertex_color(1, Color.GREEN)
        polygon.set_vertex_color(2, Color.BLUE)
        ```

        ---
        
        :Raises:
        - IndexError: Если индекс вне диапазона [0, vertex_count-1]
        """
        self.get_vertex(index).color = color
        return self

    def set_all_vertices_colors(self, colors: list[Color]) -> Self:
        """
        #### Устанавливает цвета для всех вершин

        ---

        :Description:
        - Устанавливает цвета для всех вершин многоугольника
        - Количество цветов должно совпадать с количеством вершин
        - Позволяет создавать сложные градиентные эффекты
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - colors (List[Color]): Список цветов для каждой вершины

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.add_vertex(Vector2f(0, 0))
        polygon.add_vertex(Vector2f(100, 0))
        polygon.add_vertex(Vector2f(50, 100))
        
        # Устанавливаем цвета для всех вершин
        polygon.set_all_vertices_colors([
            Color.RED,
            Color.GREEN,
            Color.BLUE
        ])
        ```

        :Raises:
        - ValueError: Если количество цветов не совпадает с количеством вершин
        """
        vertex_count = self.get_vertex_count()
        if len(colors) != vertex_count:
            raise ValueError(f"Expected {vertex_count} colors, got {len(colors)}")
            
        for i in range(vertex_count):
            self.get_vertex(i).color = colors[i]
            
        return self

    def __repr__(self) -> str:
        """
        #### Возвращает строковое представление объекта

        ---

        :Description:
        - Предоставляет информативное описание многоугольника
        - Включает количество вершин для быстрой диагностики

        ---

        :Returns:
        - str: Строка в формате 'PolygonShape(vertices:X)'

        ---

        :Example:
        ```python
        polygon = PolygonShape()
        polygon.add_vertex(Vector2f(0, 0))
        polygon.add_vertex(Vector2f(100, 0))
        print(polygon)  # 'PolygonShape(vertices:2)'
        ```
        """
        return f'PolygonShape(vertices:{self.get_vertex_count()})'