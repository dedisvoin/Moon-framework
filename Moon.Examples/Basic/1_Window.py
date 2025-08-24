import sys
sys.path.append("./")
from Moon.python.Window import *

window = Window()
window.set_wait_fps(FPS_UNLIMIT_CONST)
window.set_view_info()
window.enable_fpsmonitor_keybinding()
window.set_fpsmonitor_keybinding("1+2+3")
events = WindowEvents()


while window.update(events):
    window.clear()
    window.view_info()
    window.display()