import sys
sys.path.append('./')
import time
from Moon.python.Vectors import *

r = 1000000

print(f"Size of Vector2f(..., ...): {sys.getsizeof(Vec2f(12000,0))}")

print("Vectors multiplication test")
print(f"Count: {r}")
print("Initializing...")
start = time.time()
vectors = [Vec2f.random() * 10 for _ in range(r)]
two_vectors = [Vec2f.random() * 10 for _ in range(r)]
result = Vec2f(0, 0)
print(sys.getsizeof(vectors) + sys.getsizeof(two_vectors) + sys.getsizeof(result))
print(time.time() - start)


print("start test...")
start = time.time()
for i in range(r):
    result += vectors[i] * two_vectors[i]
print(time.time() - start)


