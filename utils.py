import pygame

def play_music(file, loops=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops)

def stop_music():
    pygame.mixer.music.stop()

def load_sound(file):
    return pygame.mixer.Sound(file)

def play_sound(sound):
    sound.play()
