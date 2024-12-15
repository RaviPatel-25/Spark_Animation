import pygame
import random
import math
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Drag-Following Cracker Animation with Starry Universe")

BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
]

clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, color, speed, angle, radius):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.angle = angle
        self.radius = radius
        self.lifetime = random.randint(50, 100)
        self.alpha = 255

    def update(self):
        self.x += self.speed * math.cos(self.angle) + random.uniform(-0.5, 0.5)
        self.y += self.speed * math.sin(self.angle) + random.uniform(-0.5, 0.5)
        self.lifetime -= 1
        self.radius = max(0, self.radius - 0.1)
        self.alpha = max(0, int((self.lifetime / 100) * 255))

    def draw(self, surface):
        if self.lifetime > 0 and self.radius > 0:
            surface.set_alpha(self.alpha)
            pygame.draw.circle(
                surface, self.color, (int(self.x), int(self.y)), int(self.radius)
            )

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.radius = random.randint(1, 3)
        self.speed = random.uniform(0.1, 0.9)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = 0
            self.radius = random.randint(1, 3)
            self.speed = random.uniform(0.05, 0.2)

    def draw(self, surface):
        pygame.draw.circle(surface, COLORS[-1], (self.x, self.y), self.radius)

particles = []
stars = [Star() for _ in range(300)]

def create_cracker(x, y):
    for _ in range(20):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        radius = random.randint(2, 8)
        color = random.choice(COLORS[:-1])
        particles.append(Particle(x, y, color, speed, angle, radius))

dragging = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    if dragging:
        x, y = pygame.mouse.get_pos()
        create_cracker(x, y)

    for star in stars:
        star.update()

    screen.fill(BLACK)

    for star in stars:
        star.draw(screen)

    for particle in particles[:]:
        particle.update()
        particle.draw(screen)
        if particle.lifetime <= 0 or particle.radius <= 0:
            particles.remove(particle)

    pygame.display.flip()

    clock.tick(60)
