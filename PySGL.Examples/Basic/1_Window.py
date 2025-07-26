import sys
sys.path.append("./")
from PySGL.python.Window import *

window = Window(style=Window.Style.No, title="test").set_view_info()

events = WindowEvents()
window.set_system_cursor(SystemCursors.Hand)
window.enable_rounded_corners()

while window.update(events):
    window.clear()
    window.view_info()
    window.display()
