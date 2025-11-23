import sys
import math
sys.path.append('./')

# Предполагаемые импорты из вашей библиотеки Moon
from Moon.python.Window import *
from Moon.python.Rendering.Sprites import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Vectors import *
from Moon.python.Inputs import KeyBoardInterface



window = Window(title="DataSetGenerate", style=Window.Style.Resize | Window.Style.Close)
window.set_wait_fps(FPS_VSYNC_CONST)
window_events = WindowEvents()
window.set_view_info()


circle = CircleShape()
def create_image(resolution: int = 256, index: int = 0):
    circle.set_color(Color.random())
    circle.set_radius(random.randint(20, 100))
    circle.set_position(random.randint(0, resolution), random.randint(0, resolution))

    render_texture = RenderTexture2D().Init(resolution, resolution)
    render_texture.clear()
    render_texture.draw(circle)
    render_texture.display()

    Image.CopyFromTexture(render_texture.get_texture()).save(f"demos\demo_12\data\image_{i}.png")

    return render_texture






for i in range(3):
    create_image(256, i)

