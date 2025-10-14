import sys
sys.path.append('./')

import math
import os
from Moon.python.Window import Window, WindowEvents
from Moon.python.Colors import *
from Moon.python.Vectors import Vector3f, Vector2f
from Moon.python.Rendering.Vertexes import VertexArray, Vertex

class OBJLoader:
    """Класс для загрузки и парсинга OBJ файлов"""

    @staticmethod
    def load_obj(file_path):
        """
        Загрузка OBJ файла и преобразование в структуру для рендеринга

        :Args:
        - file_path (str): Путь к OBJ файлу

        :Returns:
        - dict: Словарь с геометрией объекта
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"OBJ файл не найден: {file_path}")

        vertices = []
        texture_coords = []
        normals = []
        faces = []

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                if not parts:
                    continue

                # Вершины
                if parts[0] == 'v':
                    vertex = Vector3f(float(parts[1]), float(parts[2]), float(parts[3]))
                    vertices.append(vertex)

                # Текстурные координаты
                elif parts[0] == 'vt':
                    if len(parts) >= 3:
                        tex_coord = Vector2f(float(parts[1]), float(parts[2]))
                        texture_coords.append(tex_coord)

                # Нормали
                elif parts[0] == 'vn':
                    normal = Vector3f(float(parts[1]), float(parts[2]), float(parts[3]))
                    normals.append(normal)

                # Полигоны (грани)
                elif parts[0] == 'f':
                    face_vertices = []
                    for part in parts[1:]:
                        # Разбираем индексы вершины/текстуры/нормали
                        indices = part.split('/')
                        vertex_idx = int(indices[0]) - 1  # OBJ индексы начинаются с 1

                        tex_idx = -1
                        normal_idx = -1

                        if len(indices) > 1 and indices[1]:
                            tex_idx = int(indices[1]) - 1
                        if len(indices) > 2 and indices[2]:
                            normal_idx = int(indices[2]) - 1

                        face_vertices.append({
                            'vertex_idx': vertex_idx,
                            'tex_idx': tex_idx,
                            'normal_idx': normal_idx
                        })

                    # Преобразуем полигон в треугольники (триангуляция)
                    if len(face_vertices) >= 3:
                        # Простая триангуляция веером
                        for i in range(1, len(face_vertices) - 1):
                            triangle = [
                                face_vertices[0],
                                face_vertices[i],
                                face_vertices[i + 1]
                            ]
                            faces.append(triangle)

        return {
            'vertices': vertices,
            'texture_coords': texture_coords,
            'normals': normals,
            'faces': faces
        }


class OptimizedMesh3D:
    """
    Оптимизированный класс для отображения 3D мешей из OBJ файлов
    с отсечением невидимых граней и затенением
    """

    def __init__(self, position: Vector3f = Vector3f(0, 0, 0), scale: float = 1.0):
        self.position = position
        self.scale = scale
        self.rotation = Vector3f(0, 0, 0)
        self.rotation_speed = Vector3f(0, 1, 0)

        # Предварительно вычисленные значения
        self.camera_direction = Vector3f(0, 0, 1)
        self.light_direction = Vector3f(0.5, 0.5, -1).normalize()

        # VertexArray для рендера
        self.vertex_array = VertexArray()
        self.vertex_array.set_primitive_type(VertexArray.PrimitiveType.TRIANGLES)

        # Геометрия меша
        self.base_vertices = []
        self.faces = []
        self.colors = [COLOR_RED, COLOR_GREEN, COLOR_BLUE]

        # Кэш для тригонометрических функций
        self._sin_cache = {}
        self._cos_cache = {}

    def load_from_obj(self, file_path: str):
        """
        Загрузка меша из OBJ файла

        :Args:
        - file_path (str): Путь к OBJ файлу
        """
        obj_data = OBJLoader.load_obj(file_path)

        # Сохраняем исходные вершины
        self.base_vertices = obj_data['vertices']

        # Создаем структуру граней для рендеринга
        self.faces = []
        color_index = 0

        for face in obj_data['faces']:
            if len(face) != 3:
                continue  # Пропускаем не треугольники

            # Получаем индексы вершин
            vertex_indices = [f['vertex_idx'] for f in face]

            # Вычисляем нормаль для грани
            v0 = self.base_vertices[vertex_indices[0]]
            v1 = self.base_vertices[vertex_indices[1]]
            v2 = self.base_vertices[vertex_indices[2]]

            # Векторы сторон треугольника
            edge1 = Vector3f(v1.x - v0.x, v1.y - v0.y, v1.z - v0.z)
            edge2 = Vector3f(v2.x - v0.x, v2.y - v0.y, v2.z - v0.z)

            # Векторное произведение для получения нормали
            normal = Vector3f(
                edge1.y * edge2.z - edge1.z * edge2.y,
                edge1.z * edge2.x - edge1.x * edge2.z,
                edge1.x * edge2.y - edge1.y * edge2.x
            ).normalize()

            # Цвет для грани (циклически)
            color = self.colors[color_index % len(self.colors)]
            color_index += 1

            self.faces.append({
                'vertices': vertex_indices,
                'normal': normal,
                'color': color,
                'triangles': [tuple(vertex_indices)]  # Уже треугольник
            })

    def create_sphere(self, radius: float = 1.0, segments: int = 16):
        """Создание сферы (альтернатива OBJ загрузке)"""
        self.base_vertices = []
        self.faces = []

        # Генерация вершин сферы
        for i in range(segments + 1):
            lat = math.pi * i / segments
            sin_lat = math.sin(lat)
            cos_lat = math.cos(lat)

            for j in range(segments + 1):
                lon = 2 * math.pi * j / segments
                sin_lon = math.sin(lon)
                cos_lon = math.cos(lon)

                x = radius * sin_lat * cos_lon
                y = radius * sin_lat * sin_lon
                z = radius * cos_lat

                self.base_vertices.append(Vector3f(x, y, z))

        # Генерация треугольников
        color_index = 0
        for i in range(segments):
            for j in range(segments):
                v0 = i * (segments + 1) + j
                v1 = v0 + 1
                v2 = v0 + (segments + 1)
                v3 = v2 + 1

                if i > 0:
                    normal = self.base_vertices[v0].normalize()
                    color = self.colors[color_index % len(self.colors)]
                    color_index += 1

                    self.faces.append({
                        'vertices': [v0, v2, v1],
                        'normal': normal,
                        'color': color,
                        'triangles': [(v0, v2, v1)]
                    })

                if i < segments - 1:
                    normal = self.base_vertices[v3].normalize()
                    color = self.colors[color_index % len(self.colors)]
                    color_index += 1

                    self.faces.append({
                        'vertices': [v1, v2, v3],
                        'normal': normal,
                        'color': color,
                        'triangles': [(v1, v2, v3)]
                    })

    def _get_trig_values(self, angle):
        """Кэширование тригонометрических значений"""
        key = int(angle * 1000)
        if key not in self._sin_cache:
            rad = math.radians(angle)
            self._sin_cache[key] = math.sin(rad)
            self._cos_cache[key] = math.cos(rad)
        return self._sin_cache[key], self._cos_cache[key]

    def _rotate_vertex_optimized(self, vertex: Vector3f) -> Vector3f:
        """Оптимизированное вращение вершины"""
        sx, cx = self._get_trig_values(self.rotation.x)
        sy, cy = self._get_trig_values(self.rotation.y)
        sz, cz = self._get_trig_values(self.rotation.z)

        # Вращение вокруг X
        y1 = vertex.y * cx - vertex.z * sx
        z1 = vertex.y * sx + vertex.z * cx

        # Вращение вокруг Y
        x2 = vertex.x * cy + z1 * sy
        z2 = -vertex.x * sy + z1 * cy

        # Вращение вокруг Z
        x3 = x2 * cz - y1 * sz
        y3 = x2 * sz + y1 * cz

        return Vector3f(x3, y3, z2)

    def _rotate_vector_optimized(self, vector: Vector3f) -> Vector3f:
        """Оптимизированное вращение вектора"""
        return self._rotate_vertex_optimized(vector)

    def _is_face_visible_optimized(self, face_normal: Vector3f) -> bool:
        """Проверка видимости грани"""
        return face_normal.dot(self.camera_direction) < 0

    def _calculate_face_depth_optimized(self, face_vertices: list, rotated_vertices: list) -> float:
        """Расчет глубины грани"""
        return sum(rotated_vertices[i].z for i in face_vertices) / len(face_vertices)

    def set_position(self, pos: Vector3f):
        self.position = pos

    def set_scale(self, scale: float):
        self.scale = scale

    def set_rotation_speed(self, speed: Vector3f):
        self.rotation_speed = speed

    def update(self):
        """Обновление меша"""
        self.rotation.x = (self.rotation.x + self.rotation_speed.x) % 360
        self.rotation.y = (self.rotation.y + self.rotation_speed.y) % 360
        self.rotation.z = (self.rotation.z + self.rotation_speed.z) % 360

        self._update_vertices_optimized()

    def _update_vertices_optimized(self):
        """Обновление вершин для рендеринга"""
        # Применяем вращение и масштаб ко всем вершинам
        rotated_vertices = []
        for vertex in self.base_vertices:
            # Масштабирование
            scaled_vertex = Vector3f(
                vertex.x * self.scale,
                -vertex.y * self.scale,
                vertex.z * self.scale
            )
            # Вращение
            rotated_vertex = self._rotate_vertex_optimized(scaled_vertex)
            rotated_vertices.append(rotated_vertex)

        # Очищаем массив вершин
        self.vertex_array.clear()

        # Собираем видимые грани
        visible_faces = []

        for face in self.faces:
            rotated_normal = self._rotate_vector_optimized(face['normal'])

            if self._is_face_visible_optimized(rotated_normal):
                depth = self._calculate_face_depth_optimized(face['vertices'], rotated_vertices)

                # Вычисление освещения
                light_intensity = max(0.3, min(1.0, abs(rotated_normal.dot(self.light_direction))))

                # Затемнение цвета
                base_color = face['color']
                shaded_color = Color(
                    int(base_color.r * light_intensity),
                    int(base_color.g * light_intensity),
                    int(base_color.b * light_intensity)
                )

                visible_faces.append({
                    'face': face,
                    'depth': depth,
                    'rotated_vertices': rotated_vertices,
                    'shaded_color': shaded_color
                })

        # Сортировка по глубине
        visible_faces.sort(key=lambda x: x['depth'], reverse=True)

        # Добавление вершин в VertexArray
        pos_x, pos_y = self.position.x, self.position.y

        for face_info in visible_faces:
            face = face_info['face']
            rot_verts = face_info['rotated_vertices']
            color = face_info['shaded_color']

            for triangle in face['triangles']:
                for idx in triangle:
                    v = rot_verts[idx]

                    # Проекция 3D в 2D
                    z = v.z + 10
                    if z <= 0:
                        z = 0.1

                    scale = 300 / z
                    screen_x = v.x * scale + pos_x
                    screen_y = v.y * scale + pos_y

                    self.vertex_array.append(Vertex(Vector2f(screen_x, screen_y), color))

    def draw(self, window: Window):
        """Отрисовка меша"""
        window.draw(self.vertex_array)


class MeshViewerApp:
    """Приложение для просмотра 3D мешей"""

    def __init__(self):
        self.window = Window(1200, 800, "3D Mesh Viewer - OBJ Loader")
        self.events = WindowEvents()
        self.window.set_wait_fps(180)

        # Создаем меш
        self.mesh = OptimizedMesh3D(position=Vector3f(600, 400, 0), scale=7.0)

        # Попытка загрузить OBJ файл или создать сферу по умолчанию
        obj_files = [
            "demos\model.obj"
        ]

        mesh_loaded = False
        for obj_file in obj_files:

                self.mesh.load_from_obj(obj_file)
                print(f"Успешно загружен: {obj_file}")
                mesh_loaded = True
                break


        # Если OBJ не найден, создаем сферу
        if not mesh_loaded:
            print("OBJ файлы не найдены, создается сфера...")
            self.mesh.create_sphere(radius=3.0, segments=20)

        # Настройки окна
        self.window.set_clear_color(Color(20, 20, 40))
        self.window.set_view_info(True)

    def run(self):
        """Главный цикл приложения"""
        center_x = self.window.get_width() / 2
        center_y = self.window.get_height() / 2

        while self.window.update(self.events):
            self.window.clear()

            # Плавное движение
            timer = self.window.get_global_timer(10)

            self.mesh.set_position(Vector3f(center_x, center_y, 0))

            # Обновление и отрисовка
            self.mesh.update()
            self.mesh.draw(self.window)

            self.window.view_info()
            self.window.display()

        self.window.close()


# Запуск приложения
if __name__ == "__main__":
    app = MeshViewerApp()
    app.run()
