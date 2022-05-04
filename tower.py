import pygame

from _STALE import *
from pocisk import Pocisk


class Tower:

    def __init__(self, mouse_pos, kind, counter, dt):
        self.rect = pygame.Rect(mouse_pos[0] - 10, mouse_pos[1] - 10, 20, 20)
        self.center = mouse_pos

        self.kind = kind
        self.counter = counter
        self.level_damage, self.level_range, self.level_special, self.level = (0, 0, 0, 0)

        (self.image, self.color, self.total_cost, self.damage, self.speed, self.range,
            self.reload, self.bullet_size) = TOWERS[self.kind]

        self.lifespan = self.range / self.speed * 1000

        if self.kind == 1:
            self.pierce = 2
        elif self.kind == 2:
            self.multishot = 2
            self.electro = 0.1 * dt * 60

    def shoot(self, game, opponent):
        if (game.counter - self.counter > self.reload) or self.can_shoot:
            game.bullets.append(Pocisk(self, game.mouse_pos, game.counter, opponent))
            self.counter = game.counter

            if self.kind == 2:
                self.can_shoot = True

        if self.kind == 2:
            opponent.lose_hp(self.electro)

    def upgrade(self, game, upgrade_id):

        if (upgrade_id % 4) == 3:
            game.sell_tower(self.total_cost)

        if (upgrade_id % 4) == 0 and (game.money >= TOWER_UPGRADES[self.kind][0][0]) and (self.level_damage <= 4):
            self.increase_damage(TOWER_UPGRADES[self.kind][0][1])
            self.increase_cost(game, TOWER_UPGRADES[self.kind][0][0])

            if self.kind == 2:
                self.multishot += 1

        elif (upgrade_id % 4) == 1 and (game.money >= TOWER_UPGRADES[self.kind][1][0]) and (self.level_range <= 4):
                self.increase_range(TOWER_UPGRADES[self.kind][1][1])
                self.increase_cost(game, TOWER_UPGRADES[self.kind][1][0])

        elif (upgrade_id % 4) == 2 and (self.level_special <= 4):
            self.increase_special(game)

        self.level = (self.level_damage + self.level_range + self.level_special) // 3
        self.image = TOWERS[self.kind + (self.level * 3)][0]

    def increase_cost(self, game, cost):
        game.money -= cost
        self.total_cost += cost

    def increase_damage(self, damage):
        self.damage += damage
        self.level_damage += 1

    def increase_range(self, range):
        self.range += range
        self.level_range += 1

        self.lifespan = (self.range / self.speed * 1000)

    def increase_special(self, game, reload=30, pierce_rate=2, electro_rate=4):

        if (game.money >= TOWER_UPGRADES[self.kind][2]):
            self.level_special += 1
            self.speed += 50
            self.increase_cost(game, TOWER_UPGRADES[self.kind][2])
            # 200 (INIT), 170, 140, 110, 80, 50
            if self.kind == 0:
                self.reload -= reload
            # 2 (INIT), 3, 5, 8, 12, 17
            elif self.kind == 1:
                self.pierce = 2 + (self.level_special * (self.level_special + 1) / pierce_rate)
            # 0.1 (INIT), 0.5, 1.5, 3, 5, 7.5
            elif self.kind == 2:
                self.electro = self.level_special * (self.level_special + 1) / electro_rate * game.dt * 60
