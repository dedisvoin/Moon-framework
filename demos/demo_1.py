import sys
sys.path.append('./')

from Moon.python.Window import *

window = Window()
window_events = WindowEvents()


while window.update(window_events):
    window.clear()
    window.display()