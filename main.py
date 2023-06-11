import sys
import pygame

from game import Game
from settings import *


pygame.init()

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(pygame.image.load('assets/images/icon.ico'))
clock = pygame.time.Clock()
game = Game(screen, game_params)


def run_game():
    while True:
        getInput.update()
        if getInput.is_terminated():
            pygame.quit()
            sys.exit()
        game.update()
        clock.tick(FPS)


run_game()