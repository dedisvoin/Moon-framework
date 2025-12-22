import math

from noise import pnoise2
from typing import Optional, overload, Union, Tuple

from Moon.python.Vectors import *


def perlin_noise(x: float, y: float, octaves: int = 1, persistance: float = 0.5, lacunarity: float = 2.0) -> float:
    """
    #### Генерирует шум Перлина для заданных координат.

    ---

    :Args:
    - x, y: координаты точки, для которой вычисляется шум
    - octaves: количество октав (слоев) шума
    - persistence: коэффициент, определяющий, как сильно влияет каждая октава на общий шум
    - lacunarity: коэффициент, определяющий, как часто изменяются частоты октав

    :Returns:
    - float: значение шума Перлина для заданных координат
    """
    value = pnoise2(x, y, octaves=octaves, persistence=persistance, lacunarity=lacunarity)
    return value


# ==============================================================
# Расстояния и проверки коллизий
# ==============================================================

@overload
def distance(arg1: float, arg2: float, arg3: float, arg4: float) -> float:
    """
    #### Вычисляет евклидово расстояние между двумя точками.

    ---

    :Args:
    - x1, y1: координаты первой точки
    - x2, y2: координаты второй точки

    :Returns:
    - float: расстояние между точками
    """
    ...

@overload
def distance(arg1: Vector2Type, arg2: Vector2Type) -> float:
    """
    #### Вычисляет евклидово расстояние между двумя точками.

    ---

    :Args:
    - v1: вектор положения первой точки
    - v2: вектор положения второй точки

    :Returns:
    - float: расстояние между точками
    """
    ...

def distance(arg1: Vector2Type | Number, arg2: Vector2Type | Number, arg3: Optional[Number] = None, arg4: Optional[Number] = None):
    if isinstance(arg1, Vec2TT) and isinstance(arg2, Vec2TT):
        return math.hypot(arg1.x - arg2.x, arg1.y - arg2.y)
    elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)) and isinstance(arg3, (int, float)) and isinstance(arg4, (int, float)):
        return math.hypot(arg3 - arg1, arg4 - arg2)
    raise TypeError("Invalid arguments - expected either 4 numbers or 2 vectors")


@overload
def distance_squared(arg1: float, arg2: float, arg3: float, arg4: float) -> float:
    """
    #### Вычисляет квадрат расстояния между точками (оптимизация для сравнений).

    ---

    :Args:
    - x1, y1: координаты первой точки
    - x2, y2: координаты второй точки

    :Returns:
    - float: квадрат расстояния между точками
    """
    ...

@overload
def distance_squared(arg1: Vector2Type, arg2: Vector2Type) -> float:
    """
    #### Вычисляет квадрат расстояния между точками (оптимизация для сравнений).

    ---

    :Args:
    - v1: вектор положения первой точки
    - v2: вектор положения второй точки

    :Returns:
    - float: квадрат расстояния между точками
    """
    ...

def distance_squared(arg1: Vector2Type | Number, arg2: Vector2Type | Number, arg3: Optional[Number] = None, arg4: Optional[Number] = None):
    if isinstance(arg1, Vec2TT) and isinstance(arg2, Vec2TT):
        dx, dy = arg2.x - arg1.x, arg2.y - arg1.y
    elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)) and isinstance(arg3, (int, float)) and isinstance(arg4, (int, float)):
        dx, dy = arg3 - arg1, arg4 - arg2
    else:
        raise TypeError("Invalid arguments - expected either 4 numbers or 2 vectors")
    return dx * dx + dy * dy


# ==============================================================
# Коллизии кругов
# ==============================================================

@overload
def circles_collision(arg1: float, arg2: float, arg3: float, arg4: float, arg5: float, arg6: float) -> bool:
    """
    #### Проверяет пересечение двух кругов.

    ---

    :Args:
    - x1, y1: центр первого круга
    - r1: радиус первого круга
    - x2, y2: центр второго круга
    - r2: радиус второго круга

    :Returns:
    - bool: True если круги пересекаются или касаются
    """
    ...

@overload
def circles_collision(arg1: Vector2Type, arg2: float, arg3: Vector2Type, arg4: float) -> bool:
    """
    #### Проверяет пересечение двух кругов.

    ---

    :Args:
    - v1: центр первого круга (вектор)
    - r1: радиус первого круга
    - v2: центр второго круга (вектор)
    - r2: радиус второго круга

    :Returns:
    - bool: True если круги пересекаются или касаются
    """
    ...

def circles_collision(arg1, arg2, arg3, arg4, arg5=None, arg6=None) -> bool:
    if isinstance(arg1, Vec2TT) and isinstance(arg3, Vec2TT):
        # Формат: circles_collision(v1, r1, v2, r2)
        return distance_squared(arg1, arg3) <= (arg2 + arg4)**2
    elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)) and isinstance(arg3, (int, float))\
     and isinstance(arg4, (int, float)) and isinstance(arg5, (int, float)) and isinstance(arg6, (int, float)):
        # Формат: circles_collision(x1, y1, r1, x2, y2, r2)
        return distance_squared(arg1, arg2, arg4, arg5) <= (arg3 + arg6)**2
    raise TypeError("Invalid arguments - expected either 6 numbers or 2 vectors and 2 radii")


# ==============================================================
# Коллизии прямоугольников
# ==============================================================

@overload
def rects_collision(arg1: float, arg2: float, arg3: float, arg4: float,
                   arg5: float, arg6: float, arg7: float, arg8: float) -> bool:
    """
    #### Проверяет пересечение двух прямоугольников (AABB).

    ---

    :Args:
    - x1, y1: левый верхний угол первого прямоугольника
    - w1, h1: ширина и высота первого прямоугольника
    - x2, y2: левый верхний угол второго прямоугольника
    - w2, h2: ширина и высота второго прямоугольника

    :Returns:
    - bool: True если прямоугольники пересекаются
    """
    ...

@overload
def rects_collision(arg1: Vector2Type, arg2: Vector2Type,
                   arg3: Vector2Type, arg4: Vector2Type) -> bool:
    """
    #### Проверяет пересечение двух прямоугольников (AABB).

    ---

    :Args:
    - pos1: позиция первого прямоугольника (вектор)
    - size1: размер первого прямоугольника (вектор)
    - pos2: позиция второго прямоугольника (вектор)
    - size2: размер второго прямоугольника (вектор)

    :Returns:
    - bool: True если прямоугольники пересекаются
    """
    ...

def rects_collision(arg1, arg2, arg3, arg4, arg5=None, arg6=None, arg7=None, arg8=None) -> bool:
    if isinstance(arg1, Vec2TT) and isinstance(arg2, Vec2TT) and isinstance(arg3, Vec2TT) and isinstance(arg4, Vec2TT):
        # Формат: rects_collision(pos1, size1, pos2, size2)
        pos1, size1, pos2, size2 = arg1, arg2, arg3, arg4
        return (pos1.x <= pos2.x + size2.x and
                pos1.x + size1.x >= pos2.x and
                pos1.y <= pos2.y + size2.y and
                pos1.y + size1.y >= pos2.y)

    elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)) and isinstance(arg3, (int, float)) and isinstance(arg4, (int, float))\
     and isinstance(arg5, (int, float)) and isinstance(arg6, (int, float)) and isinstance(arg7, (int, float)) and isinstance(arg8, (int, float)):
        # Формат: rects_collision(x1, y1, w1, h1, x2, y2, w2, h2)
        x1, y1, w1, h1, x2, y2, w2, h2 = arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)

    raise TypeError("Invalid arguments - expected either 8 numbers or 4 vectors")


# ==============================================================
# Новые полезные методы
# ==============================================================

def point_in_rect(  point_x: float,
                    point_y: float,
                    rect_x: float,
                    rect_y: float,
                    rect_w: float,
                    rect_h: float) -> bool:
    """
    #### Проверяет, находится ли точка внутри прямоугольника.

    ---

    :Args:
    - point_x: координата x точки или вектор положения
    - rect_x: координата x прямоугольника или вектор положения
    - rect_w: ширина прямоугольника или вектор размера
    - rect_h: высота прямоугольника (если rect_w не вектор)

    :Returns:
    - bool: True если точка внутри прямоугольника
    """
    return rect_x <= point_x <= rect_x + rect_w and rect_y <= point_y <= rect_y + rect_h

def line_intersection(x1: float, y1: float, x2: float, y2: float,
                     x3: float, y3: float, x4: float, y4: float) -> Union[Tuple[float, float], None]:
    """
    #### Находит точку пересечения двух отрезков.

    ---

    :Args:
    - x1, y1: начало первого отрезка
    - x2, y2: конец первого отрезка
    - x3, y3: начало второго отрезка
    - x4, y4: конец второго отрезка

    :Returns:
    - Tuple[float, float] или None: координаты пересечения или None если отрезки не пересекаются
    """
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0:  # Линии параллельны
        return None

    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    if ua < 0 or ua > 1:  # Пересечение вне первого отрезка
        return None

    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    if ub < 0 or ub > 1:  # Пересечение вне второго отрезка
        return None

    return (x1 + ua*(x2-x1), (y1 + ua*(y2-y1)))


def circle_line_collision(circle_x: float, circle_y: float, radius: float,
                         line_x1: float, line_y1: float, line_x2: float, line_y2: float) -> bool:
    """
    #### Проверяет пересечение круга и отрезка.

    ---

    :Args:
    - circle_x, circle_y: центр круга
    - radius: радиус круга
    - line_x1, line_y1: начало отрезка
    - line_x2, line_y2: конец отрезка

    :Returns:
    - bool: True если есть пересечение
    """
    # Вектор отрезка
    seg_vx = line_x2 - line_x1
    seg_vy = line_y2 - line_y1

    # Вектор от начала отрезка к центру круга
    pt_vx = circle_x - line_x1
    pt_vy = circle_y - line_y1

    # Проекция вектора pt_v на seg_v
    len_sq = seg_vx*seg_vx + seg_vy*seg_vy
    proj = (pt_vx*seg_vx + pt_vy*seg_vy) / len_sq if len_sq != 0 else 0

    # Ближайшая точка на отрезке
    closest_x = line_x1 + min(max(proj, 0), 1) * seg_vx
    closest_y = line_y1 + min(max(proj, 0), 1) * seg_vy

    # Расстояние до ближайшей точки
    dist_x = closest_x - circle_x
    dist_y = closest_y - circle_y
    dist_sq = dist_x*dist_x + dist_y*dist_y

    return dist_sq <= radius*radius


def rotate_point(center_x: float, center_y: float, point_x: float, point_y: float, angle: float) -> Tuple[float, float]:
    """
    #### Поворачивает точку вокруг центра на заданный угол.

    ---

    :Args:
    - center_x, center_y: центр вращения
    - point_x, point_y: вращаемая точка
    - angle: угол в радианах

    :Returns:
    - Tuple[float, float]: новые координаты точки
    """
    s = math.sin(angle)
    c = math.cos(angle)

    # Переносим точку в начало координат
    x = point_x - center_x
    y = point_y - center_y

    # Поворачиваем
    x_new = x * c - y * s
    y_new = x * s + y * c

    # Возвращаем обратно
    return (x_new + center_x, y_new + center_y)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    #### Ограничивает значение заданными границами.

    ---

    :Args:
    - value: исходное значение
    - min_val: минимальное допустимое значение
    - max_val: максимальное допустимое значение

    :Returns:
    - float: значение в пределах [min_val, max_val]
    """
    return max(min_val, min(value, max_val))


def lerp(a: float, b: float, t: float) -> float:
    """
    #### Линейная интерполяция между двумя значениями.

    ---

    :Args:
    - a: начальное значение
    - b: конечное значение
    - t: параметр интерполяции (0.0 - a, 1.0 - b)

    :Returns:
    - float: интерполированное значение
    """
    return a + (b - a) * clamp(t, 0.0, 1.0)


def point_on_line_segment(px: float, py: float,
                        x1: float, y1: float,
                        x2: float, y2: float,
                        max_distance: float = 1.0,
                        tolerance: float = 1e-6) -> bool:
    """
    #### Проверяет, находится ли точка рядом с отрезком в пределах заданного расстояния.

    ---

    :Args:
    - px, py: координаты точки
    - x1, y1: начало отрезка
    - x2, y2: конец отрезка
    - max_distance: максимальное расстояние от линии, при котором точка считается "на отрезке"
    - tolerance: допустимая погрешность при расчетах

    :Returns:
    - bool: True если точка находится на расстоянии <= max_distance от отрезка
    """
    # Вектор отрезка
    segment_vec_x = x2 - x1
    segment_vec_y = y2 - y1

    # Вектор от начала отрезка к точке
    point_vec_x = px - x1
    point_vec_y = py - y1

    # Длина отрезка в квадрате
    segment_length_sq = segment_vec_x**2 + segment_vec_y**2

    # Проекция точки на отрезок (параметр t)
    t = 0.0
    if segment_length_sq > tolerance:
        t = max(0, min(1, (point_vec_x * segment_vec_x + point_vec_y * segment_vec_y) / segment_length_sq))

    # Ближайшая точка на отрезке
    closest_x = x1 + t * segment_vec_x
    closest_y = y1 + t * segment_vec_y

    # Расстояние от точки до ближайшей точки на отрезке
    distance_sq = (px - closest_x)**2 + (py - closest_y)**2

    return distance_sq <= max_distance**2
