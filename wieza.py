import pygame

from STALE import *
from pocisk import Pocisk


class Wieza:

    def __init__(self, pozycja_myszy, rodzaj_wybranej_wiezy):
        self.obiekt = pygame.Rect(pozycja_myszy[0] - 10, pozycja_myszy[1] - 10, 20, 20)
        self.pole = pozycja_myszy
        self.rodzaj = rodzaj_wybranej_wiezy
        self.licznik = 0
        self.predkosc = 1
        self.poziom_atak, self.poziom_zasieg, self.poziom_reszta, self.poziom = (0, 0, 0, 0)

        (self.typ, self.kolor, self.koszt, self.obrazenia, self.zasieg,
            self.przeladowanie,self.dlugosc_zycia, self.rozmiar_pocisku) = WIEZE[self.rodzaj - 1]

        self.cena_calkowita = self.koszt
        if self.rodzaj == 1: 
            self.koszt_atak = 4
            self.koszt_zasieg = 1
            self.koszt_reszta = 2

        elif self.rodzaj == 2:
            self.koszt_atak = 10
            self.koszt_zasieg = 2
            self.koszt_reszta = 20
            self.przebicie = 1

        elif self.rodzaj == 3:
            self.koszt_atak = 40
            self.koszt_zasieg = 4
            self.koszt_reszta = 30
            self.ilu_na_raz = 3
            self.elektryzacja = 0

    def strzal(self, gra):
        if self.licznik + self.przeladowanie <= gra.licznik:
            self.licznik = gra.licznik
            gra.lista_pociskow.append(Pocisk(self, gra))

    def polepszenie(self, gra, polepszenie):
        gra.wybrano_wieze = True

        if self.rodzaj == 1:
            if (polepszenie % 4) == 0:
                if gra.pieniadze >= 4 and self.poziom_atak <= 4:
                    self.cena_calkowita += 4
                    gra.pieniadze -= 4
                    self.obrazenia += 5
                    self.poziom_atak += 1

            elif (polepszenie % 4) == 1:
                if gra.pieniadze >= 1 and self.poziom_zasieg <= 4:
                    self.cena_calkowita += 1
                    gra.pieniadze -= 1
                    self.dlugosc_zycia += 30
                    self.zasieg += 15
                    self.poziom_zasieg += 1

            elif (polepszenie % 4) == 2:
                if gra.pieniadze >= 2 and self.poziom_reszta <= 4:
                    self.cena_calkowita += 2
                    gra.pieniadze -= 2
                    self.przeladowanie -= 1
                    self.predkosc += 0.4
                    self.poziom_reszta += 1

            elif (polepszenie % 4) == 3:
                gra.wybrano_wieze = False
                gra.pieniadze += self.cena_calkowita
                gra.lista_wiez.pop(gra.wybrana_wieza)

        elif self.rodzaj == 2:
            if (polepszenie % 4) == 0:
                if gra.pieniadze >= 10 and self.poziom_atak <= 4:
                    self.cena_calkowita += 10
                    gra.pieniadze -= 10
                    self.obrazenia += 20
                    self.poziom_atak += 1

            elif (polepszenie % 4) == 1:
                if gra.pieniadze >= 2 and self.poziom_zasieg <= 4:
                    self.cena_calkowita += 2
                    gra.pieniadze -= 2
                    self.dlugosc_zycia += 15
                    self.zasieg += 30
                    self.poziom_zasieg += 1

            elif (polepszenie % 4) == 2:
                if gra.pieniadze >= 20 and self.poziom_reszta <= 4:
                    self.cena_calkowita += 20
                    gra.pieniadze -= 20
                    self.przeladowanie -= 1
                    self.przebicie += 1
                    self.poziom_reszta += 1

            elif (polepszenie % 4) == 3:
                gra.wybrano_wieze = False
                gra.pieniadze += self.cena_calkowita
                gra.lista_wiez.pop(gra.wybrana_wieza)

        elif self.rodzaj == 3:
            if (polepszenie % 4) == 0:
                if gra.pieniadze >= 40 and self.poziom_atak <= 4:
                    self.cena_calkowita += 40
                    gra.pieniadze -= 40
                    self.obrazenia += 1
                    self.ilu_na_raz += 1
                    self.poziom_atak += 1

            elif (polepszenie % 4) == 1:
                if gra.pieniadze >= 4 and self.poziom_zasieg <= 4:
                    self.cena_calkowita += 4
                    gra.pieniadze -= 4
                    self.dlugosc_zycia += 5
                    self.zasieg += 15
                    self.poziom_zasieg += 1

            elif (polepszenie % 4) == 2:
                if gra.pieniadze >= 30 and self.poziom_reszta <= 4:
                    self.cena_calkowita += 30
                    gra.pieniadze -= 30
                    self.predkosc += 0.2
                    self.elektryzacja += 1
                    self.poziom_reszta += 1

            elif (polepszenie % 4) == 3:
                gra.wybrano_wieze = False
                gra.pieniadze += self.cena_calkowita
                gra.lista_wiez.pop(gra.wybrana_wieza)

        self.poziom = (self.poziom_atak + self.poziom_zasieg + self.poziom_reszta) // 3
        self.typ = WIEZE[self.rodzaj - 1 + (self.poziom * 3)][0]
