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
    


from typing import List, Tuple


def decompose_concave_polygon(vertices: List[Tuple[float, float]]) -> List[List[Tuple[float, float]]]:
    """
    Разбивает вогнутый полигон на выпуклые части используя алгоритм Bayazit.
    
    Args:
        vertices: Список вершин полигона в формате [(x1, y1), (x2, y2), ...]
                 Вершины должны быть упорядочены по границе полигона (по или против часовой стрелки)
    
    Returns:
        Список выпуклых полигонов, каждый в том же формате [(x1, y1), (x2, y2), ...]
    
    Example:
        >>> # Вогнутая форма типа "бумеранг"
        >>> concave = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]
        >>> convex_parts = decompose_concave_polygon(concave)
        >>> len(convex_parts)  # Ожидаем 2 выпуклых полигона
        2
    """
    if len(vertices) < 3:
        return []
    
    # Проверяем, является ли полигон уже выпуклым
    if _is_convex(vertices):
        return [vertices]
    
    # Создаем копию вершин для работы
    polygon = vertices.copy()
    result = []
    
    # Основной цикл декомпозиции
    while len(polygon) > 2:
        # Ищем точку рефлекса (вогнутую)
        reflex_index = _find_reflex_vertex(polygon)
        
        if reflex_index == -1:
            # Если вогнутых вершин нет, полигон выпуклый
            result.append(polygon.copy())
            break
        
        # Пытаемся найти диагональ для разреза
        cut_success, new_polygons = _try_cut_polygon(polygon, reflex_index)
        
        if cut_success:
            # Успешно разрезали, добавляем первый полигон
            result.append(new_polygons[0])
            # Продолжаем с оставшимся полигоном
            polygon = new_polygons[1]
        else:
            # Не удалось разрезать, используем резервный метод
            sub_polygons = _decompose_by_ear_clipping(polygon)
            result.extend(sub_polygons)
            break
    
    return result


def _is_convex(vertices: List[Tuple[float, float]]) -> bool:
    """Проверяет, является ли полигон выпуклым."""
    n = len(vertices)
    if n < 3:
        return False
    
    # Используем знак векторного произведения для определения выпуклости
    sign = 0
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        p3 = vertices[(i + 2) % n]
        
        # Вычисляем векторное произведение
        cross = (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])
        
        if abs(cross) > 1e-10:  # Игнорируем очень маленькие значения
            if sign == 0:
                sign = 1 if cross > 0 else -1
            elif (cross > 0 and sign < 0) or (cross < 0 and sign > 0):
                return False  # Нашли изменение знака -> полигон вогнутый
    
    return True


def _find_reflex_vertex(polygon: List[Tuple[float, float]]) -> int:
    """Находит индекс первой вогнутой вершины в полигоне."""
    n = len(polygon)
    
    for i in range(n):
        prev = polygon[(i - 1 + n) % n]
        curr = polygon[i]
        next_v = polygon[(i + 1) % n]
        
        # Вычисляем векторное произведение
        cross = (curr[0] - prev[0]) * (next_v[1] - curr[1]) - \
                (curr[1] - prev[1]) * (next_v[0] - curr[0])
        
        # Для полигона с обходом против часовой стрелки, 
        # отрицательное векторное произведение указывает на вогнутую вершину
        if cross < -1e-10:  # Небольшой допуск для числовой стабильности
            return i
    
    return -1  # Вогнутых вершин не найдено


def _try_cut_polygon(polygon: List[Tuple[float, float]], reflex_index: int) -> Tuple[bool, List]:
    """
    Пытается разрезать полигон через вогнутую вершину.
    
    Args:
        polygon: Исходный полигон
        reflex_index: Индекс вогнутой вершины
    
    Returns:
        (успех, [полигон1, полигон2]) если удалось разрезать,
        (False, []) в противном случае
    """
    n = len(polygon)
    reflex = polygon[reflex_index]
    
    # Ищем подходящую вершину для создания диагонали
    for j in range(n):
        if j == reflex_index or j == (reflex_index - 1) % n or j == (reflex_index + 1) % n:
            continue  # Пропускаем соседние вершины
        
        target = polygon[j]
        
        # Проверяем, является ли диагональ внутренней
        if _is_diagonal_inside(polygon, reflex_index, j):
            # Разрезаем полигон по диагонали
            poly1, poly2 = _split_by_diagonal(polygon, reflex_index, j)
            
            # Проверяем, что оба полученных полигона валидны
            if len(poly1) >= 3 and len(poly2) >= 3:
                return True, [poly1, poly2]
    
    return False, []


def _is_diagonal_inside(polygon: List[Tuple[float, float]], i: int, j: int) -> bool:
    """Проверяет, является ли отрезок между вершинами i и j внутренней диагональю."""
    n = len(polygon)
    a = polygon[i]
    b = polygon[j]
    
    # Диагональ должна лежать внутри полигона
    # Проверяем пересечение с другими сторонами
    for k in range(n):
        k_next = (k + 1) % n
        
        # Пропускаем стороны, смежные с диагональю
        if k == i or k == j or k_next == i or k_next == j:
            continue
        
        c = polygon[k]
        d = polygon[k_next]
        
        if _segments_intersect(a, b, c, d):
            return False  # Диагональ пересекает сторону полигона
    
    # Проверяем, что диагональ лежит внутри полигона
    # Для этого проверяем среднюю точку диагонали
    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    
    return _is_point_inside_polygon(mid, polygon)


def _segments_intersect(p1: Tuple[float, float], p2: Tuple[float, float],
                        p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
    """Проверяет, пересекаются ли два отрезка."""
    def orientation(px, py, qx, qy, rx, ry):
        val = (qy - py) * (rx - qx) - (qx - px) * (ry - qy)
        if abs(val) < 1e-10:
            return 0  # Коллинеарны
        return 1 if val > 0 else 2
    
    o1 = orientation(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
    o2 = orientation(p1[0], p1[1], p2[0], p2[1], p4[0], p4[1])
    o3 = orientation(p3[0], p3[1], p4[0], p4[1], p1[0], p1[1])
    o4 = orientation(p3[0], p3[1], p4[0], p4[1], p2[0], p2[1])
    
    # Общий случай
    if o1 != o2 and o3 != o4:
        return True
    
    return False


def _split_by_diagonal(polygon: List[Tuple[float, float]], i: int, j: int) -> Tuple[List, List]:
    """Разрезает полигон по диагонали между вершинами i и j."""
    n = len(polygon)
    
    # Создаем первый полигон (от i до j по часовой стрелке)
    poly1 = []
    idx = i
    while True:
        poly1.append(polygon[idx])
        if idx == j:
            break
        idx = (idx + 1) % n
    
    # Создаем второй полигон (от j до i по часовой стрелке)
    poly2 = []
    idx = j
    while True:
        poly2.append(polygon[idx])
        if idx == i:
            break
        idx = (idx + 1) % n
    
    return poly1, poly2


def _is_point_inside_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """Проверяет, находится ли точка внутри полигона (алгоритм winding number)."""
    x, y = point
    n = len(polygon)
    winding_number = 0
    
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        
        if y1 <= y:
            if y2 > y and (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1) > 0:
                winding_number += 1
        else:
            if y2 <= y and (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1) < 0:
                winding_number -= 1
    
    return winding_number != 0


def _decompose_by_ear_clipping(polygon: List[Tuple[float, float]]) -> List[List[Tuple[float, float]]]:
    """
    Резервный метод: разбивает полигон на треугольники методом ear clipping,
    а затем объединяет треугольники в выпуклые полигоны.
    """
    triangles = _triangulate_by_ear_clipping(polygon)
    
    if not triangles:
        return []
    
    # Объединяем смежные треугольники в выпуклые полигоны
    convex_polygons = []
    used = [False] * len(triangles)
    
    for i in range(len(triangles)):
        if used[i]:
            continue
        
        current = triangles[i]
        used[i] = True
        
        # Пытаемся объединить с соседними треугольниками
        for j in range(i + 1, len(triangles)):
            if used[j]:
                continue
            
            merged = _merge_triangles_if_convex(current, triangles[j])
            if merged is not None:
                current = merged
                used[j] = True
        
        convex_polygons.append(current)
    
    return convex_polygons


def _triangulate_by_ear_clipping(polygon: List[Tuple[float, float]]) -> List[List[Tuple[float, float]]]:
    """Триангулирует полигон методом ear clipping."""
    n = len(polygon)
    if n < 3:
        return []
    
    # Создаем список индексов
    indices = list(range(n))
    triangles = []
    
    while len(indices) > 3:
        ear_found = False
        
        for i in range(len(indices)):
            prev_idx = indices[(i - 1) % len(indices)]
            curr_idx = indices[i]
            next_idx = indices[(i + 1) % len(indices)]
            
            prev = polygon[prev_idx]
            curr = polygon[curr_idx]
            next_v = polygon[next_idx]
            
            # Проверяем, является ли вершина ухом
            if _is_ear(prev, curr, next_v, polygon, indices, i):
                # Добавляем треугольник
                triangles.append([prev, curr, next_v])
                # Удаляем текущую вершину
                indices.pop(i)
                ear_found = True
                break
        
        if not ear_found:
            # Не удалось найти ухо, возвращаем то, что есть
            break
    
    # Добавляем последний треугольник
    if len(indices) == 3:
        triangles.append([polygon[indices[0]], polygon[indices[1]], polygon[indices[2]]])
    
    return triangles


def _is_ear(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float],
           polygon: List[Tuple[float, float]], indices: List[int], index: int) -> bool:
    """Проверяет, является ли треугольник ухом."""
    # Проверяем, что треугольник не содержит других вершин
    for i in range(len(polygon)):
        if i == indices[(index - 1) % len(indices)] or \
           i == indices[index] or \
           i == indices[(index + 1) % len(indices)]:
            continue
        
        if _is_point_in_triangle(polygon[i], p1, p2, p3):
            return False
    
    return True


def _is_point_in_triangle(point: Tuple[float, float], 
                         p1: Tuple[float, float], 
                         p2: Tuple[float, float], 
                         p3: Tuple[float, float]) -> bool:
    """Проверяет, находится ли точка внутри треугольника."""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    d1 = sign(point, p1, p2)
    d2 = sign(point, p2, p3)
    d3 = sign(point, p3, p1)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)


def _merge_triangles_if_convex(triangle1: List[Tuple[float, float]], 
                              triangle2: List[Tuple[float, float]]) -> Optional[List[Tuple[float, float]]]:
    """
    Объединяет два треугольника в один полигон, если результат выпуклый.
    """
    # Находим общее ребро
    common_edge = None
    for i in range(3):
        for j in range(3):
            if triangle1[i] == triangle2[j] and triangle1[(i + 1) % 3] == triangle2[(j + 2) % 3]:
                common_edge = (triangle1[i], triangle1[(i + 1) % 3])
                break
        if common_edge:
            break
    
    if not common_edge:
        return None  # Треугольники не смежные
    
    # Создаем объединенный полигон
    merged = []
    
    # Добавляем вершины из первого треугольника, исключая общее ребро
    for i in range(3):
        if triangle1[i] != common_edge[0] and triangle1[i] != common_edge[1]:
            merged.append(triangle1[i])
    
    # Добавляем вершины из второго треугольника
    for i in range(3):
        if triangle2[i] != common_edge[0] and triangle2[i] != common_edge[1]:
            merged.append(triangle2[i])
    
    # Добавляем общие вершины
    merged.append(common_edge[0])
    merged.append(common_edge[1])
    
    # Упорядочиваем вершины по часовой стрелке
    merged = _order_vertices_clockwise(merged)
    
    # Проверяем выпуклость
    if _is_convex(merged):
        return merged
    
    return None


def _order_vertices_clockwise(vertices: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """Упорядочивает вершины полигона по часовой стрелке."""
    if len(vertices) < 3:
        return vertices
    
    # Находим центр
    center_x = sum(v[0] for v in vertices) / len(vertices)
    center_y = sum(v[1] for v in vertices) / len(vertices)
    
    # Сортируем по углу относительно центра
    def angle_from_center(vertex):
        dx = vertex[0] - center_x
        dy = vertex[1] - center_y
        return math.atan2(dy, dx)
    
    return sorted(vertices, key=angle_from_center, reverse=True)


