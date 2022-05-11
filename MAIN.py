from _CONSTANTS import *

from opponent import Opponent
from player import Player
from tower import Tower


class Game:

    def __init__(self, round):
        self.initialize_attributes(round)
        self.draw()
        pygame_display_update()

        while self.running:
            self.game_time()
            self.rounds()

            self.events()
            self.update()

            self.draw()
            self.display_update()

    def initialize_attributes(self, round):
        self.opponents_counter = pygame_time_get_ticks()
        self.player = Player(self.opponents_counter)

        self.len_opponents = 0
        self.opponents_rects = []
        self.opponents_images = []
        self.opponents = []

        self.bullets = []
        self.towers = {}

        self.start = START
        self.counter = 0

        self.opponent_number = OPPONENT
        self.round = (round - 1)

        round = min(LEN_WAVES_1, self.round)
        self.len_wave = len(WAVES[round])
        self.round_gaps = OPPONENTS_GAPS[round]
        self.gap = self.round_gaps[self.opponent_number]

        self.tower_is_selected = False
        self.tower_buying = False
        self.next_round = False

        self.base_health = BASE_HEALTH
        self.points = POINTS
        self.money = MONEY

        self.clock = pygame_time_Clock()
        self.mouse_pos = MOUSE_POSITION
        self.running = True


    def game_time(self):
        self.time = self.clock.tick(FRAMERATE)
        self.dt = (self.time * GAME_SPEED)

    def rounds(self):
        #if self.round < LEN_WAVES_1:
        #    self.next_round = True
        #else:
        #    self.next_round = False
        if self.start:
            self.counter += self.time

            if (self.counter - self.opponents_counter > self.gap
              and self.opponent_number < self.len_wave):

                self.opponents.append(Opponent(self.round, self.opponent_number, self.opponents_images))
                self.len_opponents += 1

                self.gap = self.round_gaps[self.opponent_number]
                self.opponents_counter = self.counter
                self.opponent_number += 1

            elif self.opponent_number == self.len_wave and self.next_round:
                self.opponent_number = 0
                self.next_round = False
                self.round += 1

                round = min(LEN_WAVES_1, self.round)
                self.round_gaps = OPPONENTS_GAPS[round]
                self.len_wave = len(WAVES[round])


    def events(self):
        self.mouse_pos = pygame_mouse_get_pos()
        self.interface_changed = False

        for event in pygame_event_get():
            if event.type == MOUSEBUTTONUP and event.button == 1:
                # MOUSE INSIDE MAP
                if self.mouse_pos[0] < MAP_WIDTH:
                    if self.tower_buying:
                        self.place_tower()
                    else:
                        self.check_tower_selection()
                # MOUSE OUTSIDE MAP
                else:
                    if not self.check_tower_texture():
                        if self.tower_buying:
                            self.place_tower()
                        elif self.tower_is_selected:
                            self.check_tower_upgrade()
                        else:
                            self.player.shooting = False

                    if TEXTURES[0][1].collidepoint(self.mouse_pos):
                        self.new_round()

                    elif TEXTURES[1][1].collidepoint(self.mouse_pos):
                        self.exit()
            # KEYBOARD
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.new_round()

                elif event.key in PYGAME_K1_K2_K3:
                    self.tower_to_buy(event.key - 49)

                elif event.key == K_ESCAPE:
                    if self.tower_is_selected or self.tower_buying:
                        self.tower_flags_to_False()
                    else:
                        self.exit()

                elif event.key == K_p:
                    self.pause_loop()
            # EXIT
            elif event.type == QUIT:
                self.exit()

    def check_tower_selection(self):
        for tower in self.towers.values():
            if tower.rect.collidepoint(self.mouse_pos):
                self.tower_is_selected = True
                self.choosen_tower = tower
                return

        self.player.shooting = not self.player.shooting
        self.tower_flags_to_False()

    def check_tower_texture(self):
        for i, texture in enumerate(TEXTURES[2:5]):
            if texture[1].collidepoint(self.mouse_pos):
                self.tower_to_buy(i)
                return True

        return False

    def check_tower_upgrade(self):
        choosen_4 = (self.choosen_tower.kind * 4)

        for i in range(choosen_4, choosen_4 + 4):
            if TOWER_TEXTURES[i][1].collidepoint(self.mouse_pos):
                self.choosen_tower.upgrade(self, i)
                return

        self.tower_flags_to_False()


    def update(self):
        self.player.shoot(self)
        self.player.move(self.dt)

        self.update_opponents()
        self.update_bullets()
        self.update_towers()

    def update_opponents(self):
        for opponent in self.opponents:
            opponent.is_electrified = False
            opponent.move(self.dt)

        if self.len_opponents:
            self.opponents_rects = numpy_array([(opponent.rect.left, opponent.rect.top, opponent.rect.bottom, opponent.rect.right) for opponent in self.opponents], dtype=int)

            collided_opponent_index = cython_collidelist(BASE_RECT.left, BASE_RECT.top, BASE_RECT.bottom, BASE_RECT.right, self.opponents_rects)
            if collided_opponent_index != -1:
                self.base_health -= self.opponents[collided_opponent_index].damage
                self.kill_opponent(collided_opponent_index)

                if self.base_health <= 0:
                    self.exit()

        if self.len_opponents:
            collided_opponent_index = cython_collidelist(self.player.rect.left, self.player.rect.top, self.player.rect.bottom, self.player.rect.right, self.opponents_rects)

            if collided_opponent_index != -1:
                self.player.health -= (self.opponents[collided_opponent_index].damage * self.dt * 60)

                if self.player.health <= 0:
                    self.exit()

    def update_bullets(self):

        for i, bullet in enumerate(self.bullets):
            bullet.move(self.dt)
            # BULLET TERMINATION
            if bullet.kind != 'player' and (bullet.end_date < self.counter):
                self.bullets.pop(i)
                continue
            # BULLET OUTSIDE THE MAP
            if bullet.rect.x < 0 or bullet.rect.y < 0 or bullet.rect.x > W_8_ or bullet.rect.y > H_8_:
                self.bullets.pop(i)
                continue

            if self.len_opponents:
                collided_opponent_index = cython_collidelist(bullet.rect.left, bullet.rect.top, bullet.rect.bottom, bullet.rect.right, self.opponents_rects)

                if collided_opponent_index != -1:
                    opponent = self.opponents[collided_opponent_index]
                    '''MESS TO CLEAN'''
                    if bullet.kind == 1 and (bullet.id not in opponent.ids):
                        opponent.lose_hp(bullet.damage, self.towers.get(bullet.tower_id))
                        opponent.ids.append(bullet.id)
                        bullet.pierce -= 1

                        if bullet.pierce == 0:
                            self.bullets.pop(i)

                    elif bullet.kind != 1:
                        opponent.lose_hp(bullet.damage, self.towers.get(bullet.tower_id))
                        self.bullets.pop(i)

                    if opponent.health <= 0:
                        self.points += opponent.points
                        self.money += opponent.money

                        self.kill_opponent(collided_opponent_index)

                        if bullet.kind == 'player':
                            self.player.experience += opponent.points
                            self.player.check_level_up()

    def update_towers(self):
        '''MESS TO CLEAN'''
        for tower in self.towers.values():
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

                        opponent.lose_hp(tower.electro, tower)

                        if opponent.health <= 0:
                            self.kill_opponent(i)

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

    def kill_opponent(self, index):
        self.opponents_rects = numpy_delete(self.opponents_rects, index, 0)
        self.opponents_images.pop(index)
        self.opponents.pop(index)

        self.len_opponents -= 1


    def draw(self):
        player = self.player

        WINDOW_blits((GRASS, *TRACE_TILES, FOREST))

        for tower in self.towers.values():
            WINDOW_blit(tower.image, tower.rect)

        WINDOW_blits(tuple(zip(self.opponents_images, self.opponents_rects)))
        for opponent in self.opponents:
            pygame_draw_rect(WINDOW, WHITE, opponent.hp_bar)
            if opponent.max_health > opponent.health:
                pygame_draw_rect(WINDOW, RED, opponent.hp_bar_lost)

            if opponent.is_electrified:
                WINDOW_blit(ELECTRO, (opponent.rect.x - ((opponent.size - 15) / 2), opponent.rect.y - ((opponent.size - 15) / 2)))

        if self.tower_is_selected:
            pygame_draw_circle(WINDOW, self.choosen_tower.color, self.choosen_tower.center, self.choosen_tower.range, 2)

        if self.tower_buying:
            pygame_draw_rect(WINDOW, self.tower_to_buy_color, (max(0, min(MAP_WIDTH - 20, self.mouse_pos[0] - 10)), max(0, min(MAP_HEIGHT - 20, self.mouse_pos[1] - 10)), 20, 20))
            pygame_draw_circle(WINDOW, self.tower_to_buy_color, (max(0, min(MAP_WIDTH - 20, self.mouse_pos[0] - 10)) + 10, max(0, min(MAP_HEIGHT - 20, self.mouse_pos[1] - 10)) + 10), self.tower_to_buy_range, 2)

        pygame_draw_rect(WINDOW, (64, 64, 64), (MAP_WIDTH, 0, MENUSIZE, MAP_HEIGHT))

        WINDOW_blits((
            (FONT30_render(f'Round:{self.round + self.start}', True, WHITE), (W_57, H_105_)),

            *TEXTURES,

            (FONT30_render(f'{player.level} | {round(100 * (player.experience - player.to_previous) / (player.to_next - player.to_previous), 2)}%', True, WHITE), PLAYER_LEVEL_RECT),
            (FONT30_render(f'{player.damage} | {round(1000 / player.reload, 2)}', True, WHITE), PLAYER_DAMAGE_RECT),
            (FONT30_render(f'{player.speed}', True, WHITE), PLAYER_SPEED_RECT),
            (FONT30_render(f'{int(player.health)}', True, WHITE), PLAYER_HEALTH_RECT),
            (FONT30_render(f'{self.money}', True, WHITE), PLAYER_MONEY_RECT),
            (FONT30_render(f'Points: {self.points}', True, WHITE), POINTS_RECT),

            (FONT30_render('10$', True, WHITE), RECT_10_DOL),
            (FONT30_render('30$', True, WHITE), RECT_30_DOL),
            (FONT30_render('50$', True, WHITE), RECT_50_DOL),
            (FONT30_render('1.', True, WHITE), DOT_1),
            (FONT30_render('2.', True, WHITE), DOT_2),
            (FONT30_render('3.', True, WHITE), DOT_3),

            (FONT40_render(f'{self.base_health}', True, WHITE), BASE_HP_STRING),

            (DRUID, player.rect)
        ))

        self.draw_health_bar(player)

        if self.tower_is_selected:
            self.blit_tower_textures()

        for bullet in self.bullets:
            if bullet.kind == 'player':
                WINDOW_blit(MAGIC_BALL, bullet.rect)
            else:
                pygame_draw_rect(WINDOW, bullet.color, bullet.rect)

    def draw_health_bar(self, player):
        state = int((player.health / (player.max_health + 1)) * 5)
        bar_width = pygame_Rect((player.x, player.y - 5, player.health / player.max_health * DRUID_SIZE, 5))

        if state == 4:
            color = (player.max_health - player.health) / player.max_health
            pygame_draw_rect(WINDOW, (0, int(1275 * color), 255), bar_width)

        elif state == 3:
            color = (player.health - (3 * player.max_health / 5)) / player.max_health
            pygame_draw_rect(WINDOW, (0, 255, int(1275 * color)), bar_width)

        elif state == 2:
            color = ((3 * player.max_health / 5) - player.health) / player.max_health
            pygame_draw_rect(WINDOW, (int(1275 * color), 255, 0), bar_width)

        elif state == 1:
            color = (player.health - (player.max_health / 5)) / player.max_health
            pygame_draw_rect(WINDOW, (255, int(1275 * color), 0), bar_width)

        else:
            color = (player.health / player.max_health)
            pygame_draw_rect(WINDOW, (int(1275 * color), 0, 0), bar_width)

    def blit_tower_textures(self):
        tower = self.choosen_tower
        tower4 = (tower.kind * 4)

        WINDOW_blits((
            *TOWER_TEXTURES[tower4 : (tower4 + 4)],

            (FONT30_render(f'{TOWER_UPGRADES[tower.kind][0][0]}$', True, RED), TOWER_TEXTURES[0][1].move(0, 50)),
            (FONT30_render(f'{TOWER_UPGRADES[tower.kind][1][0]}$', True, RED), TOWER_TEXTURES[1][1].move(0, 50)),
            (FONT30_render(f'{TOWER_UPGRADES[tower.kind][2]}$', True, RED), TOWER_TEXTURES[2][1].move(0, 50)),
            (FONT30_render(f'{tower.total_cost}$', True, RED), TOWER_TEXTURES[3][1].move(0, 50)),
            (FONT30_render(f'{tower.level_damage}', True, PURPLE), TOWER_TEXTURES[0][1]),
            (FONT30_render(f'{tower.level_range}', True, PURPLE), TOWER_TEXTURES[1][1]),
            (FONT30_render(f'{tower.level_special}', True, PURPLE), TOWER_TEXTURES[2][1]),
            (FONT30_render('Damage dealt:', True, WHITE), TOWER_TEXTURES[2][1].move(0, 75)),
            (FONT30_render(f'{int(tower.damage_dealt)}', True, WHITE), TOWER_TEXTURES[2][1].move(0, 95))
        ))

    def display_update(self):
        if self.tower_is_selected or self.interface_changed:
            update_rects[1] = TOWER_INTERFACE_RECT
        else:
            update_rects[1] = INTERFACE_RECT

        pygame_display_update(update_rects)


    def new_round(self):
        self.start = True

        if self.counter != 0:
            self.next_round = True

    def pause_loop(self):
        pause = True

        while pause:
            self.game_time()

            for event in pygame_event_get():
                if event.type == QUIT:
                    self.exit()
                elif event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_p):
                    pause = False

    def exit(self):
        self.running = False


    def tower_to_buy(self, index):
        self.tower_to_buy_color = TOWERS[index][1]
        self.tower_to_buy_range = TOWERS[index][5]
        self.tower_to_buy_type = index
        self.tower_buying = True

    def place_tower(self):
        new_tower_rect = pygame_Rect(max(0, min(MAP_WIDTH - 20, self.mouse_pos[0] - 10)), max(0, min(MAP_HEIGHT - 20, self.mouse_pos[1] - 10)), 20, 20)
        new_tower_id = pygame_time_get_ticks()

        for tile in TRACE_TILES:
            if (tile[1].colliderect(new_tower_rect)
              or BASE_RECT.colliderect(new_tower_rect)):

                self.tower_buying = False
                return

        for tower in self.towers.values():
            if tower.rect.colliderect(new_tower_rect):
                self.tower_buying = False
                return

        self.choosen_tower = Tower(new_tower_rect, self.tower_to_buy_type, self.counter, self.dt, new_tower_id)
        if self.choosen_tower.total_cost <= self.money:
            self.towers[new_tower_id] = self.choosen_tower
            self.money -= self.choosen_tower.total_cost
            self.tower_flags_to_False(is_selected=True)
            return

        self.tower_flags_to_False()

    def sell_tower(self, tower):
        self.money += tower.total_cost
        self.tower_flags_to_False()
        del self.towers[tower.id]

    def tower_flags_to_False(self, is_selected=False):
        self.tower_is_selected = is_selected
        self.tower_buying = False

        self.interface_changed = True


    def __str__(self):
        return (f'Number of opponents: {len(self.opponents)}\n'
                + f'Number of bullets: {len(self.bullets)}\n'
                + f'Number of towers: {len(self.towers)}')

    def __repr__(self):
        return f'Game({self.round + 1})'


if __name__ == '__main__':
    game = Game(round=ROUND)
