import pygame
from player import Player
from asteroid import Asteroid
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.level = 1
        self.num_asteroids = 4  # Start with 4 big asteroids
        self.asteroids = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_asteroids()
        
        self.score = 0
        self.highscore = 0
        self.font = pygame.font.Font(None, 36)
    
    def spawn_asteroids(self):
        for _ in range(self.num_asteroids):
            asteroid = Asteroid(size=60)
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
        
        # Display the score, highscore, and lives
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        highscore_text = self.font.render(f"Highscore: {self.highscore}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
        self.screen.blit(highscore_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
    
    def handle_collisions(self):
        hits = pygame.sprite.groupcollide(self.player.bullets, self.asteroids, True, True)
        if hits:
            for hit in hits:
                for asteroid in hits[hit]:
                    new_asteroids = asteroid.split()
                    self.asteroids.add(new_asteroids)
                    self.all_sprites.add(new_asteroids)
                    
                    # Update score based on asteroid size
                    if asteroid.size == 60:
                        self.score += 20
                    elif asteroid.size == 30:
                        self.score += 50
                    elif asteroid.size == 15:
                        self.score += 100
        
        if not self.asteroids:  # Check if all asteroids are cleared
            self.level += 1
            self.num_asteroids += 1  # Increase the number of asteroids for the next level
            self.spawn_asteroids()
        
        if pygame.sprite.spritecollideany(self.player, self.asteroids):
            # Handle player collision (reset player position)
            if self.score > self.highscore:
                self.highscore = self.score
            self.score = 0
            self.player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.player.velocity = pygame.math.Vector2(0, 0)
