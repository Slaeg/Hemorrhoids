import pygame

def play_music(file, loops=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops)

def stop_music():
    pygame.mixer.music.stop()

def load_sound(file):
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error as e:
        print(f"Unable to load sound file: {file}")
        print(f"Error: {e}")
        return None

def play_sound(sound):
    print(f"play_sound called with sound object: {sound}")  # Debug print
    if sound:
        sound.play()
    else:
        print("Warning: Attempted to play a sound that wasn't loaded")