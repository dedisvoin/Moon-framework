from typing import TypeAlias, TypeVar
from Moon.python.Rendering.Text import Text, BaseText
from Moon.python.Rendering.Shapes import *
from Moon.python.Rendering.Shapes.Rectangle import *
from Moon.python.Rendering.Shapes.Circle import *

from Moon.python.Rendering.Vertexes import VertexList

Sprite2D = TypeVar('Sprite2D')
AnimatedSprite2D = TypeVar('AnimatedSprite2D')

type Drawable = CircleShape | RectangleShape | Text | BaseText | VertexList | PolylineShape | LineShape
             #LineShape | BaseLineShape | PolygoneShape | LineThinShape | LinesThinShape

DrawableTuple = (CircleShape | RectangleShape | Text | BaseText | VertexList | PolylineShape | LineShape | \
            #LineShape | BaseLineShape | PolygoneShape | LineThinShape | LinesThinShape | \
             Sprite2D | AnimatedSprite2D)
