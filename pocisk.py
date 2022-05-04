import pygame
import random

from _STALE import *


class Pocisk:

    def __init__(self, wieza, gra, przeciwnik=None):
        self.rodzaj = wieza.rodzaj
        self.czas_powstania = gra.counter

        if self.rodzaj == 'gracz':
            self.obrazenia = gra.player.damage
            self.predkosc = gra.player.bullet_speed

            self.x, self.y, *_ = gra.player.rect
            self.obiekt = pygame.Rect(self.x, self.y, 8, 8)

            (x, y) = (gra.mouse_pos[0] - self.x, gra.mouse_pos[1] - self.y)

        else:
            if self.rodzaj == 2:
                self.id = random.random()
                self.przebicie = wieza.przebicie

            elif self.rodzaj == 3:
                self.elektryzacja = wieza.elektryzacja

            self.data_konca = wieza.dlugosc_zycia + self.czas_powstania
            self.obrazenia = wieza.obrazenia
            self.predkosc = wieza.predkosc

            self.x, self.y = wieza.pole
            self.obiekt = pygame.Rect(self.x, self.y, wieza.rozmiar_pocisku, wieza.rozmiar_pocisku)
            self.kolor = WIEZE[self.rodzaj - 1][1]

            (x, y) = (przeciwnik.x + (przeciwnik.rozmiar / 2) - self.x,
                   przeciwnik.y + (przeciwnik.rozmiar / 2) - self.y)

        self.kierunek_x = x / ((x**2 + y**2) ** 0.5) * self.predkosc
        self.kierunek_y = y / ((x**2 + y**2) ** 0.5) * self.predkosc

    def move(self, dt):
        self.x += self.kierunek_x * dt
        self.y += self.kierunek_y * dt
        self.obiekt.x, self.obiekt.y = (self.x, self.y)
