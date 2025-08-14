from .Colors import Color
from enum import Enum, auto
from typing import NoReturn, Optional, Callable, TypeAlias, Union, overload, Self, Literal
from uuid import uuid4

type FunctionOrMethod =     Callable

Number: TypeAlias =               int | float
type OptionalNumber =       Optional[Number]

type TwoNumberList =        list[Number] | tuple[Number, Number]
type TwoIntegerList =       list[int] | tuple[int, int]
type TwoFloatList =         list[float] | tuple[float, float]

type ThreeNumbersList =     list[Number] | tuple[Number, Number, Number]
type FourNumbersList =      list[Number] | tuple[Number, Number, Number, Number]
type ColorType =            Color | ThreeNumbersList

type Identifier =           int | str
type OptionalIdentifier =   Optional[Identifier]


def AutoIdentifier() -> Identifier:
    """
    #### Генерирует уникальный идентификатор.

    ---

    :Returns:
    - идентификатор
    """
    return str(uuid4())


class OriginTypes(Enum):
    TOP_CENTER =        auto()
    DOWN_CENTER =       auto()
    LEFT_CENTER =       auto()
    RIGHT_CENTER =      auto()
    CENTER =            auto()
    TOP_LEFT =          auto()
    TOP_RIGHT =         auto()
    DOWN_LEFT =         auto()
    DOWN_RIGHT =        auto()
