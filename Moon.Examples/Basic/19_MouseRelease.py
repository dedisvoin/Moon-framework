import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Inputs import *

window = Window()
window.set_wait_fps(60)
window.set_view_info()
window.enable_fpsmonitor_keybinding()
events = WindowEvents()


while window.update(events):
    window.clear()
    window.view_info()
    window.display()