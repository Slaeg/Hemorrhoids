import pygame

class Explosion(pygame.sprite.Sprite):
    FRAMES = 10
    COLOR = (255, 0, 0)

    def __init__(self, center):
        super().__init__()
        self.center = center
        self.current_frame = 0
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
    
    def update(self):
        if self.current_frame < self.FRAMES:
            radius = (self.current_frame + 1) * 5
            alpha = max(0, 255 - (self.current_frame * 25))
            self.image.fill((0, 0, 0, 0))
            pygame.draw.circle(self.image, (*self.COLOR[:3], alpha), (self.rect.width // 2, self.rect.height // 2), radius)
            self.current_frame += 1
        else:
            self.kill()
