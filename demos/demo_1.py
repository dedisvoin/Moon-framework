import sys
sys.path.append('./')


from Moon.python.Inputs import *
from Moon.python.Window import *

window = Window()
window_events = WindowEvents()


while window.update(window_events):
    window.clear()

    if KeyBoardInterface.get_press("q"):
        print("Pressed 'q'")
    if KeyBoardInterface.get_press("w+e"):
        print("Pressed 'w' and 'e'")
    if KeyBoardInterface.get_click("r"):
        print("Clicked 'r'")
    if KeyBoardInterface.get_click('w+r'):
        print("Clicked 'w' and 'r'")

    if MouseInterface.get_click('left'):
        print("Clicked left mouse button")
    if MouseInterface.get_press('right'):
        print("Pressed right mouse button")
    window.display()
