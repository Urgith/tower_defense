import copy
import sys

from STALE import *
from gracz import Gracz
from przeciwnik import Przeciwnik
from wieza import Wieza


class Gra:

    def __init__(self):
        self.initialize_attributes()

        while True:
            self.clock.tick(FPS_MAX)

            self.rounds()
            self.events()
            self.interactions()
            self.draw()

    def initialize_attributes(self):
        self.okno_gry = pygame.display.set_mode((MAP_WIDTH + MENUSIZE, MAP_HEIGHT))
        self.gracz = Gracz()

        self.lista_przeciwnikow = []
        self.lista_pociskow = []
        self.lista_wiez = []

        self.numer_przeciwnika = 0
        self.licznik = 0
        self.runda = 0

        self.kliknieto_w_kolejna_runde = False
        self.wybrano_wieze_do_kupienia = False
        self.wybrano_wieze = False
        self.start = False

        self.zdrowie_lasu = 100
        self.pieniadze = 50
        self.punkty = 0

        self.to_update = (
            pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT),   # mapa
            pygame.Rect(MAP_WIDTH, 0, MENUSIZE, 117),   # interfejs góra
            pygame.Rect(MAP_WIDTH, MAP_HEIGHT - 123, MENUSIZE, 123)   # interfejs dół
        )
        self.previous_to_update = copy.deepcopy(self.to_update)

        self.clock = pygame.time.Clock()

    def rounds(self):
        if self.start:
            self.licznik += 1

            if ((self.licznik % PREDKOSC_WYCHODZENIA) == 0
              and self.numer_przeciwnika < len(WAVES[self.runda])
              and self.runda != (len(WAVES) - 1)):

                self.lista_przeciwnikow.append(Przeciwnik(self.runda, self.numer_przeciwnika))
                self.numer_przeciwnika += 1

            elif self.kliknieto_w_kolejna_runde and self.numer_przeciwnika == len(WAVES[self.runda]):
                self.kliknieto_w_kolejna_runde = False
                self.numer_przeciwnika = 0
                self.runda += 1

                self.gracz.awansowanie()

    def events(self):
        self.pozycja_myszy = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.wybrano_wieze_do_kupienia or self.wybrano_wieze:
                        self.wybrano_wieze_do_kupienia = False
                        self.wybrano_wieze = False
                        self.to_update[1].h = 117

                    else:
                        sys.exit()

                elif event.key == pygame.K_p:
                    self.pause()

                elif event.key in {pygame.K_1, pygame.K_2, pygame.K_3}:
                    self.mainly_to_display_choosen_tower(event.key - 49)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                if self.pozycja_myszy[0] < MAP_WIDTH and self.pozycja_myszy[1] < MAP_HEIGHT:
                    if self.wybrano_wieze_do_kupienia:
                        self.place_tower()

                    else:
                        for i, wieza in enumerate(self.lista_wiez):
                            if wieza.obiekt.collidepoint(self.pozycja_myszy):
                                self.wybrano_wieze = True
                                self.to_update[1].h = 264
                                self.wybrana_wieza = i
                                break
                        # NEW SYNTAX
                        else:
                            self.wybrano_wieze = False
                            self.gracz.strzal(self)

                elif pygame.Rect(*TEKSTURY[0][1], 50, 50).collidepoint(self.pozycja_myszy):
                    self.start = True

                    if self.licznik:
                        self.kliknieto_w_kolejna_runde = True

                elif pygame.Rect(*TEKSTURY[1][1], 70, 70).collidepoint(self.pozycja_myszy):
                    sys.exit()

                else:
                    for i, tekstura in enumerate(TEKSTURY[2:5]):
                        if pygame.Rect(*(tekstura[1]), 20, 20).collidepoint(self.pozycja_myszy):
                            self.mainly_to_display_choosen_tower(i)
                            break

                    if self.wybrano_wieze:
                        for i in range((self.lista_wiez[self.wybrana_wieza].rodzaj - 1) * 4, self.lista_wiez[self.wybrana_wieza].rodzaj * 4):
                            if TEKSTURY_INTERFEJSU_WIEZY[i][1].collidepoint(self.pozycja_myszy):
                                self.lista_wiez[self.wybrana_wieza].polepszenie(self, i)
                                break

    def interactions(self):
        self.gracz.ruch()

        for i, przeciwnik in enumerate(self.lista_przeciwnikow):
            przeciwnik.ruch()

            if przeciwnik.obiekt.colliderect(BASE_RECT):
                self.zdrowie_lasu -= przeciwnik.atak
                self.lista_przeciwnikow.pop(i)
            elif przeciwnik.obiekt.colliderect(self.gracz.obiekt):
                self.gracz.zdrowie -= przeciwnik.atak

            if self.gracz.zdrowie <= 0 or self.zdrowie_lasu <= 0:
                sys.exit()

        for i, pocisk in enumerate(self.lista_pociskow):
            pocisk.ruch()

            if pocisk.rodzaj != 'gracz' and (pocisk.czas_powstania + pocisk.dlugosc_zycia <= self.licznik):
                self.lista_pociskow.pop(i)
                continue

            if pocisk.obiekt.x < 0 or pocisk.obiekt.y < 0 or pocisk.obiekt.x > MAP_WIDTH - 8 or pocisk.obiekt.y > MAP_HEIGHT - 8:
                self.lista_pociskow.pop(i)
                continue

            for j, przeciwnik in enumerate(self.lista_przeciwnikow):
                if pocisk.obiekt.colliderect(przeciwnik.obiekt):

                    if pocisk.rodzaj == 2 and (pocisk.id not in przeciwnik.ids):
                        przeciwnik.ids.append(pocisk.id)
                        przeciwnik.zdrowie -= pocisk.obrazenia
                        pocisk.przebicie -= 1

                        if pocisk.przebicie == 0:
                            ostatni_pocisk = self.lista_pociskow.pop(i)

                    elif pocisk.rodzaj != 2:
                        przeciwnik.zdrowie -= pocisk.obrazenia
                        ostatni_pocisk = self.lista_pociskow.pop(i)

                    if przeciwnik.zdrowie <= 0:
                        self.punkty += przeciwnik.punkty
                        self.pieniadze += przeciwnik.monety
                        self.lista_przeciwnikow.pop(j)

                        if ostatni_pocisk.rodzaj == 'gracz':
                            self.gracz.doswiadczenie += przeciwnik.punkty

                    break

        for wieza in self.lista_wiez:
            ilu_juz_zaatakowano = 0

            for przeciwnik in self.lista_przeciwnikow:
                if (
                  (przeciwnik.obiekt.x - wieza.pole[0])**2 + (przeciwnik.obiekt.y - wieza.pole[1])**2)**0.5 <= wieza.zasieg \
                  or ((przeciwnik.obiekt.x + przeciwnik.rozmiar - wieza.pole[0])**2 + (przeciwnik.obiekt.y - wieza.pole[1])**2)**0.5 <= wieza.zasieg \
                  or ((przeciwnik.obiekt.x - wieza.pole[0])**2 + (przeciwnik.obiekt.y + przeciwnik.rozmiar - wieza.pole[1])**2)**0.5 <= wieza.zasieg \
                  or ((przeciwnik.obiekt.x + przeciwnik.rozmiar - wieza.pole[0])**2 + (przeciwnik.obiekt.y + przeciwnik.rozmiar - wieza.pole[1])**2)**0.5 <= wieza.zasieg:

                    self.celowany_przeciwnik = przeciwnik
                    wieza.strzal(self)

                    ilu_juz_zaatakowano += 1
                    if wieza.rodzaj != 3 or ilu_juz_zaatakowano == wieza.ilu_na_raz:
                        break

    def draw(self):
        self.okno_gry.blits((
            (TRAWA, (0, 0)), *MAPA_DRAW))

        for wieza in self.lista_wiez:
            self.okno_gry.blit(wieza.typ, (wieza.obiekt[0], wieza.obiekt[1]))

        for przeciwnik in self.lista_przeciwnikow:
            self.okno_gry.blit(przeciwnik.rodzaj, (przeciwnik.obiekt.x - ((przeciwnik.rozmiar - 15) / 2), przeciwnik.obiekt.y - ((przeciwnik.rozmiar - 15) / 2)))

            if przeciwnik.zdrowie > 0:
                pygame.draw.rect(self.okno_gry, (0,255,0), pygame.Rect(przeciwnik.obiekt.x - 5, przeciwnik.obiekt.y - 10, (25 * przeciwnik.zdrowie) // przeciwnik.startowe_zdrowie, 3))

                if przeciwnik.startowe_zdrowie > przeciwnik.zdrowie:
                    pygame.draw.rect(self.okno_gry, (255,0,0), pygame.Rect(przeciwnik.obiekt.x - 5 + (25 * przeciwnik.zdrowie) // przeciwnik.startowe_zdrowie, przeciwnik.obiekt.y - 10, (25 * (przeciwnik.startowe_zdrowie - przeciwnik.zdrowie)) // przeciwnik.startowe_zdrowie, 3))

        for pocisk in self.lista_pociskow:
            if pocisk.rodzaj == 'gracz':
                self.okno_gry.blit(KULA_MOCY, (pocisk.obiekt.x, pocisk.obiekt.y))
            else:
                pygame.draw.rect(self.okno_gry, pocisk.kolor, pocisk.obiekt)

        if self.wybrano_wieze:
            pygame.draw.circle(self.okno_gry, self.lista_wiez[self.wybrana_wieza].kolor, self.lista_wiez[self.wybrana_wieza].pole, self.lista_wiez[self.wybrana_wieza].zasieg, 1)

        pygame.draw.rect(self.okno_gry, (0,0,0), (MAP_WIDTH, 0, MENUSIZE, MAP_HEIGHT))

        if self.wybrano_wieze:
            self.okno_gry.blits((
                *TEKSTURY_INTERFEJSU_WIEZY[(self.lista_wiez[self.wybrana_wieza].rodzaj - 1) * 4 : self.lista_wiez[self.wybrana_wieza].rodzaj * 4],

                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].koszt_atak}$'    , True, (255,0,0)), (TEKSTURY_INTERFEJSU_WIEZY[0][1][0] + 5, TEKSTURY_INTERFEJSU_WIEZY[0][1][1] + 50)),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].koszt_zasieg}$'  , True, (255,0,0)), (TEKSTURY_INTERFEJSU_WIEZY[1][1][0] + 5, TEKSTURY_INTERFEJSU_WIEZY[1][1][1] + 50)),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].koszt_reszta}$'  , True, (255,0,0)), (TEKSTURY_INTERFEJSU_WIEZY[2][1][0] + 5, TEKSTURY_INTERFEJSU_WIEZY[2][1][1] + 50)),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].cena_calkowita}$', True, (255,0,0)), (TEKSTURY_INTERFEJSU_WIEZY[3][1][0] + 5, TEKSTURY_INTERFEJSU_WIEZY[3][1][1] + 50)),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].poziom_atak}'    , True, (255,0,255)), (TEKSTURY_INTERFEJSU_WIEZY[0][1][0] + 5, TEKSTURY_INTERFEJSU_WIEZY[0][1][1] + 5)),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].poziom_zasieg}'  , True, (255,0,255)), (TEKSTURY_INTERFEJSU_WIEZY[1][1][0] + 5, TEKSTURY_INTERFEJSU_WIEZY[1][1][1] + 5)),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].poziom_reszta}'  , True, (255,0,255)), (TEKSTURY_INTERFEJSU_WIEZY[2][1][0] + 5, TEKSTURY_INTERFEJSU_WIEZY[2][1][1] + 5)),
            ))

        self.okno_gry.blits((
            (FONT30.render(f'Round:{self.runda + self.start}', True, (255,255,255)), (MAP_WIDTH + 57, MAP_HEIGHT - 105)),

            *TEKSTURY,

            (FONT30.render(f'{self.gracz.poziom}', True, (255,255,255)), (MAP_WIDTH + 23, 2)),
            (FONT30.render(f'{5 + self.gracz.poziom}', True, (255,255,255)), (MAP_WIDTH + 23, 23)),
            (FONT30.render(f'{self.gracz.predkosc}', True, (255,255,255)), (MAP_WIDTH + 23, 41)),
            (FONT30.render(f'{self.gracz.zdrowie}', True, (255,255,255)), (MAP_WIDTH + 23, 59)),
            (FONT30.render(f'{self.pieniadze}', True, (255,255,255)), (MAP_WIDTH + 23, 81)),
            (FONT30.render(f'Points: {self.punkty}', True, (255,255,255)), (MAP_WIDTH + 10, 100)),

            (FONT30.render('10$', True, (255,255,255)), (MAP_WIDTH + 115, MAP_HEIGHT - 73)),
            (FONT30.render('30$', True, (255,255,255)), (MAP_WIDTH + 115, MAP_HEIGHT - 48)),
            (FONT30.render('50$', True, (255,255,255)), (MAP_WIDTH + 115, MAP_HEIGHT - 23)),
            (FONT30.render('1.', True, (255,255,255)), (MAP_WIDTH + 75, MAP_HEIGHT - 73)),
            (FONT30.render('2.', True, (255,255,255)), (MAP_WIDTH + 75, MAP_HEIGHT - 48)),
            (FONT30.render('3.', True, (255,255,255)), (MAP_WIDTH + 75, MAP_HEIGHT - 23)),

            (FONT40.render(f'{self.zdrowie_lasu}', True, (255,255,255)), (BASE_RECT.x - (1.5 * TILESIZE), BASE_RECT.y)),

            (DRUID, (self.gracz.obiekt.x, self.gracz.obiekt.y))
        ))

        self.draw_health_bar()

        if self.wybrano_wieze_do_kupienia:
            pygame.draw.rect(self.okno_gry, self.kolor_wybranej_wiezy, (self.pozycja_myszy[0] - 10, self.pozycja_myszy[1] - 10, 20, 20))
            pygame.draw.circle(self.okno_gry, self.kolor_wybranej_wiezy, self.pozycja_myszy, self.zasieg_wybranej_wiezy, 1)

        if self.to_update == self.previous_to_update:
            pygame.display.update(self.to_update)
        else:
            pygame.display.update(self.previous_to_update)
            self.previous_to_update = copy.deepcopy(self.to_update)

    def mainly_to_display_choosen_tower(self, i):
        self.wybrano_wieze_do_kupienia = True
        self.zasieg_wybranej_wiezy = WIEZE[i][4]
        self.kolor_wybranej_wiezy = WIEZE[i][1]
        self.rodzaj_wybranej_wiezy = i + 1

    @staticmethod
    def pause():
        pause = True

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_p):
                    pause = False

    def place_tower(self):
        # TO OPTIMIZE
        mozna_postawic = True
        nowa_wieza_rect = pygame.Rect(self.pozycja_myszy[0] - 10, self.pozycja_myszy[1] - 10, 20, 20)

        for r in range(MAP_HEIGHT):
            for c in range(MAP_WIDTH):
                if (pygame.Rect(TILESIZE * c, TILESIZE * r, TILESIZE, TILESIZE).colliderect(nowa_wieza_rect)
                  and (self.pozycja_myszy[0] < 10
                  or self.pozycja_myszy[1] < 10
                  or self.pozycja_myszy[0] > MAP_WIDTH - 10
                  or self.pozycja_myszy[1] > MAP_HEIGHT - 10
                  or MAPA[r][c] in {0, 10, 3, 5, 50, 6, 60, 7, 70, 8, 80})):

                    mozna_postawic = False

        for wieza in self.lista_wiez:
            if wieza.obiekt.colliderect(nowa_wieza_rect):
                mozna_postawic = False

        self.lista_wiez.append(Wieza(self.pozycja_myszy, self.rodzaj_wybranej_wiezy))
        self.pieniadze -= self.lista_wiez[-1].koszt
        if (not mozna_postawic) or (self.pieniadze < 0):
            self.pieniadze += self.lista_wiez[-1].koszt
            self.lista_wiez.pop()

        self.wybrano_wieze_do_kupienia = False

    def draw_health_bar(self):
        stan = int((self.gracz.zdrowie / (self.gracz.max_zdrowie + 1)) * 3)
        pasek = pygame.Rect((self.gracz.x, self.gracz.y - 5, self.gracz.zdrowie / self.gracz.max_zdrowie * DRUID_SIZE, 5))

        if stan == 2:
            color = (self.gracz.max_zdrowie - self.gracz.zdrowie) / self.gracz.max_zdrowie
            pygame.draw.rect(self.okno_gry, (int(765 * color), 255, 0), pasek)

        elif stan == 1:
            color = (self.gracz.zdrowie - (self.gracz.max_zdrowie / 3)) / self.gracz.max_zdrowie
            pygame.draw.rect(self.okno_gry, (255, int(765 * color), 0), pasek)

        else:
            color = (self.gracz.zdrowie / self.gracz.max_zdrowie)
            pygame.draw.rect(self.okno_gry, (int(765 * color), 0, 0), pasek)


if __name__ == '__main__':
    Gra()
