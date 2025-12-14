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
class PolylineShape:
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

    def __str__(self) -> str:
        return f"PolylineShape(vertices:{self.get_points_count()})"

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

    def __str__(self) -> str:
        return f"LineShape(start:{self.get_start_point().position}, end:{self.get_end_point().position})"

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


@final 
class WidelineShape:
    """
    #### Класс для работы с толстыми линиями с закругленными концами

    ---

    :Description:
    - Представляет собой линию с изменяемой толщиной (радиусом)
    - Поддерживает как прямоугольные, так и закругленные концы
    - Использует примитив TriangleFan для заполнения геометрии
    - Автоматически генерирует меш (сетку) для отображения линии

    ---

    :Features:
    - Настройка радиуса (толщины) линии
    - Включение/отключение закругления концов
    - Управление качеством аппроксимации закруглений
    - Автоматическое обновление геометрии при изменении параметров
    - Цветовое оформление всей линии
    """

    def __init__(self):
        """
        #### Инициализирует новую толстую линию

        ---

        :Description:
        - Создает пустой список вершин с типом примитива TriangleFan
        - Устанавливает начальные параметры линии
        - Подготавливает структуру для генерации меша

        ---

        :Initial State:
        - Пустой список вершин
        - Тип примитива: TriangleFan (веер треугольников)
        - Радиус по умолчанию: 10 единиц
        - Закругление включено
        - Качество аппроксимации: 10 сегментов
        - Цвет по умолчанию: черный
        - Автоматическое обновление отключено
        """
        self.__vertex_list = VertexList()
        self.__vertex_list.set_primitive_type(VertexListTypes.TriangleFan)

        self.__start_point:     Optional[Vector2Type] = None
        self.__end_point:       Optional[Vector2Type] = None
        self.__radius:          Number = 10
        self.__rounded:         bool = True
        self.__approximation:   int = 10
        self.__color:           Color = COLOR_BLACK

        self.__auto_rematch:    bool = False

    def __str__(self) -> str:
        return f'WidelineShape(start:{self.__start_point}, end:{self.__end_point})'

    def set_auto_rematch(self, flag: bool) -> Self:
        """
        #### Включает или выключает автоматическое обновление геометрии

        ---

        :Description:
        - При включении геометрия автоматически пересчитывается при каждом рендеринге
        - При выключении требуется явный вызов rematch_mesh()
        - Удобно для статичных линий для повышения производительности

        ---

        :Args:
        - flag (bool): True - включить автообновление, False - выключить

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        wideline.set_auto_rematch(True)  # Автоматическое обновление включено
        ```

        :Note:
        - При частом изменении параметров линии рекомендуется включать автообновление
        - Для статичных линий лучше выключить для оптимизации производительности
        """
        self.__auto_rematch = flag
        return self
    
    def get_auto_rematch(self) -> bool:
        """
        #### Возвращает статус автоматического обновления геометрии

        ---

        :Description:
        - Позволяет проверить, включено ли автоматическое обновление меша
        - Полезно для отладки и оптимизации

        ---

        :Returns:
        - bool: True если автообновление включено, иначе False

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        auto_update = wideline.get_auto_rematch()  # False (по умолчанию)
        ```
        """
        return self.__auto_rematch

    def set_rounded(self, flag: bool) -> Self:
        """
        #### Включает или выключает закругление концов линии

        ---

        :Description:
        - При включении концы линии будут закругленными
        - При выключении концы будут прямоугольными
        - Влияет на внешний вид и количество вершин в меше

        ---

        :Args:
        - flag (bool): True - закругленные концы, False - прямоугольные

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        wideline.set_rounded(True)    # Концы закругленные (по умолчанию)
        wideline.set_rounded(False)   # Концы прямоугольные
        ```

        :Note:
        - Закругленные концы требуют больше вершин для отображения
        - Прямоугольные концы более производительны
        """
        self.__rounded = flag
        return self
    
    def get_rounded(self) -> bool:
        """
        #### Возвращает статус закругления концов

        ---

        :Description:
        - Позволяет проверить, включено ли закругление концов линии
        - Полезно для условной логики рендеринга

        ---

        :Returns:
        - bool: True если концы закругленные, иначе False

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        is_rounded = wideline.get_rounded()  # True (по умолчанию)
        ```
        """
        return self.__rounded

    def set_radius(self, radius: Number) -> Self:
        """
        #### Устанавливает радиус (толщину) линии

        ---

        :Description:
        - Определяет толщину отображаемой линии
        - Влияет на размер генерируемого меша
        - Применяется ко всей длине линии

        ---

        :Args:
        - radius (Number): Новое значение радиуса (толщины) в пикселях

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        wideline.set_radius(5)   # Тонкая линия
        wideline.set_radius(20)  # Толстая линия
        ```

        :Note:
        - Радиус применяется равномерно с обеих сторон центральной оси
        - Слишком большой радиус может вызвать визуальные артефакты
        """
        self.__radius = radius
        return self
    
    def get_radius(self) -> Number:
        """
        #### Возвращает текущий радиус линии

        ---

        :Description:
        - Возвращает установленное значение толщины линии
        - Полезно для вычислений связанных с геометрией

        ---

        :Returns:
        - Number: Текущее значение радиуса

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        thickness = wideline.get_radius()  # 10 (по умолчанию)
        ```
        """
        return self.__radius

    def set_color(self, color: Color) -> Self:
        """
        #### Устанавливает цвет всей линии

        ---

        :Description:
        - Применяет указанный цвет ко всем вершинам линии
        - Немедленно обновляет цвет существующих вершин
        - Поддерживает fluent-интерфейс

        ---

        :Args:
        - color (Color): Новый цвет линии

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        wideline.set_color(Color.RED)     # Красная линия
        wideline.set_color(Color.BLUE)    # Синяя линия
        ```

        :Note:
        - Цвет применяется равномерно по всей линии
        - Градиенты не поддерживаются данным методом
        """
        self.__color = color
        self.__vertex_list.set_color(color)
        return self
    
    def get_color(self) -> Color:
        """
        #### Возвращает текущий цвет линии

        ---

        :Description:
        - Возвращает цвет, установленный через set_color()
        - Используется системой рендеринга для отображения

        ---

        :Returns:
        - Color: Текущий цвет линии

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        wideline.set_color(Color.GREEN)
        current_color = wideline.get_color()  # Color.GREEN
        ```
        """
        return self.__color
    
    def set_approximation(self, number: int) -> Self:
        """
        #### Устанавливает качество аппроксимации закруглений

        ---

        :Description:
        - Определяет количество сегментов для аппроксимации окружности
        - Влияет на гладкость закругленных концов
        - Большие значения дают более гладкие кривые, но требуют больше вершин

        ---

        :Args:
        - number (int): Количество сегментов аппроксимации (минимум 3)

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        wideline.set_approximation(5)   # Низкое качество, высокая производительность
        wideline.set_approximation(20)  # Высокое качество, больше вершин
        ```

        :Note:
        - Влияет только на закругленные концы (при rounded=True)
        - Рекомендуемое значение: 10-20 для баланса качества и производительности
        """
        self.__approximation = number
        return self

    def get_approximation(self) -> int:
        """
        #### Возвращает текущее качество аппроксимации

        ---

        :Description:
        - Возвращает количество сегментов для аппроксимации окружности
        - Полезно для настройки уровня детализации

        ---

        :Returns:
        - int: Текущее количество сегментов аппроксимации

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        quality = wideline.get_approximation()  # 10 (по умолчанию)
        ```
        """
        return self.__approximation

    def set_start_position(self, pos: Vector2Type) -> Self:
        """
        #### Устанавливает позицию начальной точки линии

        ---

        :Description:
        - Определяет начальную координату толстой линии
        - Влияет на направление и длину линии
        - Требует установки конечной точки для формирования линии

        ---

        :Args:
        - pos (Vector2Type): Координаты начальной точки

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        wideline.set_start_position(Vector2f(0, 0))
        wideline.set_end_position(Vector2f(100, 100))
        ```

        :Note:
        - Линия не будет отображаться пока не установлены обе точки
        - Требуется вызов rematch_mesh() для обновления геометрии (если auto_rematch=False)
        """
        self.__start_point = pos
        return self

    def set_end_position(self, pos: Vector2Type) -> Self:
        """
        #### Устанавливает позицию конечной точки линии

        ---

        :Description:
        - Определяет конечную координату толстой линии
        - Вместе с начальной точкой формирует ось линии
        - Влияет на направление и длину линии

        ---

        :Args:
        - pos (Vector2Type): Координаты конечной точки

        ---

        :Returns:
        - Self: Текущий объект для цепочки вызовов

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        wideline.set_start_position(Vector2f(0, 0))
        wideline.set_end_position(Vector2f(100, 100))
        # Создана диагональная линия из (0,0) в (100,100)
        ```

        :Note:
        - Линия не будет отображаться пока не установлены обе точки
        - Требуется вызов rematch_mesh() для обновления геометрии (если auto_rematch=False)
        """
        self.__end_point = pos
        return self

    def rematch_mesh(self):
        """
        #### Пересчитывает и обновляет геометрию линии

        ---

        :Description:
        - Генерирует новый меш (сетку) на основе текущих параметров
        - Создает геометрию с учетом радиуса и закругления концов
        - Заполняет список вершин для рендеринга

        ---

        :Algorithm:
        1. Вычисляет нормализованный вектор направления линии
        2. Создает перпендикулярный вектор для толщины
        3. Генерирует вершины в зависимости от типа концов:
           - Прямоугольные: 4 вершины по углам прямоугольника
           - Закругленные: множественные вершины для аппроксимации окружностей

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        wideline.set_start_position(Vector2f(0, 0))
        wideline.set_end_position(Vector2f(100, 0))
        wideline.set_radius(5)
        wideline.rematch_mesh()  # Генерирует геометрию линии
        ```

        :Note:
        - Должен быть вызван после изменения любых параметров линии (если auto_rematch=False)
        - Требует установки обеих точек (start и end)
        - Очищает существующий список вершин перед генерацией
        """
        # Вычисляем нормализованный вектор направления линии
        normal = (self.__end_point - self.__start_point).normalize_at()
        # Создаем перпендикулярный вектор для толщины
        dummy_ = normal.rotate(90) * self.__radius
        # Очищаем существующие вершины
        self.__vertex_list.clear()

        if not self.__rounded:
            # Генерация прямоугольных концов - 4 вершины
            self.__vertex_list.auto_append(Vertex2d.FromPosition(self.__start_point + dummy_))
            self.__vertex_list.auto_append(Vertex2d.FromPosition(self.__end_point + dummy_))
            dummy_.rotate_at(180)
            self.__vertex_list.auto_append(Vertex2d.FromPosition(self.__end_point + dummy_))
            self.__vertex_list.auto_append(Vertex2d.FromPosition(self.__start_point + dummy_))
            self.__vertex_list.set_color(self.__color)
        else:
            # Генерация закругленных концов
            approximation_angle = 180 / self.__approximation
            # Вершины для начального закругления
            for i in range(self.__approximation + 1):
                if i != 0: dummy_.rotate_at(approximation_angle)
                self.__vertex_list.auto_append(Vertex2d.FromPosition(self.__start_point + dummy_))

            # Вершины для конечного закругления
            for i in range(self.__approximation + 1):
                if i != 0: dummy_.rotate_at(approximation_angle)
                self.__vertex_list.auto_append(Vertex2d.FromPosition(self.__end_point + dummy_))
            
            self.__vertex_list.set_color(self.__color)


    def get_ptr(self) -> ctypes.c_void_p:
        """
        #### Возвращает указатель на нативный объект вершин

        ---

        :Description:
        - Предоставляет доступ к низкоуровневому объекту вершин для рендеринга
        - При включенном auto_rematch автоматически обновляет геометрию
        - Для внутреннего использования в системе рендеринга

        ---

        :Returns:
        - ctypes.c_void_p: Указатель на нативный VertexList

        ---

        :Example:
        ```python
        wideline = WidelineShape()
        # ... настройка параметров линии ...
        vertex_ptr = wideline.get_ptr()  # Получаем указатель для рендеринга
        ```

        :Note:
        - Если auto_rematch=True, вызывает rematch_mesh() перед возвратом указателя
        - Изменение указателя может привести к неопределенному поведению
        - Используется системой рендеринга для отображения линии
        """
        if self.__auto_rematch: 
            self.rematch_mesh()
        return self.__vertex_list.get_ptr()
    
