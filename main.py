import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PARTICLE_RADIUS = 10
SPRING_CONSTANT = 0.1
FRICTION = 0.8
DRAG = 0.1

# Add more balls
NUM_PARTICLES_X = 30
NUM_PARTICLES_Y = 30

# Particle class
class Particle:
    def __init__(self, x, y, fixed=False):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.fixed = fixed
        self.initial_x = x
        self.initial_y = y

    def apply_force(self, force_x, force_y):
        if not self.fixed:
            self.vx += force_x
            self.vy += force_y

    def update(self):
        if not self.fixed:
            self.vx *= FRICTION
            self.vy *= FRICTION
            self.vx -= self.vx * DRAG
            self.vy -= self.vy * DRAG
            self.x += self.vx
            self.y += self.vy

# Spring class
class Spring:
    def __init__(self, particle_a, particle_b, length):
        self.particle_a = particle_a
        self.particle_b = particle_b
        self.length = length

    def update(self):
        dx = self.particle_b.x - self.particle_a.x
        dy = self.particle_b.y - self.particle_a.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        spring_force = SPRING_CONSTANT * (distance - self.length)

        angle = math.atan2(dy, dx)
        force_a_x = spring_force * math.cos(angle)
        force_a_y = spring_force * math.sin(angle)
        force_b_x = -force_a_x
        force_b_y = -force_a_y

        self.particle_a.apply_force(force_a_x, force_a_y)
        self.particle_b.apply_force(force_b_x, force_b_y)

# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.color = (0, 255, 0)  # Button color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ripple Effect Simulator')
clock = pygame.time.Clock()

# Create particles in a grid-like structure with more balls
particles = [[Particle(x, y, fixed=(x == 0 or x == WIDTH - 1 or y == 0 or y == HEIGHT - 1)) for y in range(0, HEIGHT, HEIGHT // NUM_PARTICLES_Y)] for x in range(0, WIDTH, WIDTH // NUM_PARTICLES_X)]

# Connect particles with springs
springs = []
for i in range(len(particles) - 1):
    for j in range(len(particles[0]) - 1):
        spring_a = Spring(particles[i][j], particles[i + 1][j], WIDTH // NUM_PARTICLES_X)
        spring_b = Spring(particles[i][j], particles[i][j + 1], HEIGHT // NUM_PARTICLES_Y)
        springs.extend([spring_a, spring_b])

# Initialize reset button
reset_button = Button(WIDTH - 120, HEIGHT - 50, 100, 40, "Reset")

running = True
grabbed_particle = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if reset_button.rect.collidepoint(mx, my):
                # Reset all particles to their initial state
                for row in particles:
                    for particle in row:
                        particle.x, particle.y = particle.initial_x, particle.initial_y
                        particle.vx, particle.vy = 0, 0
            else:
                for row in particles:
                    for particle in row:
                        distance = math.sqrt((mx - particle.x) ** 2 + (my - particle.y) ** 2)
                        if distance < PARTICLE_RADIUS and not particle.fixed:
                            grabbed_particle = particle
        elif event.type == pygame.MOUSEBUTTONUP:
            grabbed_particle = None

    if grabbed_particle:
        grabbed_particle.x, grabbed_particle.y = pygame.mouse.get_pos()
        grabbed_particle.vx = 0
        grabbed_particle.vy = 0

    for spring in springs:
        spring.update()

    for row in particles:
        for particle in row:
            particle.update()

    screen.fill((255, 255, 255))

    for spring in springs:
        pygame.draw.line(screen, (0, 0, 0), (int(spring.particle_a.x), int(spring.particle_a.y)),
                         (int(spring.particle_b.x), int(spring.particle_b.y)), 2)

    for row in particles:
        for particle in row:
            speed = math.sqrt(particle.vx ** 2 + particle.vy ** 2)
            red_value = min(255, int(speed * 30))  # Adjust the multiplier for sensitivity
            color = (red_value, 0, 255 - red_value)
            pygame.draw.circle(screen, color, (int(particle.x), int(particle.y)), PARTICLE_RADIUS)

    reset_button.draw(screen)  # Draw the reset button

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
