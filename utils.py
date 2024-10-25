import pygame

def play_music(file, loops=-1):
    """
    Play background music.

    Args:
        file (str): The file path of the music to play.
        loops (int, optional): The number of times to repeat the music. Defaults to -1 (infinite loop).
    """
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops)

def stop_music():
    """
    Stop the background music.
    """
    pygame.mixer.music.stop()

def load_sound(file):
    """
    Load a sound effect.

    Args:
        file (str): The file path of the sound effect to load.

    Returns:
        pygame.mixer.Sound: The loaded sound effect, or None if loading failed.
    """
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error as e:
        print(f"Unable to load sound file: {file}")
        print(f"Error: {e}")
        return None

def play_sound(sound):
    """
    Play a sound effect.

    Args:
        sound (pygame.mixer.Sound): The sound effect to play.
    """
    if sound:
        sound.play()
    else:
        print("Warning: Attempted to play a sound that wasn't loaded")
