import math
from typing import overload, Union, Tuple
from noise import pnoise2

from .Vectors import *


def perlin_noise(x: float, y: float, octaves: int = 1, persistance: float = 0.5, lacunarity: float = 2.0) -> float:
    """
    Генерирует шум Перлина для заданных координат.

    Параметры:
        x, y: координаты точки, для которой вычисляется шум
        octaves: количество октав (слоев) шума
        persistence: коэффициент, определяющий, как сильно влияет каждая октава на общий шум
        lacunarity: коэффициент, определяющий, как часто изменяются частоты октав

    Возвращает:
        float: значение шума Перлина для заданных координат
    """
    value = pnoise2(x, y, octaves=octaves, persistence=persistance, lacunarity=lacunarity)
    return value





# ==============================================================
# Расстояния и проверки коллизий
# ==============================================================

@overload
def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Вычисляет евклидово расстояние между двумя точками.
    
    Параметры:
        x1, y1: координаты первой точки
        x2, y2: координаты второй точки
    
    Возвращает:
        float: расстояние между точками
    """
    ...

@overload
def distance(v1: VectorType, v2: VectorType) -> float:
    """
    Вычисляет евклидово расстояние между двумя точками.
    
    Параметры:
        v1: вектор положения первой точки
        v2: вектор положения второй точки
    
    Возвращает:
        float: расстояние между точками
    """
    ...

def distance(x1, y1, x2=None, y2=None):
    if isinstance(x1, (Vector2f, Vector2i)) and isinstance(y1, (Vector2f, Vector2i)):
        return math.hypot(y1.x - x1.x, y1.y - x1.y)
    elif all(isinstance(i, (int, float)) for i in [x1, y1, x2, y2]):
        return math.hypot(x2 - x1, y2 - y1)
    raise TypeError("Invalid arguments - expected either 4 numbers or 2 vectors")

@overload
def distance_squared(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Вычисляет квадрат расстояния между точками (оптимизация для сравнений).
    """
    ...

@overload
def distance_squared(v1: VectorType, v2: VectorType) -> float:
    """
    Вычисляет квадрат расстояния между точками (оптимизация для сравнений).
    """
    ...

def distance_squared(x1, y1, x2=None, y2=None):
    if isinstance(x1, VectorType) and isinstance(y1, VectorType):
        dx, dy = y1.x - x1.x, y1.y - x1.y
    elif all(isinstance(i, (int, float)) for i in [x1, y1, x2, y2]):
        dx, dy = x2 - x1, y2 - y1
    else:
        raise TypeError("Invalid arguments")
    return dx*dx + dy*dy

# ==============================================================
# Коллизии кругов
# ==============================================================

@overload
def circles_collision(x1: float, y1: float, r1: float, x2: float, y2: float, r2: float) -> bool:
    """
    Проверяет пересечение двух кругов.
    
    Параметры:
        x1, y1: центр первого круга
        r1: радиус первого круга
        x2, y2: центр второго круга
        r2: радиус второго круга
    
    Возвращает:
        bool: True если круги пересекаются или касаются
    """
    ...

@overload
def circles_collision(v1: VectorType, r1: float, v2: VectorType, r2: float) -> bool:
    """
    Проверяет пересечение двух кругов.
    
    Параметры:
        v1: центр первого круга (вектор)
        r1: радиус первого круга
        v2: центр второго круга (вектор)
        r2: радиус второго круга
    
    Возвращает:
        bool: True если круги пересекаются или касаются
    """
    ...

def circles_collision(x1, y1, r1, x2=None, y2=None, r2=None) -> bool:
    if isinstance(x1, VectorType) and isinstance(y1, VectorType):
        return distance_squared(x1, y1) <= (r1 + x2)**2  # x2 здесь выступает как r2
    elif all(isinstance(i, (int, float)) for i in [x1, y1, r1, x2, y2, r2]):
        return distance_squared(x1, y1, x2, y2) <= (r1 + r2)**2
    raise TypeError("Invalid arguments")

# ==============================================================
# Коллизии прямоугольников
# ==============================================================

@overload
def rects_collision(x1: float, y1: float, w1: float, h1: float, 
                    x2: float, y2: float, w2: float, h2: float) -> bool:
    """
    Проверяет пересечение двух прямоугольников (AABB).
    
    Параметры:
        x1, y1: левый верхний угол первого прямоугольника
        w1, h1: ширина и высота первого прямоугольника
        x2, y2: левый верхний угол второго прямоугольника
        w2, h2: ширина и высота второго прямоугольника
    
    Возвращает:
        bool: True если прямоугольники пересекаются
    """
    ...

@overload
def rects_collision(pos1: VectorType, size1: VectorType, 
                    pos2: VectorType, size2: VectorType) -> bool:
    """
    Проверяет пересечение двух прямоугольников (AABB).
    
    Параметры:
        pos1: позиция первого прямоугольника (вектор)
        size1: размер первого прямоугольника (вектор)
        pos2: позиция второго прямоугольника (вектор)
        size2: размер второго прямоугольника (вектор)
    
    Возвращает:
        bool: True если прямоугольники пересекаются
    """
    ...

def rects_collision(x1, y1, w1, h1, x2=None, y2=None, w2=None, h2=None) -> bool:
    if isinstance(x1, (Vector2f, Vector2i)) and isinstance(y1, (Vector2i, Vector2f)):
        pos1, size1, pos2, size2 = x1, y1, w1, h1
        return (pos1.x <= pos2.x + size2.x and 
                pos1.x + size1.x >= pos2.x and
                pos1.y <= pos2.y + size2.y and 
                pos1.y + size1.y >= pos2.y)
    
    elif all(isinstance(i, (int, float)) for i in [x1, y1, w1, h1, x2, y2, w2, h2]):
        return (x1 < x2 + w2 and 
                x1 + w1 > x2 and 
                y1 < y2 + h2 and 
                y1 + h1 > y2)
    
    raise TypeError("Invalid arguments")

# ==============================================================
# Новые полезные методы
# ==============================================================

def point_in_rect(point_x: Union[float, VectorType], 
                 rect_x: Union[float, VectorType], 
                 rect_w: Union[float, VectorType], 
                 rect_h: float = None) -> bool:
    """
    Проверяет, находится ли точка внутри прямоугольника.
    
    Параметры:
        point_x: координата x точки или вектор положения
        rect_x: координата x прямоугольника или вектор положения
        rect_w: ширина прямоугольника или вектор размера
        rect_h: высота прямоугольника (если rect_w не вектор)
    
    Возвращает:
        bool: True если точка внутри прямоугольника
    """
    if isinstance(point_x, VectorType):
        point, rect_pos, rect_size = point_x, rect_x, rect_w
        return (rect_pos.x <= point.x <= rect_pos.x + rect_size.x and 
                rect_pos.y <= point.y <= rect_pos.y + rect_size.y)
    else:
        return (rect_x <= point_x <= rect_x + rect_w and 
                rect_w <= rect_h <= rect_w + rect_h)

def line_intersection(x1: float, y1: float, x2: float, y2: float,
                     x3: float, y3: float, x4: float, y4: float) -> Union[Tuple[float, float], None]:
    """
    Находит точку пересечения двух отрезков.
    
    Параметры:
        Координаты двух отрезков (x1,y1)-(x2,y2) и (x3,y3)-(x4,y4)
    
    Возвращает:
        Tuple[float, float] или None: координаты пересечения или None если отрезки не пересекаются
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
    Проверяет пересечение круга и отрезка.
    
    Параметры:
        circle_x, circle_y: центр круга
        radius: радиус круга
        line_x1, line_y1: начало отрезка
        line_x2, line_y2: конец отрезка
    
    Возвращает:
        bool: True если есть пересечение
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
    Поворачивает точку вокруг центра на заданный угол.
    
    Параметры:
        center_x, center_y: центр вращения
        point_x, point_y: вращаемая точка
        angle: угол в радианах
    
    Возвращает:
        Tuple[float, float]: новые координаты точки
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
    Ограничивает значение заданными границами.
    
    Параметры:
        value: исходное значение
        min_val: минимальное допустимое значение
        max_val: максимальное допустимое значение
    
    Возвращает:
        float: значение в пределах [min_val, max_val]
    """
    return max(min_val, min(value, max_val))

def lerp(a: float, b: float, t: float) -> float:
    """
    Линейная интерполяция между двумя значениями.
    
    Параметры:
        a: начальное значение
        b: конечное значение
        t: параметр интерполяции (0.0 - a, 1.0 - b)
    
    Возвращает:
        float: интерполированное значение
    """
    return a + (b - a) * clamp(t, 0.0, 1.0)

def point_on_line_segment(px: float, py: float, 
                         x1: float, y1: float, 
                         x2: float, y2: float, 
                         tolerance: float = 1e-6) -> bool:
    """
    Проверяет, лежит ли точка на отрезке с заданной точностью.
    
    Параметры:
        px, py: координаты точки
        x1, y1: начало отрезка
        x2, y2: конец отрезка
        tolerance: допустимая погрешность
    
    Возвращает:
        bool: True если точка на отрезке
    """
    cross = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
    if abs(cross) > tolerance:
        return False
    
    dot = (px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)
    if dot < 0:
        return False
    
    squared_len = (x2 - x1)**2 + (y2 - y1)**2
    if dot > squared_len:
        return False
    
    return True


import random


class PerlinNoise2D:
    def __init__(self, seed: int = None):
        """Инициализация генератора шума Перлина.
        
        Args:
            seed (int, optional): Seed для генератора случайных чисел. 
                                 Если None, используется случайный seed.
        """
        self.seed = seed if seed is not None else random.randint(0, 1000000)
        random.seed(self.seed)
        
        # Создаем таблицу перестановок (256 случайных чисел)
        self.p: List[int] = list(range(256))
        random.shuffle(self.p)
        # Дублируем для упрощения вычислений
        self.p += self.p
        
        # Таблица градиентов для 2D
        self.gradients = [(math.cos(2 * math.pi * i / 256), 
                          math.sin(2 * math.pi * i / 256)) 
                         for i in range(256)]
    
    def fade(self, t: float) -> float:
        """6t^5 - 15t^4 + 10t^3 (функция плавности Кен Перлина)."""
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def lerp(self, a: float, b: float, t: float) -> float:
        """Линейная интерполяция между a и b."""
        return a + t * (b - a)
    
    def grad(self, hash: int, x: float, y: float) -> float:
        """Вычисляет скалярное произведение вектора градиента и вектора расстояния."""
        # Выбираем градиент из таблицы
        g = self.gradients[hash % 256]
        return g[0] * x + g[1] * y
    
    def noise(self, x: float, y: float) -> float:
        """Вычисляет значение шума Перлина в точке (x, y)."""
        # Определяем углы единичного квадрата, содержащего точку
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255
        
        # Дробные части координат
        x -= math.floor(x)
        y -= math.floor(y)
        
        # Вычисляем функции плавности
        u = self.fade(x)
        v = self.fade(y)
        
        # Хеши углов квадрата
        A = self.p[X] + Y
        AA = self.p[A]
        AB = self.p[A + 1]
        B = self.p[X + 1] + Y
        BA = self.p[B]
        BB = self.p[B + 1]
        
        # Линейная интерполяция
        return self.lerp(
            self.lerp(self.grad(AA, x, y), 
            self.grad(BA, x-1, y), u),
            self.lerp(self.grad(AB, x, y-1), 
            self.grad(BB, x-1, y-1), u),
            v)

