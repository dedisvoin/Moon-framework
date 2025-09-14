import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Engine.ParticleSystem import *
from Moon.python.Inputs import MouseInterface

window = Window()
window.set_wait_fps(600)
events = WindowEvents()
window.set_view_info()





ps = CPU_ParticleSystem()
p = CPU_Particle(color=Color(255*0.5, 200*0.5, 150*0.5, 255), size=100, shape=ParticleShapes.LightCircle)
p.spreading_angle = 90
p.max_speed = 100
p.min_speed = 10
p.resize = -10
p.angular_distribution_area = 360
p.resistance = 0.99
p.max_size = 100
p.min_size = 20
p.max_velocity_rotation_speed = 30
p.min_velocity_rotation_speed = 0

p2 = CPU_Particle(color=Color(155*0.5, 250*0.5, 150*0.5, 255), size=100, shape=ParticleShapes.LightCircle)
p2.spreading_angle = 100
p2.max_speed = 16
p2.min_speed = 10
p2.resize = -3
p2.angular_distribution_area = 100
p2.resistance = 2
p2.max_size = 40
p2.min_size = 20
p2.max_velocity_rotation_speed = 10
p2.min_velocity_rotation_speed = 4


ps.lightning = True


while window.update(events):
    
    window.clear(COLOR_BLACK)

    render_time = window.get_render_time(10)
    ps.emit_per_time(p2, CPU_ParticleEmitters.Point(window.get_center() + Vector2f(0, 0)), 0.01, 1, window.get_render_time(), emitter_id="1")
    #ps.emit_per_time(p2, CPU_ParticleEmitters.Point(window.get_center() + Vector2f(-300, 0)), 0.01, 5, window.get_render_time(), emitter_id='2')
    ps.update(render_time)

    window.draw(ps)
    window.view_info()
    window.display()