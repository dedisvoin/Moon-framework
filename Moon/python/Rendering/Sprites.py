import time

from Moon.python.Rendering.Drawable import *
from Moon.python.Rendering.RenderStates import RenderStates
from Moon.python.Rendering.Shaders import *

from Moon.python.Vectors import Vector2Type
from Moon.python.Views import ViewPtr
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


class RenderTexture(object):
    def __init__(self) -> None:
        self.__ptr = LIB_MOON._RenderTexture_Init()

        self.__size: None | Vector2i = None

    def __del__(self):
        LIB_MOON._RenderTexture_Delete(self.__ptr)

    def __eq__(self, other: "object | RenderTexture") -> bool:
        if isinstance(other, RenderTexture):
            return self.__ptr == other.get_ptr()
        return False

    def __ne__(self, other: "object | RenderTexture") -> bool:
        if isinstance(other, RenderTexture):
            return not self.__eq__(other)
        return True

    def set_smooth(self, smooth: bool = True) -> None:
        """
        #### Set the smoothness of the render texture.

        ---

        :Args:
            smooth (bool): Whether the render texture should be smooth.
        """
        LIB_MOON._RenderTexture_SetSmooth(self.__ptr, smooth)

    def get_size(self) -> Vector2i | None:
        return self.__size

    def Init(self, width: int, height: int, arg: None | ContextSettingsPtr = None) -> Self:
        """
        #### Create a new render texture.

        ---

        :Args:
            width (int): The width of the render texture.
            height (int): The height of the render texture.
            arg (ContextSettingsPtr, optional): The context settings for the render texture. Defaults to None.
        """
        self.__size = Vector2i(width, height)
        if arg is None:
            LIB_MOON._RenderTexture_Create(self.__ptr, width, height)
        else:
            LIB_MOON._RenderTexture_CreateWithSettings(self.__ptr, width, height, arg)
        return self

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

    def get_texture(self) -> "Texture":
        texture_ptr = self.get_texture_ptr()
        texture = Texture()
        texture.load_from_ptr(texture_ptr)
        return texture


LIB_MOON._Texture_Init.argtypes = []
LIB_MOON._Texture_Init.restype = TexturePtr

LIB_MOON._Texture_LoadFromFile.argtypes = [TexturePtr, ctypes.c_char_p]
LIB_MOON._Texture_LoadFromFile.restype = ctypes.c_bool

LIB_MOON._Texture_LoadFromFileWithBoundRect.argtypes = [TexturePtr, ctypes.c_char_p,
                                                         ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Texture_LoadFromFileWithBoundRect.restype = ctypes.c_bool

LIB_MOON._Texture_Delete.argtypes = [TexturePtr]
LIB_MOON._Texture_Delete.restype = None

LIB_MOON._Texture_GetMaximumSize.argtypes = [TexturePtr]
LIB_MOON._Texture_GetMaximumSize.restype = ctypes.c_int

LIB_MOON._Texture_GetSizeX.argtypes = [TexturePtr]
LIB_MOON._Texture_GetSizeX.restype = ctypes.c_int

LIB_MOON._Texture_GetSizeY.argtypes = [TexturePtr]
LIB_MOON._Texture_GetSizeY.restype = ctypes.c_int

LIB_MOON._Texture_SetRepeated.argtypes = [TexturePtr, ctypes.c_bool]
LIB_MOON._Texture_SetRepeated.restype = None

LIB_MOON._Texture_SetSmooth.argtypes = [TexturePtr, ctypes.c_bool]
LIB_MOON._Texture_SetSmooth.restype = None

LIB_MOON._Texture_Swap.argtypes = [TexturePtr, TexturePtr]
LIB_MOON._Texture_Swap.restype = None

LIB_MOON._Texture_SubTexture.argtypes = [TexturePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Texture_SubTexture.restype = TexturePtr

class Texture(object):
    """
    Represents a texture resource managed by the Moon framework.
    Attributes:
        __ptr (TexturePtr): Internal pointer to the native texture object.
    """
    def __init__(self):
        # Initialize the texture object
        self.__ptr: TexturePtr | None = LIB_MOON._Texture_Init()

    def __del__(self):
        # Delete the texture object and release resources
        LIB_MOON._Texture_Delete(self.__ptr)
        self.__ptr = None

    def __eq__(self, other: object) -> bool:
        # Compare two Texture objects for equality
        if not isinstance(other, Texture):
            return False
        return self.__ptr == other.__ptr

    def __ne__(self, other: object) -> bool:
        # Compare two Texture objects for inequality
        return not self.__eq__(other)

    def set_ptr(self, ptr: TexturePtr) -> Self:
        # Set the internal pointer to a given TexturePtr
        self.__ptr = ptr
        return self

    def get_ptr(self) -> TexturePtr | None:
        # Get the internal pointer to the texture object
        return self.__ptr

    def is_init(self) -> bool:
        # Check if the texture object is initialized
        if self.__ptr != 0 or self.__ptr != None: return True
        return False

    def get_max_size(self) -> int:
        # Get the maximum supported texture size
        return LIB_MOON._Texture_GetMaximumSize(self.__ptr)

    def get_size(self) -> Vector2i:
        # Get the size of the texture as a Vector2i
        return Vector2i(
            LIB_MOON._Texture_GetSizeX(self.__ptr),
            LIB_MOON._Texture_GetSizeY(self.__ptr)
        )

    def set_repeat(self, value: bool = True) -> Self:
        # Set whether the texture should repeat when drawn outside its bounds
        LIB_MOON._Texture_SetRepeated(self.__ptr, value)
        return self

    def set_smooth(self, value: bool = True) -> Self:
        # Set whether the texture should use smoothing (linear filtering)
        LIB_MOON._Texture_SetSmooth(self.__ptr, value)
        return self

    def swap(self, other: "Texture") -> Self:
        # Swap the contents of this texture with another
        LIB_MOON._Texture_Swap(self.__ptr, other.get_ptr())
        return self

    def get_sub_texture_ptr(self, rect_pos: Vector2i, rect_size: Vector2i) -> TexturePtr:
        # Get a pointer to a sub-region of the texture
        texture_ptr = LIB_MOON._Texture_SubTexture(self.__ptr, rect_pos.x, rect_pos.y, rect_size.x, rect_size.y)
        return texture_ptr

    def get_sub_texture(self, rect_pos: Vector2i, rect_size: Vector2i) -> "Texture":
        # Get a Texture object representing a sub-region of the texture
        texture_ptr = self.get_sub_texture_ptr(rect_pos, rect_size)
        texture = Texture()
        texture.load_from_ptr(texture_ptr)
        return texture

    def load_from_file(self, filename: str) -> tuple[bool, Self]:
        # Load the texture from a file
        result = LIB_MOON._Texture_LoadFromFile(self.__ptr, filename.encode('utf-8'))
        return result, self

    def load_from_file_with_bound_rect(self, filename: str, rect_pos: Vector2i, rect_size: Vector2i) -> tuple[bool, Self]:
        # Load the texture from a file, using a specified rectangle region
        result = LIB_MOON._Texture_LoadFromFileWithBoundRect(self.__ptr, filename.encode('utf-8'),
                                                    rect_pos.x, rect_pos.y, rect_size.x, rect_size.y)
        return result, self

    def load_from_ptr(self, ptr: TexturePtr) -> bool:
        # Load the texture from an existing pointer
        if ptr is not None:
            self.__ptr = ptr
            return True
        return False



LIB_MOON._Sprite_Init.argtypes = []
LIB_MOON._Sprite_Init.restype = SpritePtr

LIB_MOON._Sprite_LinkTexture.argtypes = [SpritePtr, TexturePtr, ctypes.c_bool]
LIB_MOON._Sprite_LinkTexture.restype = None

LIB_MOON._Sprite_LinkRenderTexture.argtypes = [SpritePtr, RenderTexturePtr, ctypes.c_bool]
LIB_MOON._Sprite_LinkRenderTexture.restype = None

LIB_MOON._Sprite_SetTextureRect.argtypes = [SpritePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Sprite_SetTextureRect.restype = None

LIB_MOON._Sprite_SetScale.argtypes = [SpritePtr, ctypes.c_double, ctypes.c_double]
LIB_MOON._Sprite_SetScale.restype = None

# Добавляем недостающие биндинги для Sprite

LIB_MOON._Sprite_SetRotation.argtypes = [SpritePtr, ctypes.c_double]
LIB_MOON._Sprite_SetRotation.restype = None

LIB_MOON._Sprite_SetPosition.argtypes = [SpritePtr, ctypes.c_double, ctypes.c_double]
LIB_MOON._Sprite_SetPosition.restype = None

LIB_MOON._Sprite_SetOrigin.argtypes = [SpritePtr, ctypes.c_double, ctypes.c_double]
LIB_MOON._Sprite_SetOrigin.restype = None

LIB_MOON._Sprite_SetColor.argtypes = [SpritePtr, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
LIB_MOON._Sprite_SetColor.restype = None

LIB_MOON._Sprite_GetColorR.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetColorR.restype = ctypes.c_int

LIB_MOON._Sprite_GetColorG.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetColorG.restype = ctypes.c_int

LIB_MOON._Sprite_GetColorB.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetColorB.restype = ctypes.c_int

LIB_MOON._Sprite_GetColorA.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetColorA.restype = ctypes.c_int

LIB_MOON._Sprite_GetRotation.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetRotation.restype = ctypes.c_int

LIB_MOON._Sprite_GetScaleX.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetScaleX.restype = ctypes.c_double

LIB_MOON._Sprite_GetScaleY.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetScaleY.restype = ctypes.c_double

LIB_MOON._Sprite_GetPositionX.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetPositionX.restype = ctypes.c_double

LIB_MOON._Sprite_GetPositionY.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetPositionY.restype = ctypes.c_double

# Также нужно добавить биндинг для удаления спрайта, если его нет
LIB_MOON._Sprite_Delete.argtypes = [SpritePtr]
LIB_MOON._Sprite_Delete.restype = None


LIB_MOON._Sprite_GetGlobalBoundRectX.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetGlobalBoundRectX.restype = ctypes.c_double

LIB_MOON._Sprite_GetGlobalBoundRectY.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetGlobalBoundRectY.restype = ctypes.c_double

LIB_MOON._Sprite_GetGlobalBoundRectW.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetGlobalBoundRectW.restype = ctypes.c_double

LIB_MOON._Sprite_GetGlobalBoundRectH.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetGlobalBoundRectH.restype = ctypes.c_double

LIB_MOON._Sprite_Rotate.argtypes = [SpritePtr, ctypes.c_double]
LIB_MOON._Sprite_Rotate.restype = None

LIB_MOON._Sprite_Scale.argtypes = [SpritePtr, ctypes.c_double, ctypes.c_double]
LIB_MOON._Sprite_Scale.restype = None

LIB_MOON._Sprite_GetLocalBoundRectX.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetLocalBoundRectX.restype = ctypes.c_double

LIB_MOON._Sprite_GetLocalBoundRectY.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetLocalBoundRectY.restype = ctypes.c_double

LIB_MOON._Sprite_GetLocalBoundRectW.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetLocalBoundRectW.restype = ctypes.c_double

LIB_MOON._Sprite_GetLocalBoundRectH.argtypes = [SpritePtr]
LIB_MOON._Sprite_GetLocalBoundRectH.restype = ctypes.c_double

type Seconds = float
type Time = Seconds

class Sprite2D(object):

    __slots__ = ('__ptr', '__flip_vector', '__size')

    def __init__(self):
        self.__ptr = LIB_MOON._Sprite_Init()
        self.__flip_vector = Vector2i(1, 1)
        self.__size = Vector2f.zero()

    def __del__(self):
        LIB_MOON._Sprite_Delete(self.__ptr)

    def get_global_bounds(self) -> tuple[Vector2f, Vector2f]:
        return (
            Vector2f(LIB_MOON._Sprite_GetGlobalBoundRectX(self.__ptr),
                     LIB_MOON._Sprite_GetGlobalBoundRectY(self.__ptr)),
            Vector2f(abs(LIB_MOON._Sprite_GetGlobalBoundRectW(self.__ptr)),
                     abs(LIB_MOON._Sprite_GetGlobalBoundRectH(self.__ptr)))
        )

    def get_global_bounds_size(self) -> Vector2f:
        return Vector2f(
            abs(LIB_MOON._Sprite_GetGlobalBoundRectW(self.__ptr)),
            abs(LIB_MOON._Sprite_GetGlobalBoundRectH(self.__ptr))
        )


    def get_size(self, use_cache: bool = True) -> Vector2f:
        if use_cache:
            return self.__size
        self.__size = self.get_global_bounds_size()
        return self.__size

    def get_local_bounds(self) -> tuple[Vector2f, Vector2f]:
        return (
            Vector2f(LIB_MOON._Sprite_GetLocalBoundRectX(self.__ptr),
                     LIB_MOON._Sprite_GetLocalBoundRectY(self.__ptr)),
            Vector2f(abs(LIB_MOON._Sprite_GetLocalBoundRectW(self.__ptr)),
                     abs(LIB_MOON._Sprite_GetLocalBoundRectH(self.__ptr)))
        )

    def get_local_bounds_size(self) -> Vector2f:
        return Vector2f(
            abs(LIB_MOON._Sprite_GetLocalBoundRectW(self.__ptr)),
            abs(LIB_MOON._Sprite_GetLocalBoundRectH(self.__ptr))
        )

    def get_flips(self) -> Vector2i:
        return self.__flip_vector

    def rotate(self, angle: Number) -> Self:
        LIB_MOON._Sprite_Rotate(self.__ptr, angle)
        return self

    def scale(self, scale_x: Number = 1, scale_y: Number = 1) -> Self:
        LIB_MOON._Sprite_Scale(self.__ptr, scale_x, scale_y)
        return self

    def flip(self, x: bool | None = None, y: bool | None = None) -> Self:
        scale = self.get_scale()
        new_flips = [1, 1]
        if isinstance(x, bool) and x:
            new_flips[0] = -1
        else:
            new_flips[0] = 1
        if isinstance(y, bool) and y:
            new_flips[1] = -1
        else:
            new_flips[1] = 1

        self.__flip_vector.x *= new_flips[0]
        self.__flip_vector.y *= new_flips[1]

        self.set_scale(scale.x * new_flips[0], scale.y * new_flips[1])

        return self

    def set_flip_x(self, value: bool) -> Self:
        if value != (self.__flip_vector.x == -1):
            self.flip(x=True)
        return self

    def set_flip_y(self, value: bool) -> Self:
        if value != (self.__flip_vector.y == -1):
            self.flip(y=True)
        return self

    def link_texture(self, texture: Texture, reset_rect: bool = False) -> Self:
        LIB_MOON._Sprite_LinkTexture(self.__ptr, texture.get_ptr(), reset_rect)
        return self

    def link_render_texture(self, texture: RenderTexture, reset_rect: bool = False) -> Self:
        LIB_MOON._Sprite_LinkRenderTexture(self.__ptr, texture.get_ptr(), reset_rect)
        return self

    def set_texture_rect(self, rect_pos: Vector2i, rect_size: Vector2i) -> Self:
        LIB_MOON._Sprite_SetTextureRect(self.__ptr, rect_pos.x, rect_pos.y, rect_size.x, rect_size.y)
        return self

    def set_scale(self, arg1: float, arg2: Optional[float] = None) -> Self:
        if arg2 is not None:
            LIB_MOON._Sprite_SetScale(self.__ptr, arg1, arg2)
        else:
            LIB_MOON._Sprite_SetScale(self.__ptr, arg1, arg1)
        self.__size = self.get_global_bounds_size()
        return self

    def set_rotation(self, angle: float) -> Self:
        """Устанавливает поворот спрайта в градусах"""
        LIB_MOON._Sprite_SetRotation(self.__ptr, angle)
        self.__size = self.get_global_bounds_size()
        return self

    def set_position(self, position: Vector2Type) -> Self:
        """Устанавливает позицию спрайта из Vector2f"""
        LIB_MOON._Sprite_SetPosition(self.__ptr, position.x, position.y)
        return self

    def set_origin(self, origin: Vector2Type) -> Self:
        """Устанавливает точку отсчета (origin) спрайта из Vector2f"""
        LIB_MOON._Sprite_SetOrigin(self.__ptr, origin.x, origin.y)
        return self

    def set_typed_origin(self, origin_type: OriginTypes) -> Self:
        """Устанавливает точку отсчета (origin) спрайта из OriginTypes"""
        bounds = self.get_global_bounds()
        scale = self.get_scale()
        if origin_type == OriginTypes.TOP_LEFT:
            self.set_origin(Vector2f(0, 0))
        elif origin_type == OriginTypes.TOP_CENTER:
            self.set_origin(Vector2f(-bounds[1].x / 2 / scale.x, 0))
        elif origin_type == OriginTypes.TOP_RIGHT:
            self.set_origin(Vector2f(-bounds[1].x / scale.x, 0))
        elif origin_type == OriginTypes.LEFT_CENTER:
            self.set_origin(Vector2f(0, -bounds[1].y / 2 / scale.y))
        elif origin_type == OriginTypes.CENTER:
            self.set_origin(Vector2f(-bounds[1].x / 2 / scale.x, -bounds[1].y / 2 / scale.y))
        elif origin_type == OriginTypes.RIGHT_CENTER:
            self.set_origin(Vector2f(-bounds[1].x / scale.x, -bounds[1].y / 2 / scale.y))
        elif origin_type == OriginTypes.DOWN_LEFT:
            self.set_origin(Vector2f(0, -bounds[1].y / scale.y))
        elif origin_type == OriginTypes.DOWN_CENTER:
            self.set_origin(Vector2f(-bounds[1].x / 2 / scale.x, -bounds[1].y / scale.y))
        elif origin_type == OriginTypes.DOWN_RIGHT:
            self.set_origin(Vector2f(-bounds[1].x / scale.x, -bounds[1].y / scale.y))
        return self

    def set_color(self, color: Color) -> Self:
        """Устанавливает цвет спрайта"""
        LIB_MOON._Sprite_SetColor(self.__ptr, color.r, color.g, color.b, color.a)
        return self

    def get_color(self) -> Color:
        """Возвращает цвет спрайта"""
        return Color(
            LIB_MOON._Sprite_GetColorR(self.__ptr),
            LIB_MOON._Sprite_GetColorG(self.__ptr),
            LIB_MOON._Sprite_GetColorB(self.__ptr),
            LIB_MOON._Sprite_GetColorA(self.__ptr)
        )

    def get_rotation(self) -> float:
        """Возвращает угол поворота спрайта в градусах"""
        return LIB_MOON._Sprite_GetRotation(self.__ptr)

    def get_scale(self) -> Vector2f:
        """Возвращает масштаб спрайта"""
        return Vector2f(
            LIB_MOON._Sprite_GetScaleX(self.__ptr),
            LIB_MOON._Sprite_GetScaleY(self.__ptr)
        )

    def get_position(self) -> Vector2f:
        """Возвращает позицию спрайта"""
        return Vector2f(
            LIB_MOON._Sprite_GetPositionX(self.__ptr),
            LIB_MOON._Sprite_GetPositionY(self.__ptr)
        )

    def get_position_x(self) -> float:
        return LIB_MOON._Sprite_GetPositionX(self.__ptr)

    def get_position_y(self) -> float:
        return LIB_MOON._Sprite_GetPositionY(self.__ptr)

    def get_ptr(self) -> SpritePtr:
        return self.__ptr

type FrameTime = float

class AnimatedSprite2D(Sprite2D):

    __slots__ = ("__frames_count", "__frame_time", "__texture_size", "__ptr", "__is_started",
                '__flip_vector', '__size', '__current_frame_index', '__last_time', '__cycle')

    def __init__(self, texture_size: Vector2i, frames_count: int, frame_time: FrameTime):
        super().__init__()
        self.__frames_count = frames_count
        self.__frame_time = frame_time
        self.__texture_size = texture_size
        self.set_texture_rect(Vector2i.zero(), self.__texture_size)

        self.__current_frame_index = 0
        self.__last_time = 0

        self.__cycle = True
        self.__is_started = False

    def start(self):
        self.__is_started = True

    def restart(self):
        self.__current_frame_index = 0
        self.__last_time = time.time()
        self.__is_started = True

    def stop(self):
        self.__is_started = False

    def get_frames_count(self) -> int:
        return self.__frames_count

    def get_texture_size(self) -> Vector2i:
        return self.__texture_size

    def get_frame_time(self) -> FrameTime:
        return self.__frame_time

    def update(self):
        at_time = time.time()
        delta = at_time - self.__last_time
        if self.__is_started:
            if delta >= self.__frame_time:
                self.__current_frame_index += 1
                self.__last_time = at_time
        if self.__current_frame_index >= self.__frames_count:
            if self.__cycle:
                self.__current_frame_index = 0
            else:
                self.__current_frame_index -= 1
                self.stop()
        super().set_texture_rect(Vector2i(self.__current_frame_index * self.__texture_size.x, 0), self.__texture_size)

    def get_ptr(self) -> SpritePtr:
        return super().get_ptr()

ImagePtr = ctypes.c_void_p
LIB_MOON._Image_TextureCopyToImage.argtypes = [TexturePtr]
LIB_MOON._Image_TextureCopyToImage.restype = ImagePtr

LIB_MOON._Image_RenderTextureCopyToImage.argtypes = [TexturePtr]
LIB_MOON._Image_RenderTextureCopyToImage.restype = ImagePtr

LIB_MOON._Image_Delete.argtypes = [ImagePtr]
LIB_MOON._Image_Delete.restype = None

LIB_MOON._Image_Save.argtypes = [ImagePtr, ctypes.c_char_p]
LIB_MOON._Image_Save.restype = ctypes.c_bool

LIB_MOON._Image_Init.argtypes = []
LIB_MOON._Image_Init.restype = ImagePtr

class Image:
    @classmethod
    def CopyFromTexture(cls, texture: Texture) -> "Image":
        img = Image()
        ptr = LIB_MOON._Image_TextureCopyToImage(texture.get_ptr())
        img.set_ptr(ptr)
        return img
    
    @classmethod
    def CopyFromRenderTexture(cls, texture: RenderTexture) -> "Image":
        img = Image()
        ptr = LIB_MOON._Image_RenderTextureCopyToImage(texture.get_ptr())
        img.set_ptr(ptr)
        return img

    def __init__(self):
        self.__ptr = LIB_MOON._Image_Init()

    def get_ptr(self) -> ImagePtr:
        return self.__ptr
    
    def set_ptr(self, ptr: ImagePtr) -> Self:
        self.__ptr = ptr

    def save(self, file_path: str) -> bool:
        print(self.__ptr)
        return LIB_MOON._Image_Save(self.__ptr, file_path.encode('utf-8'))
