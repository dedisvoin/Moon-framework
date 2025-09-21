import sys
sys.path.append('./')


from Moon.python.Inputs import *
from Moon.python.Window import *

window = Window()
window_events = WindowEvents()


manager = ListenersManager()
manager.add_listener(Listener(Listener.ObjectType.KEYBOARD,
    Listener.EventType.CLICK, 'clicker', 'enter'))
manager.add_listener(Listener(Listener.ObjectType.KEYBOARD,
    Listener.EventType.CLICK, 'combination', 'a+b'))

while window.update(window_events):
    window.clear()

    manager.update()
    if manager.get('clicker'): print("click enter")
    if manager.get('combination'): print("a+b")

    window.display()
