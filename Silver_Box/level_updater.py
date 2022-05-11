import json
import pygame

from player import Player
from game_stuff import *


pygame.init()

# Доступные для размещения на уровне объекты
available_objects = {
    "Player": [Player, "all_the_groups"],
    "Box": [Box, "walls"],
    "PlatformLeft": [PlatformLeft, "walls"],
    "PlatformRight": [PlatformRight, "walls"],
    "PlatformMiddle": [PlatformMiddle, "walls"]
}


def get_available_objects():
    return available_objects


# Получение матрицы уровня
def get_level(path):
    l_level = None
    with open(path, "r") as level:
        l_level = json.load(level)
        level.close()
    return l_level


# Запись изменения уровня
def change_level(path, level_data):
    with open(path, "w") as level:
        json.dump(level_data, level)
        level.close()


# Загрузка уровня
def load_level(path, groups_data):
    level_data = get_level(path)
    for key in level_data:
        # Объект
        obj = available_objects[level_data[key][0]][0]
        # Группа или группы
        obj_group = groups_data \
            if available_objects[level_data[key][0]][1] == "all_the_groups" else \
            groups_data[available_objects[level_data[key][0]][1]]
        # Координаты
        obj_coord = (int(key.split()[0]), int(key.split()[1]))
        # Именованные аргументы
        obj_kwargs = level_data[key][1]
        # Создание объекта
        obj(obj_group, obj_coord, **obj_kwargs)
