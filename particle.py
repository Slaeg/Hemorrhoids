import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.Surface((3, 3))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.math.Vector2(random.uniform(-0.5, 0.5), random.uniform(1, 2))
        self.lifetime = random.randint(10, 20)

    def update(self):
        self.rect.center += self.velocity
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()