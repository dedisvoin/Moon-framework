import sys
sys.path.append("./")
from PySGL.python.Window import *
from PySGL.python.Engine.BoxColliders import *



window = Window().set_view_info()
events = WindowEvents()


collider_space = ColliderLayer()
collider_space.add_collider(BoxCollider2D(600, 50, ColliderMaterial(), ColliderType.STATIC)).set_position(0, 500)
collider_space.add_collider(BoxCollider2D(50, 50, ColliderMaterial(bounce=Vector2f(0, 0.8)), ColliderType.DYNAMIC).set_position(300, 300))

while window.update(events):
    window.clear()

    collider_space.update(1)
    collider_space.view_info(window)
    window.view_info()
    window.display()
