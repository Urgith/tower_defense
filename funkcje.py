import pygame


def image_load(name, location=None):
    image = pygame.image.load(name).convert()

    if location is not None: 
        image.set_colorkey(image.get_at(location))

    return image


def quit():
    import sys

    pygame.quit()
    sys.exit(0)
