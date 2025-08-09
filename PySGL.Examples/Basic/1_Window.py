import sys
sys.path.append("./")
from PySGL.python.Window import *

window = Window()
events = WindowEvents()

while window.update(events):
    window.clear()
    window.display()