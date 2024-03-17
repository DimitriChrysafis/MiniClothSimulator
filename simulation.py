# simulation.py
import math

class Simulation:
    def __init__(self):

        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 60
        self.PARTICLE_RADIUS = 10
        self.SPRING_CONSTANT = 0.1
        self.FRICTION = 0.9
        self.DRAG = 0.05

        self.NUM_PARTICLES_X = 30
        self.NUM_PARTICLES_Y = 30
