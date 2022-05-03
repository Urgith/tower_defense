import pygame

from CONSTANTS import *
from pocisk import Pocisk


class Gracz:

    def __init__(self):
        self.x, self.y = (DRUID_X, DRUID_Y)
        self.obiekt = pygame.Rect(self.x, self.y, DRUID_SIZE, DRUID_SIZE)
        self.previous_obiekt = pygame.Rect(self.x, self.y, DRUID_SIZE, DRUID_SIZE)

        self.doswiadczenie = 0
        self.poziom = 0
        self.do_poprzedniego = 0
        self.do_nastepnego = 10

        self.zdrowie = self.max_zdrowie = 1000
        self.przeladowanie = STARTING_FIRE_RATE
        self.obrazenia = 10
        self.predkosc = 100

        self.predkosc_pocisku = 200
        self.strzelam = STARTING_FIRING

        self.rodzaj = 'gracz'

    def move(self, dt):
        self.previous_obiekt.x, self.previous_obiekt.y = (self.x, self.y)

        self.klikniete = pygame.key.get_pressed()
        x, y = (0, 0)

        if self.klikniete[pygame.K_w]:
            self.y -= self.predkosc * dt
            y = -1

        if self.klikniete[pygame.K_a]:
            self.x -= self.predkosc * dt
            x = -1

        if self.klikniete[pygame.K_s]:
            self.y += self.predkosc * dt
            y = 1

        if self.klikniete[pygame.K_d]:
            self.x += self.predkosc * dt
            x = 1
        # 0.4 ~= 2**0.5 - 1
        if x and y:
            self.x -= 0.414 * x * self.predkosc * dt
            self.y -= 0.414 * y * self.predkosc * dt

        if self.x < 0:
            self.x = 0
        elif self.x > MAP_WIDTH - DRUID_SIZE:
            self.x = MAP_WIDTH - DRUID_SIZE

        if self.y < 0:
            self.y = 0
        elif self.y > MAP_HEIGHT - DRUID_SIZE:
            self.y = MAP_HEIGHT - DRUID_SIZE

        self.obiekt.x, self.obiekt.y = (self.x, self.y)

    def shoot(self, gra):
        if self.strzelam and (gra.licznik - gra.licznik_strzelania > self.przeladowanie):
            gra.lista_pociskow.append(Pocisk(self, gra))
            gra.licznik_strzelania = gra.licznik

    def check_level_up(self):
        if self.doswiadczenie >= self.do_nastepnego:
            self.poziom = int((self.doswiadczenie // 10) ** 0.5)

            self.predkosc = 100 + (10 * self.poziom)
            self.obrazenia = 10 + int(((self.poziom + 1) * self.poziom) / 2)
            self.przeladowanie = 1000 / (4 + (self.poziom / 10))

            self.max_zdrowie = int(1000 * (1 + (self.poziom / 10)))
            self.zdrowie = self.max_zdrowie

            self.predkosc_pocisku = 200 + (20 * self.poziom)

            self.do_poprzedniego = self.do_nastepnego
            self.do_nastepnego += 10 + (20 * self.poziom)
