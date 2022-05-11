import pygame

from constants import *


pygame.init()


# BASE OBJECTS ------------------------------------------------------------------------------------
class WallHorizontal(pygame.sprite.Sprite):
    def __init__(self, group, coord, **kwargs):
        super(WallHorizontal, self).__init__(group)
        self.image = pygame.Surface((GRID_SIZE - WALL_SHIFT * 2, 1))
        self.image.fill(DEFAULT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + WALL_SHIFT
        self.rect.y = coord[1]


class WallVertical(pygame.sprite.Sprite):
    def __init__(self, group, coord, **kwargs):
        super(WallVertical, self).__init__(group)
        self.image = pygame.Surface((1, GRID_SIZE - WALL_SHIFT * 2))
        self.image.fill(DEFAULT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1] + WALL_SHIFT


# MAIN OBJECTS ------------------------------------------------------------------------------------
class PlatformLeft:
    def __init__(self, group, coord, **kwargs):
        coord = (coord[0] * GRID_SIZE, coord[1] * GRID_SIZE)
        WallHorizontal(group, coord)
        WallHorizontal(group, (coord[0], coord[1] + GRID_SIZE))
        WallVertical(group, coord)


class PlatformMiddle:
    def __init__(self, group, coord, **kwargs):
        coord = (coord[0] * GRID_SIZE, coord[1] * GRID_SIZE)
        WallHorizontal(group, coord)
        WallHorizontal(group, (coord[0], coord[1] + GRID_SIZE))


class PlatformRight:
    def __init__(self, group, coord, **kwargs):
        coord = (coord[0] * GRID_SIZE, coord[1] * GRID_SIZE)
        WallHorizontal(group, coord)
        WallHorizontal(group, (coord[0], coord[1] + GRID_SIZE))
        WallVertical(group, (coord[0] + GRID_SIZE, coord[1]))


class Box:
    def __init__(self, group, coord, **kwargs):
        coord = (coord[0] * GRID_SIZE, coord[1] * GRID_SIZE)
        WallHorizontal(group, coord)
        WallHorizontal(group, (coord[0], coord[1] + GRID_SIZE))
        WallVertical(group, coord)
        WallVertical(group, (coord[0] + GRID_SIZE, coord[1]))
