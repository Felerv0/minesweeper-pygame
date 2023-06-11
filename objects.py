import pygame
from settings import sprites


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], sprite, *groups):
        super().__init__(*groups)
        self.image = sprite
        self.rect = self.image.get_rect(topleft=pos)

    def set_sprite(self, sprite):
        self.image = sprite


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], sprite, *groups):
        super().__init__(*groups)
        self.image = sprite
        self.rect = self.image.get_rect(topleft=pos)
        self.is_hovered = False

    def hover(self):
        self.is_hovered = True
        self.image = sprites['face_smile_pressed']

    def unhover(self):
        self.is_hovered = False
        self.image = sprites['face_smile']

    def ooh(self):
        self.is_hovered = False
        self.image = sprites['face_ooh']

    def loss(self):
        self.image = sprites['face_lose']

    def win(self):
        self.image = sprites['face_win']


class CellButton(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], *groups):
        super().__init__(*groups)
        self.image = sprites['blank']
        self.rect = self.image.get_rect(topleft=pos)
        self.is_hovered = False
        self.opened = False
        self.flagged = False

    def flag(self):
        if not self.opened:
            if self.flagged:
                self.flagged = False
                self.image = sprites['blank']
            else:
                self.is_hovered = False
                self.flagged = True
                self.image = sprites['flagged']

    def hover(self):
        if not self.opened and not self.flagged:
            self.image = sprites['tile0']
            self.is_hovered = True

    def unhover(self):
        if self.is_hovered and not self.opened:
            self.image = sprites['blank']
            self.is_hovered = False

    def pressed(self, n):
        if not self.flagged and not self.opened:
            self.image = sprites[f'tile{n}']
            self.is_hovered = False
            self.flagged = False
            self.opened = True

    def bombed(self, n):
        self.opened = True
        if n == -1 and not self.flagged:
            self.image = sprites['mine']
        elif n != -1 and self.flagged:
            self.image = sprites['mine_crossed']