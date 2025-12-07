import ctypes
from typing import Self, Final, final

from Moon.python.Types import *
from Moon.python.Colors import *
from Moon.python.Vectors import Vector2f, Vector2i, Vector2Type, Vector2TypeTuple
from Moon.python.Rendering.Vertexes import Vertex2d, VertexList, VertexListTypes, NativeVertex2dPtr

from Moon.python.utils import find_library


# Загружаем DLL библиотеку
try:
    LIB_MOON: Final[ctypes.CDLL] = ctypes.CDLL(find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")

@final
class Polyline:
    """
    #### Класс для работы с ломаными линиями

    ---

    :Description:
    - Представляет собой последовательность соединенных отрезков
    - Использует примитив LineStrip для непрерывного отображения
    - Поддерживает динамическое добавление и удаление точек
    - Автоматическое управление вершинами через VertexList

    ---

    :Features:
    - Добавление точек в начало и конец ломаной
    - Глобальная установка цвета для всех сегментов
    - Получение количества точек и управление ими
    - Очистка и полное перестроение ломаной
    """

    def __init__(self):
        """
        #### Инициализирует новую ломаную линию

        ---

        :Description:
        - Создает пустой список вершин с типом примитива LineStrip
        - Устанавливает начальный цвет линии
        - Готовит структуру для последующего добавления точек

        ---

        :Initial State:
        - Пустой список вершин
        - Тип примитива: LineStrip (последовательные отрезки)
        - Цвет по умолчанию: черный
        """
        self.__vertex_list = VertexList()
        self.__vertex_list.set_primitive_type(VertexListTypes.LineStrip)

        self.__color = COLOR_BLACK
        self.__vertex_list.set_color(self.__color)

    def clear(self):
        """
        #### Полностью очищает ломаную линию

        ---

        :Description:
        - Удаляет все точки из ломаной
        - Сохраняет текущие настройки цвета и типа примитива
        - Подготавливает объект для построения новой ломаной

        ---

        :Example:
        ```python
        polyline = Polyline()
        polyline.append_point(Vector2f(0, 0))
        polyline.append_point(Vector2f(100, 0))
        # Теперь ломаная содержит 2 точки

        polyline.clear()
        # Ломаная полностью очищена, точек нет
        ```
        """
        self.__vertex_list.clear()

    def append_point(self, point: Vector2f):
        """
        #### Добавляет точку в конец ломаной

        ---

        :Description:
        - Создает новую вершину в указанной позиции
        - Добавляет вершину в конец списка вершин
        - Автоматически расширяет ломаную линию

        ---

        :Args:
        - point (Vector2f): Координаты новой точки

        ---

        :Example:
        ```python
        polyline = Polyline()
        polyline.append_point(Vector2f(0, 0))    # Начальная точка
        polyline.append_point(Vector2f(50, 50))  # Продолжение линии
        polyline.append_point(Vector2f(100, 0))  # Конечная точка
        ```

        :Note:
        - Первая добавленная точка становится началом ломаной
        - Каждая последующая точка соединяется с предыдущей отрезком
        """
        self.__vertex_list.append(Vertex2d().FromPosition(point))

    def prepend_point(self, point: Vector2f):
        """
        #### Добавляет точку в начало ломаной

        ---

        :Description:
        - Создает новую вершину в указанной позиции
        - Добавляет вершину в начало списка вершин
        - Сдвигает существующие точки вперед

        ---

        :Args:
        - point (Vector2f): Координаты новой точки

        ---

        :Example:
        ```python
        polyline = Polyline()
        polyline.append_point(Vector2f(100, 0))  # Исходная первая точка
        polyline.prepend_point(Vector2f(0, 0))   # Теперь (0,0) - начало
        # Ломаная: (0,0) -> (100,0)
        ```

        :Note:
        - Полезно для расширения ломаной в обратном направлении
        - Может быть менее эффективно при большом количестве точек
        """
        self.__vertex_list.prepend(Vertex2d().FromPosition(point))

    def set_global_color(self, color: Color):
        """
        #### Устанавливает глобальный цвет для всей ломаной

        ---

        :Description:
        - Применяет указанный цвет ко всем сегментам ломаной
        - Переопределяет индивидуальные цвета вершин
        - Немедленно обновляет отображение

        ---

        :Args:
        - color (Color): Новый цвет ломаной линии

        ---

        :Example:
        ```python
        polyline = Polyline()
        polyline.set_global_color(Color.RED)  # Вся ломаная станет красной
        ```

        :Note:
        - Глобальный цвет имеет приоритет над цветами отдельных вершин
        - Для разноцветной ломаной не используйте этот метод
        """
        self.__vertex_list.set_color(color)

    def get_global_color(self) -> Color:
        """
        #### Возвращает текущий глобальный цвет ломаной

        ---

        :Description:
        - Возвращает цвет, установленный через set_global_color()
        - Не отражает индивидуальные цвета вершин
        - None означает, что глобальный цвет не установлен

        ---

        :Returns:
        - Color: Текущий глобальный цвет или None

        ---

        :Example:
        ```python
        polyline = Polyline()
        polyline.set_global_color(Color.BLUE)
        color = polyline.get_global_color()  # Color.BLUE
        ```
        """
        return self.__color

    def get_points_count(self) -> int:
        """
        #### Возвращает количество точек в ломаной

        ---

        :Description:
        - Возвращает текущее количество вершин в ломаной
        - Для n точек будет (n-1) сегментов
        - Пустая ломаная возвращает 0

        ---

        :Returns:
        - int: Количество точек в ломаной

        ---

        :Example:
        ```python
        polyline = Polyline()
        polyline.append_point(Vector2f(0, 0))
        polyline.append_point(Vector2f(50, 50))
        count = polyline.get_points_count()  # 2
        ```
        """
        return self.__vertex_list.length()

    def remove_point(self, index: int):
        """
        #### Удаляет точку из ломаной по индексу

        ---

        :Description:
        - Удаляет вершину с указанным индексом
        - Автоматически перестраивает соединения между точками
        - Сдвигает индексы последующих точек

        ---

        :Args:
        - index (int): Индекс удаляемой точки (0-based)

        ---

        :Example:
        ```python
        polyline = Polyline()
        polyline.append_point(Vector2f(0, 0))
        polyline.append_point(Vector2f(50, 50))
        polyline.append_point(Vector2f(100, 0))
        # Ломаная: 0->50->100

        polyline.remove_point(1)
        # Теперь ломаная: 0->100
        ```

        :Raises:
        - IndexError: Если индекс вне диапазона [0, points_count-1]
        """
        self.__vertex_list.remove(index)

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

    def __repr__(self) -> str:
        """
        #### Возвращает строковое представление объекта

        ---

        :Description:
        - Предоставляет информативное описание ломаной
        - Включает количество точек для быстрой диагностики

        ---

        :Returns:
        - str: Строка в формате 'PolyLine(points:X)'

        ---

        :Example:
        ```python
        polyline = Polyline()
        polyline.append_point(Vector2f(0, 0))
        print(polyline)  # 'PolyLine(points:1)'
        ```
        """
        return f'PolyLine(points:{self.get_points_count()})'


@final
class LineShape:
    """
    #### Класс для работы с отдельными отрезками

    ---

    :Description:
    - Представляет собой одиночный отрезок между двумя точками
    - Использует примитив Lines для отображения одного отрезка
    - Поддерживает установку начальной и конечной точек
    - Оптимизирован для работы с отдельными линиями

    ---

    :Features:
    - Инициализация начальной и конечной точек
    - Индивидуальная настройка позиций концов отрезка
    - Глобальная установка цвета линии
    - Прямой доступ к вершинам отрезка
    """

    def __init__(self):
        """
        #### Инициализирует новый отрезок

        ---

        :Description:
        - Создает пустой список вершин с типом примитива Lines
        - Устанавливает начальный цвет отрезка
        - Подготавливает структуру для двух вершин (начало и конец)

        ---

        :Initial State:
        - Пустой список вершин
        - Тип примитива: Lines (отдельные отрезки)
        - Цвет по умолчанию: черный
        - Требует инициализации точек через init_points()
        """
        self.__vertex_array = VertexList()
        self.__vertex_array.set_primitive_type(VertexListTypes.Lines)
        self.__color = COLOR_BLACK
        self.__vertex_array.set_color(self.__color)

    def clear(self):
        """
        #### Очищает отрезок (удаляет все вершины)

        ---

        :Description:
        - Удаляет начальную и конечную точки отрезка
        - Сохраняет настройки цвета и типа примитива
        - Переводит отрезок в неинициализированное состояние

        ---

        :Example:
        ```python
        line = LineShape()
        line.init_points(Vector2f(0, 0), Vector2f(100, 100))
        line.clear()  # Теперь отрезок пуст
        ```

        :Note:
        - После clear() необходимо повторно вызвать init_points()
        - Без точек отрезок не будет отображаться
        """
        self.__vertex_array.clear()

    def set_global_color(self, color: Color) -> Self:
        """
        #### Устанавливает цвет отрезка

        ---

        :Description:
        - Применяет указанный цвет ко всему отрезку
        - Немедленно обновляет отображение
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - color (Color): Новый цвет отрезка

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        line = LineShape()
        line.init_points(Vector2f(0, 0), Vector2f(100, 100))
        line.set_global_color(Color.RED)  # Отрезок становится красным
        ```
        """
        self.__color = color
        self.__vertex_array.set_color(color)
        return self

    def get_global_color(self) -> Optional[Color]:
        """
        #### Возвращает текущий цвет отрезка

        ---

        :Description:
        - Возвращает цвет, установленный через set_global_color()
        - None означает, что цвет не установлен

        ---

        :Returns:
        - Optional[Color]: Текущий цвет отрезка или None

        ---

        :Example:
        ```python
        line = LineShape()
        line.set_global_color(Color.GREEN)
        color = line.get_global_color()  # Color.GREEN
        ```
        """
        return self.__color

    def init_points(self, point_1: Vector2Type = Vector2f.zero(), point_2: Vector2Type = Vector2f.zero()) -> Self:
        """
        #### Инициализирует начальную и конечную точки отрезка

        ---

        :Description:
        - Создает две вершины в указанных позициях
        - Автоматически добавляет вершины в массив
        - Подготавливает отрезок к отображению
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - point_1 (Vector2Type): Начальная точка отрезка (по умолчанию (0,0))
        - point_2 (Vector2Type): Конечная точка отрезка (по умолчанию (0,0))

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        line = LineShape()
        line.init_points(Vector2f(10, 10), Vector2f(200, 150))
        # Создан отрезок от (10,10) до (200,150)
        ```

        :Note:
        - Должен быть вызван перед использованием других методов
        - Точки можно изменить позже через set_start_position()/set_end_position()
        """
        self.__vertex_array.auto_append(Vertex2d().FromPosition(point_1))
        self.__vertex_array.auto_append(Vertex2d().FromPosition(point_2))
        return self

    def set_start_position(self, point: Vector2Type) -> Self:
        """
        #### Устанавливает позицию начальной точки отрезка

        ---

        :Description:
        - Обновляет координаты начальной точки
        - Немедленно обновляет отображение отрезка
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - point (Vector2Type): Новая позиция начальной точки

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        line = LineShape()
        line.init_points(Vector2f(0, 0), Vector2f(100, 100))
        line.set_start_position(Vector2f(50, 50))
        # Теперь отрезок от (50,50) до (100,100)
        ```

        :Note:
        - Требует предварительного вызова init_points()
        - Изменяет только начальную точку, конечная остается неизменной
        """
        self.__vertex_array.get(0).position = point
        return self

    def set_end_position(self, point: Vector2Type) -> Self:
        """
        #### Устанавливает позицию конечной точки отрезка

        ---

        :Description:
        - Обновляет координаты конечной точки
        - Немедленно обновляет отображение отрезка
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - point (Vector2Type): Новая позиция конечной точки

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        line = LineShape()
        line.init_points(Vector2f(0, 0), Vector2f(100, 100))
        line.set_end_position(Vector2f(200, 50))
        # Теперь отрезок от (0,0) до (200,50)
        ```

        :Note:
        - Требует предварительного вызова init_points()
        - Изменяет только конечную точку, начальная остается неизменной
        """
        self.__vertex_array.get(1).position = point
        return self

    def get_start_point(self) -> NativeVertex2dPtr:
        """
        #### Возвращает указатель на начальную точку отрезка

        ---

        :Description:
        - Предоставляет прямой доступ к вершине начальной точки
        - Позволяет модифицировать свойства вершины
        - Возвращает NativeVertex2dPtr для низкоуровневого доступа

        ---

        :Returns:
        - NativeVertex2dPtr: Указатель на вершину начальной точки

        ---

        :Example:
        ```python
        line = LineShape()
        line.init_points(Vector2f(0, 0), Vector2f(100, 100))
        start_vertex = line.get_start_point()
        start_vertex.color = Color.RED  # Изменяем цвет начальной точки
        ```

        :Note:
        - Изменения через указатель применяются немедленно
        - Будьте осторожны с модификацией позиции - используйте set_start_position()
        """
        return self.__vertex_array.get(0)

    def get_end_point(self) -> NativeVertex2dPtr:
        """
        #### Возвращает указатель на конечную точку отрезка

        ---

        :Description:
        - Предоставляет прямой доступ к вершине конечной точки
        - Позволяет модифицировать свойства вершины
        - Возвращает NativeVertex2dPtr для низкоуровневого доступа

        ---

        :Returns:
        - NativeVertex2dPtr: Указатель на вершину конечной точки

        ---

        :Example:
        ```python
        line = LineShape()
        line.init_points(Vector2f(0, 0), Vector2f(100, 100))
        end_vertex = line.get_end_point()
        end_vertex.color = Color.BLUE  # Изменяем цвет конечной точки
        ```

        :Note:
        - Изменения через указатель применяются немедленно
        - Будьте осторожны с модификацией позиции - используйте set_end_position()
        """
        return self.__vertex_array.get(1)

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
        - Используется системой рендеринга для отображения отрезка
        - Изменение указателя может привести к неопределенному поведению
        """
        return self.__vertex_array.get_ptr()
