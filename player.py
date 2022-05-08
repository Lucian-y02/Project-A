import pygame

from constants import *


pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, groups: dict, coord, **kwargs):
        super(Player, self).__init__(groups["players"])
        self.image = pygame.Surface((44, 64))
        self.image.fill(DEFAULT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] * GRID_SIZE + (GRID_SIZE - self.rect.width) // 2
        self.rect.y = coord[1] * GRID_SIZE + (GRID_SIZE - self.rect.height) // 2

        # Move
        if kwargs.get("control", "keyboard_1") == "game_pad_1":
            self.game_pad = pygame.joystick.Joystick(0)
            self.check_events = self.game_pad_check_pressing
        elif kwargs.get("control", "keyboard_1") == "game_pad_2":
            self.game_pad = pygame.joystick.Joystick(1)
            self.check_events = self.game_pad_check_pressing
        elif kwargs.get("control", "keyboard_1") == "keyboard_1":
            self.check_events = self.keyboard_1_check_pressing
        else:
            self.check_events = self.keyboard_2_check_pressing
        self.move_x = 0
        self.move_y = 0
        self.speed = PLAYER_DEFAULT_SPEED

    def update(self):
        self.move_x = 0
        self.move_y = 0

        self.check_events()
        self.check_collision()

        self.rect.move_ip(self.move_x, self.move_y)

    def keyboard_1_check_pressing(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            self.move_x += self.speed
        if key[pygame.K_a]:
            self.move_x -= self.speed

    def keyboard_2_check_pressing(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.move_x += self.speed
        if key[pygame.K_LEFT]:
            self.move_x -= self.speed

    def game_pad_check_pressing(self):
        if abs(self.game_pad.get_hat(0)[0]):
            self.move_x += self.speed * self.game_pad.get_hat(0)[0]
        elif abs(self.game_pad.get_axis(0)):
            self.move_x += self.speed * self.game_pad.get_axis(0)

    def check_collision(self):
        pass
