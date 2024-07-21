import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (25, 25))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.rotation_speed = 5
        self.velocity = pygame.math.Vector2(0, 0)
        self.bullets = pygame.sprite.Group()
        self.lives = float('inf')  # Infinite lives for development

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_UP]:
            self.thrust()
        
        self.velocity *= 0.99  # Damping to slow down gradually
        self.rect.center += self.velocity

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        
        self.wrap_around_screen()

    def thrust(self):
        radians = math.radians(self.angle)
        self.velocity.x += 0.5 * math.sin(radians)
        self.velocity.y -= 0.5 * math.cos(radians)

    def fire(self):
        bullet = Bullet(self.rect.center, self.angle)
        self.bullets.add(bullet)

    def wrap_around_screen(self):
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
