import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, FPS
from utils import load_sound, play_sound
from asteroid import Asteroid
from ufo import UFO
from ufo_bullet import UFOBullet
from particle import Particle
from player import Player

class Game:
    instance = None

    def __new__(cls, screen):
        if cls.instance is None:
            cls.instance = super(Game, cls).__new__(cls)
            cls.instance.initialize(screen)
        return cls.instance

    def initialize(self, screen):
        """Initialize game state and resources."""
        self.screen = screen
        self.highscore = 0
        self.font_filename = "assets/fonts/Layn.ttf"
        self.font = pygame.font.Font(self.font_filename, 16)
        self.sounds = {
            'shoot': load_sound('assets/sounds/shoot.wav'),
            'explosion': load_sound('assets/sounds/explosion.wav'),
            'ufo': load_sound('assets/sounds/ufo.wav'),
            'ufo_shoot': load_sound('assets/sounds/ufo_shoot.wav'),
        }
        self.state = "TITLE"
        self.game_over_delay = 2 * FPS  # 2 seconds delay at 60 FPS
        self.game_over_timer = 0
        self.background = pygame.image.load("assets/images/background1.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.initialize_game()

    def initialize_game(self):
        """Set up initial game state."""
        self.player = Player()
        self.player.start_invulnerability()
        self.level = 1
        self.num_asteroids = 4
        self.asteroids = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.particles = pygame.sprite.Group()
        self.spawn_asteroids()
        
        self.score = 0
        self.ufo_timer = 0
        self.ufo_interval = 10 * 60  # UFO appears every 10 seconds at 60 FPS
        self.game_over = False

    def handle_events(self):
        """Process game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.state == "TITLE" and event.key == pygame.K_SPACE:
                    self.state = "PLAYING"
                    self.initialize_game()
                elif self.state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        self.player_shoot()
                elif self.state == "GAME_OVER" and event.key == pygame.K_r:
                    self.reset_game()
                    self.state = "PLAYING"
        return True

    def reset_game(self):
        """Reset the game state for a new game."""
        self.highscore = max(self.score, self.highscore)
        self.initialize_game()

    def update(self):
        """Update game state."""
        if self.state == "PLAYING":
            if not self.game_over:
                self.all_sprites.update()
                self.player.bullets.update()
                self.ufo_bullets.update()
                self.particles.update()
                self.ufos.update()
                self.handle_collisions()
                self.handle_ufo_fire()
                
                self.ufo_timer += 1
                if self.ufo_timer >= self.ufo_interval and len(self.ufos) == 0:
                    self.spawn_ufo()
                    self.ufo_timer = 0
            else:
                self.particles.update()
                
                self.game_over_timer += 1
                if self.game_over_timer >= self.game_over_delay:
                    self.state = "GAME_OVER"

    def draw(self):
        """Render the game state to the screen."""
        if self.state == "TITLE":
            self.screen.fill(WHITE)
            self.draw_title_screen()
        elif self.state == "PLAYING" or (self.game_over and self.game_over_timer < self.game_over_delay):
            self.screen.blit(self.background, (0, 0))
            for sprite in self.all_sprites:
                if sprite != self.player:
                    self.screen.blit(sprite.image, sprite.rect)
            if not self.game_over:
                self.player.draw(self.screen)
            self.player.bullets.draw(self.screen)
            self.ufo_bullets.draw(self.screen)
            self.particles.draw(self.screen)
            
            self.draw_hud()
        elif self.state == "GAME_OVER":
            self.screen.fill(WHITE)
            self.draw_game_over()
        
        pygame.display.flip()

    
    def draw_title_screen(self):
        """Draw the title screen."""
        title_font = pygame.font.Font(self.font_filename, 64)
        title_text = title_font.render("Haemorrhoids", True, BLACK)
        start_text = self.font.render("Press SPACE to start", True, BLACK)
        controls_text1 = self.font.render("Controls:", True, BLACK)
        controls_text2 = self.font.render("Arrow keys to move", True, BLACK)
        controls_text3 = self.font.render("SPACE to shoot", True, BLACK)

        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        controls_rect1 = controls_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4 - 60))
        controls_rect2 = controls_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4 - 30))
        controls_rect3 = controls_text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(start_text, start_rect)
        self.screen.blit(controls_text1, controls_rect1)
        self.screen.blit(controls_text2, controls_rect2)
        self.screen.blit(controls_text3, controls_rect3)

    def draw_game_over(self):
        """Draw the game over screen."""
        self.screen.fill(WHITE)

        game_over_font = pygame.font.Font(self.font_filename, 64)
        game_over_text = game_over_font.render("GAME OVER", True, BLACK)
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        highscore_text = self.font.render(f"Highscore: {self.highscore}", True, BLACK)
        restart_text = self.font.render("Press R to Restart", True, BLACK)

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        highscore_rect = highscore_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(highscore_text, highscore_rect)
        self.screen.blit(restart_text, restart_rect)

    def draw_hud(self):
        """Draw the heads-up display (score, highscore, lives)."""
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        highscore_text = self.font.render(f"Highscore: {self.highscore}", True, BLACK)
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, BLACK)
        self.screen.blit(score_text, (SCREEN_WIDTH - 250, 10))
        self.screen.blit(highscore_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))

    def handle_collisions(self):
        """Handle collisions between game objects."""
        self.handle_bullet_asteroid_collisions()
        self.handle_bullet_ufo_collisions()
        self.handle_ufo_bullet_player_collision()
        self.handle_player_object_collisions()

        if not self.asteroids:
            self.level_up()

    def handle_bullet_asteroid_collisions(self):
        """Handle collisions between player bullets and asteroids."""
        hits = pygame.sprite.groupcollide(self.player.bullets, self.asteroids, True, True, pygame.sprite.collide_mask)
        for bullet, hit_asteroids in hits.items():
            for asteroid in hit_asteroids:
                self.asteroid_explosion(asteroid)
                new_asteroids = asteroid.split()
                self.asteroids.add(new_asteroids)
                self.all_sprites.add(new_asteroids)
                self.update_score(asteroid.size)

    def handle_bullet_ufo_collisions(self):
        """Handle collisions between player bullets and UFOs."""
        ufo_hits = pygame.sprite.groupcollide(self.player.bullets, self.ufos, True, True, pygame.sprite.collide_mask)
        for bullet, hit_ufos in ufo_hits.items():
            for ufo in hit_ufos:
                self.score += ufo.points
                self.ufo_explosion(ufo)
                self.ufo_timer = 0

    def handle_ufo_bullet_player_collision(self):
        """Handle collisions between UFO bullets and the player."""
        if pygame.sprite.spritecollideany(self.player, self.ufo_bullets, pygame.sprite.collide_mask):
            self.player_hit()

    def handle_player_object_collisions(self):
        """Handle collisions between the player and asteroids or UFOs."""
        if (pygame.sprite.spritecollide(self.player, self.asteroids, False, pygame.sprite.collide_mask) or 
            pygame.sprite.spritecollide(self.player, self.ufos, False, pygame.sprite.collide_mask)):
            self.player_hit()

    def level_up(self):
        """Increase difficulty and spawn new asteroids."""
        self.level += 1
        self.num_asteroids += 1
        self.spawn_asteroids()

    def update_score(self, asteroid_size):
        """Update the score based on the size of the destroyed asteroid."""
        if asteroid_size == 60:
            self.score += 20
        elif asteroid_size == 30:
            self.score += 50
        elif asteroid_size == 15:
            self.score += 100

    def player_hit(self):
        """Handle player being hit by an asteroid, UFO, or UFO bullet."""
        if not self.player.invulnerable:
            self.player.hit()
            if self.player.death_position:
                self.create_explosion_particles(self.player.death_position)
                self.player.death_position = None
            play_sound(self.sounds['explosion'])
            
            self.highscore = max(self.score, self.highscore)
            
            if self.player.lives <= 0:
                self.game_over = True
                self.game_over_timer = 0
                self.player.kill()

    def handle_ufo_fire(self):
        """Handle UFO firing bullets."""
        for ufo in self.ufos:
            bullet = ufo.fire(self.player.rect.center)
            if bullet:
                self.all_sprites.add(bullet)
                self.ufo_bullets.add(bullet)

    def player_shoot(self):
        """Handle player shooting."""
        if not self.game_over:
            play_sound(self.sounds['shoot'])
            self.player.fire()

    def asteroid_explosion(self, asteroid):
        """Create explosion effect for destroyed asteroid."""
        self.create_explosion_particles(asteroid.rect.center)
        play_sound(self.sounds['explosion'])

    def ufo_explosion(self, ufo):
        """Create explosion effect for destroyed UFO."""
        self.create_explosion_particles(ufo.rect.center)
        play_sound(self.sounds['explosion'])

    def create_explosion_particles(self, position):
        """Create particle effect for explosions."""
        colors = [(255, 165, 0), (255, 69, 0), (255, 215, 0)]
        num_particles = random.randint(30, 50)
        
        for _ in range(num_particles):
            color = random.choice(colors)
            size = random.randint(2, 5)
            speed = random.uniform(1, 4)
            lifetime = random.randint(30, 90)
            
            particle = Particle(position, color, size, speed, lifetime)
            self.particles.add(particle)
            self.all_sprites.add(particle)

        central_particle = Particle(position, (255, 255, 255), 8, 0.5, 45)
        self.particles.add(central_particle)
        self.all_sprites.add(central_particle)

    def spawn_asteroids(self):
        """Spawn asteroids at the start of a level."""
        for _ in range(self.num_asteroids):
            asteroid = Asteroid(size=60)
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)

    def spawn_ufo(self):
        """Spawn a UFO."""
        if len(self.ufos) == 0:
            size = UFO.BIG_SIZE if random.random() < 0.7 else UFO.SMALL_SIZE
            ufo = UFO(size, self.sounds['ufo_shoot'])
            self.ufos.add(ufo)
            self.all_sprites.add(ufo)
            play_sound(self.sounds['ufo'])

    def add_particle(self, particle):
        """Add a particle to the game."""
        self.particles.add(particle)