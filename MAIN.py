from _CONSTANTS import *

from player import Player
from opponent import Opponent
from tower import Tower


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

    def __str__(self):
        return (f'Number of opponents: {len(self.opponents)}\n'
                + f'Number of bullets: {len(self.bullets)}\n'
                + f'Number of towers: {len(self.towers)}')

    def initialize_attributes(self):
        self.opponents_counter = pygame_time_get_ticks()
        self.game_window = pygame_display_set_mode((MAP_WIDTH + MENUSIZE, MAP_HEIGHT), FULLSCREEN)
        self.player = Player(self.opponents_counter)

        self.opponents = []
        self.bullets = []
        self.towers = []

        self.counter = 0

        self.start = False
        self.round = 0
        self.opponent_number = 0

        self.len_wave = len(WAVES[self.round])
        self.round_gaps = OPPONENTS_GAPS[self.round]
        self.gap = self.round_gaps[self.opponent_number]

        self.next_round = False
        self.tower_buying = False
        self.tower_is_selected = False

        self.base_health = 100
        self.points = 0
        self.money = STARTING_MONEY

        #self.interface_up_height = 117
        #self.change_interface = False
        #self.previous = []

        self.clock = pygame_time_Clock()
        self.mouse_pos = STARTING_MOUSE_POSITION


    def rounds(self):
        '''MESS TO CLEAN, it should have like 5 lines or code, not 20...'''
        #self.counter += self.time
        #self.next_round = True
        #if self.round < LEN_WAVES:
        if self.start:
            self.counter += self.time

            if (self.counter - self.opponents_counter > self.gap
              and self.opponent_number < self.len_wave):

                self.opponents.append(Opponent(self.round, self.opponent_number))
                self.opponent_number += 1
                self.opponents_counter = self.counter

                if self.opponent_number < self.len_wave:
                    self.gap = self.round_gaps[self.opponent_number]

            elif self.opponent_number == self.len_wave and self.next_round:
                self.next_round = False
                self.opponent_number = 0
                self.round += 1

                if self.round < LEN_WAVES:
                    self.len_wave = len(WAVES[self.round])
                    self.round_gaps = OPPONENTS_GAPS[self.round]
                else:
                    self.len_wave = len(WAVES[-1])
                    self.round_gaps = OPPONENTS_GAPS[min(self.round, LEN_WAVES - 1)]

    def events(self):
        self.mouse_pos = pygame_mouse_get_pos()

        for event in pygame_event_get():
            if event.type == QUIT:
                exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.tower_buying or self.tower_is_selected:
                        self.tower_flags_to_False()
                    else:
                        print(self)
                        exit()

                elif event.key == K_p:
                    self.pause_loop()

                elif event.key in PYGAME_K1_K2_K3:
                    self.tower_to_buy(event.key - 49)

                elif event.key == K_SPACE:
                    self.new_round()

            elif event.type == MOUSEBUTTONUP and event.button == 1:

                if self.mouse_pos[0] < MAP_WIDTH and self.mouse_pos[1] < MAP_HEIGHT:
                    if self.tower_buying:
                        self.place_tower()

                    else:
                        for tower in self.towers:
                            if tower.rect.collidepoint(self.mouse_pos):
                                #self.change_interface = True
                                self.tower_is_selected = True
                                self.choosen_tower = tower
                                break

                        else:
                            self.player.shooting = not self.player.shooting
                            self.tower_flags_to_False()

                elif TEXTURES[0][1].collidepoint(self.mouse_pos):
                    self.new_round()

                elif TEXTURES[1][1].collidepoint(self.mouse_pos):
                    exit()

                else:
                    for i, texture in enumerate(TEXTURES[2:5]):
                        if texture[1].collidepoint(self.mouse_pos):
                            self.tower_to_buy(i)
                            break

                    if self.tower_is_selected:
                        choosen_4 = (self.choosen_tower.kind * 4)

                        for i in range(choosen_4, choosen_4 + 4):
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

            if opponent.rect.colliderect(BASE_RECT):
                self.base_health -= opponent.damage
                self.opponents.remove(opponent)

                if self.base_health <= 0:
                    exit()

                continue

            elif opponent.rect.colliderect(self.player.rect):
                self.player.health -= opponent.damage * self.dt * 60

                if self.player.health <= 0:
                    exit()
            # for drawing
            opponent.is_electrified = False

    def update_bullets(self):
        opponents_rects_list = [opponent.rect for opponent in self.opponents]

        for i, bullet in enumerate(self.bullets):
            bullet.move(self.dt)

            if bullet.kind != 'player' and (bullet.end_date < self.counter):
                self.bullets.pop(i)
                continue

            if bullet.rect.x < 0 or bullet.rect.y < 0 or bullet.rect.x > W_8_ or bullet.rect.y > H_8_:
                self.bullets.pop(i)
                continue

            collided_opponent_index = bullet.rect.collidelist(opponents_rects_list)
            if collided_opponent_index != -1:
                opponent = self.opponents[collided_opponent_index]

                if bullet.kind == 1 and (bullet.id not in opponent.ids):
                    opponent.lose_hp(bullet.damage)
                    opponent.ids.append(bullet.id)
                    bullet.pierce -= 1

                    if bullet.pierce == 0:
                        self.bullets.pop(i)

                elif bullet.kind != 1:
                    opponent.lose_hp(bullet.damage)
                    self.bullets.pop(i)

                if opponent.health <= 0:
                    self.points += opponent.points
                    self.money += opponent.money

                    self.opponents.pop(collided_opponent_index)
                    opponents_rects_list.pop(collided_opponent_index)

                    if bullet.kind == 'player':
                        self.player.experience += opponent.points
                        self.player.check_level_up()

    def update_towers(self):
        for tower in self.towers:
            shooted_opponents = 0
            tower.can_shoot = False

            if tower.kind == 2:
                for i, opponent in enumerate(self.opponents):
                    x, y, size, _ = opponent.rect

                    if (
                      (x - tower.center[0])**2 + (y - tower.center[1])**2)**0.5 <= tower.range \
                      or ((x + size - tower.center[0])**2 + (y - tower.center[1])**2)**0.5 <= tower.range \
                      or ((x - tower.center[0])**2 + (y + size - tower.center[1])**2)**0.5 <= tower.range \
                      or ((x + size - tower.center[0])**2 + (y + size - tower.center[1])**2)**0.5 <= tower.range \
                      and tower.electro > 0:

                        opponent.lose_hp(tower.electro)

                        if opponent.health <= 0:
                            self.opponents.pop(i)

                        opponent.is_electrified = True

            for opponent in self.opponents:
                x, y, size, _ = opponent.rect

                if (
                  (x - tower.center[0])**2 + (y - tower.center[1])**2)**0.5 <= tower.range \
                  or ((x + size - tower.center[0])**2 + (y - tower.center[1])**2)**0.5 <= tower.range \
                  or ((x - tower.center[0])**2 + (y + size - tower.center[1])**2)**0.5 <= tower.range \
                  or ((x + size - tower.center[0])**2 + (y + size - tower.center[1])**2)**0.5 <= tower.range:

                    tower.shoot(self, opponent)
                    shooted_opponents += 1

                    if tower.kind != 2 or shooted_opponents == tower.multishot:
                        break


    def draw(self):
        window = self.game_window
        player = self.player

        window.blits(((GRASS, (0, 0)), *MAP_DRAW, (FOREST, BASE_RECT)))

        for tower in self.towers:
            window.blit(tower.image, tower.rect)

        for opponent in self.opponents:
            window.blit(opponent.kind, opponent.rect)

            pygame_draw_rect(window, WHITE, opponent.hp_bar)
            if opponent.max_health > opponent.health:
                pygame_draw_rect(window, RED, opponent.hp_bar_lost)

            if opponent.is_electrified:
                window.blit(ELECTRO, (opponent.rect.x - ((opponent.size - 15) / 2), opponent.rect.y - ((opponent.size - 15) / 2)))

        pygame_draw_rect(window, (0,0,0), (MAP_WIDTH, 0, MENUSIZE, MAP_HEIGHT))

        window.blits((
            (FONT30.render(f'Round:{self.round + self.start}', True, WHITE), (W_57, H_105_)),

            *TEXTURES,

            (FONT30.render(f'{player.level} | {round(100 * (player.experience - player.to_previous) / (player.to_next - player.to_previous), 2)}%', True, WHITE), (W_23, 2)),
            (FONT30.render(f'{player.damage} | {round(1000 / player.reload, 2)}', True, WHITE), (W_23, 23)),
            (FONT30.render(f'{player.speed}', True, WHITE), (W_23, 41)),
            (FONT30.render(f'{int(player.health)}', True, WHITE), (W_23, 59)),
            (FONT30.render(f'{self.money}', True, WHITE), (W_23, 81)),
            (FONT30.render(f'Points: {self.points}', True, WHITE), (W_10, 100)),

            (FONT30.render('10$', True, WHITE), (W_115, H_73_)),
            (FONT30.render('30$', True, WHITE), (W_115, H_48_)),
            (FONT30.render('50$', True, WHITE), (W_115, H_23_)),
            (FONT30.render('1.', True, WHITE), (W_75, H_73_)),
            (FONT30.render('2.', True, WHITE), (W_75, H_48_)),
            (FONT30.render('3.', True, WHITE), (W_75, H_23_)),

            (FONT40.render(f'{self.base_health}', True, WHITE), BASE_HP_STRING),

            (DRUID, player.rect)
        ))

        self.draw_health_bar(player)

        if self.tower_is_selected:
            tower = self.choosen_tower
            tower4 = (tower.kind * 4)

            window.blits((
                *TOWER_TEXTURES[tower4 : (tower4 + 4)],

                (FONT30.render(f'{TOWER_UPGRADES[tower.kind][0][0]}$'    , True, RED), TOWER_TEXTURES[0][1].move(0, 50)),
                (FONT30.render(f'{TOWER_UPGRADES[tower.kind][1][0]}$'  , True, RED), TOWER_TEXTURES[1][1].move(0, 50)),
                (FONT30.render(f'{TOWER_UPGRADES[tower.kind][2]}$'  , True, RED), TOWER_TEXTURES[2][1].move(0, 50)),
                (FONT30.render(f'{tower.total_cost}$', True, RED), TOWER_TEXTURES[3][1].move(0, 50)),
                (FONT30.render(f'{tower.level_damage}', True, PURPLE), TOWER_TEXTURES[0][1]),
                (FONT30.render(f'{tower.level_range}', True, PURPLE), TOWER_TEXTURES[1][1]),
                (FONT30.render(f'{tower.level_special}', True, PURPLE), TOWER_TEXTURES[2][1]),
            ))

            pygame_draw_circle(window, tower.color, tower.center, tower.range, 2)

        for bullet in self.bullets:
            if bullet.kind == 'player':
                window.blit(MAGIC_BALL, bullet.rect)
            else:
                pygame_draw_rect(window, bullet.color, bullet.rect)

        if self.tower_buying:
            pygame_draw_rect(window, self.tower_to_buy_color, (self.mouse_pos[0] - 10, self.mouse_pos[1] - 10, 20, 20))
            pygame_draw_circle(window, self.tower_to_buy_color, self.mouse_pos, self.tower_to_buy_range, 2)

        pygame_display_update(GAME_RECT)

    def draw_health_bar(self, player):
        state = int((player.health / (player.max_health + 1)) * 5)
        bar_width = pygame_Rect((player.x, player.y - 5, player.health / player.max_health * DRUID_SIZE, 5))

        if state == 4:
            color = (player.max_health - player.health) / player.max_health
            pygame_draw_rect(self.game_window, (0, int(1275 * color), 255), bar_width)

        elif state == 3:
            color = (player.health - (3 * player.max_health / 5)) / player.max_health
            pygame_draw_rect(self.game_window, (0, 255, int(1275 * color)), bar_width)

        elif state == 2:
            color = ((3 * player.max_health / 5) - player.health) / player.max_health
            pygame_draw_rect(self.game_window, (int(1275 * color), 255, 0), bar_width)

        elif state == 1:
            color = (player.health - (player.max_health / 5)) / player.max_health
            pygame_draw_rect(self.game_window, (255, int(1275 * color), 0), bar_width)

        else:
            color = (player.health / player.max_health)
            pygame_draw_rect(self.game_window, (int(1275 * color), 0, 0), bar_width)


    def new_round(self):
        self.start = True

        if self.counter != 0:
            self.next_round = True

    def pause_loop(self):

        pause = True
        while pause:
            self.time = self.clock.tick(FRAMERATE)
            self.dt = self.time * GAME_SPEED

            for event in pygame_event_get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_p):
                    pause = False


    def tower_to_buy(self, i):
        self.tower_buying = True
        self.tower_to_buy_type = i
        self.tower_to_buy_range = TOWERS[i][5]
        self.tower_to_buy_color = TOWERS[i][1]

    def place_tower(self):
        new_tower_rect = pygame_Rect(self.mouse_pos[0] - 10, self.mouse_pos[1] - 10, 20, 20)

        for tile in MAP_DRAW:
            if (pygame_Rect(*tile[1], TILESIZE, TILESIZE).colliderect(new_tower_rect)
              or BASE_RECT.colliderect(new_tower_rect)
              or self.mouse_pos[0] < 10
              or self.mouse_pos[1] < 10
              or self.mouse_pos[0] > W_10_
              or self.mouse_pos[1] > H_10_):

                self.tower_buying = False
                return

        for tower in self.towers:
            if tower.rect.colliderect(new_tower_rect):
                self.tower_buying = False
                return

        self.choosen_tower = Tower(self.mouse_pos, self.tower_to_buy_type, self.counter, self.dt)
        self.towers.append(self.choosen_tower)
        self.money -= self.towers[-1].total_cost
        if (not self.tower_buying) or (self.money < 0):
            self.sell_tower(self.towers[-1].total_cost)
        else:
            self.tower_is_selected = True

        self.tower_buying = False

    def sell_tower(self, total_cost):
        self.tower_flags_to_False()
        self.money += total_cost
        self.towers.remove(self.choosen_tower)

    def tower_flags_to_False(self):
        #self.change_interface = False
        self.tower_buying = False
        self.tower_is_selected = False


if __name__ == '__main__':
    Gra()
