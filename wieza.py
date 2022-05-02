import pygame

from CONSTANTS import *
from pocisk import Pocisk


class Wieza:

    def __init__(self, pozycja_myszy, rodzaj_wybranej_wiezy, licznik, dt):
        self.obiekt = pygame.Rect(pozycja_myszy[0] - 10, pozycja_myszy[1] - 10, 20, 20)
        self.pole = pozycja_myszy
        self.rodzaj = rodzaj_wybranej_wiezy
        self.licznik = licznik
        self.poziom_atak, self.poziom_zasieg, self.poziom_reszta, self.poziom = (0, 0, 0, 0)

        (self.typ, self.kolor, self.cena_calkowita, self.obrazenia, self.predkosc, self.zasieg,
            self.przeladowanie, self.rozmiar_pocisku) = WIEZE[self.rodzaj - 1]

        self.dlugosc_zycia = self.zasieg / self.predkosc * 1000

        if self.rodzaj == 2:
            self.przebicie = 2
        elif self.rodzaj == 3:
            self.ilu_na_raz = 2
            self.elektryzacja = 0.1 * dt * 60

    def shoot(self, gra):
        if (gra.licznik - self.licznik > self.przeladowanie) or self.mozna_strzelac:
            gra.lista_pociskow.append(Pocisk(self, gra))
            self.licznik = gra.licznik

            if self.rodzaj == 3:
                self.mozna_strzelac = True

        if self.rodzaj == 3:
            gra.celowany_przeciwnik.zdrowie -= self.elektryzacja

    def upgrade(self, gra, polepszenie):
        gra.wybrano_wieze = True

        if (polepszenie % 4) == 3:
            gra.sell_tower(self.cena_calkowita)

        if (polepszenie % 4) == 0 and (gra.pieniadze >= WIEZE_POLEPSZENIA[self.rodzaj - 1][0][0]) and (self.poziom_atak <= 4):
            self.increase_damage(WIEZE_POLEPSZENIA[self.rodzaj - 1][0][1])
            self.increase_cost(gra, WIEZE_POLEPSZENIA[self.rodzaj - 1][0][0])

            if self.rodzaj == 3:
                self.ilu_na_raz += 1

        elif (polepszenie % 4) == 1 and (gra.pieniadze >= WIEZE_POLEPSZENIA[self.rodzaj - 1][1][0]) and (self.poziom_zasieg <= 4):
                self.increase_range(WIEZE_POLEPSZENIA[self.rodzaj - 1][1][1])
                self.increase_cost(gra, WIEZE_POLEPSZENIA[self.rodzaj - 1][1][0])

        elif (polepszenie % 4) == 2 and (self.poziom_reszta <= 4):
            self.increase_special(gra)

        self.poziom = (self.poziom_atak + self.poziom_zasieg + self.poziom_reszta) // 3
        self.typ = WIEZE[self.rodzaj - 1 + (self.poziom * 3)][0]

    def increase_cost(self, gra, cost):
        gra.pieniadze -= cost
        self.cena_calkowita += cost

    def increase_damage(self, damage):
        self.obrazenia += damage
        self.poziom_atak += 1

    def increase_range(self, range):
        self.zasieg += range
        self.poziom_zasieg += 1

        self.dlugosc_zycia = (self.zasieg / self.predkosc * 1000)

    def increase_special(self, gra, reload=30, pierce_rate=2, electro_rate=4):
        if (gra.pieniadze >= WIEZE_POLEPSZENIA[self.rodzaj - 1][2]):
            self.poziom_reszta += 1
            self.predkosc += 50
            self.increase_cost(gra, WIEZE_POLEPSZENIA[self.rodzaj - 1][2])
            # 200 (INIT), 170, 140, 110, 80, 50
            if self.rodzaj == 1:
                self.przeladowanie -= reload
            # 2 (INIT), 3, 5, 8, 12, 17
            elif self.rodzaj == 2:
                self.przebicie = 2 + (self.poziom_reszta * (self.poziom_reszta + 1) / pierce_rate)
            # 0.1 (INIT), 0.5, 1.5, 3, 5, 7.5
            elif self.rodzaj == 3:
                self.elektryzacja = self.poziom_reszta * (self.poziom_reszta + 1) / electro_rate * gra.dt * 60
