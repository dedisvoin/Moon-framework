
from copy import copy
import time

from Moon.python.Rendering.Drawable import *
from Moon.python.Rendering.RenderStates import RenderStates
from Moon.python.Rendering.Shaders import *

from Moon.python.Time import TIMER_BUFFER, Timer, wait_call
from Moon.python.Views import View, ViewPtr
from Moon.python.Types import *
from Moon.python.Colors import *

from Moon.python.utils import find_library
import ctypes

# Загружаем DLL библиотеку
try:
    LIB_MOON = ctypes.CDLL(find_library())
except Exception as e:
    raise ImportError(f"Failed to load PySGL library: {e}")


RenderTexturePtr =      ctypes.c_void_p
TexturePtr =            ctypes.c_void_p
SpritePtr =             ctypes.c_void_p
ContextSettingsPtr =    ctypes.c_void_p


LIB_MOON._RenderTexture_Init.argtypes = []
LIB_MOON._RenderTexture_Init.restype = ctypes.c_void_p

LIB_MOON._RenderTexture_Create.argtypes = [RenderTexturePtr, ctypes.c_int, ctypes.c_int]
LIB_MOON._RenderTexture_Create.restype = ctypes.c_bool
LIB_MOON._RenderTexture_CreateWithContextSettings.argtypes = [RenderTexturePtr, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
LIB_MOON._RenderTexture_CreateWithContextSettings.restype = ctypes.c_bool

LIB_MOON._RenderTexture_Draw.argtypes = [RenderTexturePtr, ctypes.c_void_p]
LIB_MOON._RenderTexture_Draw.restype = None
LIB_MOON._RenderTexture_DrawWithShader.argtypes = [RenderTexturePtr, ctypes.c_void_p, ctypes.c_void_p]
LIB_MOON._RenderTexture_DrawWithShader.restype = None
LIB_MOON._RenderTexture_DrawWithRenderStates.argtypes = [RenderTexturePtr, ctypes.c_void_p, ctypes.c_void_p]
LIB_MOON._RenderTexture_DrawWithRenderStates.restype = None

LIB_MOON._RenderTexture_Clear.argtypes = [RenderTexturePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._RenderTexture_Clear.restype = None

LIB_MOON._RenderTexture_Display.argtypes = [RenderTexturePtr]
LIB_MOON._RenderTexture_Display.restype = None

LIB_MOON._RenderTexture_SetView.argtypes = [RenderTexturePtr, ctypes.c_void_p]
LIB_MOON._RenderTexture_SetView.restype = None

LIB_MOON._RenderTexture_GetDefaultView.argtypes = [RenderTexturePtr]
LIB_MOON._RenderTexture_GetDefaultView.restype = ctypes.c_void_p

LIB_MOON._RenderTexture_GetView.argtypes = [RenderTexturePtr]
LIB_MOON._RenderTexture_GetView.restype = ctypes.c_void_p

LIB_MOON._RenderTexture_GetTexture.argtypes = [RenderTexturePtr]
LIB_MOON._RenderTexture_GetTexture.restype = TexturePtr

LIB_MOON._RenderTexture_Delete.argtypes = [RenderTexturePtr]
LIB_MOON._RenderTexture_Delete.restype = None

LIB_MOON._RenderTexture_SetSmooth.argtypes = [RenderTexturePtr, ctypes.c_bool]
LIB_MOON._RenderTexture_SetSmooth.restype = None


class RenderTexture:
    def __init__(self) -> None:
        self.__ptr = LIB_MOON._RenderTexture_Init()

    def __del__(self):
        LIB_MOON._RenderTexture_Delete(self.__ptr)

    def set_smooth(self, smooth: bool = True) -> None:
        """
        #### Set the smoothness of the render texture.

        ---

        :Args:
            smooth (bool): Whether the render texture should be smooth.
        """
        LIB_MOON._RenderTexture_SetSmooth(self.__ptr, smooth)

    def create(self, width: int, height: int, arg: None | ContextSettingsPtr = None):
        """
        #### Create a new render texture.

        ---

        :Args:
            width (int): The width of the render texture.
            height (int): The height of the render texture.
            arg (ContextSettingsPtr, optional): The context settings for the render texture. Defaults to None.
        """
        if arg is None:
            LIB_MOON._RenderTexture_Create(self.__ptr, width, height)
        else:
            LIB_MOON._RenderTexture_CreateWithSettings(self.__ptr, width, height, arg)

    @overload
    def draw(self, shape: Drawable, arg: None = None):
        """
        Draw a drawable object to the render texture.

        ---

        :Args:
            shape (Drawable): The drawable object to draw.
            arg (None, optional): The render states to use. Defaults to None.
        """
        ...

    @overload
    def draw(self, shape: Drawable, arg: RenderStates):
        """
        Draw a drawable object to the render texture with render states.

        ---

        :Args:
            shape (Drawable): The drawable object to draw.
            arg (RenderStates): The render states to use.
        """
        ...

    @overload
    def draw(self, shape: Drawable, arg: Shader):
        """
        Draw a drawable object to the render texture with a shader.

        ---

        :Args:
            shape (Drawable): The drawable object to draw.
            arg (Shader): The shader to use.
        """
        ...


    def draw(self, shape: Drawable, arg: None | RenderStates | Shader = None):
        if arg is None:
            LIB_MOON._RenderTexture_Draw(self.__ptr, shape.get_ptr())
        elif isinstance(arg, RenderStates):
            LIB_MOON._RenderTexture_DrawWithRenderStates(self.__ptr, shape.get_ptr(), arg.get_ptr())
        elif isinstance(arg, Shader):
            LIB_MOON._RenderTexture_DrawWithShader(self.__ptr, shape.get_ptr(), arg.get_ptr())
        else:
            raise TypeError("Invalid argument type")


    def get_ptr(self) -> RenderTexturePtr:
        """
        #### Get the pointer to the render texture.

        ---

        :Returns:
            RenderTexturePtr: The pointer to the render texture.
        """
        return self.__ptr


    def clear(self, color: Color = COLOR_WHITE) -> None:
        """
        #### Clear the render texture with the specified color.

        ---

        :Args:
            color (Color, optional): The color to clear the render texture with. Defaults to COLOR_WHITE.
        """
        LIB_MOON._RenderTexture_Clear(self.__ptr, color.r, color.g, color.b, color.a)


    def display(self) -> None:
        """
        #### Display the render texture on the screen.

        ---

        :Args:
            None
        """
        LIB_MOON._RenderTexture_Display(self.__ptr)


    def get_view_ptr(self) -> ViewPtr:
        """
        #### Get the view of the render texture.

        ---

        :Returns:
            ViewPtr: The view of the render texture.
        """
        return LIB_MOON._RenderTexture_GetView(self.__ptr)


    def get_default_view_ptr(self) -> ViewPtr:
        """
        #### Get the default view of the render texture.

        ---

        :Returns:
            ViewPtr: The default view of the render texture.
        """
        return LIB_MOON._RenderTexture_GetDefaultView(self.__ptr)


    def get_texture_ptr(self) -> TexturePtr:
        """
        #### Get the texture of the render texture.

        ---

        :Returns:
            TexturePtr: The texture of the render texture.
        """
        return LIB_MOON._RenderTexture_GetTexture(self.__ptr)
