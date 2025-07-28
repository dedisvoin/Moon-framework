from PySGL.python.Rendering.Shapes import *
from PySGL.python.Vectors import *

from dataclasses import dataclass

@dataclass
class ParticlePoint:
    position: Final[Vector2f]
    speed: Final[Vector2f]


p = ParticlePoint.position = 10