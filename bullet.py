import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT  # Ensure you import these constants

class Bullet(pygame.sprite.Sprite):
    COLOR = (255, 165, 0)
    SPEED = 10

    def __init__(self, position, angle):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)
        radians = math.radians(angle)
        self.velocity = pygame.math.Vector2(math.sin(radians), -math.cos(radians)) * self.SPEED
    
    def update(self):
        self.rect.center += self.velocity
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
