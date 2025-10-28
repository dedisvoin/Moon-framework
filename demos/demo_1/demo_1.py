import sys
sys.path.append('./')


from Moon.python.Inputs import *
from Moon.python.Window import *

window = Window(title="Привet")
window_events = WindowEvents()

window.set_system_cursor(SystemCursors.SizeAll)


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

    if KeyBoardInterface.get_click('s'):
        set_mouse_position_in_window(window, Vector2i(100, 100))


    if KeyBoardInterface.get_click('m'):
        MouseInterface.daemon_move(Vector2i(100, 100), 1)
    if KeyBoardInterface.get_click('n'):
        MouseInterface.daemon_move(Vector2i(1920 - 100, 100), 1)

    window.display()
