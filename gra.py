import sys

from _STALE import *
from gracz import Gracz
from przeciwnik import Przeciwnik
from wieza import Wieza


class Gra:

    def __init__(self):
        self.initialize_attributes()

        while True:
            self.time = self.clock.tick(FRAMERATE)
            self.dt = (self.time * GAME_SPEED)

            self.rounds()
            self.events()
            self.update()
            self.draw()

    def initialize_attributes(self):
        self.game_window = pygame.display.set_mode((MAP_WIDTH + MENUSIZE, MAP_HEIGHT))
        self.player = Gracz()

        self.opponents = []
        self.bullets = []
        self.towers = []

        self.opponents_counter = pygame.time.get_ticks()
        self.counter = 0

        self.start = False
        self.round = 0
        self.len_wave = len(WAVES[0])
        self.opponent_number = 0

        self.next_round = False
        self.tower_buying = False
        self.tower_is_selected = False

        self.base_health = 100
        self.points = 0
        self.money = STARTING_MONEY

        #self.interface_up_height = 117
        #self.change_interface = False
        #self.previous = []

        self.clock = pygame.time.Clock()
        self.mouse_pos = STARTING_MOUSE_POSITION


    def rounds(self):
        self.counter += self.time
        self.next_round = True
        if self.round < LEN_WAVES:
        #if self.start:
        #    self.counter += self.time

            if (self.counter - self.opponents_counter > OPPONENTS_GAP
              and self.opponent_number < self.len_wave):

                self.opponents.append(Przeciwnik(self.round, self.opponent_number))
                self.opponent_number += 1
                self.opponents_counter = self.counter

            elif self.opponent_number == self.len_wave and self.next_round:
                self.next_round = False
                self.opponent_number = 0
                self.round += 1

                if self.round < LEN_WAVES:
                    self.len_wave = len(WAVES[self.round])
                else:
                    self.len_wave = len(WAVES[-1])

    def events(self):
        #self.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.tower_buying or self.tower_is_selected:
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

                if self.mouse_pos[0] < MAP_WIDTH and self.mouse_pos[1] < MAP_HEIGHT:
                    if self.tower_buying:
                        self.place_tower()

                    else:
                        for tower in self.towers:
                            if tower.obiekt.collidepoint(self.mouse_pos):
                                #self.change_interface = True
                                self.tower_is_selected = True
                                self.choosen_tower = tower
                                break

                        else:
                            self.player.strzelam = not self.player.strzelam
                            self.tower_flags_to_False()

                elif TEXTURES[0][1].collidepoint(self.mouse_pos):
                    self.new_round()

                elif TEXTURES[1][1].collidepoint(self.mouse_pos):
                    sys.exit()

                else:
                    for i, texture in enumerate(TEXTURES[2:5]):
                        if texture[1].collidepoint(self.mouse_pos):
                            self.tower_to_buy(i)
                            break

                    if self.tower_is_selected:
                        choosen_4 = (self.choosen_tower.rodzaj * 4)

                        for i in range(choosen_4 - 4, choosen_4):
                            if TOWER_TEXTURES[i][1].collidepoint(self.mouse_pos):
                                self.choosen_tower.upgrade(self, i)
                                break


    def update(self):
        self.player.shoot(self)
        self.player.move(self.dt)

        self.update_opponents()
        self.update_bullets()
        self.update_towers()

    def update_opponents(self):
        for opponent in self.opponents:
            opponent.move(self.dt)

            if opponent.obiekt.colliderect(BASE_RECT):
                self.base_health -= opponent.atak
                self.opponents.remove(opponent)

                if self.base_health <= 0:
                    sys.exit()

                continue

            elif opponent.obiekt.colliderect(self.player.obiekt):
                self.player.zdrowie -= opponent.atak * self.dt * 60

                if self.player.zdrowie <= 0:
                    sys.exit()
            # for drawing
            opponent.is_electrified = False

    def update_bullets(self):
        opponents_rects_list = [opponent.obiekt for opponent in self.opponents]

        for i, bullet in enumerate(self.bullets):
            bullet.move(self.dt)

            if bullet.rodzaj != 'gracz' and (bullet.data_konca < self.counter):
                self.bullets.pop(i)
                continue

            if bullet.obiekt.x < 0 or bullet.obiekt.y < 0 or bullet.obiekt.x > W_8_ or bullet.obiekt.y > H_8_:
                self.bullets.pop(i)
                continue

            collided_opponent_index = bullet.obiekt.collidelist(opponents_rects_list)
            if collided_opponent_index != -1:
                opponent = self.opponents[collided_opponent_index]

                if bullet.rodzaj == 2 and (bullet.id not in opponent.ids):
                    opponent.lose_hp(bullet.obrazenia)
                    opponent.ids.append(bullet.id)
                    bullet.przebicie -= 1

                    if bullet.przebicie == 0:
                        self.bullets.pop(i)

                elif bullet.rodzaj != 2:
                    opponent.lose_hp(bullet.obrazenia)
                    self.bullets.pop(i)

                if opponent.zdrowie <= 0:
                    self.points += opponent.points
                    self.money += opponent.monety

                    self.opponents.pop(collided_opponent_index)
                    opponents_rects_list.pop(collided_opponent_index)

                    if bullet.rodzaj == 'gracz':
                        self.player.doswiadczenie += opponent.points
                        self.player.check_level_up()

    def update_towers(self):
        for tower in self.towers:
            shooted_opponents = 0
            tower.mozna_strzelac = False

            if tower.rodzaj == 3:
                for i, opponent in enumerate(self.opponents):
                    x, y, rozmiar, _ = opponent.obiekt

                    if (
                      (x - tower.pole[0])**2 + (y - tower.pole[1])**2)**0.5 <= tower.zasieg \
                      or ((x + rozmiar - tower.pole[0])**2 + (y - tower.pole[1])**2)**0.5 <= tower.zasieg \
                      or ((x - tower.pole[0])**2 + (y + rozmiar - tower.pole[1])**2)**0.5 <= tower.zasieg \
                      or ((x + rozmiar - tower.pole[0])**2 + (y + rozmiar - tower.pole[1])**2)**0.5 <= tower.zasieg:

                        if tower.elektryzacja > 0:
                            opponent.lose_hp(tower.elektryzacja)

                            if opponent.zdrowie <= 0:
                                self.opponents.pop(i)

                            opponent.is_electrified = True

            for opponent in self.opponents:
                x, y, rozmiar, _ = opponent.obiekt

                if (
                  (x - tower.pole[0])**2 + (y - tower.pole[1])**2)**0.5 <= tower.zasieg \
                  or ((x + rozmiar - tower.pole[0])**2 + (y - tower.pole[1])**2)**0.5 <= tower.zasieg \
                  or ((x - tower.pole[0])**2 + (y + rozmiar - tower.pole[1])**2)**0.5 <= tower.zasieg \
                  or ((x + rozmiar - tower.pole[0])**2 + (y + rozmiar - tower.pole[1])**2)**0.5 <= tower.zasieg:

                    tower.shoot(self, opponent)
                    shooted_opponents += 1

                    if tower.rodzaj != 3 or shooted_opponents == tower.ilu_na_raz:
                        break


    def draw(self):
        window = self.game_window
        player = self.player

        window.blits(((GRASS, (0, 0)), *MAP_DRAW, (FOREST, BASE_RECT)))

        for tower in self.towers:
            window.blit(tower.typ, tower.obiekt)

        for opponent in self.opponents:
            window.blit(opponent.rodzaj, opponent.obiekt)

            pygame.draw.rect(window, WHITE, opponent.hp_bar)
            if opponent.startowe_zdrowie > opponent.zdrowie:
                pygame.draw.rect(window, RED, opponent.hp_bar_lost)

            if opponent.is_electrified:
                window.blit(ELECTRO, (opponent.obiekt.x - ((opponent.rozmiar - 15) / 2), opponent.obiekt.y - ((opponent.rozmiar - 15) / 2)))

        pygame.draw.rect(window, (0,0,0), (MAP_WIDTH, 0, MENUSIZE, MAP_HEIGHT))

        window.blits((
            (FONT30.render(f'Round:{self.round + self.start}', True, WHITE), (W_57, H_105_)),

            *TEXTURES,

            (FONT30.render(f'{player.poziom} | {round(100 * (player.doswiadczenie - player.do_poprzedniego) / (player.do_nastepnego - player.do_poprzedniego), 2)}%', True, WHITE), (W_23, 2)),
            (FONT30.render(f'{player.obrazenia} | {1000 / player.przeladowanie}', True, WHITE), (W_23, 23)),
            (FONT30.render(f'{player.predkosc}', True, WHITE), (W_23, 41)),
            (FONT30.render(f'{int(player.zdrowie)}', True, WHITE), (W_23, 59)),
            (FONT30.render(f'{self.money}', True, WHITE), (W_23, 81)),
            (FONT30.render(f'Points: {self.points}', True, WHITE), (W_10, 100)),

            (FONT30.render('10$', True, WHITE), (W_115, H_73_)),
            (FONT30.render('30$', True, WHITE), (W_115, H_48_)),
            (FONT30.render('50$', True, WHITE), (W_115, H_23_)),
            (FONT30.render('1.', True, WHITE), (W_75, H_73_)),
            (FONT30.render('2.', True, WHITE), (W_75, H_48_)),
            (FONT30.render('3.', True, WHITE), (W_75, H_23_)),

            (FONT40.render(f'{self.base_health}', True, WHITE), BASE_HP_STRING),

            (DRUID, player.obiekt)
        ))

        self.draw_health_bar(player)

        if self.tower_is_selected:
            tower = self.choosen_tower
            window.blits((
                *TOWER_TEXTURES[(tower.rodzaj - 1) * 4 : tower.rodzaj * 4],

                (FONT30.render(f'{WIEZE_POLEPSZENIA[tower.rodzaj - 1][0][0]}$'    , True, RED), (TOWER_TEXTURES[0][1][0], TOWER_TEXTURES[0][1][1] + 50)),
                (FONT30.render(f'{WIEZE_POLEPSZENIA[tower.rodzaj - 1][1][0]}$'  , True, RED), (TOWER_TEXTURES[1][1][0], TOWER_TEXTURES[1][1][1] + 50)),
                (FONT30.render(f'{WIEZE_POLEPSZENIA[tower.rodzaj - 1][2]}$'  , True, RED), (TOWER_TEXTURES[2][1][0], TOWER_TEXTURES[2][1][1] + 50)),
                (FONT30.render(f'{tower.cena_calkowita}$', True, RED), (TOWER_TEXTURES[3][1][0], TOWER_TEXTURES[3][1][1] + 50)),
                (FONT30.render(f'{tower.poziom_atak}'    , True, PURPLE), (TOWER_TEXTURES[0][1][0], TOWER_TEXTURES[0][1][1])),
                (FONT30.render(f'{tower.poziom_zasieg}'  , True, PURPLE), (TOWER_TEXTURES[1][1][0], TOWER_TEXTURES[1][1][1])),
                (FONT30.render(f'{tower.poziom_reszta}'  , True, PURPLE), (TOWER_TEXTURES[2][1][0], TOWER_TEXTURES[2][1][1])),
            ))

            pygame.draw.circle(window, tower.kolor, tower.pole, tower.zasieg, 2)

        for bullet in self.bullets:
            if bullet.rodzaj == 'gracz':
                window.blit(MAGIC_BALL, bullet.obiekt)
            else:
                pygame.draw.rect(window, bullet.kolor, bullet.obiekt)

        if self.tower_buying:
            pygame.draw.rect(window, self.tower_to_buy_color, (self.mouse_pos[0] - 10, self.mouse_pos[1] - 10, 20, 20))
            pygame.draw.circle(window, self.tower_to_buy_color, self.mouse_pos, self.tower_to_buy_range, 2)

        pygame.display.update()

    def draw_health_bar(self, player):
        state = int((player.zdrowie / (player.max_zdrowie + 1)) * 5)
        bar_width = pygame.Rect((player.x, player.y - 5, player.zdrowie / player.max_zdrowie * DRUID_SIZE, 5))

        if state == 4:
            color = (player.max_zdrowie - player.zdrowie) / player.max_zdrowie
            pygame.draw.rect(self.game_window, (0, int(1275 * color), 255), bar_width)

        elif state == 3:
            color = (player.zdrowie - (3 * player.max_zdrowie / 5)) / player.max_zdrowie
            pygame.draw.rect(self.game_window, (0, 255, int(1275 * color)), bar_width)

        elif state == 2:
            color = ((3 * player.max_zdrowie / 5) - player.zdrowie) / player.max_zdrowie
            pygame.draw.rect(self.game_window, (int(1275 * color), 255, 0), bar_width)

        elif state == 1:
            color = (player.zdrowie - (player.max_zdrowie / 5)) / player.max_zdrowie
            pygame.draw.rect(self.game_window, (255, int(1275 * color), 0), bar_width)

        else:
            color = (player.zdrowie / player.max_zdrowie)
            pygame.draw.rect(self.game_window, (int(1275 * color), 0, 0), bar_width)


    def new_round(self):
        self.start = True

        if self.counter != 0:
            self.next_round = True

    def pause_loop(self):

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
        self.tower_buying = True
        self.tower_to_buy_type = (i + 1)
        self.tower_to_buy_range = WIEZE[i][5]
        self.tower_to_buy_color = WIEZE[i][1]

    def place_tower(self):
        new_tower_rect = pygame.Rect(self.mouse_pos[0] - 10, self.mouse_pos[1] - 10, 20, 20)

        for tile in MAP_DRAW:
            if (pygame.Rect(*tile[1], TILESIZE, TILESIZE).colliderect(new_tower_rect)
              or BASE_RECT.colliderect(new_tower_rect)
              or self.mouse_pos[0] < 10
              or self.mouse_pos[1] < 10
              or self.mouse_pos[0] > W_10_
              or self.mouse_pos[1] > H_10_):

                self.tower_buying = False
                return

        for tower in self.towers:
            if tower.obiekt.colliderect(new_tower_rect):
                self.tower_buying = False
                return

        self.choosen_tower = Wieza(self.mouse_pos, self.tower_to_buy_type, self.counter, self.dt)
        self.towers.append(self.choosen_tower)
        self.money -= self.towers[-1].cena_calkowita
        if (not self.tower_buying) or (self.money < 0):
            self.sell_tower(self.towers[-1].cena_calkowita)
        else:
            self.tower_is_selected = True

        self.tower_buying = False

    def sell_tower(self, full_price):
        self.tower_flags_to_False()
        self.money += full_price
        self.towers.remove(self.choosen_tower)

    def tower_flags_to_False(self):
        #self.change_interface = False
        self.tower_buying = False
        self.tower_is_selected = False


if __name__ == '__main__':
    Gra()
