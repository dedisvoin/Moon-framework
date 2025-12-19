import sys
sys.path.append('./')

import math
import os
from numba import jit, float32, int32, njit
import numpy as np
from Moon.python.Window import Window, WindowEvents
from Moon.python.Colors import *
from Moon.python.Vectors import Vector3f, Vector2f
from Moon.python.Rendering.Vertexes import *

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


# Numba-оптимизированные функции
@jit(nopython=True)
def rotate_vertices_numba(vertices, scale, rotation_x, rotation_y, rotation_z):
    """Оптимизированное вращение всех вершин с использованием Numba"""
    num_vertices = vertices.shape[0]
    result = np.empty((num_vertices, 3), dtype=np.float32)

    # Преобразуем углы в радианы и вычисляем тригонометрические функции
    sx = math.sin(math.radians(rotation_x))
    cx = math.cos(math.radians(rotation_x))
    sy = math.sin(math.radians(rotation_y))
    cy = math.cos(math.radians(rotation_y))
    sz = math.sin(math.radians(rotation_z))
    cz = math.cos(math.radians(rotation_z))

    for i in range(num_vertices):
        x = vertices[i, 0] * scale
        y = vertices[i, 1] * scale
        z = vertices[i, 2] * scale

        # Вращение вокруг X
        y1 = y * cx - z * sx
        z1 = y * sx + z * cx

        # Вращение вокруг Y
        x2 = x * cy + z1 * sy
        z2 = -x * sy + z1 * cy

        # Вращение вокруг Z
        x3 = x2 * cz - y1 * sz
        y3 = x2 * sz + y1 * cz

        result[i, 0] = x3
        result[i, 1] = y3
        result[i, 2] = z2

    return result

@njit(nopython=True)
def rotate_normals_numba(normals, rotation_x, rotation_y, rotation_z):
    """Оптимизированное вращение нормалей с использованием Numba"""
    num_normals = normals.shape[0]
    result = np.empty((num_normals, 3), dtype=np.float32)

    # Преобразуем углы в радианы и вычисляем тригонометрические функции
    sx = math.sin(math.radians(rotation_x))
    cx = math.cos(math.radians(rotation_x))
    sy = math.sin(math.radians(rotation_y))
    cy = math.cos(math.radians(rotation_y))
    sz = math.sin(math.radians(rotation_z))
    cz = math.cos(math.radians(rotation_z))

    for i in range(num_normals):
        x = normals[i, 0]
        y = normals[i, 1]
        z = normals[i, 2]

        # Вращение вокруг X
        y1 = y * cx - z * sx
        z1 = y * sx + z * cx

        # Вращение вокруг Y
        x2 = x * cy + z1 * sy
        z2 = -x * sy + z1 * cy

        # Вращение вокруг Z
        x3 = x2 * cz - y1 * sz
        y3 = x2 * sz + y1 * cz

        # Нормализация
        length = math.sqrt(x3*x3 + y3*y3 + z2*z2)
        if length > 0:
            result[i, 0] = x3 / length
            result[i, 1] = y3 / length
            result[i, 2] = z2 / length
        else:
            result[i, 0] = 0
            result[i, 1] = 0
            result[i, 2] = 0

    return result

@njit(nopython=True)
def check_face_visibility_numba(rotated_normals, camera_dir):
    """Оптимизированная проверка видимости всех граней"""
    num_normals = rotated_normals.shape[0]
    visibility = np.empty(num_normals, dtype=np.bool_)

    for i in range(num_normals):
        dot_product = (rotated_normals[i, 0] * camera_dir[0] +
                      rotated_normals[i, 1] * camera_dir[1] +
                      rotated_normals[i, 2] * camera_dir[2])
        visibility[i] = dot_product < 0

    return visibility

@njit(nopython=True)
def calculate_lighting_numba(rotated_normals, light_dir):
    """Оптимизированное вычисление освещения для всех граней"""
    num_normals = rotated_normals.shape[0]
    intensities = np.empty(num_normals, dtype=np.float32)

    for i in range(num_normals):
        dot_product = (rotated_normals[i, 0] * light_dir[0] +
                      rotated_normals[i, 1] * light_dir[1] +
                      rotated_normals[i, 2] * light_dir[2])
        intensity = abs(dot_product)
        intensities[i] = max(0.3, min(1.0, intensity))

    return intensities

@njit(nopython=True, )
def calculate_face_depths_numba(face_indices, rotated_vertices):
    """Оптимизированное вычисление глубины для всех граней"""
    num_faces = face_indices.shape[0]
    depths = np.empty(num_faces, dtype=np.float32)

    for i in range(num_faces):
        idx0 = face_indices[i, 0]
        idx1 = face_indices[i, 1]
        idx2 = face_indices[i, 2]

        z0 = rotated_vertices[idx0, 2] if 0 <= idx0 < len(rotated_vertices) else 0.0
        z1 = rotated_vertices[idx1, 2] if 0 <= idx1 < len(rotated_vertices) else 0.0
        z2 = rotated_vertices[idx2, 2] if 0 <= idx2 < len(rotated_vertices) else 0.0

        depths[i] = (z0 + z1 + z2) / 3.0

    return depths


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
        self.vertex_array = VertexList()
        self.vertex_array.set_primitive_type(VertexListTypes.Triangles)

        # Геометрия меша
        self.base_vertices = []
        self.faces = []
        self.colors = [COLOR_GRAY]

        # NumPy массивы для Numba оптимизаций
        self._vertices_np = None
        self._normals_np = None
        self._face_indices_np = None  # Теперь это будет NumPy массив
        self._face_colors = []

    def load_from_obj(self, file_path: str):
        """
        Загрузка меша из OBJ файла

        :Args:
        - file_path (str): Путь к OBJ файлу
        """
        obj_data = OBJLoader.load_obj(file_path)

        # Сохраняем исходные вершины
        self.base_vertices = obj_data['vertices']

        # Создаем NumPy массив вершин для Numba
        self._vertices_np = np.array([[v.x, v.y, v.z] for v in self.base_vertices], dtype=np.float32)

        # Создаем структуру граней для рендеринга
        self.faces = []
        face_indices_list = []
        normals_list = []
        self._face_colors = []

        color_index = 0

        for face in obj_data['faces']:
            if len(face) != 3:
                continue  # Пропускаем не треугольники

            # Получаем индексы вершин
            vertex_indices = [f['vertex_idx'] for f in face]
            face_indices_list.append(vertex_indices)

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

            normals_list.append([normal.x, normal.y, normal.z])

            # Цвет для грани (циклически)
            color = self.colors[color_index % len(self.colors)]
            color_index += 1
            self._face_colors.append(color)

            self.faces.append({
                'vertices': vertex_indices,
                'normal': normal,
                'color': color,
                'triangles': [tuple(vertex_indices)]
            })

        # Создаем NumPy массивы
        self._normals_np = np.array(normals_list, dtype=np.float32)
        self._face_indices_np = np.array(face_indices_list, dtype=np.int32)

    def create_sphere(self, radius: float = 1.0, segments: int = 16):
        """Создание сферы (альтернатива OBJ загрузке)"""
        self.base_vertices = []
        self.faces = []
        face_indices_list = []
        normals_list = []
        self._face_colors = []

        vertices_list = []
        color_index = 0

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

                vertex = Vector3f(x, y, z)
                self.base_vertices.append(vertex)
                vertices_list.append([x, y, z])

        # Создаем NumPy массив вершин
        self._vertices_np = np.array(vertices_list, dtype=np.float32)

        # Генерация треугольников
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

                    face_indices_list.append([v0, v2, v1])
                    normals_list.append([normal.x, normal.y, normal.z])
                    self._face_colors.append(color)

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

                    face_indices_list.append([v1, v2, v3])
                    normals_list.append([normal.x, normal.y, normal.z])
                    self._face_colors.append(color)

                    self.faces.append({
                        'vertices': [v1, v2, v3],
                        'normal': normal,
                        'color': color,
                        'triangles': [(v1, v2, v3)]
                    })

        # Создаем NumPy массивы
        self._normals_np = np.array(normals_list, dtype=np.float32)
        self._face_indices_np = np.array(face_indices_list, dtype=np.int32)

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
        """Обновление вершин для рендеринга с использованием Numba"""
        if (self._vertices_np is None or self._normals_np is None or
            self._face_indices_np is None or len(self._face_indices_np) == 0):
            return

        # Оптимизированные вычисления с Numba
        rotated_vertices = rotate_vertices_numba(
            self._vertices_np, self.scale,
            self.rotation.x, self.rotation.y, self.rotation.z
        )

        rotated_normals = rotate_normals_numba(
            self._normals_np,
            self.rotation.x, self.rotation.y, self.rotation.z
        )

        # Проверка видимости граней
        camera_dir = np.array([self.camera_direction.x, self.camera_direction.y, self.camera_direction.z], dtype=np.float32)
        face_visibility = check_face_visibility_numba(rotated_normals, camera_dir)

        # Вычисление освещения
        light_dir = np.array([self.light_direction.x, self.light_direction.y, self.light_direction.z], dtype=np.float32)
        light_intensities = calculate_lighting_numba(rotated_normals, light_dir)

        # Вычисление глубины для видимых граней
        depths = calculate_face_depths_numba(self._face_indices_np, rotated_vertices)

        # Очищаем массив вершин
        self.vertex_array.clear()

        # Собираем видимые грани для отрисовки
        visible_faces = []

        for i in range(len(self._face_indices_np)):
            if face_visibility[i]:
                visible_faces.append({
                    'index': i,
                    'depth': depths[i],
                    'light_intensity': light_intensities[i]
                })

        # Сортировка по глубине
        visible_faces.sort(key=lambda x: x['depth'], reverse=True)

        # Добавление вершин в VertexArray
        for face_info in visible_faces:
            i = face_info['index']
            face_indices = self._face_indices_np[i]
            light_intensity = face_info['light_intensity']
            base_color = self._face_colors[i]

            # Затемнение цвета
            shaded_color = Color(
                int(base_color.r * light_intensity),
                int(base_color.g * light_intensity),
                int(base_color.b * light_intensity)
            )

            # Добавляем вершины треугольника
            for idx in face_indices:
                if 0 <= idx < len(rotated_vertices):
                    v = rotated_vertices[idx]

                    # Проекция 3D в 2D
                    z = v[2] + 10
                    if z <= 0:
                        z = 0.1

                    scale = 300 / z
                    screen_x = v[0] * scale + self.position.x
                    screen_y = v[1] * scale + self.position.y

                    self.vertex_array.auto_append(
                        Vertex2d.FromPositionAndColor(Vector2f(screen_x, screen_y), shaded_color)
                    )

    def draw(self, window: Window):
        """Отрисовка меша"""
        window.draw(self.vertex_array)


class MeshViewerApp:
    """Приложение для просмотра 3D мешей"""

    def __init__(self):
        self.window = Window(1200, 800, "3D Mesh Viewer - OBJ Loader", dynamic_update=True)
        self.events = WindowEvents()
        self.window.set_wait_fps(180)

        # Создаем меш
        self.mesh = OptimizedMesh3D(position=Vector3f(600, 400, 0), scale=8.0)

        # Попытка загрузить OBJ файл или создать сферу по умолчанию
        obj_files = [
            "demos\demo_6\model.obj"
        ]

        mesh_loaded = False
        for obj_file in obj_files:
            try:
                self.mesh.load_from_obj(obj_file)
                print(f"Успешно загружен: {obj_file}")
                mesh_loaded = True
                break
            except FileNotFoundError:
                continue

        # Если OBJ не найден, создаем сферу
        if not mesh_loaded:
            print("OBJ файлы не найдены, создается сфера...")
            self.mesh.create_sphere(radius=3.0, segments=20)

        # Настройки окна
        self.window.set_clear_color(Color(20, 20, 40))
        self.window.set_view_info(True)

    def run(self):
        """Главный цикл приложения"""
        while self.window.update(self.events):
            self.window.clear()

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
