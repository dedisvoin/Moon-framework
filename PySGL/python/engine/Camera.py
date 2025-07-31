from PySGL.python.Views import *
from PySGL.python.Vectors import *
from PySGL.python.Window import Window

class Camera2D:
    def __init__(self, width: int, height: int):
        if width <= 0 or height <= 0:
            raise ValueError("Camera dimensions must be positive")

        self.__width = width
        self.__height = height

        self.__view = View(FloatRect(0, 0, self.__width, self.__height))

        self.__target_center: None | Vector2f = Vector2f(0, 0)
        self.__target_zoom: float = 1
        self.__saved_zoom: float =1
        self.__zoom: float = 1

        self.__lerp_movement: float = 0.1
        self.__lerp_zoom: float = 0.1

        self.__target_shake = Vector2f(0, 0)
        self.__shake_lerp = Vector2f(0.9, 0.9)

        self.__shake_only_x = False
        self.__shake_only_y = False

        self.__angle = 0
        self.__target_angle = 0
        self.__angle_lerp = 0.1

        # Использование координат двух обьектов для слежения за обоими обьектами
        self.__first_target: Vector2i | Vector2f | BaseVector2 | None = None
        self.__second_target: Vector2i | Vector2f | BaseVector2 | None = None
        self.__two_target_factor: float = 0.5
        self.__use_two_target: bool =  False

        self.__auto_scale_padding: float | int = 0

        self.__window: Window | None = None

    def set_window(self, window: Window) -> Self:
        self.__window = window
        return self

    def set_two_target_factor(self, factor: float = 0.5) -> Self:
        self.__two_target_factor = factor

    def set_auto_scale_padding(self, padding: float) -> Self:
        self.__auto_scale_padding = padding

    def get_auto_scale_padding(self) -> float | int:
        return self.__auto_scale_padding
    
    def set_using_two_target(self, flag: bool = True) -> Self:
        self.__use_two_target = flag

    def get_using_two_target(self) -> bool:
        return self.__use_two_target

    def get_view(self) -> View:
        return self.__view

    def get_zoom(self) -> float:
        return self.__zoom

    def shake(self, amplitude: float = 5) -> Self:
        self.__target_shake = Vector2f(amplitude, amplitude)
        self.__shake_only_x = False
        self.__shake_only_y = False

    def shake_x(self, amplitude: float = 5) -> Self:
        self.__target_shake = Vector2f(amplitude, 0)
        self.__shake_only_x = True

    def shake_y(self, amplitude: float = 5) -> Self:
        self.__target_shake = Vector2f(0, amplitude)
        self.__shake_only_y = True

    def set_lerp_rotate(self, lerp: float) -> Self:
        self.__angle_lerp =lerp

    def set_lerp_movement(self, lerp: float) -> Self:
        self.__lerp_movement = lerp

    def set_target_angle(self, angle: float) -> Self:
        self.__target_angle = angle

    def set_lerp_zoom(self, lerp: float) -> Self:
        self.__lerp_zoom = lerp

    def follow(self, position_1: Vector2f, position_2: Vector2f | None = None) -> Self:
        self.__target_center = position_1

        if position_2 != None:
            self.__first_target = position_1
            self.__second_target = position_2
            

    def set_target_zoom(self, zoom: float = 1) -> Self:
        self.__target_zoom = zoom
        self.__saved_zoom = zoom

    def set_size(self, width: int, height: int) -> Self:
        self.__view.set_size(width, height)
        self.__width = width
        self.__height = height

    def get_center_position(self) -> Vector2f:
        return Vector2f(*self.__view.get_center())
    
    def get_size(self) -> Vector2f:
        size = self.__view.get_float_rect().get_size()
        return Vector2f(*size) * self.__zoom
    
    def get_position(self) -> Vector2f:
        return self.current_center 

    def update(self, delta: float = 1) -> None:
        if self.__window and self.__window.get_resized():
            self.__width = self.__window.get_size().x
            self.__height = self.__window.get_size().y
            self.__view.set_size(self.__width, self.__height)

        if self.__use_two_target:

            pos_1 = self.__first_target.as_tuple()
            pos_2 = self.__second_target.as_tuple()
            normal = Vector2f(pos_1[0] - pos_2[0], pos_1[1] - pos_2[1])
            self.__target_center = self.__second_target + normal * self.__two_target_factor
        

        self.current_center = Vector2f(*self.__view.get_center())
        self.current_center += (self.__target_center - self.current_center) * self.__lerp_movement * delta
        self.__view.set_center(*self.current_center.xy)

        if self.__use_two_target:
            vector_delta = (self.__first_target - self.__second_target)
            distance_x = abs(vector_delta.x)
            distance_y = abs(vector_delta.y)

            k = 0.5 / max(self.__two_target_factor, 1 - self.__two_target_factor)

            d_x = max(distance_x / ((self.__width - self.__auto_scale_padding) * k), self.__saved_zoom)
            d_y = max(distance_y / ((self.__height - self.__auto_scale_padding) * k), self.__saved_zoom)


            self.__target_zoom = max(d_x, d_y)
        else:
            self.__target_zoom = self.__saved_zoom
            

        self.__zoom += (self.__target_zoom - self.__zoom) * self.__lerp_zoom * delta
        self.__view.set_size(self.__width * self.__zoom, self.__height * self.__zoom)

        
        self.__target_shake *= self.__shake_lerp ** delta
        
        if self.__shake_only_x == False and self.__shake_only_y == False:
            self.__target_shake = self.__target_shake.rotated(randint(0, 360))
        elif self.__shake_only_x:
            self.__target_shake.x *= uniform(-1, 1)
        elif self.__shake_only_y:
            self.__target_shake.y *= uniform(-1, 1)
        
        self.__view.move(self.__target_shake.x, self.__target_shake.y)


        self.__angle += (self.__target_angle - self.__angle) * self.__angle_lerp

        self.__view.set_angle(self.__angle)

    def apply(self, window: Window) -> None:
        window.set_view(self.__view)

    def reapply(self, window: Window) -> None:
        window.set_view(window.get_default_view())


class CameraMachine2D(Camera2D):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.__position = Vector2f(0, 0)

    def move(self, x: float = 0, y: float = 0) -> Self:
        self.__position += Vector2f(x, y)
        return self

    def get_position(self) -> Vector2f:
        return self.__position 
    
    def set_position(self, position: Vector2f) -> Self:
        self.__position = position
        return self

    def update(self):
        self.follow(self.__position)
        super().update(1)
