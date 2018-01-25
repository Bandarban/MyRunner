import pygame
from pygame.locals import *
import os, sys


def load_image(img_path, colorkey=None):
    try:
        image = pygame.image.load(img_path)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    except pygame.error as error:
        print('Cannot load image:', img_path, error)
        exit(0)


a, b = load_image("img/Exit.png")
