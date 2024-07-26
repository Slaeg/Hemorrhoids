import pygame
import random
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from bullet import Bullet  # Ensure Bullet is imported

class UFO(pygame.sprite.Sprite):
    BIG_SIZE = 40
    SMALL_SIZE = 20
    BIG_SPEED = 1.5
    SMALL_SPEED = 2.5
    BIG_POINTS = 500
    SMALL_POINTS = 1000

    def __init__(self, size):
        super().__init__()
        self.size = size
        if self.size == self.BIG_SIZE:
            self.image = pygame.image.load("assets/images/ufo_big.png").convert_alpha()
            self.speed = self.BIG_SPEED
            self.points = self.BIG_POINTS
            self.fire_probability = 0.01
        else:
            self.image = pygame.image.load("assets/images/ufo_small.png").convert_alpha()
            self.speed = self.SMALL_SPEED
            self.points = self.SMALL_POINTS
            self.fire_probability = 0.03

        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.rect.x = -self.rect.width if random.choice([True, False]) else SCREEN_WIDTH
        self.velocity = pygame.math.Vector2(self.speed if self.rect.x == -self.rect.width else -self.speed, 0)
    
    def update(self):
        self.rect.x += self.velocity.x
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
    
    def fire(self):
        if random.random() < self.fire_probability:
            return Bullet(self.rect.center, self.get_angle_to_player())
        return None

    def get_angle_to_player(self):
        # This method needs the player's position, so you might need to pass it from the game class
        player_pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Placeholder
        return (player_pos - pygame.Vector2(self.rect.center)).angle_to(pygame.Vector2(1, 0))
