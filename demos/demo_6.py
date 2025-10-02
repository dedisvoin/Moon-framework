import sys
sys.path.append('./')

import math
from Moon.python.Window import Window, WindowEvents
from Moon.python.Colors import *
from Moon.python.Vectors import Vector3f, Vector2f
from Moon.python.Rendering.Vertexes import VertexArray, Vertex

class Cube3D:
    """
    #### Класс для создания и отрисовки 3D куба с отсечением невидимых граней

    ---

    :Description:
    - Создает 3D куб с использованием VertexArray
    - Поддерживает вращение вокруг всех осей
    - Использует треугольники для построения граней
    - Отсекает невидимые грани (backface culling)
    - Сортирует грани по глубине для правильного отображения
    """

    def __init__(self, size: float = 1.0, position: Vector3f = Vector3f(0, 0, 0)):
        """
        #### Инициализация 3D куба

        ---

        :Args:
        - size (float): Размер куба (длина ребра)
        - position (Vector3f): Позиция центра куба в пространстве
        """
        self.size = size
        self.position = position
        self.rotation = Vector3f(0, 0, 0)  # Углы вращения вокруг осей X, Y, Z
        self.rotation_speed = Vector3f(0.5, 2.5, 1)  # Скорость вращения

        # Цвета для каждой грани куба
        self.face_colors = [
            COLOR_GREEN
        ] * 6

        # Направление камеры (вектор взгляда)
        self.camera_direction = Vector3f(0, 0, 1)

        # Создаем массив вершин для куба
        self.vertex_array = VertexArray()
        self.vertex_array.set_primitive_type(VertexArray.PrimitiveType.TRIANGLES)

        # Сохраняем исходную геометрию для пересчета
        self._create_base_geometry()

    def set_position(self, pos: Vector3f):
        self.position = pos

    def _create_base_geometry(self):
        """Создает базовую геометрию куба"""
        half_size = self.size / 2.0

        # Базовые вершины куба в локальных координатах
        self.base_vertices = [
            # Передняя грань
            Vector3f(-half_size, -half_size, half_size),  # 0
            Vector3f(half_size, -half_size, half_size),   # 1
            Vector3f(half_size, half_size, half_size),    # 2
            Vector3f(-half_size, half_size, half_size),   # 3

            # Задняя грань
            Vector3f(-half_size, -half_size, -half_size), # 4
            Vector3f(-half_size, half_size, -half_size),  # 5
            Vector3f(half_size, half_size, -half_size),   # 6
            Vector3f(half_size, -half_size, -half_size),  # 7
        ]

        # Определяем грани куба (индексы вершин и нормали)
        self.faces = [
            {
                'name': 'front',
                'vertices': [0, 1, 2, 3],
                'normal': Vector3f(0, 0, 1),  # Направлена вперед
                'color': self.face_colors[0],
                'triangles': [(0, 1, 2), (2, 3, 0)]
            },
            {
                'name': 'back',
                'vertices': [4, 5, 6, 7],
                'normal': Vector3f(0, 0, -1),  # Направлена назад
                'color': self.face_colors[1],
                'triangles': [(4, 5, 6), (6, 7, 4)]
            },
            {
                'name': 'right',
                'vertices': [1, 7, 6, 2],
                'normal': Vector3f(1, 0, 0),  # Направлена вправо
                'color': self.face_colors[2],
                'triangles': [(1, 7, 6), (6, 2, 1)]
            },
            {
                'name': 'left',
                'vertices': [4, 0, 3, 5],
                'normal': Vector3f(-1, 0, 0),  # Направлена влево
                'color': self.face_colors[3],
                'triangles': [(4, 0, 3), (3, 5, 4)]
            },
            {
                'name': 'top',
                'vertices': [3, 2, 6, 5],
                'normal': Vector3f(0, 1, 0),  # Направлена вверх
                'color': self.face_colors[4],
                'triangles': [(3, 2, 6), (6, 5, 3)]
            },
            {
                'name': 'bottom',
                'vertices': [4, 7, 1, 0],
                'normal': Vector3f(0, -1, 0),  # Направлена вниз
                'color': self.face_colors[5],
                'triangles': [(4, 7, 1), (1, 0, 4)]
            }
        ]

    def _is_face_visible(self, face_normal: Vector3f) -> bool:
        """
        #### Проверяет видимость грани

        ---

        :Description:
        - Использует скалярное произведение для определения видимости
        - Грань видима если ее нормаль направлена К камере

        :Args:
        - face_normal (Vector3f): Нормаль грани после вращения

        :Returns:
        - bool: True если грань видима, False если невидима
        """
        # Нормализуем векторы для точного расчета
        normalized_normal = face_normal.normalize()
        normalized_camera = self.camera_direction.normalize()

        # Скалярное произведение: если > 0 - грань направлена К камере (видима)
        dot_product = normalized_normal.dot(normalized_camera)

        # Возвращаем True если грань направлена К камере
        return dot_product < 0

    def _calculate_face_depth(self, face_vertices: list, rotated_vertices: list) -> float:
        """
        #### Вычисляет среднюю глубину грани для сортировки

        ---

        :Args:
        - face_vertices (list): Индексы вершин грани
        - rotated_vertices (list): Список повернутых вершин

        :Returns:
        - float: Средняя z-координата грани (глубина)
        """
        total_z = 0
        for vertex_idx in face_vertices:
            total_z += rotated_vertices[vertex_idx].z
        return total_z / len(face_vertices)

    def update(self, delta_time: float):
        """
        #### Обновление вращения куба

        ---

        :Args:
        - delta_time (float): Время с последнего обновления
        """
        # Обновляем углы вращения
        self.rotation.x += self.rotation_speed.x * delta_time
        self.rotation.y += self.rotation_speed.y * delta_time
        self.rotation.z += self.rotation_speed.z * delta_time

        # Нормализуем углы
        self.rotation.x %= 360
        self.rotation.y %= 360
        self.rotation.z %= 360

        self._update_vertices()

    def _rotate_vertex(self, vertex: Vector3f) -> Vector3f:
        """
        #### Применяет вращение к вершине

        ---

        :Args:
        - vertex (Vector3f): Исходная вершина

        :Returns:
        - Vector3f: Повернутая вершина
        """
        # Вращение вокруг оси X
        y = vertex.y * math.cos(math.radians(self.rotation.x)) - vertex.z * math.sin(math.radians(self.rotation.x))
        z = vertex.y * math.sin(math.radians(self.rotation.x)) + vertex.z * math.cos(math.radians(self.rotation.x))

        # Вращение вокруг оси Y
        x = vertex.x * math.cos(math.radians(self.rotation.y)) + z * math.sin(math.radians(self.rotation.y))
        z = -vertex.x * math.sin(math.radians(self.rotation.y)) + z * math.cos(math.radians(self.rotation.y))

        # Вращение вокруг оси Z
        x_new = x * math.cos(math.radians(self.rotation.z)) - y * math.sin(math.radians(self.rotation.z))
        y_new = x * math.sin(math.radians(self.rotation.z)) + y * math.cos(math.radians(self.rotation.z))

        return Vector3f(x_new, y_new, z)

    def _rotate_vector(self, vector: Vector3f) -> Vector3f:
        """
        #### Применяет вращение к вектору (для нормалей)

        ---

        :Args:
        - vector (Vector3f): Исходный вектор

        :Returns:
        - Vector3f: Повернутый вектор
        """
        # Вращение вокруг оси X
        y = vector.y * math.cos(math.radians(self.rotation.x)) - vector.z * math.sin(math.radians(self.rotation.x))
        z = vector.y * math.sin(math.radians(self.rotation.x)) + vector.z * math.cos(math.radians(self.rotation.x))

        # Вращение вокруг оси Y
        x = vector.x * math.cos(math.radians(self.rotation.y)) + z * math.sin(math.radians(self.rotation.y))
        z = -vector.x * math.sin(math.radians(self.rotation.y)) + z * math.cos(math.radians(self.rotation.y))

        # Вращение вокруг оси Z
        x_new = x * math.cos(math.radians(self.rotation.z)) - y * math.sin(math.radians(self.rotation.z))
        y_new = x * math.sin(math.radians(self.rotation.z)) + y * math.cos(math.radians(self.rotation.z))

        return Vector3f(x_new, y_new, z)

    def _update_vertices(self):
        """Обновляет позиции вершин с учетом вращения, отсечения невидимых граней и сортировки по глубине"""
        # Применяем вращение к базовым вершинам
        rotated_vertices = []
        for vertex in self.base_vertices:
            rotated = self._rotate_vertex(vertex)
            rotated_vertices.append(rotated)

        # Очищаем массив вершин
        self.vertex_array.clear()

        # Собираем видимые грани с информацией о глубине
        visible_faces = []

        for face in self.faces:
            # Поворачиваем нормаль грани
            rotated_normal = self._rotate_vector(face['normal'])

            # Проверяем видимость грани
            if self._is_face_visible(rotated_normal):
                # Вычисляем среднюю глубину грани
                depth = self._calculate_face_depth(face['vertices'], rotated_vertices)

                # Сохраняем информацию о грани
                visible_faces.append({
                    'face': face,
                    'depth': depth,
                    'rotated_vertices': rotated_vertices
                })

        # СОРТИРОВКА: сортируем грани по глубине (от дальних к ближним)
        visible_faces.sort(key=lambda x: x['depth'], reverse=True)

        # Добавляем грани в порядке от дальних к ближним
        for face_info in visible_faces:
            face = face_info['face']
            rotated_vertices = face_info['rotated_vertices']

            # Добавляем треугольники видимой грани
            for triangle in face['triangles']:
                for vertex_idx in triangle:
                    vertex_3d = rotated_vertices[vertex_idx]

                    # Проекция 3D в 2D с перспективой
                    z = vertex_3d.z + 10  # Сдвиг по Z для перспективы
                    scale = 200 / (z + 10)  # Масштаб в зависимости от глубины

                    screen_x = vertex_3d.x * scale + self.position.x
                    screen_y = vertex_3d.y * scale + self.position.y

                    # Создаем вершину
                    vertex = Vertex(
                        Vector2f(screen_x, screen_y),
                        face['color']
                    )
                    self.vertex_array.append(vertex)

    def draw(self, window: Window):
        """
        #### Отрисовывает куб в окне

        ---

        :Args:
        - window (Window): Окно для отрисовки
        """
        window.draw(self.vertex_array)


class AdvancedCube3D(Cube3D):
    """
    #### Улучшенная версия 3D куба с затенением

    ---

    :Features:
    - Отсечение невидимых граней
    - Простое затенение на основе нормалей
    - Более реалистичная перспективная проекция
    - Сортировка граней по глубине
    """

    def __init__(self, size: float = 1.0, position: Vector3f = Vector3f(0, 0, 0)):
        super().__init__(size, position)
        self.light_direction = Vector3f(0.5, 0.5, -1).normalize()

    def _update_vertices(self):
        """Обновляет вершины с затенением и сортировкой"""
        rotated_vertices = []
        for vertex in self.base_vertices:
            rotated = self._rotate_vertex(vertex)
            rotated_vertices.append(rotated)

        self.vertex_array.clear()

        # Собираем видимые грани с информацией о глубине
        visible_faces = []

        for face in self.faces:
            # Поворачиваем нормаль грани
            rotated_normal = self._rotate_vector(face['normal'])

            # Проверяем видимость грани
            if self._is_face_visible(rotated_normal):
                # Вычисляем среднюю глубину грани
                depth = self._calculate_face_depth(face['vertices'], rotated_vertices)

                # Вычисляем интенсивность освещения
                light_intensity = max(0.3, rotated_normal.dot(self.light_direction))

                # Затемняем цвет грани
                shaded_color = Color(
                    int(face['color'].r * light_intensity),
                    int(face['color'].g * light_intensity),
                    int(face['color'].b * light_intensity)
                )

                # Сохраняем информацию о грани
                visible_faces.append({
                    'face': face,
                    'depth': depth,
                    'rotated_vertices': rotated_vertices,
                    'shaded_color': shaded_color
                })

        # СОРТИРОВКА: сортируем грани по глубине (от дальних к ближним)
        visible_faces.sort(key=lambda x: x['depth'], reverse=True)

        # Добавляем грани в порядке от дальних к ближним
        for face_info in visible_faces:
            face = face_info['face']
            rotated_vertices = face_info['rotated_vertices']
            shaded_color = face_info['shaded_color']

            # Добавляем треугольники
            for triangle in face['triangles']:
                for vertex_idx in triangle:
                    vertex_3d = rotated_vertices[vertex_idx]

                    # Улучшенная перспективная проекция
                    z = vertex_3d.z + 10  # Большее расстояние для лучшей перспективы
                    if z <= 0: z = 0.1  # Избегаем деления на ноль

                    scale = 600 / z  # Масштаб в зависимости от глубины

                    screen_x = vertex_3d.x * scale + self.position.x
                    screen_y = vertex_3d.y * scale + self.position.y

                    vertex = Vertex(
                        Vector2f(screen_x, screen_y),
                        shaded_color
                    )
                    self.vertex_array.append(vertex)


class RotatingCubeApp:
    """
    #### Приложение с вращающимся 3D кубом

    ---

    :Description:
    - Создает окно с вращающимся разноцветным кубом
    - Управляет обновлением и отрисовкой сцены
    - Обрабатывает пользовательский ввод
    """

    def __init__(self, use_advanced_cube: bool = True):
        """Инициализация приложения"""
        self.window = Window(800, 600, "3D Rotating Cube - Backface Culling & Depth Sorting")
        self.events = WindowEvents()
        self.window.set_wait_fps(180)

        if use_advanced_cube:
            self.cube = AdvancedCube3D(size=5.0, position=Vector3f(400, 300, 0))
        else:
            self.cube = Cube3D(size=8.0, position=Vector3f(400, 300, 0))

        # Настройки окна
        self.window.set_clear_color(Color(20, 20, 40))  # Темно-синий фон
        self.window.set_view_info(True)  # Показать информацию о FPS

    def run(self):
        """Запуск основного цикла приложения"""
        while self.window.update(self.events):
            # Обновление состояния

            # Очистка экрана
            self.window.clear()

            # Обновление и отрисовка куба
            self.cube.set_position(Vector3f(self.window.get_width() / 2, self.window.get_height() / 2 + math.sin(self.window.get_global_timer(10)) * 10, 0))
            self.cube.update(self.window.get_delta())
            self.cube.draw(self.window)

            # Отображение информации и обновление экрана
            self.window.view_info()
            self.window.display()

        # Закрытие окна при выходе
        self.window.close()


# Запуск приложения
if __name__ == "__main__":
    # Используйте True для версии с затенением, False для базовой версии
    app = RotatingCubeApp(use_advanced_cube=True)
    app.run()
