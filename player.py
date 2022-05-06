from _CONSTANTS import *
from bullet import Bullet


class Player:

    def __init__(self, opponents_counter):
        self.shooting_counter = opponents_counter

        self.x, self.y = (DRUID_X, DRUID_Y)
        self.rect = pygame_Rect(self.x, self.y, DRUID_SIZE, DRUID_SIZE)
        #self.previous_obiekt = pygame_Rect(self.x, self.y, DRUID_SIZE, DRUID_SIZE)

        self.experience = 0
        self.level = 0
        self.to_previous = 0
        self.to_next = 10

        self.health = self.max_health = 1000
        self.reload = FIRE_RATE
        self.damage = 10
        self.speed = 100

        self.bullet_speed = 200
        self.shooting = FIRING

        self.kind = 'player'

    def move(self, dt):
        #self.previous_obiekt.x, self.previous_obiekt.y = (self.x, self.y)

        pressed = pygame_key_get_pressed()
        x, y = (0, 0)

        if pressed[K_w]:
            self.y -= self.speed * dt
            y = -1

        if pressed[K_a]:
            self.x -= self.speed * dt
            x = -1

        if pressed[K_s]:
            self.y += self.speed * dt
            y = 1

        if pressed[K_d]:
            self.x += self.speed * dt
            x = 1
        # 0.4 ~= 2**0.5 - 1
        if x and y:
            self.x -= 0.414 * x * self.speed * dt
            self.y -= 0.414 * y * self.speed * dt

        if self.x < 0:
            self.x = 0
        elif self.x > W_MINUS_DRUID:
            self.x = W_MINUS_DRUID

        if self.y < 0:
            self.y = 0
        elif self.y > H_MINUS_DRUID:
            self.y = H_MINUS_DRUID

        self.rect.x, self.rect.y = (self.x, self.y)

    def shoot(self, game):
        if self.shooting and (game.counter - self.shooting_counter > self.reload):
            game.bullets.append(Bullet(self, game.mouse_pos, game.counter))
            self.shooting_counter = game.counter

    def check_level_up(self):
        if self.experience >= self.to_next:
            self.level += 1
            level = self.level

            self.speed = 100 + (10 * level)
            self.damage = 10 + int(((level + 1) * level) / 2)
            self.reload = 1000 / (4 + (level / 10))

            self.max_health = int(1000 * (1 + (level / 10)))
            self.health = self.max_health

            self.bullet_speed = 200 + (20 * level)

            self.to_previous = self.to_next
            self.to_next = 20 * (1 + level) ** math_log(1 + level, 4)
