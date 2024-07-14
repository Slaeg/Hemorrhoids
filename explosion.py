import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.center = center
        self.frames = 10  # Number of frames for the explosion animation
        self.current_frame = 0
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
    
    def update(self):
        if self.current_frame < self.frames:
            radius = (self.current_frame + 1) * 5  # Increase the radius over time
            color = (255, 0, 0, max(0, 255 - (self.current_frame * 25)))  # Fade out over time
            self.image.fill((0, 0, 0, 0))  # Clear the image
            pygame.draw.circle(self.image, color, (self.rect.width // 2, self.rect.height // 2), radius)
            self.current_frame += 1
        else:
            self.kill()  # Remove the explosion after the last frame
