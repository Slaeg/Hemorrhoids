import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
from utils import load_sound, play_sound
from asteroid import Asteroid
from explosion import Explosion
from ufo import UFO
from ufo_bullet import UFOBullet
from particle import Particle

class Game:
    instance = None

    def __init__(self, screen):
        if Game.instance is None:
            Game.instance = self
        self.screen = screen
        self.highscore = 0
        self.font = pygame.font.Font("assets/fonts/Layn.ttf", 16)  # Load custom font
        self.sounds = {
            'shoot': load_sound('assets/sounds/shoot.wav'),
            'explosion': load_sound('assets/sounds/explosion.wav'),
            'ufo': load_sound('assets/sounds/ufo.wav'),
        }
        self.initialize_game()

    def initialize_game(self):
        from player import Player  # Import Player here to avoid circular import
        self.player = Player()
        self.level = 1
        self.num_asteroids = 4  # Start with 4 big asteroids
        self.asteroids = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.explosions = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.spawn_asteroids()
        
        self.score = 0
        self.ufo_timer = 0
        self.ufo_interval = 5 * 60  # UFO appears every 5 seconds at 60 FPS
        self.game_over = False

    def reset_game(self):
        print("Resetting game")  # Debug print
        self.highscore = max(self.score, self.highscore)  # Update highscore before resetting
        self.initialize_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player_shoot()
                elif event.key == pygame.K_r and self.game_over:
                    print("R key pressed, resetting game")  # Debug print
                    self.reset_game()
        return True

    def update(self):
        if not self.game_over:
            self.all_sprites.update()
            self.player.bullets.update()
            self.ufo_bullets.update()
            self.explosions.update()
            self.ufos.update()
            self.particles.update()
            self.handle_collisions()
            self.handle_ufo_fire()
            
            self.ufo_timer += 1
            if self.ufo_timer >= self.ufo_interval and len(self.ufos) == 0:
                self.spawn_ufo()
                self.ufo_timer = 0

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.player.bullets.draw(self.screen)
        self.ufo_bullets.draw(self.screen)
        self.explosions.draw(self.screen)
        self.particles.draw(self.screen)
        
        if self.game_over:
            self.draw_game_over()
        
        # Display the score, highscore, and lives
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        highscore_text = self.font.render(f"Highscore: {self.highscore}", True, BLACK)
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, BLACK)
        self.screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
        self.screen.blit(highscore_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))

    def draw_game_over(self):
        game_over_text = self.font.render("GAME OVER", True, BLACK)
        restart_text = self.font.render("Press R to Restart", True, BLACK)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    def handle_collisions(self):
        # Player bullets with asteroids
        hits = pygame.sprite.groupcollide(self.player.bullets, self.asteroids, True, True, pygame.sprite.collide_mask)
        for bullet, hit_asteroids in hits.items():
            for asteroid in hit_asteroids:
                self.asteroid_explosion(asteroid)
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
        
        # Player bullets with UFOs
        ufo_hits = pygame.sprite.groupcollide(self.player.bullets, self.ufos, True, True, pygame.sprite.collide_mask)
        for bullet, hit_ufos in ufo_hits.items():
            for ufo in hit_ufos:
                self.score += ufo.points
                self.ufo_explosion(ufo)
                self.ufo_timer = 0  # Reset the timer to spawn a new UFO after the current one is destroyed
        
        # UFO bullets with player
        if pygame.sprite.spritecollideany(self.player, self.ufo_bullets, pygame.sprite.collide_mask):
            self.player_hit()

        # Player with asteroids or UFOs
        if (pygame.sprite.spritecollide(self.player, self.asteroids, False, pygame.sprite.collide_mask) or 
            pygame.sprite.spritecollide(self.player, self.ufos, False, pygame.sprite.collide_mask)):
            self.player_hit()

        if not self.asteroids:  # Check if all asteroids are cleared
            self.level += 1
            self.num_asteroids += 1  # Increase the number of asteroids for the next level
            self.spawn_asteroids()

    def player_hit(self):
        if not self.player.invulnerable:
            self.player.hit()
            explosion = Explosion(self.player.rect.center)
            self.explosions.add(explosion)
            self.all_sprites.add(explosion)
            play_sound(self.sounds['explosion'])
            
            if self.score > self.highscore:
                self.highscore = self.score
            
            if self.player.lives > 0:
                self.player.respawn()
            else:
                print("Game over")  # Debug print
                self.game_over = True

    def handle_ufo_fire(self):
        for ufo in self.ufos:
            bullet = ufo.fire(self.player.rect.center)
            if bullet:
                self.all_sprites.add(bullet)
                self.ufo_bullets.add(bullet)

    def player_shoot(self):
        print("player_shoot method called")  # Debug print
        if self.sounds['shoot']:
            print("Attempting to play shoot sound")  # Debug print
            play_sound(self.sounds['shoot'])
        else:
            print("Warning: Shoot sound not loaded")
        self.player.fire()

    def asteroid_explosion(self, asteroid):
        explosion = Explosion(asteroid.rect.center)
        self.explosions.add(explosion)
        self.all_sprites.add(explosion)
        play_sound(self.sounds['explosion'])
        for _ in range(20):
            particle = Particle(asteroid.rect.center, (150, 150, 150))
            self.particles.add(particle)

    def ufo_explosion(self, ufo):
        explosion = Explosion(ufo.rect.center)
        self.explosions.add(explosion)
        self.all_sprites.add(explosion)
        play_sound(self.sounds['explosion'])
        for _ in range(20):
            particle = Particle(ufo.rect.center, (255, 0, 0))
            self.particles.add(particle)

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
            play_sound(self.sounds['ufo'])

    def add_particle(self, particle):
        self.particles.add(particle)