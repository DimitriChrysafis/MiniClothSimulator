# particle.py
import math
from simulation import Simulation

class Particle:
    def __init__(self, x, y, fixed=False):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.fixed = fixed
        self.initial_x = x
        self.initial_y = y
        self.simulation = Simulation()

    def apply_force(self, force_x, force_y):
        if not self.fixed:
            self.vx += force_x
            self.vy += force_y

    def update(self):
        if not self.fixed:
            self.vx *= self.simulation.FRICTION
            self.vy *= self.simulation.FRICTION
            self.vx -= self.vx * self.simulation.DRAG
            self.vy -= self.vy * self.simulation.DRAG
            self.x += self.vx
            self.y += self.vy
