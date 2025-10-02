from Moon.python.Rendering.Text import Text, BaseText
from Moon.python.Rendering.Shapes import (
    BaseLineShape, CircleShape, RectangleShape, LineShape, PolygoneShape,
    LineThinShape, LinesThinShape
)

from Moon.python.Rendering.Vertexes import VertexArray
type Drawable = CircleShape | RectangleShape | LineShape | BaseLineShape | \
                PolygoneShape | LineThinShape | LinesThinShape | Text | BaseText | VertexArray

_Drawable = (CircleShape | RectangleShape | LineShape | BaseLineShape | \
             PolygoneShape | LineThinShape | LinesThinShape | Text | BaseText | VertexArray)
