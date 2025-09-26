from Moon.python.Rendering.Text import Text, BaseText
from Moon.python.Rendering.Shapes import (
    BaseLineShape, CircleShape, RectangleShape, LineShape, PolygoneShape,
    LineThinShape, LinesThinShape
)

type Drawable = CircleShape | RectangleShape | LineShape | BaseLineShape | \
                PolygoneShape | LineThinShape | LinesThinShape | Text | BaseText


_Drawable = (CircleShape | RectangleShape | LineShape | BaseLineShape | \
             PolygoneShape | LineThinShape | LinesThinShape | Text | BaseText)
