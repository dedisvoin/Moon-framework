import sys
sys.path.append('./')

from Moon.python.Vectors import *


vec_1 = Vec2i(1, 2)
vec_1 += Vec2f(3.5, 4).to_int()  # Vector2i(4, 6)
print(vec_1)


vec_1 = Vec2i(5, 4)
vec_1 *= Vec2f(1, 2.6)  # Vector2i(5, 8)
print(vec_1)
print(*vec_1)
