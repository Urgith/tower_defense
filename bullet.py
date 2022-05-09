from _CONSTANTS import *


class Bullet:

    def __init__(self, tower, mouse_pos, counter, opponent=None):
        self.kind = tower.kind

        if self.kind == 'player':
            self.damage = tower.damage
            self.speed = tower.bullet_speed
            self.tower_id = self.kind

            tower_rect = tower.rect
            tower_rect.move_ip(DRUID_BY_10_PLUS_1, DRUID_BY_20)
            self.position = pygame_math_Vector2(tower_rect.x, tower_rect.y)
            self.rect = pygame_Rect(self.position.x, self.position.y, 8, 8)

            (x, y) = (mouse_pos - self.position)

        else:
            if self.kind == 1:
                self.id = random_random()
                self.pierce = tower.pierce

            elif self.kind == 2:
                self.electro = tower.electro

            self.end_date = tower.lifespan + counter
            self.damage = tower.damage
            self.speed = tower.speed
            self.tower_id = tower.id

            self.position = pygame_math_Vector2(tower.rect.centerx - (tower.bullet_size // 2), tower.rect.centery - (tower.bullet_size // 2))
            self.rect = pygame_Rect(self.position.x, self.position.y, tower.bullet_size, tower.bullet_size)
            self.color = BULLET_COLORS[self.kind]

            (x, y) = (opponent.x + (opponent.size / 2) - self.position.x,
                   opponent.y + (opponent.size / 2) - self.position.y)

        self.direction = pygame_math_Vector2(x, y) * self.speed / ((x**2 + y**2) ** 0.5)

    def move(self, dt):
        self.position += (self.direction * dt)
        self.rect.topleft = self.position
