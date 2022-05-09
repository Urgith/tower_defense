from _CONSTANTS import *


class Opponent:

    def __init__(self, round, opponent_number, opponents_images):
        self.kind = WAVES[min(round, LEN_WAVES_1)][opponent_number][0]
        opponents_images.append(self.kind)

        (self.health, self.speed, self.damage, self.points,
            self.money, self.size) = ENEMIES[self.kind]

        self.TILESIZE_SIZE_BY_2 = (TILESIZE - self.size) // 2
        self.x, self.y = (self.TILESIZE_SIZE_BY_2, 0)
        self.hp_bar_x, self.hp_bar_y = (0, -5)
        self.mov_x, self.mov_y = (0, 0)

        self.rect = pygame_Rect(self.x, self.y, self.size, self.size)
        self.hp_bar = pygame_Rect(self.hp_bar_x, self.hp_bar_y, TILESIZE, 2)
        self.hp_bar_lost = pygame_Rect(TILESIZE, self.hp_bar_y, TILESIZE, 2)

        self.health = int(self.health * (1.1**round))
        self.max_health = self.health

        self.tile_x, self.tile_y = (0, TILESIZE_BY_2)
        self.tile = AREA[self.tile_y][self.tile_x]
        self.ids = []

        self.is_electrified = False

    def move(self, dt):
        if self.mov_x == 0:
            tile = AREA[int((self.rect.centery + self.mov_y) / TILESIZE)][self.tile_x]
        else:
            tile = AREA[self.tile_y][int((self.rect.centerx + self.mov_x) / TILESIZE)]

        if tile != self.tile and tile not in {0, 1, 10}:
            self.tile = tile

            if self.tile in {5, 50}:
                self.mov_x = -TILESIZE_BY_2
                self.mov_y = 0
            elif self.tile in {6, 60}:
                self.mov_x = TILESIZE_BY_2
                self.mov_y = 0
            elif self.tile in {7, 70}:
                self.mov_y = TILESIZE_BY_2
                self.mov_x = 0
            else:
                self.mov_y = -TILESIZE_BY_2
                self.mov_x = 0

            self.tile_x = int((self.rect.centerx + self.mov_x) / TILESIZE)
            self.tile_y = int((self.rect.centery + self.mov_y) / TILESIZE)

        if self.tile in {5, 50}:
            self.x += self.speed * dt

            self.rect.x = self.x
            self.hp_bar.x = self.x - self.TILESIZE_SIZE_BY_2
            self.hp_bar_lost.x = self.hp_bar.x + self.hp_bar.w

        elif self.tile in {6, 60}:
            self.x -= self.speed * dt
            
            self.rect.x = self.x
            self.hp_bar.x = self.x - self.TILESIZE_SIZE_BY_2
            self.hp_bar_lost.x = self.hp_bar.x + self.hp_bar.w

        elif self.tile in {7, 70}:
            self.y -= self.speed * dt
            self.rect.y = self.hp_bar.y = self.hp_bar_lost.y = self.y

        else:
            self.y += self.speed * dt
            self.rect.y = self.hp_bar.y = self.hp_bar_lost.y = self.y

    def lose_hp(self, damage, tower=None):
        damage = min(self.health, damage)

        self.health -= damage
        self.update_hp_bar()

        if tower is not None:
            tower.damage_dealt += damage

    def update_hp_bar(self):
        self.hp_bar.w = TILESIZE * (self.health / self.max_health)
        self.hp_bar_lost.w = TILESIZE - self.hp_bar.w

        self.hp_bar.x = self.x - self.TILESIZE_SIZE_BY_2
        self.hp_bar_lost.x = self.hp_bar.x + self.hp_bar.w
