import pygame
import random
import math

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color, size=3, speed=2, lifetime=60):
        super().__init__()
        self.original_size = size
        self.size = size
        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size, size), size)
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * speed
        self.pos = pygame.math.Vector2(pos)
        self.lifetime = lifetime
        self.original_lifetime = lifetime
        self.color = color

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos
        self.lifetime -= 1
        
        # Fade out the particle
        alpha = int(255 * (self.lifetime / self.original_lifetime))
        self.image.set_alpha(alpha)
        
        # Shrink the particle
        self.size = self.original_size * (self.lifetime / self.original_lifetime)
        new_image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(new_image, self.color, (self.size, self.size), self.size)
        self.image = new_image
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.lifetime <= 0:
            self.kill()