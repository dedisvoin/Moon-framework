from Moon.python.Vectors import Vector2f
from Moon.python.Rendering.Shapes import *
from Moon.python.Rendering.Sprites import *
from Moon.python.Rendering.Vertexes import *

from dataclasses import dataclass

def _CREATE_CIRCLE_PARTICLE_TEXTURE(resolution: int = 100) -> RenderTexture:
    texture = RenderTexture().create(resolution, resolution)
    texture.clear(COLOR_TRANSPARENT)

    circle = CircleShape(30).set_origin_radius(resolution / 2)
    circle.set_position(resolution / 2, resolution / 2)
    circle.set_color(COLOR_WHITE)

    texture.draw(circle)
    texture.display()
    del circle
    return texture


class Particle:
    def __init__(self):
        self.position: Vector2f = Vector2f(0, 0)
        self.speed: Vector2f = Vector2f(0, 0)
        self.color: Color = COLOR_AQUA
        self.size: Vector2f = Vector2f(10, 10)


class ParticleEmiters:
    class Point:
        def __init__(self, position: Vector2f):
            self.position = position

class ParticleSystem:
    def __init__(self):
        self.particles: list[Particle] = []

        self.particles_vertexes = VertexArray().set_primitive_type(VertexArray.PrimitiveType.QUADS)

    def construct(self, particle: Particle, emmiter: ParticleEmiters) -> Particle:
        if isinstance(emmiter, ParticleEmiters.Point):
            particle.position = emmiter.position
            particle.speed = Vector2f(0, random.uniform(0, 10)).rotate_at(random.randint(0, 360))
            return particle


    def emit(self, emiter: ParticleEmiters, count: int = 10):
        for _ in range(count):
            p = Particle()
            p = self.construct(p, emiter)
            self.particles.append(p)
            del p

    def update(self):
        self.particles_vertexes.clear()

        for p in self.particles:
            self.particles_vertexes.append(Vertex(p.position + Vector2f(-p.size.x / 2, -p.size.y / 2)))
            self.particles_vertexes.append(Vertex(p.position + Vector2f(p.size.x / 2, -p.size.y / 2)))
            self.particles_vertexes.append(Vertex(p.position + Vector2f(p.size.x / 2, p.size.y / 2)))
            self.particles_vertexes.append(Vertex(p.position + Vector2f(-p.size.x / 2, p.size.y / 2)))

            p.position += p.speed

    def render(self, window):
        window.draw(self.particles_vertexes)