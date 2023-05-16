"""scenes.py module"""

import sys
from threading import Thread, active_count

from basic_engine import scene
from pygame import constants

from . import algorithms, cubes


class SplashScreenScene(scene.Scene):
    """Scene that renders a splash screen."""

    def __init__(self, screen):
        super().__init__(screen)

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))

    def update(self) -> None:
        return super().update()


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
