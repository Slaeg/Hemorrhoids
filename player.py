import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    """A class representing the player in the game."""

    def __init__(self):
        """
        Initialize the player.

        Args:
            None
        """
        super().__init__()
        self.original_image = pygame.image.load("assets/images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (25, 25))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.rotation_speed = 5
        self.velocity = pygame.math.Vector2(0, 0)
        self.bullets = pygame.sprite.Group()
        self.lives = 3
        self.respawn_timer = 0
        self.respawn_delay = 180  # 3 seconds at 60 FPS
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 180  # 3 seconds at 60 FPS
        self.flash_interval = 5  # Flash every 1/4 second at 60 FPS
        self.visible = True
        self.death_position = None

    def update(self):
        """Update the player's state."""
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            return

        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.visible = True
            else:
                # Toggle visibility every flash_interval frames
                if self.invulnerable_timer % self.flash_interval == 0:
                    self.visible = not self.visible

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

    def hit(self):
        """Handle the player being hit by an asteroid, UFO, or UFO bullet."""
        if not self.invulnerable:
            self.lives -= 1
            self.death_position = self.rect.center  # Store the death position
            if self.lives > 0:
                self.respawn()
            else:
                self.kill()

    def respawn(self):
        """Respawn the player at the center of the screen."""
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = pygame.math.Vector2(0, 0)
        self.start_invulnerability()

    def start_invulnerability(self):
        """Start the player's invulnerability period."""
        self.invulnerable = True
        self.invulnerable_timer = self.invulnerable_duration
        self.visible = True

    def thrust(self):
        """Apply thrust to the player."""
        radians = math.radians(self.angle)
        self.velocity.x += 0.5 * math.sin(radians)
        self.velocity.y -= 0.5 * math.cos(radians)

    def fire(self):
        """Fire a bullet from the player's position."""
        bullet = Bullet(self.rect.center, self.angle)
        self.bullets.add(bullet)

    def wrap_around_screen(self):
        """Wrap the player around the screen edges."""
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

    def draw(self, surface):
        """Draw the player on the given surface."""
        if self.visible:
            surface.blit(self.image, self.rect)