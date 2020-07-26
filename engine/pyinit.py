import pygame
pygame.init()

global game_display
global display_mode


def init(resolution, caption, mode):
    global game_display
    global display_mode
    display_mode = mode
    if mode == "fullscreen":
        game_display = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    elif mode == "window":
        game_display = pygame.display.set_mode(resolution)
    pygame.display.set_caption(str(caption))