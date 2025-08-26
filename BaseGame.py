from Moon.python.Window import *
from Moon.python.Rendering.Sprites import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Engine.Camera import Camera2D
from Moon.python.Rendering.Shaders import *
from Moon.python.Audio import *
from Moon.python.Inputs import *
from Moon.python.Math import distance
from Moon.python.Engine.ParticleSystem import *
import random


window = Window(1920, 1080, title="Minesweeper", context_settings=ContextSettings().set_antialiasing_level(8), vsync=True, style=Window.Style.FullScreenDesktop).set_view_info()
window.enable_fpsmonitor_keybinding()
window.set_fpsmonitor_keybinding('shift+m')
window.enable_ghosting()
window.set_wait_fps(60)
window.set_fps_monitor_opened(False)
window_events = WindowEvents()


NATIVE_SCREEN_RESOLUTION = get_screen_resolution()

class Cell:
    def __init__(self):
        self.open = False
        self.this_mine = False
        self.position = None
        self.mine_count = 0
        self.flagged = False
        self.opening_progress = 0.0  # Прогресс анимации открытия (0..1)
        self.start = False
        self.draging = 0


class Game:
    def __init__(self):
        self.map_cell_size = 10
        self.flag_count = 0
        sprites = LoadSpriteArrayFromSprite("game_data/spites.png", [10, 10], self.map_cell_size / 10)
        self.data = {
            'mine_sprite': sprites[9],
            "1": sprites[0],
            "2": sprites[1],
            "3": sprites[2],
            "4": sprites[3],
            "5": sprites[4],
            "6": sprites[5],
            "7": sprites[6],
            "8": sprites[7],
            "flag": sprites[8],
            "closed": sprites[10],  # Спрайт для закрытой клетки
            "cell_open_sound": MultiSound(Sound(SoundBuffer("game_data/cell_opening.wav")), 30).set_volume_all(50),
            "flag_set_sound": Sound(SoundBuffer("game_data/flag_set.wav")).set_volume(60),
            "flag_destroy_sound": Sound(SoundBuffer("game_data/flag_destroy.wav")).set_pitch(0.6).set_volume(60),
            "moving": MultiSound(Sound(SoundBuffer("game_data\moving.wav")), 10).set_volume_all(20),
            "no_opened": MultiSound(Sound(SoundBuffer(r"game_data\no opened.wav")), 10).set_volume_all(80)
        }
        self.outlined_mine = BaseSprite.FromTexture(apply_outline_to_texture(self.data['mine_sprite'].get_texture(), COLOR_WHITE, 1, PIXEL_PERFECT_OUTLINE_SHADER))
        self.outlined_flag = BaseSprite.FromTexture(apply_outline_to_texture(self.data['flag'].get_texture(), COLOR_WHITE, 1, PIXEL_PERFECT_OUTLINE_SHADER))
        self.many_flags = LoadSprite("game_data\many_flags.png")
        self.many_flags.set_position(0, NATIVE_SCREEN_RESOLUTION[1] - 73)
        self.many_flags_alpha = 0
        self.many_flags_target_alpha = 0
        self.flag_druging = 0

        self.down_right_plan = LoadSprite("game_data\down_right_plan.png")
        self.down_right_plan.set_typed_origin(OriginTypes.DOWN_RIGHT)
        self.down_right_plan.set_position(NATIVE_SCREEN_RESOLUTION[0], NATIVE_SCREEN_RESOLUTION[1])

        self.global_particle_system = CPU_ParticleSystem()
        self.global_particle_system.lightning = False


        self.local_particle_system = CPU_ParticleSystem()
        self.local_particle_system.lightning = False



        self.person_particles_emitter = CPU_ParticleEmitters.Rect(Vector2f(0, 0), self.map_cell_size*5, self.map_cell_size*5)

        self.person_not_moving_particles = CPU_Particle(color=COLOR_WHITE, size=30, shape=ParticleShapes.Rectangle)
        self.person_not_moving_particles.spreading_angle = 90
        self.person_not_moving_particles.max_speed = 1000
        self.person_not_moving_particles.min_speed = 100
        self.person_not_moving_particles.resize = -20
        self.person_not_moving_particles.angular_distribution_area = 45
        self.person_not_moving_particles.resistance = 0.1
        self.person_not_moving_particles.max_size = 20
        self.person_not_moving_particles.min_size = 5
        self.person_not_moving_particles.max_velocity_rotation_speed = 0
        self.person_not_moving_particles.min_velocity_rotation_speed = 0
        self.person_not_moving_particles.max_rotation_speed = 100
        self.person_not_moving_particles.min_rotation_speed = -100

        self.cell_opening_emitter = CPU_ParticleEmitters.Rect(Vector2f(0, 0), self.map_cell_size, self.map_cell_size)

        self.cel_open_particles = CPU_Particle(color=COLOR_WHITE, size=30, shape=ParticleShapes.Rectangle)
        self.cel_open_particles.spreading_angle = 0
        self.cel_open_particles.max_speed = 100
        self.cel_open_particles.min_speed = 10
        self.cel_open_particles.resize = -20
        self.cel_open_particles.angular_distribution_area = 360
        self.cel_open_particles.resistance = 0.5
        self.cel_open_particles.max_size = 14
        self.cel_open_particles.min_size = 1
        self.cel_open_particles.max_velocity_rotation_speed = 0
        self.cel_open_particles.min_velocity_rotation_speed = 0
        self.cel_open_particles.max_rotation_speed = 100
        self.cel_open_particles.min_rotation_speed = -100

        self.flag_delete_particle = CPU_Particle(color=COLOR_RED, size=30, shape=ParticleShapes.Rectangle)
        self.flag_delete_particle.spreading_angle = 0
        self.flag_delete_particle.max_speed = 100
        self.flag_delete_particle.min_speed = 10
        self.flag_delete_particle.resize = -20
        self.flag_delete_particle.angular_distribution_area = 360
        self.flag_delete_particle.resistance = 0.01
        self.flag_delete_particle.max_size = 8
        self.flag_delete_particle.min_size = 1
        self.flag_delete_particle.max_velocity_rotation_speed = 0
        self.flag_delete_particle.min_velocity_rotation_speed = 0
        self.flag_delete_particle.max_rotation_speed = 100
        self.flag_delete_particle.min_rotation_speed = -100


        # Создаем текстуру для затемнения открытых клеток
        self.dark_rect = RectangleShape(self.map_cell_size, self.map_cell_size)
        self.dark_rect.set_color(Color(110, 110, 110, 100))  # Темный полупрозрачный
        
        self.__scene_texture = RenderTexture().create(window.get_size().x, window.get_size().y)
        self.__scene_sprite = BaseSprite.FromRenderTexture(self.__scene_texture)

        # Шейдер для анимации открытия
        self.__opening_shader = Shader.FromType(Shader.Type.FRAGMENT, """
        #version 120
        uniform sampler2D texture;
        uniform float progress;
        uniform vec2 cell_position;
        uniform vec2 resolution;
        
        void main() {
            // Нормализованные координаты (0..1)
            vec2 uv = gl_FragCoord.xy / resolution;
            
            // Центр клетки
            vec2 center = cell_position / resolution;
            
            // Расстояние от центра клетки (0..1)
            float dist = distance(uv, center) * 2.0;
            
            // Эффект волны
            float wave = sin(progress * 3.14159 * 2.0 - dist * 5.0) * 0.5 + 0.5;
            
            // Плавное появление с эффектом волны
            float fade = smoothstep(0.0, 1.0, progress * 1.5 - dist * 0.7 + wave * 0.3);
            
            // Изменение цвета во время анимации
            vec4 original = texture2D(texture, gl_TexCoord[0].xy);
            vec3 color = mix(
                vec3(1, 1, 1), 
                original.rgb,                        
                smoothstep(0.0, 1.0, progress)     
            );
            
            // Финальный цвет с учетом прозрачности
            gl_FragColor = vec4(color, original.a * (1 - fade));
        }
        """)

        self.__rainbow_shader = Shader.FromType(Shader.Type.FRAGMENT, """
        #version 120
        uniform sampler2D texture;
        uniform float speed;
        uniform float waveWidth;
        uniform float time;
        uniform vec2 resolution;
        uniform vec4 targetColor;

        vec3 hsv2rgb(vec3 c) {
            vec4 K = vec4(1.0, 2.0/3.0, 1.0/3.0, 3.0);
            vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
            return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
        }

        void main() {
            vec4 originalColor = texture2D(texture, gl_TexCoord[0].xy);
            if (distance(originalColor, targetColor) < 0.01) {
                vec2 uv = gl_FragCoord.xy / resolution;
                float wave = fract(length(uv) * waveWidth - time * speed);
                vec3 rainbowColor = hsv2rgb(vec3(wave, 0.8, 0.9));
                gl_FragColor = vec4(rainbowColor, originalColor.a);
            } else {
                gl_FragColor = originalColor;
            }
        }
        """)

        # Настройка шейдеров
        self.__rainbow_shader.set_uniform("speed", 0.5)
        self.__rainbow_shader.set_uniform("waveWidth", 0.001)
        self.__rainbow_shader.set_uniform("time", 0.0)
        self.__rainbow_shader.set_uniform("resolution", Vector2f(window.get_size().x, window.get_size().y))
        self.__rainbow_shader.set_uniform("targetColor", Color(100, 100, 100, 255))
        
        # Настройка шейдера огня

        self.map_size = 16
        self.mine_count = 40
        self.mine_map = None
        self.map = []
        
        self.game_over = False
        self.cells_to_open = []  # Очередь клеток для анимации открытия

        # Графика
        self.thin_line = LineThinShape()
        self.person_rect = RectangleShape(self.map_cell_size + 2, self.map_cell_size + 2)
        self.person_rect.set_origin(1, 1)
        self.person_rect.set_color(COLOR_TRANSPARENT)
        self.person_rect.set_outline_color(Color(255, 255, 255))
        self.person_rect.set_outline_thickness(1)

        self.help_rect_alpha = 255
        self.help_rect = RectangleShape(self.map_cell_size * 3, self.map_cell_size * 3)
        self.help_rect.set_origin(self.map_cell_size, self.map_cell_size)
        self.help_rect.set_color(COLOR_TRANSPARENT)
        self.help_rect.set_outline_color(Color(39, 39, 39))
        self.help_rect.set_outline_thickness(1)

        self.person_smooth_pos = [self.map_size // 2 * self.map_cell_size, self.map_size // 2 * self.map_cell_size]

        self.person_pos = [self.map_size // 2, self.map_size // 2]
        self.camera = Camera2D(*window.get_size().xy).set_zoom(0.1).set_target_zoom(0.2).set_lerp_zoom(0.2)
        self.camera.set_zoom_limits(0.1, 0.6)
        self.camera.set_center(Vector2f(self.person_pos[0] * self.map_cell_size + self.map_cell_size / 2, 
                            self.person_pos[1] * self.map_cell_size + self.map_cell_size / 2))


        self.start_circle = CircleShape(20).set_origin_radius(1)
        self.start_circle.set_color(COLOR_RED)

        
        self.white_rect = RectangleShape(*NATIVE_SCREEN_RESOLUTION)
        self.white_rect.set_outline_color(COLOR_WHITE)
        self.white_rect.set_outline_thickness(1920 / 2)
        self.white_rect.set_color(COLOR_WHITE)

        self.white_rect_size = copy(NATIVE_SCREEN_RESOLUTION)
        self.white_rect_color_alpha = 255
        self.white_rect_outline_width = 1920 / 2

        self.white_rect_target_alpha = 0
        self.white_rect_target_size = [12*5, 12*5]
        self.white_rect_target_outline_width = 5

        self.white_rect_draw = True
        
        self.down_text = Text(Font.SystemFont("calibri"))

        self.key_states = {
            'up': False, 'down': False, 'left': False, 'right': False,
            'w': False, 's': False, 'a': False, 'd': False
        }
        self.move_cooldown = 0  # Задержка между движениями при зажатии

    def set_cell_without_mine(self):
        # Сначала попробуем найти клетку вообще без мин вокруг
        safe_cells = []
        for y in range(self.map_size):
            for x in range(self.map_size):
                cell = self.map[y][x]
                if not cell.this_mine and cell.mine_count == 0:
                    safe_cells.append((x, y))
        
        # Если нашли клетки без мин, выбираем случайную
        if safe_cells:
            x, y = random.choice(safe_cells)
            self.map[y][x].start = True
            return
        
        # Если клеток без мин нет, ищем клетку с минимальным количеством мин
        min_mines = float('inf')
        candidate_cells = []
        
        for y in range(self.map_size):
            for x in range(self.map_size):
                cell = self.map[y][x]
                if not cell.this_mine:
                    if cell.mine_count < min_mines:
                        min_mines = cell.mine_count
                        candidate_cells = [(x, y)]
                    elif cell.mine_count == min_mines:
                        candidate_cells.append((x, y))
        
        # Выбираем случайную клетку с минимальным количеством мин
        if candidate_cells:
            x, y = random.choice(candidate_cells)
            self.map[y][x].start = True
        else:
            # Если вообще нет безопасных клеток (маловероятно, но на всякий случай)
            x, y = random.randint(0, self.map_size - 1), random.randint(0, self.map_size - 1)
            while self.map[y][x].this_mine:
                x, y = random.randint(0, self.map_size - 1), random.randint(0, self.map_size - 1)
            self.map[y][x].start = True

        

    def generate_mine_map(self):
        mine_map = [[0 for _ in range(self.map_size)] for _ in range(self.map_size)]
        for _ in range(self.mine_count):
            x, y = random.randint(0, self.map_size - 1), random.randint(0, self.map_size - 1)
            while mine_map[y][x] == 1:
                x, y = random.randint(0, self.map_size - 1), random.randint(0, self.map_size - 1)
            mine_map[y][x] = 1
        self.mine_map = mine_map

    def generate_game_map(self):
        for y in range(len(self.mine_map)):
            m = []
            for x in range(len(self.mine_map[0])):
                c = Cell()
                c.position = (x * self.map_cell_size, y * self.map_cell_size)
                if self.mine_map[y][x] == 1: 
                    c.this_mine = True
                else:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0: continue
                            if y + i < 0 or y + i >= len(self.mine_map): continue
                            if x + j < 0 or x + j >= len(self.mine_map[0]): continue
                            if self.mine_map[y + i][x + j] == 1: c.mine_count += 1
                m.append(c)
            self.map.append(m)

    def toggle_flag(self, x, y):
        if x < 0 or x >= self.map_size or y < 0 or y >= self.map_size:
            return
        
        cell = self.map[y][x]
        if cell.open or self.game_over:
            return
            
        if cell.flagged:
            self.data['flag_destroy_sound'].play()
            self.cell_opening_emitter.position = Vector2f(self.person_pos[0] * self.map_cell_size, self.person_pos[1] * self.map_cell_size )
            self.local_particle_system.emit(self.flag_delete_particle, self.cell_opening_emitter, 5)
            self.flag_count -= 1  # Уменьшаем счетчик флагов
        else:
            self.data['flag_set_sound'].play()
            self.flag_count += 1  # Увеличиваем счетчик флагов
            if self.flag_count > self.mine_count:
                self.flag_druging = 10
            
        cell.flagged = not cell.flagged  # Переключаем состояние флага

    def open_cell(self, x, y):
        if x < 0 or x >= self.map_size or y < 0 or y >= self.map_size:
            return
        
        cell = self.map[y][x]
        if cell.open or cell.flagged or self.game_over:
            self.data['no_opened'].auto_play()
            self.map[y][x].draging = 3
            return
        
        # Добавляем в очередь для анимации
        self.cells_to_open.append((x, y, 0.0))  # (x, y, текущий прогресс)

        if cell.this_mine:
            self.game_over = True
            self.reveal_all_mines()

    def update_opening_animation(self):
        # Обновляем анимацию открытия клеток
        for i in range(len(self.cells_to_open)-1, -1, -1):
            x, y, progress = self.cells_to_open[i]
            progress += 0.1 # Скорость анимации
            
            if progress >= 1.0:
                # Анимация завершена, открываем клетку
                cell = self.map[y][x]
                d = min(16, distance(x, y, self.person_pos[0], self.person_pos[1]))

                self.data['cell_open_sound'].set_volume_current(100 * (1 - d / 16))
                self.data['cell_open_sound'].play()
                self.cell_opening_emitter.position = Vector2f(x * self.map_cell_size, y * self.map_cell_size)
                self.local_particle_system.emit(self.cel_open_particles, self.cell_opening_emitter, 5)
                cell.open = True
                cell.opening_progress = 1.0
                self.cells_to_open.pop(i)
                
                # Если клетка пустая, добавляем соседей в очередь
                if not cell.this_mine and cell.mine_count == 0:
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if dx == 0 and dy == 0: continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.map_size and 0 <= ny < self.map_size:
                                neighbor = self.map[ny][nx]
                                if not neighbor.open and not neighbor.flagged and not neighbor.this_mine:
                                    # Проверяем, нет ли уже этой клетки в очереди
                                    if not any((nx, ny, _) in self.cells_to_open for _ in [0]):
                                        self.cells_to_open.append((nx, ny, 0.0))
            else:
                # Обновляем прогресс
                self.cells_to_open[i] = (x, y, progress)
                self.map[y][x].opening_progress = progress

    def reveal_all_mines(self):
        for row in self.map:
            for cell in row:
                if cell.this_mine:
                    cell.open = True
                    cell.opening_progress = 1

    def update(self):
        self.update_opening_animation()
        
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                self.map[y][x].draging *= 0.8


        self.global_particle_system.update(window.get_render_time())

        self.local_particle_system.update(window.get_render_time())
        
        self.camera.follow(Vector2f(self.person_pos[0] * self.map_cell_size + self.map_cell_size / 2, 
                            self.person_pos[1] * self.map_cell_size + self.map_cell_size / 2))
        self.camera.update()

        if KeyBoardInterface.get_click_combination("ctrl+="):
            self.camera.set_target_zoom(self.camera.get_target_zoom() - 0.1)
        if KeyBoardInterface.get_click_combination("ctrl+_"):
            self.camera.set_target_zoom(self.camera.get_target_zoom() + 0.1)

        if window.get_resized():
            self.camera.set_size(*window.get_size().xy)
            self.__scene_texture = RenderTexture().create(window.get_size().x, window.get_size().y)
            self.__scene_sprite = BaseSprite.FromRenderTexture(self.__scene_texture)
            # Обновляем разрешение в шейдере огня при изменении размера окна

        self.__rainbow_shader.set_uniform("time", window.get_global_timer())

        self.person_smooth_pos[0] -= (self.person_smooth_pos[0] - self.person_pos[0] * self.map_cell_size) * 0.2
        self.person_smooth_pos[1] -= (self.person_smooth_pos[1] - self.person_pos[1] * self.map_cell_size) * 0.2

        if not self.map[self.person_pos[1]][self.person_pos[0]].open:
            self.help_rect_alpha += 10

        else:
            self.help_rect_alpha -= 10
        self.help_rect_alpha = max(0, min(self.help_rect_alpha, 255))
        self.help_rect.set_outline_color(Color(39, 39, 39, self.help_rect_alpha))

    
        self.person_rect.set_position(self.person_smooth_pos[0], self.person_smooth_pos[1])
        self.help_rect.set_position(self.person_smooth_pos[0], self.person_smooth_pos[1])

    def try_move(self, direction):
        move_made = False
        
        if direction == "up":
            if self.person_pos[1] - 1 < 0:

                self.person_not_moving_particles.spreading_angle = 90
                self.person_particles_emitter.position = window.convert_view_coords_to_window_coords(
                    self.person_pos[0] * self.map_cell_size, 
                    self.person_pos[1] * self.map_cell_size, 
                    self.camera.get_view()
                )
                self.global_particle_system.emit(self.person_not_moving_particles, self.person_particles_emitter, 10)
            else:
                self.data['moving'].auto_play()
                self.person_pos[1] = max(0, self.person_pos[1] - 1)
                move_made = True
                
        elif direction == "down":
            if self.person_pos[1] + 1 > self.map_size - 1:

                self.person_not_moving_particles.spreading_angle = 270
                self.person_particles_emitter.position = window.convert_view_coords_to_window_coords(
                    self.person_pos[0] * self.map_cell_size, 
                    self.person_pos[1] * self.map_cell_size, 
                    self.camera.get_view()
                )
                self.global_particle_system.emit(self.person_not_moving_particles, self.person_particles_emitter, 10)
            else:
                self.data['moving'].auto_play()
                self.person_pos[1] = min(self.map_size - 1, self.person_pos[1] + 1)
                move_made = True
                
        elif direction == "left":
            if self.person_pos[0] - 1 < 0:

                self.person_not_moving_particles.spreading_angle = 180
                self.person_particles_emitter.position = window.convert_view_coords_to_window_coords(
                    self.person_pos[0] * self.map_cell_size, 
                    self.person_pos[1] * self.map_cell_size, 
                    self.camera.get_view()
                )
                self.global_particle_system.emit(self.person_not_moving_particles, self.person_particles_emitter, 10)
            else:
                self.data['moving'].auto_play()
                self.person_pos[0] = max(0, self.person_pos[0] - 1)
                move_made = True
                
        elif direction == "right":
            if self.person_pos[0] + 1 > self.map_size - 1:

                self.person_not_moving_particles.spreading_angle = 0
                self.person_particles_emitter.position = window.convert_view_coords_to_window_coords(
                    self.person_pos[0] * self.map_cell_size, 
                    self.person_pos[1] * self.map_cell_size, 
                    self.camera.get_view()
                )
                self.global_particle_system.emit(self.person_not_moving_particles, self.person_particles_emitter, 10)
            else:
                self.data['moving'].auto_play()
                self.person_pos[0] = min(self.map_size - 1, self.person_pos[0] + 1)
                move_made = True
        
        return move_made

    def person_update(self):
    # Обновляем состояния клавиш
        keys_to_check = ['up', 'down', 'left', 'right', 'w', 's', 'a', 'd']
        for key in keys_to_check:
            if KeyBoardInterface.get_click(key):
                self.key_states[key] = True
            if not KeyBoardInterface.get_press(key):
                self.key_states[key] = False
        
        # Обрабатываем движение с задержкой при зажатии
        move_made = False
        if self.move_cooldown <= 0:
            # Проверяем все возможные направления движения
            directions = []
            
            # Стрелки
            if self.key_states['up']: directions.append('up')
            if self.key_states['down']: directions.append('down') 
            if self.key_states['left']: directions.append('left')
            if self.key_states['right']: directions.append('right')
            
            # WASD
            if self.key_states['w']: directions.append('up')
            if self.key_states['s']: directions.append('down')
            if self.key_states['a']: directions.append('left') 
            if self.key_states['d']: directions.append('right')
            
            # Если нажата только одна клавиша движения
            if len(directions) == 1:
                direction = directions[0]
                move_made = self.try_move(direction)
                
                if move_made:
                    self.move_cooldown = 10  # Задержка между движениями при зажатии
        
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
        
        # Открытие клетки по нажатию O или E (одиночное нажатие)
        if KeyBoardInterface.get_click("o") or KeyBoardInterface.get_click("e"):
            x, y = self.person_pos[0], self.person_pos[1]
            self.open_cell(x, y)
            
        # Установка/снятие флага по нажатию F или Q (одиночное нажатие)
        if KeyBoardInterface.get_click("f") or KeyBoardInterface.get_click("q"):
            x, y = self.person_pos[0], self.person_pos[1]
            self.toggle_flag(x, y)

        
    def render_map(self, texture):
        self.thin_line.set_color(Color(50, 50, 50))
        for x in range(self.map_size + 1):
            self.thin_line.set_points(x * self.map_cell_size, 0, 
                                    x * self.map_cell_size, self.map_size * self.map_cell_size)
            texture.draw(self.thin_line)
        for y in range(self.map_size + 1):
            self.thin_line.set_points(0, y * self.map_cell_size,
                                    self.map_size * self.map_cell_size, y * self.map_cell_size)
            texture.draw(self.thin_line)

    def render_cell(self, texture, cell, x, y):
        pos_x, pos_y = x * self.map_cell_size, y * self.map_cell_size
        
        if cell.open:
            # Рисуем темный прямоугольник под открытой клеткой
            self.dark_rect.set_position(pos_x, pos_y)
            texture.draw(self.dark_rect)
            
            if cell.this_mine:
                self.data['mine_sprite'].set_position(pos_x, pos_y)
                texture.draw(self.data['mine_sprite'])
            elif cell.mine_count > 0:
                v = Vector2f(cell.draging, 0).rotate_at(random.randint(0, 360))
                self.data[str(cell.mine_count)].set_position(pos_x + v.x, pos_y + v.y)
                texture.draw(self.data[str(cell.mine_count)])
        else:
            # Всегда рисуем закрытую клетку
            if cell.opening_progress > 0:
                self.__opening_shader.set_uniform("progress", cell.opening_progress)
                self.__opening_shader.set_uniform("cell_position", Vector2f(
                    pos_x + self.map_cell_size/2, 
                    pos_y + self.map_cell_size/2
                ))
                self.__opening_shader.set_uniform("resolution", Vector2f(
                    window.get_size().x, 
                    window.get_size().y
                ))
                if cell.mine_count > 0:
                    self.data[str(cell.mine_count)].set_position(pos_x, pos_y)
                    texture.draw(self.data[str(cell.mine_count)])
                self.data['closed'].set_position(pos_x, pos_y)
                texture.draw(self.data['closed'], self.__opening_shader)
            else:
                self.data['closed'].set_position(pos_x, pos_y)
                texture.draw(self.data['closed'])
            
            # Если есть флаг, рисуем его поверх закрытой клетки
            if cell.flagged:
                v = Vector2f(cell.draging, 0).rotate_at(random.randint(0, 360))
                self.data['flag'].set_position(pos_x + v.x, pos_y + v.y)
                texture.draw(self.data['flag'])
            if cell.start:
                self.start_circle.set_position(pos_x + self.map_cell_size / 2, pos_y + self.map_cell_size / 2)
                texture.draw(self.start_circle)

    def render(self):
        self.camera.apply_texture(self.__scene_texture)
        self.__scene_texture.clear(Color(100, 100, 100))
        
        # Клетки
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                self.render_cell(self.__scene_texture, self.map[y][x], x, y)
        
        # Персонаж
        self.render_map(self.__scene_texture)
        self.__scene_texture.draw(self.person_rect)
        self.__scene_texture.draw(self.help_rect)   
        self.__scene_texture.draw(self.local_particle_system)
        self.__scene_texture.display()
        

        window.draw(self.__scene_sprite)

        # Если нужно оставить down_sprite, можно отрисовать его отдельно
        
        window.draw(self.global_particle_system)

        window.draw(self.down_right_plan)
        
      
        # Три столбца подсказок
        column1_x = NATIVE_SCREEN_RESOLUTION[0] - 370 # Левый столбец
        column2_x = NATIVE_SCREEN_RESOLUTION[0] - 240  # Центральный столбец  
        column3_x = NATIVE_SCREEN_RESOLUTION[0] - 120  # Правый столбец
        start_y = NATIVE_SCREEN_RESOLUTION[1] - 40     # Начальная позиция по Y
        
        # Столбец 1: Управление движением
        self.down_text.set_text("Movement:")
        self.down_text.set_size(16)
        self.down_text.set_color(COLOR_GRAY)
        self.down_text.set_position(column1_x, start_y - 25)
        window.draw(self.down_text)
        
        self.down_text.set_text("Arrows / WASD")
        self.down_text.set_size(16)
        self.down_text.set_color(COLOR_GRAY)
        self.down_text.set_position(column1_x, start_y-5)
        window.draw(self.down_text)
        
        # Разделитель после 1 столбца
        self.thin_line.set_points(column1_x + 115, start_y - 25, column1_x + 115, start_y + 40)
        self.thin_line.set_color(Color(100, 100, 100, 150))
        window.draw(self.thin_line)
        
        # Столбец 2: Действия с клетками
        self.down_text.set_text("Actions:")
        self.down_text.set_size(16)
        self.down_text.set_color(COLOR_GRAY)
        self.down_text.set_position(column2_x, start_y - 25)
        window.draw(self.down_text)
        
        self.down_text.set_text("Open: O / E")
        self.down_text.set_size(16)
        self.down_text.set_color(COLOR_GRAY)
        self.down_text.set_position(column2_x, start_y - 5)
        window.draw(self.down_text)
        
        self.down_text.set_text("Flag: F / Q")
        self.down_text.set_size(16)
        self.down_text.set_color(COLOR_GRAY)
        self.down_text.set_position(column2_x, start_y + 15)
        window.draw(self.down_text)
        
        # Разделитель после 2 столбца
        self.thin_line.set_points(column2_x + 100, start_y - 25, column2_x + 100, start_y + 40)
        self.thin_line.set_color(Color(100, 100, 100, 150))
        window.draw(self.thin_line)
        
        # Столбец 3: Настройки
        self.down_text.set_text("Settings:")
        self.down_text.set_size(16)
        self.down_text.set_color(COLOR_GRAY)
        self.down_text.set_position(column3_x, start_y - 25)
        window.draw(self.down_text)
        
        self.down_text.set_text("Zoom: ctrl +/-")
        self.down_text.set_size(16)
        self.down_text.set_color(COLOR_GRAY)
        self.down_text.set_position(column3_x, start_y - 5)
        window.draw(self.down_text)
        
        self.down_text.set_text("Monitor: shift M")
        self.down_text.set_size(16)
        self.down_text.set_color(COLOR_GRAY)
        self.down_text.set_position(column3_x, start_y + 15)
        window.draw(self.down_text)
        
        self.outlined_mine.set_position(2, NATIVE_SCREEN_RESOLUTION[1] - 30)
        self.outlined_mine.set_scale(3)
        window.draw(self.outlined_mine)
        
        self.down_text.set_text(f"{self.mine_count} mines")
        self.down_text.set_size(18)
        self.down_text.set_color(COLOR_WHITE)
        self.down_text.set_position(40, NATIVE_SCREEN_RESOLUTION[1]-28)
        window.draw(self.down_text)
        
    
        self.many_flags_alpha -= (self.many_flags_alpha - self.many_flags_target_alpha) * 0.1
        self.many_flags.set_color(Color(255, 255, 255, self.many_flags_alpha))
        if self.flag_count > self.mine_count:
            self.many_flags_target_alpha = 255
        else:
            self.many_flags_target_alpha = 0
        window.draw(self.many_flags)

        self.flag_druging *= 0.85
        v = Vector2f(self.flag_druging, 0).rotate_at(random.randint(0, 360))

        self.outlined_flag.set_position(2 + v.x, NATIVE_SCREEN_RESOLUTION[1] - 65 + v.y)
        self.outlined_flag.set_scale(3)
        
        window.draw(self.outlined_flag)
        
        self.down_text.set_text(f"{self.flag_count} / {self.mine_count} flags")
        self.down_text.set_size(18)
        self.down_text.set_color(COLOR_WHITE)
        self.down_text.set_position(40 + v.x, NATIVE_SCREEN_RESOLUTION[1]-60 + v.y)
        window.draw(self.down_text)

        
        if self.white_rect_draw:
            window.draw(self.white_rect)
        
    def interface_update(self):
        
        if round(self.white_rect_outline_width, 1) == self.white_rect_target_outline_width:
            self.white_rect_draw = False

        self.white_rect_color_alpha += (self.white_rect_target_alpha - self.white_rect_color_alpha) * 0.03
        self.white_rect.set_color(Color(255, 255, 255, self.white_rect_color_alpha))

        self.white_rect_size[0] += (self.white_rect_target_size[0] - self.white_rect_size[0]) * 0.4
        self.white_rect_size[1] += (self.white_rect_target_size[1] - self.white_rect_size[1]) * 0.4
        self.white_rect.set_size(*self.white_rect_size)
        self.white_rect.set_origin(self.white_rect_size[0]/2, self.white_rect_size[1]/2)
        self.white_rect.set_position(NATIVE_SCREEN_RESOLUTION[0]/2, NATIVE_SCREEN_RESOLUTION[1]/2)
        
        self.white_rect_outline_width += (self.white_rect_target_outline_width - self.white_rect_outline_width) * 0.1
        self.white_rect.set_outline_thickness(self.white_rect_outline_width)



GAME = Game()
GAME.generate_mine_map()
GAME.generate_game_map()
GAME.set_cell_without_mine()

game_start_flag = False
start_text = Text(Font.SystemFont("calibri"))
start_text.set_text("Press S to start")
start_text.set_size(200 * NATIVE_SCREEN_RESOLUTION[1] / 1080)
start_text.set_color(COLOR_BLACK)
start_text.set_typed_origin(OriginTypes.CENTER)
start_text.set_position(NATIVE_SCREEN_RESOLUTION[0]/2, NATIVE_SCREEN_RESOLUTION[1]/2 - 50 * 1080 / NATIVE_SCREEN_RESOLUTION[1])

while window.update(window_events):
    window.clear(COLOR_BLACK)
    
    if not game_start_flag:
        if KeyBoardInterface.get_click("s"):
            game_start_flag = True
    if not GAME.white_rect_draw:
        GAME.person_update()
    GAME.update()

    


    GAME.render()

    if game_start_flag:
        GAME.interface_update()
    else:
        window.draw(start_text)
    window.view_info()
    window.display()