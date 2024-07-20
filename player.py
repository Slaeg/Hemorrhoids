import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (25, 25))  # Scale to match the existing player size
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, angle):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((0, 0, 0))  # Change bullet color to black
        self.rect = self.image.get_rect(center=position)
        self.speed = 10
        radians = math.radians(angle)
        self.velocity = pygame.math.Vector2(math.sin(radians), -math.cos(radians)) * self.speed
    
    def update(self):
        self.rect.center += self.velocity
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

