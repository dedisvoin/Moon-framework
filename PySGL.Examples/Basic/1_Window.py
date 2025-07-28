import sys
sys.path.append("./")
from PySGL.python.Window import *

window = Window(title="test").set_view_info()
window.set_wait_fps(FPS_UNLIMIT_CONST)

events = WindowEvents()
window.set_system_cursor(SystemCursors.Hand)
window.enable_rounded_corners()

while window.is_open():
    if not window.update(events): window.close()
    window.clear()
    window.view_info()
    window.display()
    
