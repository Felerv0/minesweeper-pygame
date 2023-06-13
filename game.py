import pygame
from enum import Enum
from random import sample
from objects import Sprite, Button, CellButton
from settings import *


class Game:
    def __init__(self, screen, game_settings):
        self.game_settings = game_settings
        self.game_size = game_settings[0]
        self.screen = screen
        self.setup_game()

    def setup_game(self):
        # game
        # self.game = Minesweeper(*self.game_settings)

        self.touched = False
        self.mines = self.game_settings[1]
        self.flags = self.mines

        # technical
        self.status = GameStatus.playing.value
        self.timer = 0
        self.last = 0, 0

        # interface
        self.ui = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.main_button = pygame.sprite.GroupSingle()
        self.flag_numbers = []
        self.timer_numbers = []
        self.stop_timer()

        Button((screen_width / 2 - BUTTON_SIZE[0] / 2, BORDER_HORIZONTAL_SIZE[1] + 3 * CELL_SIZE[1] / 16),
               sprites['face_smile'], self.ui, self.buttons, self.main_button)
        Sprite((0, 0), sprites['corner_tl'], self.ui)
        Sprite((screen_width - CORNER_SIZE[0], 0), sprites['corner_tr'], self.ui)
        Sprite((0, screen_height - CORNER_SIZE[1]), sprites['corner_bl'], self.ui)
        Sprite((screen_width - CORNER_SIZE[0], screen_height - CORNER_SIZE[1]), sprites['corner_br'], self.ui)
        Sprite((0, BORDER_HORIZONTAL_SIZE[1] + CELL_SIZE[1] * 2), sprites['border_tl'], self.ui)
        Sprite((screen_width - CORNER_SIZE[0], BORDER_HORIZONTAL_SIZE[1] + 2 * CELL_SIZE[1]),
               sprites['border_tr'], self.ui)
        for i in range(2):
            Sprite((i * (screen_width - BORDER_VERTICAL_SIZE[0]), CORNER_SIZE[1]), sprites['border_long'], self.ui)
        for i in range(self.game_size[0]):
            Sprite((CORNER_SIZE[0] + i * BORDER_HORIZONTAL_SIZE[0], 0), sprites['border_h'], self.ui)
            Sprite((CORNER_SIZE[0] + i * BORDER_HORIZONTAL_SIZE[0], BORDER_HORIZONTAL_SIZE[1] + 2 * CELL_SIZE[1]),
                   sprites['border_h'], self.ui)
            Sprite((CORNER_SIZE[0] + i * BORDER_HORIZONTAL_SIZE[0], screen_height - BORDER_HORIZONTAL_SIZE[1]),
                   sprites['border_h'], self.ui)
        for i in range(self.game_size[1]):
            Sprite((0, 2 * (CELL_SIZE[1] + BORDER_HORIZONTAL_SIZE[1]) + i * BORDER_VERTICAL_SIZE[1]),
                   sprites['border_v'], self.ui)
            Sprite((screen_width - BORDER_VERTICAL_SIZE[0],
                    2 * (CELL_SIZE[1] + BORDER_HORIZONTAL_SIZE[1]) + i * BORDER_VERTICAL_SIZE[1]),
                   sprites['border_v'], self.ui)

        for i in range(3):
            self.flag_numbers.append(
                Sprite((BORDER_VERTICAL_SIZE[0] + 0.375 * CELL_SIZE[0] + NUMBER_SIZE[0] * i,
                        BORDER_HORIZONTAL_SIZE[1] + 0.25 * CELL_SIZE[1]), sprites['time0'], self.ui))
            self.timer_numbers.append(
                Sprite((screen_width - BORDER_VERTICAL_SIZE[0] - 0.375 * CELL_SIZE[0] - NUMBER_SIZE[0] * (i + 1),
                        BORDER_HORIZONTAL_SIZE[1] + 0.25 * CELL_SIZE[1]), sprites['time0'], self.ui))

        self.field = []
        for y in range(self.game_size[1]):
            self.field.append([
                CellButton((BORDER_VERTICAL_SIZE[0] + x * CELL_SIZE[0],
                            2 * (BORDER_HORIZONTAL_SIZE[1] + CELL_SIZE[1]) + y * CELL_SIZE[1]), self.ui, self.buttons)
                for x in range(self.game_size[0])])

    def create_field(self, coords):
        ban_coords = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                ban_coords.append((coords[0] + i, coords[1] + j))
        samples = [(i, j) for j in range(self.game_size[1]) for i in range(self.game_size[0]) if (i, j) not in ban_coords]
        # print('\n'.join([' '.join([str(int(j.is_flagged())) for j in i]) for i in self.field]))
        # print()
        mine_coords = sample(samples, self.mines)
        for x, y in mine_coords:
            self.field[y][x].change(-1)
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if i != 0 or j != 0:
                        if 0 <= x + i < self.game_size[0] and 0 <= y + j < self.game_size[1]:
                            if not self.field[y + j][x + i].is_bomb():
                                self.field[y + j][x + i].plus()
        # self.print_field()

    def check_win(self):
        return len([1 for i in range(self.game_size[0] * self.game_size[1])
                    if not self.field[i // self.game_size[0]][i % self.game_size[0]].is_opened()]) == self.mines

    def print_field(self):
        print('\n'.join([' '.join(map(str, i)).replace('-1', '*') for i in self.field]))

    def set_face(self, face):
        if face == 'ooh':
            if self.status == GameStatus.playing.value:
                self.main_button.sprite.ooh()
        elif face == 'unhover':
            if self.status == GameStatus.win.value:
                self.main_button.sprite.win()
            elif self.status == GameStatus.loss.value:
                self.main_button.sprite.loss()
            else:
                self.main_button.sprite.unhover()
        elif face == 'hover':
            self.main_button.sprite.hover()
        elif face == 'win':
            self.main_button.sprite.win()
        elif face == 'loss':
            self.main_button.sprite.loss()

    def mouse_check(self):
        if getInput.left_mouse_down or getInput.right_mouse_down:
            x, y = pygame.mouse.get_pos()
            if self.is_field_coords(x, y):
                col = (x - BORDER_VERTICAL_SIZE[0]) // CELL_SIZE[0]
                row = (y - 2 * (BORDER_HORIZONTAL_SIZE[1] + CELL_SIZE[1])) // CELL_SIZE[1]
                self.field[self.last[1]][self.last[0]].unhover()
                if self.main_button.sprite.is_hovered:
                    self.set_face('unhover')
                if 0 <= row < self.game_size[1] and 0 <= col < self.game_size[0]:
                    if getInput.left_mouse_down:
                        self.set_face('ooh')
                        self.field[row][col].hover()
                    self.last = col, row
            elif self.is_button_coords((x, y), self.main_button.sprite) and getInput.left_mouse_down:
                self.set_face('hover')
            else:
                if self.field[self.last[1]][self.last[0]].is_hovered:
                    self.field[self.last[1]][self.last[0]].unhover()
                if self.main_button.sprite.is_hovered:
                    self.set_face('unhover')
        if getInput.is_mouse_clicked():
            if self.status == GameStatus.playing.value:
                self.main_button.sprite.unhover()
            if self.is_field_coords(*getInput.mouse_up_pos):
                if getInput.mouse_up_button == getInput.LEFT_BUTTON:
                    self.open(*self.last)
                elif getInput.mouse_up_button == getInput.RIGHT_BUTTON:
                    if self.status == GameStatus.playing.value:
                        self.flag(*self.last)
            elif self.is_button_coords(getInput.mouse_up_pos, self.main_button.sprite):
                if getInput.mouse_up_button == getInput.LEFT_BUTTON:
                    self.setup_game()

    def open(self, x: int, y: int):
        if not self.field[y][x].is_flagged() and not self.field[y][x].is_opened():
            if not self.touched:
                self.create_field((x, y))
                self.start_timer()
                self.touched = True
            self.field[y][x].pressed()
            if self.field[y][x].is_n(0):
                for i in (-1, 0, 1):
                    for j in (-1, 0, 1):
                        if i != 0 or j != 0:
                            if 0 <= x + i < self.game_size[0] and 0 <= y + j < self.game_size[1]:
                                self.open(x + i, y + j)
            elif self.field[y][x].is_bomb():
                self.loss((x, y))
            if self.check_win():
                self.win()

    def win(self):
        self.stop_timer()
        self.set_face('win')
        self.status = GameStatus.win.value
        for i in range(self.game_size[0] * self.game_size[1]):
            cell = self.field[i // self.game_size[0]][i % self.game_size[0]]
            if not cell.is_opened() and not cell.is_flagged():
                self.flag(i % self.game_size[0], i // self.game_size[0])

    def loss(self, coords: tuple[int, int]):
        self.set_face('loss')
        self.status = GameStatus.loss.value
        self.stop_timer()
        for y in range(self.game_size[1]):
            for x in range(self.game_size[0]):
                if coords != (x, y):
                    self.field[y][x].bombed()
                self.field[y][x].open()

    def flag(self, x: int, y: int):
        self.field[y][x].flag()
        self.flags = self.mines - sum([len([1 for i in row if i.is_flagged()]) for row in self.field])

    def update_numbers(self):
        flags = max(min(999, self.flags), -99)
        for ind, el in enumerate(f'-0{str(flags)[-1]}' if -10 < flags < 0 else str(flags).rjust(3, '0')):
            self.flag_numbers[ind].set_sprite(sprites[f'time{el}'])
        if getInput.timer_event():
            self.timer += 1
            current_time = min(999, self.timer)
            for ind, el in enumerate(str(current_time).rjust(3, '0')[::-1]):
                self.timer_numbers[ind].set_sprite(sprites[f'time{el}'])

    @staticmethod
    def start_timer():
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    @staticmethod
    def stop_timer():
        pygame.time.set_timer(pygame.USEREVENT, 0)

    @staticmethod
    def is_field_coords(x: int, y: int):
        return BORDER_VERTICAL_SIZE[0] < x <= screen_width - BORDER_VERTICAL_SIZE[0] \
               and 2 * (BORDER_HORIZONTAL_SIZE[1] + CELL_SIZE[1]) < y <= screen_height - BORDER_HORIZONTAL_SIZE[1]

    @staticmethod
    def is_button_coords(coords: tuple[int, int], button):
        x, y = coords
        return button.rect.x < x <= button.rect.x + button.rect.width \
               and button.rect.y < y <= button.rect.y + button.rect.height

    def update(self):
        self.mouse_check()
        self.update_numbers()
        self.screen.fill((192, 192, 192))
        self.ui.draw(self.screen)
        self.buttons.update()

        pygame.display.update()


class GameStatus(Enum):
    playing = 0
    win = 1
    loss = 2