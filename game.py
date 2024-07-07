import pygame
from player import Player
from asteroid import Asteroid
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.asteroids = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_asteroids()
    
    def spawn_asteroids(self):
        for _ in range(5):
            asteroid = Asteroid()
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)
    
    def update(self):
        self.all_sprites.update()
        self.player.bullets.update()
        self.handle_collisions()
    
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.player.bullets.draw(self.screen)
    
    def handle_collisions(self):
        hits = pygame.sprite.groupcollide(self.player.bullets, self.asteroids, True, True)
        if hits:
            for hit in hits:
                # Split the asteroid into smaller ones
                for asteroid in hits[hit]:
                    new_asteroids = asteroid.split()
                    self.asteroids.add(new_asteroids)
                    self.all_sprites.add(new_asteroids)
        
        if pygame.sprite.spritecollideany(self.player, self.asteroids):
            # Handle player collision
            pass
