import sys

from STALE import *
from gracz import Gracz
from przeciwnik import Przeciwnik
from wieza import Wieza


class Gra:

    def __init__(self):
        self.initialize_attributes_and_map()

        while True:
            self.clock.tick(FPS_MAX)

            self.rounds()
            self.events()
            self.interactions()
            self.draw()

    def initialize_attributes_and_map(self):
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

        self.change_interface = False
        self.previous = None

        self.zdrowie_lasu = 100
        self.pieniadze = 50
        self.punkty = 0

        self.len_waves_round = len(WAVES[0])

        self.okno_gry.blits((
            (TRAWA, (0, 0)),
            *MAPA_DRAW,
            (LAS, BASE_RECT),
            (FONT40.render(f'{self.zdrowie_lasu}', True, WHITE), BASE_HP_STRING)
        ))

        pygame.display.update(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))

        self.interface_up_height = 117

        self.clock = pygame.time.Clock()

    def rounds(self):
        if self.start:
            self.licznik += 1

        if self.start and (self.runda != LEN_WAVES):

            if ((self.licznik % PREDKOSC_WYCHODZENIA) == 0
              and self.numer_przeciwnika < self.len_waves_round):

                self.lista_przeciwnikow.append(Przeciwnik(self.runda, self.numer_przeciwnika))
                self.numer_przeciwnika += 1

            elif self.kliknieto_w_kolejna_runde and self.numer_przeciwnika == self.len_waves_round:
                self.kliknieto_w_kolejna_runde = False
                self.numer_przeciwnika = 0
                self.runda += 1

                if self.runda != LEN_WAVES:
                    self.len_waves_round = len(WAVES[self.runda])

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
                        self.change_interface = False
                        self.wybrano_wieze = False

                    else:
                        sys.exit()

                elif event.key == pygame.K_p:
                    self.pause()

                elif event.key in {pygame.K_1, pygame.K_2, pygame.K_3}:
                    self.mainly_to_display_choosen_tower(event.key - 49)

                elif event.key == pygame.K_SPACE:
                    self.new_round()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                if self.pozycja_myszy[0] < MAP_WIDTH and self.pozycja_myszy[1] < MAP_HEIGHT:
                    if self.wybrano_wieze_do_kupienia:
                        self.place_tower()

                    else:
                        for i, wieza in enumerate(self.lista_wiez):
                            if wieza.obiekt.collidepoint(self.pozycja_myszy):
                                self.change_interface = True
                                self.wybrano_wieze = True
                                self.wybrana_wieza = i
                                break
                        # NEW SYNTAX
                        else:
                            self.gracz.strzelam = not self.gracz.strzelam
                            self.change_interface = False
                            self.wybrano_wieze = False

                elif pygame.Rect(*TEKSTURY[0][1], 50, 50).collidepoint(self.pozycja_myszy):
                    self.new_round()

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
        self.gracz.strzal(self)
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
        self.okno_gry.blits(((TRAWA, (0, 0)), *MAPA_DRAW, (LAS, BASE_RECT)))

        for wieza in self.lista_wiez:
            self.okno_gry.blit(wieza.typ, wieza.obiekt)

        for przeciwnik in self.lista_przeciwnikow:
            self.okno_gry.blit(przeciwnik.rodzaj, (przeciwnik.obiekt.x - ((przeciwnik.rozmiar - 15) / 2), przeciwnik.obiekt.y - ((przeciwnik.rozmiar - 15) / 2)))

            if przeciwnik.zdrowie > 0:
                pygame.draw.rect(self.okno_gry, (0,255,0), pygame.Rect(przeciwnik.obiekt.x - 5, przeciwnik.obiekt.y - 10, (25 * przeciwnik.zdrowie) // przeciwnik.startowe_zdrowie, 3))

                if przeciwnik.startowe_zdrowie > przeciwnik.zdrowie:
                    pygame.draw.rect(self.okno_gry, RED, pygame.Rect(przeciwnik.obiekt.x - 5 + (25 * przeciwnik.zdrowie) // przeciwnik.startowe_zdrowie, przeciwnik.obiekt.y - 10, (25 * (przeciwnik.startowe_zdrowie - przeciwnik.zdrowie)) // przeciwnik.startowe_zdrowie, 3))

        pygame.draw.rect(self.okno_gry, (0,0,0), (MAP_WIDTH, 0, MENUSIZE, MAP_HEIGHT))

        self.okno_gry.blits((
            (FONT30.render(f'Round:{self.runda + self.start}', True, WHITE), (MAP_WIDTH + 57, MAP_HEIGHT - 105)),

            *TEKSTURY,

            (FONT30.render(f'{self.gracz.poziom}', True, WHITE), (W_23, 2)),
            (FONT30.render(f'{5 + self.gracz.poziom}', True, WHITE), (W_23, 23)),
            (FONT30.render(f'{self.gracz.predkosc}', True, WHITE), (W_23, 41)),
            (FONT30.render(f'{self.gracz.zdrowie}', True, WHITE), (W_23, 59)),
            (FONT30.render(f'{self.pieniadze}', True, WHITE), (W_23, 81)),
            (FONT30.render(f'Points: {self.punkty}', True, WHITE), (MAP_WIDTH + 10, 100)),

            (FONT30.render('10$', True, WHITE), (W_115, MAP_HEIGHT - 73)),
            (FONT30.render('30$', True, WHITE), (W_115, MAP_HEIGHT - 48)),
            (FONT30.render('50$', True, WHITE), (W_115, MAP_HEIGHT - 23)),
            (FONT30.render('1.', True, WHITE), (W_75, MAP_HEIGHT - 73)),
            (FONT30.render('2.', True, WHITE), (W_75, MAP_HEIGHT - 48)),
            (FONT30.render('3.', True, WHITE), (W_75, MAP_HEIGHT - 23)),

            (FONT40.render(f'{self.zdrowie_lasu}', True, WHITE), BASE_HP_STRING),

            (DRUID, (self.gracz.obiekt.x, self.gracz.obiekt.y))
        ))

        self.draw_health_bar()

        if self.wybrano_wieze:
            self.okno_gry.blits((
                *TEKSTURY_INTERFEJSU_WIEZY[(self.lista_wiez[self.wybrana_wieza].rodzaj - 1) * 4 : self.lista_wiez[self.wybrana_wieza].rodzaj * 4],

                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].koszt_atak}$'    , True, RED), (TEKSTURY_INTERFEJSU_WIEZY[0][1][0], TEKSTURY_INTERFEJSU_WIEZY[0][1][1] + 50)),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].koszt_zasieg}$'  , True, RED), (TEKSTURY_INTERFEJSU_WIEZY[1][1][0], TEKSTURY_INTERFEJSU_WIEZY[1][1][1] + 50)),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].koszt_reszta}$'  , True, RED), (TEKSTURY_INTERFEJSU_WIEZY[2][1][0], TEKSTURY_INTERFEJSU_WIEZY[2][1][1] + 50)),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].cena_calkowita}$', True, RED), (TEKSTURY_INTERFEJSU_WIEZY[3][1][0], TEKSTURY_INTERFEJSU_WIEZY[3][1][1] + 50)),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].poziom_atak}'    , True, PURPLE), (TEKSTURY_INTERFEJSU_WIEZY[0][1][0], TEKSTURY_INTERFEJSU_WIEZY[0][1][1])),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].poziom_zasieg}'  , True, PURPLE), (TEKSTURY_INTERFEJSU_WIEZY[1][1][0], TEKSTURY_INTERFEJSU_WIEZY[1][1][1])),
                (FONT30.render(f'{self.lista_wiez[self.wybrana_wieza].poziom_reszta}'  , True, PURPLE), (TEKSTURY_INTERFEJSU_WIEZY[2][1][0], TEKSTURY_INTERFEJSU_WIEZY[2][1][1])),
            ))

            pygame.draw.circle(self.okno_gry, self.lista_wiez[self.wybrana_wieza].kolor, self.lista_wiez[self.wybrana_wieza].pole, self.lista_wiez[self.wybrana_wieza].zasieg, 2)

        for pocisk in self.lista_pociskow:
            if pocisk.rodzaj == 'gracz':
                self.okno_gry.blit(KULA_MOCY, pocisk.obiekt)
            else:
                pygame.draw.rect(self.okno_gry, pocisk.kolor, pocisk.obiekt)

        if self.wybrano_wieze_do_kupienia:
            pygame.draw.rect(self.okno_gry, self.kolor_wybranej_wiezy, (self.pozycja_myszy[0] - 10, self.pozycja_myszy[1] - 10, 20, 20))
            pygame.draw.circle(self.okno_gry, self.kolor_wybranej_wiezy, self.pozycja_myszy, self.zasieg_wybranej_wiezy, 2)

        self.to_update()

    def new_round(self):
        self.start = True

        if self.licznik != 0:
            self.kliknieto_w_kolejna_runde = True

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

    def to_update(self):
        x, y, *_ = self.gracz.obiekt
        x_plus_druid_size = x + DRUID_SIZE
        y_plus_druid_size = y + DRUID_SIZE

        rect_to_update = [
            INTERFACE_LOW_HEIGHT,
            pygame.Rect(MAP_WIDTH, 0, MENUSIZE, self.interface_up_height),
            pygame.Rect(0, 0, x_plus_druid_size, y_plus_druid_size)
        ]

        map_rects = (
            pygame.Rect(x_plus_druid_size, 0, MAP_WIDTH - x_plus_druid_size, y),
            pygame.Rect(x_plus_druid_size, y, MAP_WIDTH - x_plus_druid_size, MAP_HEIGHT - y),
            pygame.Rect(0, y_plus_druid_size, x_plus_druid_size, MAP_HEIGHT - y_plus_druid_size)
        )
        # NEW SYNTAX
        for rect in map_rects:
            for przeciwnik in self.lista_przeciwnikow:
                if rect.colliderect(przeciwnik.obiekt_z_paskiem):
                    rect_to_update.append(rect)
                    break

            else:
                for pocisk in self.lista_pociskow:
                    if rect.colliderect(pocisk.obiekt):
                        rect_to_update.append(rect)
                        break

                else:
                    for wieza in self.lista_wiez:
                        if rect.colliderect(wieza.obiekt):
                            rect_to_update.append(rect)
                            break

        if self.change_interface:
            self.interface_up_height = 264
        else:
            self.interface_up_height = 117

        if self.wybrano_wieze_do_kupienia:
            rect_to_update.append(pygame.Rect((self.pozycja_myszy[0] - self.zasieg_wybranej_wiezy), (self.pozycja_myszy[1] - self.zasieg_wybranej_wiezy), (2 * self.zasieg_wybranej_wiezy), (2 * self.zasieg_wybranej_wiezy)))

        if self.wybrano_wieze:
            rect_to_update.append(pygame.Rect((self.lista_wiez[self.wybrana_wieza].pole[0] - self.lista_wiez[self.wybrana_wieza].zasieg, self.lista_wiez[self.wybrana_wieza].pole[1] - self.lista_wiez[self.wybrana_wieza].zasieg, (2 * self.lista_wiez[self.wybrana_wieza].zasieg), (2 * self.lista_wiez[self.wybrana_wieza].zasieg))))

        if self.previous == rect_to_update:
            pygame.display.update(rect_to_update)
        else:
            pygame.display.update(self.previous)
            self.previous = rect_to_update[:]

        # WIZUALIZACJA PODZIAŁU MAPY
        #for i, rect in enumerate(map_rects):
        #    pygame.draw.rect(self.okno_gry, (85*i, 85*i, 85*i), rect)
        #pygame.display.flip()

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
