import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Inputs import KeyBoardInterface # pyright: ignore

window = Window()
window.set_view_info()

events = WindowEvents()


while window.update(events):
    if KeyBoardInterface.get_click("f"):
        print("Fullscreen mode activated")
        window.set_fullscreen()

    window.clear()
    window.view_info()
    window.display()
