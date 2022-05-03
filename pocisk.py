import pygame
import random

from _STALE import *


class Pocisk:

    def __init__(self, wieza, gra):
        self.rodzaj = wieza.rodzaj
        self.czas_powstania = gra.licznik

        if self.rodzaj == 'gracz':
            self.obrazenia = gra.gracz.obrazenia
            self.predkosc = gra.gracz.predkosc_pocisku

            self.x, self.y, *_ = gra.gracz.obiekt
            self.obiekt = pygame.Rect(self.x, self.y, 8, 8)

            (x, y) = (gra.pozycja_myszy[0] - self.x, gra.pozycja_myszy[1] - self.y)

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

            (x, y) = (gra.celowany_przeciwnik.x + (gra.celowany_przeciwnik.rozmiar / 2) - self.x,
                   gra.celowany_przeciwnik.y + (gra.celowany_przeciwnik.rozmiar / 2) - self.y)

        self.kierunek_x = x / ((x**2 + y**2) ** 0.5)
        self.kierunek_y = y / ((x**2 + y**2) ** 0.5)

    def move(self, dt):
        self.x += self.kierunek_x * dt * self.predkosc
        self.y += self.kierunek_y * dt * self.predkosc
        self.obiekt.x, self.obiekt.y = (self.x, self.y)
