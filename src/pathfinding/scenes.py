"""scenes.py module"""

import sys
from threading import Thread, active_count

from basic_engine import scene, transition, interface
from pygame import constants, image, time, transform

from . import algorithms, cubes, icon_path


class SplashScreenScene(scene.Scene):
    """Scene that renders a splash screen."""

    END_INTRO = constants.USEREVENT + 1

    def __init__(self, screen):
        super().__init__(screen)

        self.bg_colour = (255, 255, 255)
        self.app_icon = transform.scale(image.load(icon_path), (64, 64))
        self.app_label = interface.Label(self.screen,
                                         "App made by smolBlackCat",
                                         colour=(0, 0, 0), size=36, chars_per_line=20)
        self.app_icon_rect = self.app_icon.get_rect()
        self.app_icon_rect.center = self.screen_rect.center
        self.app_label.rect.center = self.screen_rect.center
        self.app_label.rect.y += self.app_icon_rect.width + 30

        time.set_timer(self.END_INTRO, 3000, 1)

    def draw(self) -> None:
        self.screen.fill(self.bg_colour)
        self.screen.blit(self.app_icon, self.app_icon_rect)
        self.app_label.draw()
        

    def update_on_event(self, event) -> None:
        if event.type == self.END_INTRO:
            self.scene_manager.change_scene(
                "main",
                transition.FadeTransition(
                    self.screen, self.scene_manager, "main", self.bg_colour, 4
                ),
            )


class ApplicationScene(scene.Scene):
    """Scene that renders all the application."""

    def __init__(self, screen):
        super().__init__(screen)

        self.cube = cubes.CharacterCube(screen)
        self.paths = cubes.PathCubeList(screen)

        self.pathfinding_algorithms = []

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        self.paths.draw()
        self.cube.draw()

    def update(self) -> None:
        self.paths.update()

    def update_on_event(self, event) -> None:
        if event.type == constants.QUIT:
            sys.exit()
        elif event.type == constants.KEYDOWN:
            if event.key == constants.K_r:
                self.paths.unblock_all()
                self.cube.reset_pos()
            elif event.key == constants.K_s:
                if active_count() == 1 and self.paths.get_objective() is not None:
                    Thread(
                        target=algorithms.astar,
                        args=(self.cube, self.paths),
                        daemon=True,
                    ).start()

            # Computing the directions clicks.
            elif event.key == constants.K_UP:
                self.cube.rect.y -= cubes.SIDE_LENGTH
            elif event.key == constants.K_DOWN:
                self.cube.rect.y += cubes.SIDE_LENGTH
            elif event.key == constants.K_RIGHT:
                self.cube.rect.x += cubes.SIDE_LENGTH
            elif event.key == constants.K_LEFT:
                self.cube.rect.x -= cubes.SIDE_LENGTH
