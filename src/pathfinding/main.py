"""Application Entry"""

import pygame
from basic_engine import game

from . import icon_path, scenes

pygame.init()


def main():
    """Main Program."""

    app = game.Game(1200, 600, "Pathfinding app", pygame.image.load(icon_path))

    app.add_scene("splash_screen", scenes.SplashScreenScene(app.screen))
    app.add_scene("main", scenes.ApplicationScene(app.screen))
    app.set_initial_view("splash_screen")

    app.start()


if __name__ == "__main__":
    main()
