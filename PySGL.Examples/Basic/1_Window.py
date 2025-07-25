import sys
sys.path.append("./")
from PySGL.python.Window import *

window = Window().set_view_info()
events = WindowEvents()

while window.update(events):
    window.clear()
    window.view_info()
    window.display()
