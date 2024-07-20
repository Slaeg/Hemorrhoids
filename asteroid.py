import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, size=60, speed=None, split_count=0):
        super().__init__()
        self.size = size
        self.split_count = split_count
        
        if self.size == 60:
            self.image = pygame.image.load("assets/images/asteroid_large.png").convert_alpha()
        elif self.size == 30:
            self.image = pygame.image.load("assets/images/asteroid_medium.png").convert_alpha()
        elif self.size == 15:
            self.image = pygame.image.load("assets/images/asteroid_small.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

        if x is None and y is None:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        else:
            self.rect.x = x
            self.rect.y = y
        
        self.speed = speed if speed is not None else random.uniform(0.5, 1.5)
        self.velocity = pygame.math.Vector2(random.choice([-1, 1]) * self.speed, random.choice([-1, 1]) * self.speed)
    
    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

    def split(self):
        if self.size > 15 and self.split_count < 2:  # Minimum size and max split count check
            new_size = self.size // 2
            new_speed = self.speed + 1
            child1 = Asteroid(self.rect.x, self.rect.y, new_size, new_speed, self.split_count + 1)
            child2 = Asteroid(self.rect.x, self.rect.y, new_size, new_speed, self.split_count + 1)
            return [child1, child2]
        else:
            return []
