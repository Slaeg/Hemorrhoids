import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game
from utils import play_music

def main():
    try:
        pygame.init()
        pygame.mixer.init()
        play_music("assets/sounds/music.mp3")

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Haemorrhoids")
        clock = pygame.time.Clock()
        game = Game(screen)
        running = True

        while running:
            running = game.handle_events()
            game.update()
            game.draw()

            clock.tick(FPS)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()