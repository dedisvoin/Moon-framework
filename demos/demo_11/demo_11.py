import sys
import math
sys.path.append('./')

# Предполагаемые импорты из вашей библиотеки Moon
from Moon.python.Window import *
from Moon.python.Rendering.Sprites import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Vectors import *
from Moon.python.Inputs import KeyBoardInterface

# --- Константы Освещения ---
# Угол источника света в градусах (135° = Сверху-Слева)
LIGHT_ANGLE = 135
# Минимальная базовая яркость объекта, чтобы избежать абсолютно черного цвета
MIN_LIGHT_HEIGHT = 0.7
MIN_LIGHT_ROTATION = 0.4
# Степень для нелинейного затенения. < 1.0 (например, 0.5) делает основание темнее.
OCCLUSION_POWER = 0.5

BASE_DIR = os.getcwd()
print(BASE_DIR)
def get_resource_path(filename):
    """Создает надежный путь к файлу в папке 'data'"""
    # os.path.join автоматически выбирает правильный разделитель (\ или /)
    return os.path.join(BASE_DIR, "data", filename)



# --- Загрузка Ресурсов ---
result, texture = Texture2D().load_from_file(get_resource_path("slices.png"))
result, texture2 = Texture2D().load_from_file(get_resource_path("slices2.png"))
result, texture3 = Texture2D().load_from_file(get_resource_path("slices3-1.png"))
result, texture4 = Texture2D().load_from_file(get_resource_path("slices3-0.png"))
result, texture5 = Texture2D().load_from_file(get_resource_path("slices4.png"))
result, texture6 = Texture2D().load_from_file(get_resource_path("slices5.png"))
result, texture7 = Texture2D().load_from_file(get_resource_path("T-Rex.png"))
result, texture8 = Texture2D().load_from_file(get_resource_path("slices6.png"))


# (Текстура, Ширина, Высота Слайса, Количество Слайсов)
textures = [(texture, 97, 97, 79), (texture2, 72, 72, 128), (texture3, 15, 32, 14),
            (texture4, 15, 34, 13), (texture5, 26, 9, 27), (texture6, 20, 21, 20), (texture7, 24, 24, 26),
            (texture8, 19, 1, 20)]


SCR = get_screen_resolution()

# --- Инициализация Окна ---
window = Window(title="Привeт",style=Window.Style.Resize | Window.Style.Close, context_settings=ContextSettings().set_depth_bits(24).set_stencil_bits(8).set_antialiasing_level(4).set_opengl_version(3, 2))
window.set_wait_fps(FPS_VSYNC_CONST)
window_events = WindowEvents()
window.set_view_info()

sprite = Sprite2D()
at_texture = textures[0]

# --- Функция Рендеринга с Динамическим Освещением и Самозатенением ---
def render_obj(pos: Vector2Type):
    global at_texture
    sprite.link_texture(at_texture[0])

    # Вращение объекта
    sprite.rotate(3 * window.get_delta())
    current_rotation = sprite.get_rotation() # Получаем текущий угол для расчета света

    slices = 5
    total_slices_count = at_texture[3] * slices # Общее число слоев для итерации

    # Итерация от самого дальнего/нижнего слоя к самому ближнему/верхнему
    for i in range(total_slices_count, 0, -1):

        # --- ЛОГИКА ПРОДВИНУТОГО ОСВЕЩЕНИЯ И САМОЗАТЕНЕНИЯ ---

        # 1. Расчет коэффициента Самозатенения по ВЫСОТЕ (L_height)

        # Нормализованная высота (0.0=низ, ~1.0=верх)
        normalized_occlusion = (total_slices_count - i) / total_slices_count

        # Применяем степень для нелинейного затенения (чем ниже, тем темнее)
        L_occlusion = pow(normalized_occlusion, OCCLUSION_POWER)

        # Интерполируем L_occlusion в заданный диапазон [MIN_LIGHT_HEIGHT, 1.0]
        L_height = MIN_LIGHT_HEIGHT + L_occlusion * (1.0 - MIN_LIGHT_HEIGHT)

        # 2. Расчет коэффициента по ПОВОРОТУ (динамическая тень от внешнего света)

        angle_diff = (current_rotation - LIGHT_ANGLE + 360) % 360
        L_rot_raw = math.cos(math.radians(angle_diff))

        # Сдвиг в диапазон [MIN_LIGHT_ROTATION, 1.0]
        L_rot_scaled = (L_rot_raw + 1) / 2
        L_rotation = MIN_LIGHT_ROTATION + L_rot_scaled * (1.0 - MIN_LIGHT_ROTATION)

        # 3. КОМБИНИРОВАННЫЙ ФАКТОР: перемножаем L_height (объем) и L_rotation (направленный свет)
        L_final = L_height

        # 4. Применение цвета (модуляция)
        color_val = int(255 * L_final)
        sprite.set_color(Color(color_val, color_val, color_val, 255))

        # ----------------------------------------

        # --- Логика Spritestacking ---
        sprite.set_texture_rect(Vector2i(0, (i // slices) * at_texture[2]), Vector2i(at_texture[1], at_texture[2]))
        sprite.set_origin(Vector2f(at_texture[1]/2, at_texture[2]/2))

        s = max(40 * math.sin(window.get_global_timer(0.5)), 0)

        # Применяем масштаб и колебание
        sprite.set_scale(7 + s/2, 7 + s/2)

        # Смещение для имитации глубины
        sprite.set_position(pos - Vector2f(0, -(7 + s/2) * i / slices) - Vector2f(0, ((7 + s/2) * at_texture[3]) / 2))

        window.draw(sprite)


# --- Основной Цикл ---
while window.update(window_events):
    window.clear(COLOR_WEB_GRAY)

    # Логика смены текстуры
    if KeyBoardInterface.get_click('1'):
        at_texture = textures[0]
    if KeyBoardInterface.get_click('2'):
        at_texture = textures[1]
    if KeyBoardInterface.get_click('3'):
        at_texture = textures[2]
    if KeyBoardInterface.get_click('4'):
        at_texture = textures[3]
    if KeyBoardInterface.get_click('5'):
        at_texture = textures[4]
    if KeyBoardInterface.get_click('6'):
        at_texture = textures[5]
    if KeyBoardInterface.get_click('7'):
        at_texture = textures[6]
    if KeyBoardInterface.get_click('8'):
        at_texture = textures[7]

    render_obj(window.get_center())
    window.view_info()

    window.display()
