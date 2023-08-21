"""scenes.py module"""

import sys
from threading import Thread, active_count

from basic_engine import scene, transition, interface
from pygame import constants, image, time, transform

from . import algorithms, cubes, languages, icon_path


class SplashScreenScene(scene.Scene):
    """Scene that renders a splash screen."""

    END_INTRO = constants.USEREVENT + 1

    def __init__(self, screen):
        super().__init__(screen)

        self.bg_colour = (255, 255, 255)
        self.app_icon = transform.scale(image.load(icon_path), (64, 64))
        self.app_label = interface.Label(
            self.screen,
            languages.message_map["main_title"],
            colour=(0, 0, 0),
            size=36,
            chars_per_line=20,
        )
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

        self.traversing = False
        self.cube = cubes.CharacterCube(screen)
        self.paths = cubes.PathCubeList(screen)

        self.algorithms_button_bar = interface.ButtonBar(
            self.screen,
            languages.message_map["algorithms_title"],
            "right",
            (
                languages.message_map["astar"],
                lambda: self.set_algorithm(
                    algorithms.astar, languages.message_map["astar"]
                ),
            ),
            (
                languages.message_map["dijkstra"],
                lambda: self.set_algorithm(
                    algorithms.dijkstra, languages.message_map["dijkstra"]
                ),
            ),
            (
                languages.message_map["dfs"],
                lambda: self.set_algorithm(
                    algorithms.dfs, languages.message_map["dfs"]
                ),
            ),
            (
                languages.message_map["bfs"],
                lambda: self.set_algorithm(
                    algorithms.bfs, languages.message_map["bfs"]
                ),
            ),
            bar_surface_colour=(41, 67, 92),
            bar_outline_colour=(21, 42, 56),
        )

        self.timer = interface.Chronometer(screen, (255, 255, 255))
        self.timer.rect.y += 10
        self.timer.rect.centerx = self.screen_rect.centerx

        self.label = interface.Label(
            screen,
            languages.message_map["no_selected_algorithm"],
            bold=True,
            size=24,
            colour=(255, 255, 255),
        )
        self.label.rect.topright = self.screen_rect.topright
        self.label.rect.x -= 10
        self.label.rect.y += 10

        self.algorithm = None
        self.running = False

    def draw(self) -> None:
        self.screen.fill((30, 30, 30))
        self.paths.draw()
        self.cube.draw()
        self.algorithms_button_bar.draw()
        self.timer.draw()
        self.label.draw()

    def update(self) -> None:
        if not self.algorithms_button_bar.active:
            self.paths.update()
        self.algorithms_button_bar.update()
        self.timer.update()

    def update_on_event(self, event) -> None:
        if event.type == constants.QUIT:
            sys.exit()
        elif event.type == constants.KEYDOWN:
            if event.key == constants.K_r:
                # Reset terrain and cube position
                self.traversing = False
                self.paths.unblock_all()
                self.cube.reset_pos()
                self.timer.reset()
            elif event.key == constants.K_t:
                # Clean the traversed terrain
                self.traversing = False
                self.paths.clean()
                self.cube.reset_pos()
                self.timer.reset()
            elif event.key == constants.K_s and self.algorithm is not None:
                if active_count() == 1 and self.paths.get_objective() is not None:
                    Thread(
                        target=lambda: self.solve_maze(self.algorithm),
                        daemon=True,
                    ).start()
            elif event.key == constants.K_c and self.traversing:
                self.traversing = False
                self.paths.clean()
                self.timer.reset()

            # Computing the directions clicks.
            elif (
                event.key == constants.K_UP
                and self.cube.rect.y > self.paths.HEIGHT_SPACING_FACTOR // 2
            ):
                self.cube.rect.y -= cubes.SIDE_LENGTH
            elif (
                event.key == constants.K_DOWN
                and self.cube.rect.y < self.paths.grid_height
            ):
                self.cube.rect.y += cubes.SIDE_LENGTH
            elif (
                event.key == constants.K_RIGHT
                and self.cube.rect.x <= self.paths.grid_width
            ):
                self.cube.rect.x += cubes.SIDE_LENGTH
            elif (
                event.key == constants.K_LEFT
                and self.cube.rect.x > self.paths.WIDTH_SPACING_FACTOR // 2
            ):
                self.cube.rect.x -= cubes.SIDE_LENGTH
        self.algorithms_button_bar.update_on_event(event)

    def solve_maze(self, fn):
        """Solve the user generated maze given the solver function.

        Args:

            fn: Function to use to solve the maze.
                Signature: fn(CharacterCube, PathCubeList)
        """

        self.traversing = True
        self.timer.start()
        print(fn(self, self.cube, self.paths))
        self.timer.stop()
        self.traversing = False

    def set_algorithm(self, new, name_new):
        self.label.update_text(
            f"{languages.message_map['selected_algorithm']}: {name_new}"
        )
        self.label.rect = self.label.image.get_rect()
        self.label.rect.topright = self.screen_rect.topright
        self.label.rect.x -= 10
        self.label.rect.y += 10
        self.algorithm = new
