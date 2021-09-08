import sys

import pygame
import pygame.freetype
from pygame.locals import *

import main as backend


pygame.init()
pygame.font.init

pygame.display.set_caption("XerPassMan")
clock = pygame.time.Clock()
WINDOW_SIZE = (400,225)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300, 200))
target_fps = 60
MONOSPACE = pygame.freetype.Font("ubuntu.ttf", 24)

def main():
    while True:
        display.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                pass
            if event.type == KEYUP:
                pass

        text_surface, rect = MONOSPACE.render("Hello World!", (0, 0, 0))
        display.blit(text_surface, (20, 125))
        MONOSPACE.render_to(display, (20, 175), "Hello World!", (0, 0, 0))
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(target_fps)

def main_menu():
    quit = False
    while True:
        display.fill((146,244,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                pass
            if event.type == KEYUP:
                pass
        if quit: return
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(target_fps)

if __name__ == "__main__":
    main()






while True:
    screen.fill((255,255,255))
    text_surface, rect = MONOSPACE.render("Hello World!", (0, 0, 0))
    screen.blit(text_surface, (20, 125))
    MONOSPACE.render_to(screen, (20, 175), "Hello World!", (0, 0, 0))
    pygame.display.flip()
pygame.quit()
