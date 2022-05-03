import sys

from _STALE import *
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
        self.pozycja_myszy = STARTING_MOUSE_POSITION
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
        #self.licznik += self.time
        #self.kliknieto_w_kolejna_runde = True

        #if self.runda < LEN_WAVES:
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
                        self.tower_flags_to_False()

                    else:
                        sys.exit()

                elif event.key == pygame.K_p:
                    self.pause_loop()

                elif event.key in PYGAME_K1_K2_K3:
                    self.tower_to_buy(event.key - 49)

                elif event.key == pygame.K_SPACE:
                    self.new_round()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                if self.pozycja_myszy[0] < MAP_WIDTH and self.pozycja_myszy[1] < MAP_HEIGHT:
                    if self.wybrano_wieze_do_kupienia:
                        self.place_tower()

                    else:
                        for wieza in self.lista_wiez:
                            if wieza.obiekt.collidepoint(self.pozycja_myszy):
                                self.change_interface = True
                                self.wybrano_wieze = True
                                self.wybrana_wieza = wieza
                                break

                        else:
                            self.gracz.strzelam = not self.gracz.strzelam
                            self.tower_flags_to_False()

                elif TEKSTURY[0][1].collidepoint(self.pozycja_myszy):
                    self.new_round()

                elif TEKSTURY[1][1].collidepoint(self.pozycja_myszy):
                    sys.exit()

                else:
                    for i, tekstura in enumerate(TEKSTURY[2:5]):
                        if tekstura[1].collidepoint(self.pozycja_myszy):
                            self.tower_to_buy(i)
                            break

                    if self.wybrano_wieze:
                        wybrana_4 = self.wybrana_wieza.rodzaj * 4
                        for i in range(wybrana_4 - 4, wybrana_4):
                            if TEKSTURY_INTERFEJSU_WIEZY[i][1].collidepoint(self.pozycja_myszy):
                                self.wybrana_wieza.upgrade(self, i)
                                break


    def update(self):
        self.gracz.shoot(self)
        self.gracz.move(self.dt)

        self.update_opponents()
        self.update_bullets()
        self.update_towers()

    def update_opponents(self):
        for i, przeciwnik in enumerate(self.lista_przeciwnikow):
            przeciwnik.move(self.dt)

            if przeciwnik.obiekt.colliderect(BASE_RECT):
                self.zdrowie_lasu -= przeciwnik.atak
                self.lista_przeciwnikow.pop(i)

                if self.zdrowie_lasu <= 0:
                    sys.exit()

                continue

            elif przeciwnik.obiekt.colliderect(self.gracz.obiekt):
                self.gracz.zdrowie -= przeciwnik.atak * self.dt * 60

                if self.gracz.zdrowie <= 0:
                    sys.exit()

            przeciwnik.is_electrified = False

    def update_bullets(self):
        lista = [przeciwnik.obiekt for przeciwnik in self.lista_przeciwnikow]

        for i, pocisk in enumerate(self.lista_pociskow):
            pocisk.move(self.dt)

            if pocisk.rodzaj != 'gracz' and (pocisk.data_konca < self.licznik):
                self.lista_pociskow.pop(i)
                continue

            if pocisk.obiekt.x < 0 or pocisk.obiekt.y < 0 or pocisk.obiekt.x > W_8_ or pocisk.obiekt.y > H_8_:
                self.lista_pociskow.pop(i)
                continue

            collision_test = pocisk.obiekt.collidelist(lista)
            if collision_test != -1:
                przeciwnik = self.lista_przeciwnikow[collision_test]

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

                    self.lista_przeciwnikow.pop(collision_test)
                    lista.pop(collision_test)

                    if pocisk.rodzaj == 'gracz':
                        self.gracz.doswiadczenie += przeciwnik.punkty
                        self.gracz.check_level_up()

    def update_towers(self):
        for wieza in self.lista_wiez:
            ilu_juz_zaatakowano = 0
            wieza.mozna_strzelac = False

            if wieza.rodzaj == 3:
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
            self.okno_gry.blit(przeciwnik.rodzaj, przeciwnik.obiekt)

            pygame.draw.rect(self.okno_gry, WHITE, przeciwnik.hp_bar)
            if przeciwnik.startowe_zdrowie > przeciwnik.zdrowie:
                pygame.draw.rect(self.okno_gry, RED, przeciwnik.hp_bar_lost)

            if przeciwnik.is_electrified:
                self.okno_gry.blit(PRAD, (przeciwnik.obiekt.x - ((przeciwnik.rozmiar - 15) / 2), przeciwnik.obiekt.y - ((przeciwnik.rozmiar - 15) / 2)))

        pygame.draw.rect(self.okno_gry, (0,0,0), (MAP_WIDTH, 0, MENUSIZE, MAP_HEIGHT))

        self.okno_gry.blits((
            (FONT30.render(f'Round:{self.runda + self.start}', True, WHITE), (W_57, H_105_)),

            *TEKSTURY,

            (FONT30.render(f'{self.gracz.poziom} | {round(100 * (self.gracz.doswiadczenie - self.gracz.do_poprzedniego) / (self.gracz.do_nastepnego - self.gracz.do_poprzedniego), 2)}%', True, WHITE), (W_23, 2)),
            (FONT30.render(f'{self.gracz.obrazenia} | {1000 / self.gracz.przeladowanie}', True, WHITE), (W_23, 23)),
            (FONT30.render(f'{self.gracz.predkosc}', True, WHITE), (W_23, 41)),
            (FONT30.render(f'{int(self.gracz.zdrowie)}', True, WHITE), (W_23, 59)),
            (FONT30.render(f'{self.pieniadze}', True, WHITE), (W_23, 81)),
            (FONT30.render(f'Points: {self.punkty}', True, WHITE), (W_10, 100)),

            (FONT30.render('10$', True, WHITE), (W_115, H_73_)),
            (FONT30.render('30$', True, WHITE), (W_115, H_48_)),
            (FONT30.render('50$', True, WHITE), (W_115, H_23_)),
            (FONT30.render('1.', True, WHITE), (W_75, H_73_)),
            (FONT30.render('2.', True, WHITE), (W_75, H_48_)),
            (FONT30.render('3.', True, WHITE), (W_75, H_23_)),

            (FONT40.render(f'{self.zdrowie_lasu}', True, WHITE), BASE_HP_STRING),

            (DRUID, self.gracz.obiekt)
        ))

        self.draw_health_bar()

        if self.wybrano_wieze:
            self.okno_gry.blits((
                *TEKSTURY_INTERFEJSU_WIEZY[(self.wybrana_wieza.rodzaj - 1) * 4 : self.wybrana_wieza.rodzaj * 4],

                (FONT30.render(f'{WIEZE_POLEPSZENIA[self.wybrana_wieza.rodzaj - 1][0][0]}$'    , True, RED), (TEKSTURY_INTERFEJSU_WIEZY[0][1][0], TEKSTURY_INTERFEJSU_WIEZY[0][1][1] + 50)),
                (FONT30.render(f'{WIEZE_POLEPSZENIA[self.wybrana_wieza.rodzaj - 1][1][0]}$'  , True, RED), (TEKSTURY_INTERFEJSU_WIEZY[1][1][0], TEKSTURY_INTERFEJSU_WIEZY[1][1][1] + 50)),
                (FONT30.render(f'{WIEZE_POLEPSZENIA[self.wybrana_wieza.rodzaj - 1][2]}$'  , True, RED), (TEKSTURY_INTERFEJSU_WIEZY[2][1][0], TEKSTURY_INTERFEJSU_WIEZY[2][1][1] + 50)),
                (FONT30.render(f'{self.wybrana_wieza.cena_calkowita}$', True, RED), (TEKSTURY_INTERFEJSU_WIEZY[3][1][0], TEKSTURY_INTERFEJSU_WIEZY[3][1][1] + 50)),
                (FONT30.render(f'{self.wybrana_wieza.poziom_atak}'    , True, PURPLE), (TEKSTURY_INTERFEJSU_WIEZY[0][1][0], TEKSTURY_INTERFEJSU_WIEZY[0][1][1])),
                (FONT30.render(f'{self.wybrana_wieza.poziom_zasieg}'  , True, PURPLE), (TEKSTURY_INTERFEJSU_WIEZY[1][1][0], TEKSTURY_INTERFEJSU_WIEZY[1][1][1])),
                (FONT30.render(f'{self.wybrana_wieza.poziom_reszta}'  , True, PURPLE), (TEKSTURY_INTERFEJSU_WIEZY[2][1][0], TEKSTURY_INTERFEJSU_WIEZY[2][1][1])),
            ))

            pygame.draw.circle(self.okno_gry, self.wybrana_wieza.kolor, self.wybrana_wieza.pole, self.wybrana_wieza.zasieg, 2)

        for pocisk in self.lista_pociskow:
            if pocisk.rodzaj == 'gracz':
                self.okno_gry.blit(KULA_MOCY, pocisk.obiekt)
            else:
                pygame.draw.rect(self.okno_gry, pocisk.kolor, pocisk.obiekt)

        if self.wybrano_wieze_do_kupienia:
            pygame.draw.rect(self.okno_gry, self.kolor_wybranej_wiezy, (self.pozycja_myszy[0] - 10, self.pozycja_myszy[1] - 10, 20, 20))
            pygame.draw.circle(self.okno_gry, self.kolor_wybranej_wiezy, self.pozycja_myszy, self.zasieg_wybranej_wiezy, 2)

        pygame.display.update()

    def draw_health_bar(self):
        stan = int((self.gracz.zdrowie / (self.gracz.max_zdrowie + 1)) * 5)
        pasek = pygame.Rect((self.gracz.x, self.gracz.y - 5, self.gracz.zdrowie / self.gracz.max_zdrowie * DRUID_SIZE, 5))

        if stan == 4:
            color = (self.gracz.max_zdrowie - self.gracz.zdrowie) / self.gracz.max_zdrowie
            pygame.draw.rect(self.okno_gry, (0, int(1275 * color), 255), pasek)

        elif stan == 3:
            color = (self.gracz.zdrowie - (3 * self.gracz.max_zdrowie / 5)) / self.gracz.max_zdrowie
            pygame.draw.rect(self.okno_gry, (0, 255, int(1275 * color)), pasek)

        elif stan == 2:
            color = ((3 * self.gracz.max_zdrowie / 5) - self.gracz.zdrowie) / self.gracz.max_zdrowie
            pygame.draw.rect(self.okno_gry, (int(1275 * color), 255, 0), pasek)

        elif stan == 1:
            color = (self.gracz.zdrowie - (self.gracz.max_zdrowie / 5)) / self.gracz.max_zdrowie
            pygame.draw.rect(self.okno_gry, (255, int(1275 * color), 0), pasek)

        else:
            color = (self.gracz.zdrowie / self.gracz.max_zdrowie)
            pygame.draw.rect(self.okno_gry, (int(1275 * color), 0, 0), pasek)

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

        for tile in MAPA_DRAW:
            if (pygame.Rect(*tile[1], TILESIZE, TILESIZE).colliderect(nowa_wieza_rect)
              or BASE_RECT.colliderect(nowa_wieza_rect)
              or self.pozycja_myszy[0] < 10
              or self.pozycja_myszy[1] < 10
              or self.pozycja_myszy[0] > W_10_
              or self.pozycja_myszy[1] > H_10_):

                self.wybrano_wieze_do_kupienia = False
                return

        for wieza in self.lista_wiez:
            if wieza.obiekt.colliderect(nowa_wieza_rect):
                self.wybrano_wieze_do_kupienia = False
                return

        self.wybrana_wieza = Wieza(self.pozycja_myszy, self.rodzaj_wybranej_wiezy, self.licznik, self.dt)
        self.lista_wiez.append(self.wybrana_wieza)
        self.pieniadze -= self.lista_wiez[-1].cena_calkowita
        if (not self.wybrano_wieze_do_kupienia) or (self.pieniadze < 0):
            self.sell_tower(self.lista_wiez[-1].cena_calkowita)

        self.wybrano_wieze_do_kupienia = False

    def sell_tower(self, cena_calkowita):
        self.tower_flags_to_False()
        self.pieniadze += cena_calkowita
        self.lista_wiez.remove(self.wybrana_wieza)

    def tower_flags_to_False(self):
        self.wybrano_wieze_do_kupienia = False
        self.wybrano_wieze = False

        self.change_interface = False


if __name__ == '__main__':
    Gra()
