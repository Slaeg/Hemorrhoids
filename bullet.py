import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT  # Ensure you import these constants

class Bullet(pygame.sprite.Sprite):
    """
    A class representing a bullet in the game.

    Attributes:
        COLOR (tuple): The color of the bullet.
        SPEED (int): The speed of the bullet.
        image (pygame.Surface): The image of the bullet.
        rect (pygame.Rect): The rectangle representing the bullet's position.
        mask (pygame.Mask): The mask for collision detection.
        velocity (pygame.math.Vector2): The velocity vector of the bullet.
    """
    COLOR = (255, 165, 0)
    SPEED = 10

    def __init__(self, position, angle):
        """
        Initialize a bullet.

        Args:
            position (tuple): The initial position of the bullet.
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
        """
        Update the bullet's position and handle screen wrapping.
        """
        self.rect.center += self.velocity
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
