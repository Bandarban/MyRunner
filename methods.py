import pygame
from pygame.locals import *


def load_image(img_path, colorkey=None, scale=None, position=None):
    try:

        image = pygame.image.load(img_path)
        if scale is not None:
            if scale is not tuple:
                image = pygame.transform.rotozoom(image, 0, 3)
            else:
                image = pygame.transform.smoothscale(image, (scale[0], scale[1]))
            image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        if position is not None:
            rect = image.get_rect()
            return image, rect.move(position)
        else:
            return image, image.get_rect()

    except pygame.error as error:
        print('Cannot load image:', img_path, error)
        exit(0)

def mask():
    pygame.mask
