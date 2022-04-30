import pygame


def image_load(name, location=None, scale=None):
    image = pygame.image.load(name).convert()

    if location is not None: 
        image.set_colorkey(image.get_at(location))

    if scale is not None:
        image = pygame.transform.scale(image, scale)

    return image
