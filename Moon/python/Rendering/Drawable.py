from typing import TypeAlias, TypeVar
from typing_extensions import TypeForm
from Moon.python.Rendering.Text import Text, BaseText
from Moon.python.Rendering.Shapes import (
    BaseLineShape, CircleShape, RectangleShape, LineShape, PolygoneShape,
    LineThinShape, LinesThinShape
)

from Moon.python.Rendering.Vertexes import VertexArray

Sprite2D = TypeVar('Sprite2D')
AnimatedSprite2D = TypeVar('AnimatedSprite2D')



type Drawable = CircleShape | RectangleShape | LineShape | BaseLineShape | \
             PolygoneShape | LineThinShape | LinesThinShape | Text | BaseText | VertexArray

DrawableTuple = (CircleShape | RectangleShape | LineShape | BaseLineShape | \
             PolygoneShape | LineThinShape | LinesThinShape | Text | BaseText | VertexArray | \
             Sprite2D | AnimatedSprite2D)
