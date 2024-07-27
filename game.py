import pygame
import random
from player import Player
from asteroid import Asteroid
from explosion import Explosion
from ufo import UFO
from ufo_bullet import UFOBullet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.level = 1
        self.num_asteroids = 4  # Start with 4 big asteroids
        self.asteroids = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()  # Add group for UFO bullets
        self.all_sprites = pygame.sprite.Group(self.player)
        self.explosions = pygame.sprite.Group()
        self.spawn_asteroids()
        
        self.score = 0
        self.highscore = 0
        self.font = pygame.font.Font("assets/fonts/Layn.ttf", 16)  # Load custom font

        self.ufo_timer = 0
        self.ufo_interval = 5 * 60  # UFO appears every 5 seconds at 60 FPS
    
    def spawn_asteroids(self):
        for _ in range(self.num_asteroids):
            asteroid = Asteroid(size=60)
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)

    def spawn_ufo(self):
        if len(self.ufos) == 0:  # Ensure only one UFO at a time
            size = UFO.BIG_SIZE if random.random() < 0.7 else UFO.SMALL_SIZE  # 70% chance for big UFO
            ufo = UFO(size)
            self.ufos.add(ufo)
            self.all_sprites.add(ufo)
            print(f"Spawned UFO of size {size}")  # Debugging statement
    
    def update(self):
        self.all_sprites.update()
        self.player.bullets.update()
        self.ufo_bullets.update()
        self.explosions.update()
        self.ufos.update()
        self.handle_collisions()
        self.handle_ufo_fire()
        
        self.ufo_timer += 1
        if self.ufo_timer >= self.ufo_interval and len(self.ufos) == 0:
            self.spawn_ufo()
            self.ufo_timer = 0
    
    def draw(self):
        self.screen.fill(WHITE)  # Change background to white
        self.all_sprites.draw(self.screen)
        self.player.bullets.draw(self.screen)
        self.ufo_bullets.draw(self.screen)
        self.explosions.draw(self.screen)
        
        # Display the score, highscore, and lives
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)  # Change text color to black
        highscore_text = self.font.render(f"Highscore: {self.highscore}", True, BLACK)  # Change text color to black
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, BLACK)  # Change text color to black
        self.screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
        self.screen.blit(highscore_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
    
    def handle_collisions(self):
        # Use masks for precise collision detection
        hits = pygame.sprite.groupcollide(self.player.bullets, self.asteroids, True, True, pygame.sprite.collide_mask)
        for bullet, hit_asteroids in hits.items():
            for asteroid in hit_asteroids:
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
        
        ufo_hits = pygame.sprite.groupcollide(self.player.bullets, self.ufos, True, True, pygame.sprite.collide_mask)
        for bullet, hit_ufos in ufo_hits.items():
            for ufo in hit_ufos:
                self.score += ufo.points
                explosion = Explosion(ufo.rect.center)
                self.explosions.add(explosion)
                self.all_sprites.add(explosion)
                self.ufo_timer = 0  # Reset the timer to spawn a new UFO after the current one is destroyed
        
        # Check collisions between UFO bullets and player
        if pygame.sprite.spritecollideany(self.player, self.ufo_bullets, pygame.sprite.collide_mask):
            if self.score > self.highscore:
                self.highscore = self.score
            
            explosion = Explosion(self.player.rect.center)
            self.explosions.add(explosion)
            self.all_sprites.add(explosion)
            
            self.score = 0
            self.player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.player.velocity = pygame.math.Vector2(0, 0)

        if not self.asteroids:  # Check if all asteroids are cleared
            self.level += 1
            self.num_asteroids += 1  # Increase the number of asteroids for the next level
            self.spawn_asteroids()
        
        # Use masks for precise collision detection between player and asteroids
        if pygame.sprite.spritecollide(self.player, self.asteroids, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(self.player, self.ufos, False, pygame.sprite.collide_mask):
            # Handle player collision (reset player position and play explosion)
            if self.score > self.highscore:
                self.highscore = self.score
            
            explosion = Explosion(self.player.rect.center)
            self.explosions.add(explosion)
            self.all_sprites.add(explosion)
            
            self.score = 0
            self.player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.player.velocity = pygame.math.Vector2(0, 0)

    def handle_ufo_fire(self):
        for ufo in self.ufos:
            bullet = ufo.fire(self.player.rect.center)
            if bullet:
                self.all_sprites.add(bullet)
                self.ufo_bullets.add(bullet)
