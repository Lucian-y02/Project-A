import pygame

from constants import *
from player import Player
from game_stuff import *
from Silver_Box import level_updater


pygame.init()


class Scene:
    def __init__(self, **kwargs):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.game_run = True

        # Flags
        self.show_fps = False
        self.show_grid = False
        self.mouse_visible = kwargs.get("mouse_visible", False)

        # Groups
        self.groups_data = {
            "players": pygame.sprite.Group(),
            "walls": pygame.sprite.Group()
        }

        # Level
        self.level_path_now = ""

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP
                                             and event.key == pygame.K_DELETE):
                self.game_run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    self.show_grid = not self.show_grid
                elif event.key == pygame.K_f:
                    self.show_fps = not self.show_fps

        # Objects update
        for key in self.groups_data:
            self.groups_data[key].update()

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)

        # Grid render
        if self.show_grid:
            for x in range(SCREEN_SIZE[0] // GRID_SIZE + 1):
                pygame.draw.line(self.screen, GRID_COLOR,
                                 (x * GRID_SIZE, 0), (x * GRID_SIZE, SCREEN_SIZE[1]))
            for y in range(SCREEN_SIZE[1] // GRID_SIZE + 1):
                pygame.draw.line(self.screen, GRID_COLOR,
                                 (0, y * GRID_SIZE), (SCREEN_SIZE[0], y * GRID_SIZE))

        # Game objects render
        for key in self.groups_data:
            self.groups_data[key].draw(self.screen)

    def play(self):
        pygame.mouse.set_visible(self.mouse_visible)
        while self.game_run:
            self.check_events()
            self.render()

            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()
        quit()

    def load_level_on_scene(self, path):
        self.level_path_now = path
        self.clear_groups_data()
        level_updater.load_level(path, self.groups_data)

    def clear_groups_data(self):
        for key in self.groups_data:
            self.groups_data[key].remove(self.groups_data[key])


if __name__ == "__main__":
    scene = Scene()
    scene.load_level_on_scene("Levels/Demo/test_level.json")
    scene.play()
