import sys
sys.path.append('./')


from Moon.python.Inputs import *
from Moon.python.Window import * # pyright: ignore
from Moon.python.Rendering.Shapes import * # pyright: ignore
from Moon.python.Audio import *  # pyright: ignore


window = Window(1920, 1080, "Moon Framework Demo", context_settings=ContextSettings().set_antialiasing_level(8))
window_events = WindowEvents()


sound = MultiSound(Sound(SoundBuffer("demos/demo_5/sound1.mp3")), 10)
sound.set_volume_all(80)

while window.update(window_events):
    window.clear()

    if MouseInterface.get_click("left"):
        sound.auto_play()

    window.display()
