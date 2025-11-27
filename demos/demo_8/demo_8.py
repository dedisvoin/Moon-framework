import sys
sys.path.append('./')



from Moon.python.Window import *
from Moon.python.Rendering.Sprites import *
from Moon.python.Rendering.CShapes import *
from Moon.python.Vectors import *



result, texture = Texture2D().load_from_file(r"demos\texture2.png")

sprite = Sprite2D().link_texture(texture)
sprite.set_scale(10, 10)
sprite.flip(True, True)
print(sprite.get_flips())



position = Vector2f(400, 300)
sprite.set_position(position)
sprite.set_texture_rect(Vector2i(5, 8), Vector2i(16, 18))
sprite.set_typed_origin(OriginTypes.CENTER)
sprite.set_flip_x(True)



bounds = sprite.get_global_bounds()
circle = CircleShape().set_color(COLOR_RED).set_origin_radius(10).set_position(position)
rectangle = RectangleShape(*bounds[1]).set_outline_color(COLOR_RED).set_outline_thickness(2).set_color(COLOR_TRANSPARENT)
rectangle.set_position(position)

window = Window(title="Привeт", context_settings=ContextSettings().set_depth_bits(24).set_stencil_bits(8).set_antialiasing_level(4).set_opengl_version(3, 2))
window.set_wait_fps(180)
window_events = WindowEvents()
window.set_view_info()

while window.update(window_events):
    window.clear()
    window.draw(sprite)
    window.draw(circle)
    window.draw(rectangle)
    window.view_info()

    mouse_vector = Vector2f.between(MouseInterface.get_position_in_window(window).xy, position.xy)
    
    sprite.set_rotation(-mouse_vector.get_angle())
    bounds = sprite.get_global_bounds()
    rectangle.set_position(position - bounds[1] / 2)
    rectangle.set_size(*bounds[1])
    
    window.display()
