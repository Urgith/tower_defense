import sys

from CONSTANTS import *
from gracz import Gracz
from przeciwnik import Przeciwnik
from wieza import Wieza


class Gra:

    def __init__(self):
        self.initialize_attributes()
        self.initialize_map()

        while True:
            self.time = self.clock.tick(FRAMERATE)
            self.dt = (self.time * GAME_SPEED)

            self.rounds()
            self.events()
            self.update()
            self.draw()

    def initialize_attributes(self):
        self.gracz = Gracz()

        #self.lista_indeksow_do_usuwania_1 = []
        #self.lista_indeksow_do_usuwania_2 = []
        self.lista_przeciwnikow = []
        self.lista_pociskow = []
        self.lista_wiez = []

        self.numer_przeciwnika = 0

        self.licznik_strzelania = pygame.time.get_ticks()
        self.licznik_rund = pygame.time.get_ticks()
        self.licznik = 0

        self.runda = 0

        self.kliknieto_w_kolejna_runde = False
        self.wybrano_wieze_do_kupienia = False
        self.wybrano_wieze = False
        self.was_paused = False
        self.start = False

        self.change_interface = False
        self.previous = []

        self.zdrowie_lasu = 100
        self.pieniadze = STARTING_MONEY
        self.punkty = 0

        self.len_waves_round = len(WAVES[0])
        self.interface_up_height = 117

        self.clock = pygame.time.Clock()

    def initialize_map(self):
        self.okno_gry = pygame.display.set_mode((MAP_WIDTH + MENUSIZE, MAP_HEIGHT))

        self.okno_gry.blits((
            (TRAWA, (0, 0)),
            *MAPA_DRAW,
            (LAS, BASE_RECT),
            (FONT40.render(f'{self.zdrowie_lasu}', True, WHITE), BASE_HP_STRING)
        ))

        pygame.display.update(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))


    def rounds(self):
        if self.start:
            self.licznik += self.time

            if (self.licznik - self.licznik_rund > OPPONENTS_GAP
              and self.numer_przeciwnika < self.len_waves_round):

                self.lista_przeciwnikow.append(Przeciwnik(self.runda, self.numer_przeciwnika))
                self.numer_przeciwnika += 1
                self.licznik_rund = self.licznik

            elif self.kliknieto_w_kolejna_runde and self.numer_przeciwnika == self.len_waves_round:
                self.kliknieto_w_kolejna_runde = False
                self.numer_przeciwnika = 0
                self.runda += 1

                if self.runda < LEN_WAVES:
                    self.len_waves_round = len(WAVES[self.runda])
                else:
                    self.len_waves_round = len(WAVES[-1])

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
                    self.pause_loop()

                elif event.key in {pygame.K_1, pygame.K_2, pygame.K_3}:
                    self.tower_to_buy(event.key - 49)

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
                            self.tower_to_buy(i)
                            break

                    if self.wybrano_wieze:
                        for i in range((self.lista_wiez[self.wybrana_wieza].rodzaj - 1) * 4, self.lista_wiez[self.wybrana_wieza].rodzaj * 4):
                            if TEKSTURY_INTERFEJSU_WIEZY[i][1].collidepoint(self.pozycja_myszy):
                                self.lista_wiez[self.wybrana_wieza].upgrade(self, i)
                                break


    def update(self):
        self.gracz.shoot(self)
        self.gracz.move(self.dt)

        #self.lista_indeksow_do_usuwania_1 = []
        for i, przeciwnik in enumerate(self.lista_przeciwnikow):
            przeciwnik.move(self.dt)

            if przeciwnik.obiekt.colliderect(BASE_RECT):
                self.zdrowie_lasu -= przeciwnik.atak
                self.lista_indeksow_do_usuwania.append(i)

                if self.zdrowie_lasu <= 0:
                    sys.exit()

                continue

            elif przeciwnik.obiekt.colliderect(self.gracz.obiekt):
                self.gracz.zdrowie -= przeciwnik.atak * self.dt * 60

                if self.gracz.zdrowie <= 0:
                    sys.exit()

            przeciwnik.is_electrified = False

        #for indeks in sorted(self.lista_indeksow_do_usuwania_1, reverse=True):
        #    del self.lista_przeciwnikow[indeks]

        #self.lista_indeksow_do_usuwania_1 = []
        for i, pocisk in enumerate(self.lista_pociskow):
            pocisk.move(self.dt)

            if pocisk.rodzaj != 'gracz' and (pocisk.czas_powstania + pocisk.dlugosc_zycia < self.licznik):
                self.lista_pociskow.pop(i)
                continue

            if pocisk.obiekt.x < 0 or pocisk.obiekt.y < 0 or pocisk.obiekt.x > MAP_WIDTH - 8 or pocisk.obiekt.y > MAP_HEIGHT - 8:
                self.lista_pociskow.pop(i)
                continue

            #self.lista_indeksow_do_usuwania_2 = []
            for j, przeciwnik in enumerate(self.lista_przeciwnikow):
                if pocisk.obiekt.colliderect(przeciwnik.obiekt):

                    if pocisk.rodzaj == 2 and (pocisk.id not in przeciwnik.ids):
                        przeciwnik.ids.append(pocisk.id)
                        przeciwnik.zdrowie -= pocisk.obrazenia
                        pocisk.przebicie -= 1

                        if pocisk.przebicie == 0:
                            self.lista_pociskow.pop(i)

                    elif pocisk.rodzaj != 2:
                        przeciwnik.zdrowie -= pocisk.obrazenia
                        self.lista_pociskow.pop(i)

                    if przeciwnik.zdrowie <= 0:
                        self.punkty += przeciwnik.punkty
                        self.pieniadze += przeciwnik.monety
                        self.lista_przeciwnikow.pop(j)

                        if pocisk.rodzaj == 'gracz':
                            self.gracz.doswiadczenie += przeciwnik.punkty
                            self.gracz.check_level_up()

                    break

            #for indeks in sorted(self.lista_indeksow_do_usuwania_2, reverse=True):
            #    del self.lista_przeciwnikow[indeks]

        #for indeks in sorted(self.lista_indeksow_do_usuwania_1, reverse=True):
        #    del self.lista_pociskow[indeks]

        for wieza in self.lista_wiez:
            ilu_juz_zaatakowano = 0
            wieza.mozna_strzelac = False

            if wieza.rodzaj == 3:
                #self.lista_indeksow_do_usuwania_1 = []
                for i, przeciwnik in enumerate(self.lista_przeciwnikow):
                    if (
                      (przeciwnik.obiekt.x - wieza.pole[0])**2 + (przeciwnik.obiekt.y - wieza.pole[1])**2)**0.5 <= wieza.zasieg \
                      or ((przeciwnik.obiekt.x + przeciwnik.rozmiar - wieza.pole[0])**2 + (przeciwnik.obiekt.y - wieza.pole[1])**2)**0.5 <= wieza.zasieg \
                      or ((przeciwnik.obiekt.x - wieza.pole[0])**2 + (przeciwnik.obiekt.y + przeciwnik.rozmiar - wieza.pole[1])**2)**0.5 <= wieza.zasieg \
                      or ((przeciwnik.obiekt.x + przeciwnik.rozmiar - wieza.pole[0])**2 + (przeciwnik.obiekt.y + przeciwnik.rozmiar - wieza.pole[1])**2)**0.5 <= wieza.zasieg:

                        if wieza.elektryzacja > 0:
                            przeciwnik.zdrowie -= wieza.elektryzacja

                            if przeciwnik.zdrowie <= 0:
                                self.lista_przeciwnikow.pop(i)

                            przeciwnik.is_electrified = True

                #for indeks in sorted(self.lista_indeksow_do_usuwania_1, reverse=True):
                #    del self.lista_przeciwnikow[indeks]

            for przeciwnik in self.lista_przeciwnikow:
                if (
                  (przeciwnik.obiekt.x - wieza.pole[0])**2 + (przeciwnik.obiekt.y - wieza.pole[1])**2)**0.5 <= wieza.zasieg \
                  or ((przeciwnik.obiekt.x + przeciwnik.rozmiar - wieza.pole[0])**2 + (przeciwnik.obiekt.y - wieza.pole[1])**2)**0.5 <= wieza.zasieg \
                  or ((przeciwnik.obiekt.x - wieza.pole[0])**2 + (przeciwnik.obiekt.y + przeciwnik.rozmiar - wieza.pole[1])**2)**0.5 <= wieza.zasieg \
                  or ((przeciwnik.obiekt.x + przeciwnik.rozmiar - wieza.pole[0])**2 + (przeciwnik.obiekt.y + przeciwnik.rozmiar - wieza.pole[1])**2)**0.5 <= wieza.zasieg:

                    self.celowany_przeciwnik = przeciwnik
                    wieza.shoot(self)

                    ilu_juz_zaatakowano += 1
                    if wieza.rodzaj != 3 or ilu_juz_zaatakowano == wieza.ilu_na_raz:
                        break

    def draw(self):
        self.okno_gry.blits(((TRAWA, (0, 0)), *MAPA_DRAW, (LAS, BASE_RECT)))

        for wieza in self.lista_wiez:
            self.okno_gry.blit(wieza.typ, wieza.obiekt)

        for przeciwnik in self.lista_przeciwnikow:
            self.okno_gry.blit(przeciwnik.rodzaj, (przeciwnik.obiekt.x - ((przeciwnik.rozmiar - 15) / 2), przeciwnik.obiekt.y - ((przeciwnik.rozmiar - 15) / 2)))

            pygame.draw.rect(self.okno_gry, WHITE, pygame.Rect(przeciwnik.obiekt.x - 5, przeciwnik.obiekt.y - 10, (25 * przeciwnik.zdrowie) // przeciwnik.startowe_zdrowie, 2))
            if przeciwnik.startowe_zdrowie > przeciwnik.zdrowie:
                pygame.draw.rect(self.okno_gry, RED, pygame.Rect(przeciwnik.obiekt.x - 5 + (25 * przeciwnik.zdrowie) // przeciwnik.startowe_zdrowie, przeciwnik.obiekt.y - 10, (25 * (przeciwnik.startowe_zdrowie - przeciwnik.zdrowie)) // przeciwnik.startowe_zdrowie, 2))

            if przeciwnik.is_electrified:
                self.okno_gry.blit(PRAD, (przeciwnik.obiekt.x - ((przeciwnik.rozmiar - 15) / 2), przeciwnik.obiekt.y - ((przeciwnik.rozmiar - 15) / 2)))

        pygame.draw.rect(self.okno_gry, (0,0,0), (MAP_WIDTH, 0, MENUSIZE, MAP_HEIGHT))

        self.okno_gry.blits((
            (FONT30.render(f'Round:{self.runda + self.start}', True, WHITE), (MAP_WIDTH + 57, MAP_HEIGHT - 105)),

            *TEKSTURY,

            (FONT30.render(f'{self.gracz.poziom} | {round(100 * (self.gracz.doswiadczenie - self.gracz.do_poprzedniego) / (self.gracz.do_nastepnego - self.gracz.do_poprzedniego), 2)}%', True, WHITE), (W_23, 2)),
            (FONT30.render(f'{self.gracz.obrazenia} | {1000 / self.gracz.przeladowanie}', True, WHITE), (W_23, 23)),
            (FONT30.render(f'{self.gracz.predkosc}', True, WHITE), (W_23, 41)),
            (FONT30.render(f'{int(self.gracz.zdrowie)}', True, WHITE), (W_23, 59)),
            (FONT30.render(f'{self.pieniadze}', True, WHITE), (W_23, 81)),
            (FONT30.render(f'Points: {self.punkty}', True, WHITE), (MAP_WIDTH + 10, 100)),

            (FONT30.render('10$', True, WHITE), (W_115, MAP_HEIGHT - 73)),
            (FONT30.render('30$', True, WHITE), (W_115, MAP_HEIGHT - 48)),
            (FONT30.render('50$', True, WHITE), (W_115, MAP_HEIGHT - 23)),
            (FONT30.render('1.', True, WHITE), (W_75, MAP_HEIGHT - 73)),
            (FONT30.render('2.', True, WHITE), (W_75, MAP_HEIGHT - 48)),
            (FONT30.render('3.', True, WHITE), (W_75, MAP_HEIGHT - 23)),

            (FONT40.render(f'{self.zdrowie_lasu}', True, WHITE), BASE_HP_STRING),

            (DRUID, self.gracz.obiekt)
        ))

        self.draw_health_bar()

        if self.wybrano_wieze:
            self.okno_gry.blits((
                *TEKSTURY_INTERFEJSU_WIEZY[(self.lista_wiez[self.wybrana_wieza].rodzaj - 1) * 4 : self.lista_wiez[self.wybrana_wieza].rodzaj * 4],

                (FONT30.render(f'{WIEZE_POLEPSZENIA[self.lista_wiez[self.wybrana_wieza].rodzaj - 1][0][0]}$'    , True, RED), (TEKSTURY_INTERFEJSU_WIEZY[0][1][0], TEKSTURY_INTERFEJSU_WIEZY[0][1][1] + 50)),
                (FONT30.render(f'{WIEZE_POLEPSZENIA[self.lista_wiez[self.wybrana_wieza].rodzaj - 1][1][0]}$'  , True, RED), (TEKSTURY_INTERFEJSU_WIEZY[1][1][0], TEKSTURY_INTERFEJSU_WIEZY[1][1][1] + 50)),
                (FONT30.render(f'{WIEZE_POLEPSZENIA[self.lista_wiez[self.wybrana_wieza].rodzaj - 1][2]}$'  , True, RED), (TEKSTURY_INTERFEJSU_WIEZY[2][1][0], TEKSTURY_INTERFEJSU_WIEZY[2][1][1] + 50)),
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

        self.display_update()


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

    def display_update(self):
        x, y, *_ = self.gracz.obiekt
        x_plus_druid_size = x + DRUID_SIZE
        y_plus_druid_size = y + DRUID_SIZE

        rect_to_update = [
            INTERFACE_LOW_HEIGHT,
            pygame.Rect(MAP_WIDTH, 0, MENUSIZE, self.interface_up_height),
        ]

        map_rects = (
            pygame.Rect(x_plus_druid_size, 0, MAP_WIDTH - x_plus_druid_size, y),
            pygame.Rect(x_plus_druid_size, y, MAP_WIDTH - x_plus_druid_size, MAP_HEIGHT - y),
            pygame.Rect(0, y_plus_druid_size, x_plus_druid_size, MAP_HEIGHT - y_plus_druid_size)
        )

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

        self.previous.append(pygame.Rect.union(pygame.Rect(0, 0, x_plus_druid_size, y_plus_druid_size), self.gracz.previous_obiekt))
        pygame.display.update()
        self.previous = rect_to_update

    def new_round(self):
        self.start = True

        if self.licznik != 0:
            self.kliknieto_w_kolejna_runde = True

    def pause_loop(self):
        #self.was_paused = True

        pause = True
        while pause:
            self.time = self.clock.tick(FRAMERATE)
            self.dt = self.time * GAME_SPEED

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_p):
                    pause = False


    def tower_to_buy(self, i):
        self.wybrano_wieze_do_kupienia = True
        self.zasieg_wybranej_wiezy = WIEZE[i][5]
        self.kolor_wybranej_wiezy = WIEZE[i][1]
        self.rodzaj_wybranej_wiezy = i + 1

    def place_tower(self):
        nowa_wieza_rect = pygame.Rect(self.pozycja_myszy[0] - 10, self.pozycja_myszy[1] - 10, 20, 20)

        for r in range(MAP_HEIGHT):
            for c in range(MAP_WIDTH):
                if (pygame.Rect(TILESIZE * c, TILESIZE * r, TILESIZE, TILESIZE).colliderect(nowa_wieza_rect)
                  and (self.pozycja_myszy[0] < 10
                  or self.pozycja_myszy[1] < 10
                  or self.pozycja_myszy[0] > MAP_WIDTH - 10
                  or self.pozycja_myszy[1] > MAP_HEIGHT - 10
                  or MAPA[r][c] != 1)):

                    self.wybrano_wieze_do_kupienia = False
                    return

        for wieza in self.lista_wiez:
            if wieza.obiekt.colliderect(nowa_wieza_rect):
                self.wybrano_wieze_do_kupienia = False
                return

        self.lista_wiez.append(Wieza(self.pozycja_myszy, self.rodzaj_wybranej_wiezy, self.licznik, self.dt))
        self.pieniadze -= self.lista_wiez[-1].cena_calkowita
        if (not self.wybrano_wieze_do_kupienia) or (self.pieniadze < 0):
            self.sell_tower(self.lista_wiez[-1].cena_calkowita)

        self.wybrano_wieze_do_kupienia = False

    def sell_tower(self, cena_calkowita):
        self.wybrano_wieze = False
        self.change_interface = False
        self.pieniadze += cena_calkowita
        self.lista_wiez.pop(self.wybrana_wieza)


if __name__ == '__main__':
    Gra()
