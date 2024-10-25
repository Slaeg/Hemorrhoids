import pygame
import random
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ufo_bullet import UFOBullet

class UFO(pygame.sprite.Sprite):
    """
    A class representing a UFO in the game.

    Attributes:
        BIG_SIZE (int): The size of a big UFO.
        SMALL_SIZE (int): The size of a small UFO.
        BIG_SPEED (float): The speed of a big UFO.
        SMALL_SPEED (float): The speed of a small UFO.
        BIG_POINTS (int): The points awarded for destroying a big UFO.
        SMALL_POINTS (int): The points awarded for destroying a small UFO.
        size (int): The size of the UFO.
        image (pygame.Surface): The image of the UFO.
        rect (pygame.Rect): The rectangle representing the UFO's position.
        mask (pygame.Mask): The mask for collision detection.
        speed (float): The speed of the UFO.
        points (int): The points awarded for destroying the UFO.
        fire_probability (float): The probability of the UFO firing a bullet.
        velocity (pygame.math.Vector2): The velocity vector of the UFO.
        direction_changed (bool): Whether the UFO has changed direction.
        shoot_sound (pygame.mixer.Sound): The sound played when the UFO fires a bullet.
    """
    BIG_SIZE = 40
    SMALL_SIZE = 20
    BIG_SPEED = 1.5
    SMALL_SPEED = 2.5
    BIG_POINTS = 500
    SMALL_POINTS = 1000

    def __init__(self, size, shoot_sound):
        """
        Initialize a UFO.

        Args:
            size (int): The size of the UFO.
            shoot_sound (pygame.mixer.Sound): The sound played when the UFO fires a bullet.
        """
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
        
        self.start_side = random.choice(['left', 'right'])
        self.rect.x = -self.rect.width if self.start_side == 'left' else SCREEN_WIDTH
        self.velocity = pygame.math.Vector2(self.speed if self.start_side == 'left' else -self.speed, 0)
        
        self.direction_changed = False
        self.shoot_sound = shoot_sound
    
    def update(self):
        """
        Update the UFO's position and handle screen wrapping.
        """
        self.rect.x += self.velocity.x
        if not self.direction_changed and ((self.start_side == 'left' and self.rect.centerx > SCREEN_WIDTH // 2) or (self.start_side == 'right' and self.rect.centerx < SCREEN_WIDTH // 2)):
            self.velocity.y = random.choice([-1, 1]) * self.speed
            self.direction_changed = True
        if self.direction_changed and ((self.start_side == 'left' and self.rect.centerx > SCREEN_WIDTH) or (self.start_side == 'right' and self.rect.centerx < 0)):
            self.velocity.y = 0

        # Screen wrapping logic
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0

        self.rect.y += self.velocity.y  # Add vertical movement
        if self.rect.top < 0:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0

    def fire(self, player_pos):
        """
        Fire a bullet at the player.

        Args:
            player_pos (tuple): The position of the player.

        Returns:
            UFOBullet: The fired bullet, or None if the UFO does not fire.
        """
        if random.random() < self.fire_probability:
            if self.shoot_sound:
                self.shoot_sound.play()
            return UFOBullet(self.rect.center, self.get_angle_to_player(player_pos))
        return None

    def get_angle_to_player(self, player_pos):
        """
        Calculate the angle to the player.

        Args:
            player_pos (tuple): The position of the player.

        Returns:
            float: The angle to the player in degrees.
        """
        return (pygame.Vector2(player_pos) - pygame.Vector2(self.rect.center)).angle_to(pygame.Vector2(1, 0))
