import sys
import random
sys.path.append("./")
from PySGL.python.Window import *

from PySGL.python.Audio import *
from PySGL.python.Rendering.Text import *
from PySGL.python.Inputs import MouseInterface


window = Window().set_view_info()
events = WindowEvents()
window.set_wait_fps(60)
window.set_ghosting().set_ghosting_min_alpha(0)
while window.update(events):
    window.clear()
    if MouseInterface.get_click('left'):
        window.disable()
    if MouseInterface.get_click('right'):
        window.enable()


    window.view_info()
    window.display()