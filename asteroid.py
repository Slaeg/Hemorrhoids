import pygame
import random
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Asteroid(pygame.sprite.Sprite):
    """A class representing an asteroid in the game."""
    
    LARGE_SIZE = 60
    MEDIUM_SIZE = 30
    SMALL_SIZE = 15

    def __init__(self, x=None, y=None, size=LARGE_SIZE, speed=None):
        """
        Initialize an asteroid.

        Args:
            x (int, optional): The x-coordinate of the asteroid. Defaults to None.
            y (int, optional): The y-coordinate of the asteroid. Defaults to None.
            size (int, optional): The size of the asteroid. Defaults to LARGE_SIZE.
            speed (float, optional): The speed of the asteroid. Defaults to None.
        """
        super().__init__()
        self.size = size
        
        if self.size == self.LARGE_SIZE:
            self.image = pygame.image.load("assets/images/asteroid_large.png").convert_alpha()
            self.base_speed = 1
        elif self.size == self.MEDIUM_SIZE:
            self.image = pygame.image.load("assets/images/asteroid_medium.png").convert_alpha()
            self.base_speed = 1.5
        elif self.size == self.SMALL_SIZE:
            self.image = pygame.image.load("assets/images/asteroid_small.png").convert_alpha()
            self.base_speed = 2

        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        if x is None and y is None:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        else:
            self.rect.x = x
            self.rect.y = y
        
        self.speed = speed if speed is not None else self.base_speed * random.uniform(0.8, 1.2)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * self.speed

    def update(self):
        """Update the asteroid's position."""
        movement = self.velocity.normalize() * self.speed
        self.rect.x += movement.x
        self.rect.y += movement.y
        self.wrap_around_screen()

    def wrap_around_screen(self):
        """Wrap the asteroid around the screen edges."""
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

    def split(self):
        """
        Split the asteroid into smaller pieces.

        Returns:
            list: A list of new smaller asteroids.
        """
        if self.size > self.SMALL_SIZE:
            new_size = self.size // 2
            new_speed = self.speed * 1.9  # Increase speed
            angle1 = random.uniform(0, 2 * math.pi)
            angle2 = angle1 + math.pi  # Opposite direction
            
            child1 = Asteroid(self.rect.centerx, self.rect.centery, new_size, new_speed)
            child2 = Asteroid(self.rect.centerx, self.rect.centery, new_size, new_speed)
            
            child1.velocity = pygame.math.Vector2(math.cos(angle1), math.sin(angle1)) * new_speed
            child2.velocity = pygame.math.Vector2(math.cos(angle2), math.sin(angle2)) * new_speed
            
            return [child1, child2]
        else:
            return []
