import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Engine.ParticleSystem import *

window = Window()
events = WindowEvents()
window.set_view_info()



ps = ParticleSystem()




while window.update(events):
    ps.emit(ParticleEmiters.Point(Vector2f(400, 400)), 2)
    ps.update()
    if int(window.get_global_timer(10)) % 10 == 0:
        print(len(ps.particles))


    window.clear()
    ps.render(window)
    window.view_info()
    window.display()