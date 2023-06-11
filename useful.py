import pygame
from os import listdir


def load_images_from_folder(folder: str, scale=1) -> dict:
    sprites = {}
    if scale == 1:
        for file_name in listdir(folder):
            sprites[file_name.split('.')[0]] = pygame.image.load(f'{folder}/{file_name}')
    else:
        for file_name in listdir(folder):
            img = pygame.image.load(f'{folder}/{file_name}')
            new_size = img.get_width() * scale, img.get_height() * scale
            sprites[file_name.split('.')[0]] = pygame.transform.scale(img, new_size)
    return sprites