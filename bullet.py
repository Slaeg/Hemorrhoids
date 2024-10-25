import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Bullet(pygame.sprite.Sprite):
    """A class representing a bullet in the game."""
    
    COLOR = (255, 165, 0)
    SPEED = 10

    def __init__(self, position, angle):
        """
        Initialize a bullet.

        Args:
            position (tuple): The (x, y) position of the bullet.
            angle (float): The angle at which the bullet is fired.
        """
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)
        radians = math.radians(angle)
        self.velocity = pygame.math.Vector2(math.sin(radians), -math.cos(radians)) * self.SPEED
    
    def update(self):
        """Update the bullet's position."""
        self.rect.center += self.velocity
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
