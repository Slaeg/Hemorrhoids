import pygame
import random
import math

class Particle(pygame.sprite.Sprite):
    """A class representing a particle in the game."""

    def __init__(self, position, color, size=3, speed=2, lifetime=60):
        """
        Initialize a particle.

        Args:
            position (tuple): The (x, y) position of the particle.
            color (tuple): The color of the particle.
            size (int, optional): The size of the particle. Defaults to 3.
            speed (float, optional): The speed of the particle. Defaults to 2.
            lifetime (int, optional): The lifetime of the particle in frames. Defaults to 60.
        """
        super().__init__()
        self.original_size = size
        self.size = size
        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size, size), size)
        self.rect = self.image.get_rect(center=position)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * speed
        self.position = pygame.math.Vector2(position)
        self.lifetime = lifetime
        self.original_lifetime = lifetime
        self.color = color

    def update(self):
        """Update the particle's position, size, and transparency."""
        self.position += self.velocity
        self.rect.center = self.position
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
