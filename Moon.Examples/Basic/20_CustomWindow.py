import sys
sys.path.append("./")
from Moon.python.Window import *

window = CustomWindow()

events = WindowEvents()
while window.update(events):
    window.clear()
    window.view_info()
    window.display()
