import pygame
import random

from _STALE import *


class Pocisk:

    def __init__(self, tower, mouse_pos, counter, opponent=None):
        self.type = tower.type

        if self.type == 'player':
            self.damage = tower.damage
            self.speed = tower.bullet_speed

            self.x, self.y, *_ = tower.rect
            self.rect = pygame.Rect(self.x, self.y, 8, 8)

            (x, y) = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)

        else:
            if self.type == 1:
                self.id = random.random()
                self.pierce = tower.pierce

            elif self.type == 2:
                self.electro = tower.electro

            self.end_date = tower.lifespan + counter
            self.damage = tower.damage
            self.speed = tower.speed

            self.x, self.y = tower.rect.center
            self.rect = pygame.Rect(self.x, self.y, tower.bullet_size, tower.bullet_size)
            self.color = tower.color

            (x, y) = (opponent.x + (opponent.size / 2) - self.x,
                   opponent.y + (opponent.size / 2) - self.y)

        self.speed_x = x / ((x**2 + y**2) ** 0.5) * self.speed
        self.speed_y = y / ((x**2 + y**2) ** 0.5) * self.speed

    def move(self, dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt
        self.rect.x, self.rect.y = (self.x, self.y)
