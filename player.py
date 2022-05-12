from time import sleep
import threading

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
        self.groups_data = groups

        # Control
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

        # Move
        self.move_x = 0
        self.move_y = 0
        self.speed = PLAYER_DEFAULT_SPEED
        # Jump
        self.do_jump = False
        self.jump_force = PLAYER_JUMP_FORCE
        self.jump_ready = False

    def update(self):
        self.move_x = 0
        self.move_y = 0

        self.check_events()
        self.move()
        self.wall_collision()

        self.rect.move_ip(self.move_x, self.move_y)

    def wall_collision(self):
        for wall in self.groups_data["walls"]:
            # WallHorizontal
            if self.rect.colliderect(wall.rect) and wall.__class__.__name__ == "WallHorizontal":
                self.rect.y = wall.rect.y - self.rect.height - 1
                self.jump_ready = True

            # WallVertical
            if self.rect.colliderect(wall.rect) and wall.__class__.__name__ == "WallVertical":
                pass

    def move(self):
        self.move_y += PLAYER_GRAVITY
        if self.do_jump:
            self.move_y -= self.jump_force

    def keyboard_1_check_pressing(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            self.move_x += self.speed
        if key[pygame.K_a]:
            self.move_x -= self.speed
        if key[pygame.K_w] and self.jump_ready:
            threading.Thread(target=self.jump).start()

    def keyboard_2_check_pressing(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.move_x += self.speed
        if key[pygame.K_LEFT]:
            self.move_x -= self.speed
        if key[pygame.K_UP] and self.jump_ready:
            threading.Thread(target=self.jump).start()

    def game_pad_check_pressing(self):
        if abs(self.game_pad.get_hat(0)[0]):
            self.move_x += self.speed * self.game_pad.get_hat(0)[0]
        elif abs(self.game_pad.get_axis(0)):
            self.move_x += self.speed * self.game_pad.get_axis(0)
        if self.game_pad.get_button(0) and self.jump_ready:
            threading.Thread(target=self.jump).start()

    def jump(self):
        self.jump_ready = False
        self.do_jump = True
        sleep(PLAYER_JUMP_TIME)
        self.do_jump = False
