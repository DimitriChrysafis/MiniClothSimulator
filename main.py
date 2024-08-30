
import pygame
from simulation import Simulation
from particle import Particle
from spring import Spring
from button import Button
import math

simulation = Simulation()

pygame.init()
screen = pygame.display.set_mode((simulation.WIDTH, simulation.HEIGHT))
pygame.display.set_caption('Ripple Effect Simulator')
clock = pygame.time.Clock()

particles = [[Particle(x, y, fixed=(x == 0 or x == simulation.WIDTH - 1 or y == 0 or y == simulation.HEIGHT - 1)) for y in range(0, simulation.HEIGHT, simulation.HEIGHT // simulation.NUM_PARTICLES_Y)] for x in range(0, simulation.WIDTH, simulation.WIDTH // simulation.NUM_PARTICLES_X)]

springs = []
for i in range(len(particles) - 1):
    for j in range(len(particles[0]) - 1):
        spring_a = Spring(particles[i][j], particles[i + 1][j], simulation.WIDTH // simulation.NUM_PARTICLES_X)
        spring_b = Spring(particles[i][j], particles[i][j + 1], simulation.HEIGHT // simulation.NUM_PARTICLES_Y)
        springs.extend([spring_a, spring_b])

reset_button = Button(simulation.WIDTH - 120, simulation.HEIGHT - 50, 100, 40, "Reset")

running = True
grabbed_particle = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if reset_button.rect.collidepoint(mx, my):
                for row in particles:
                    for particle in row:
                        particle.x, particle.y = particle.initial_x, particle.initial_y
                        particle.vx, particle.vy = 0, 0
            else:
                for row in particles:
                    for particle in row:
                        distance = math.sqrt((mx - particle.x) ** 2 + (my - particle.y) ** 2)
                        if distance < simulation.PARTICLE_RADIUS and not particle.fixed:
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
            red_value = min(255, int(speed * 30))
            color = (red_value, 0, 255 - red_value)
            pygame.draw.circle(screen, color, (int(particle.x), int(particle.y)), simulation.PARTICLE_RADIUS)

    reset_button.draw(screen)
    #Draw:)

    pygame.display.flip()
    clock.tick(simulation.FPS)

pygame.quit()
