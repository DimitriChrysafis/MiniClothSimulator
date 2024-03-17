# spring.py
import math
from simulation import Simulation

class Spring:
    def __init__(self, particle_a, particle_b, length):
        self.particle_a = particle_a
        self.particle_b = particle_b
        self.length = length
        self.simulation = Simulation()

    def update(self):
        dx = self.particle_b.x - self.particle_a.x
        dy = self.particle_b.y - self.particle_a.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        spring_force = self.simulation.SPRING_CONSTANT * (distance - self.length)

        angle = math.atan2(dy, dx)
        force_a_x = spring_force * math.cos(angle)
        force_a_y = spring_force * math.sin(angle)
        force_b_x = -force_a_x
        force_b_y = -force_a_y

        self.particle_a.apply_force(force_a_x, force_a_y)
        self.particle_b.apply_force(force_b_x, force_b_y)
