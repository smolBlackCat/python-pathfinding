"""A main that implements all the visual stuff and processing"""

import pygame
from basic_engine import game

from . import scenes

pygame.init()


def main():
    """Main Program."""

    app = game.Game(1200, 600, "Pathfinding app")

    app.add_scene("splash_screen", scenes.SplashScreenScene(app.screen))
    app.add_scene("main", scenes.ApplicationScene(app.screen))
    app.set_initial_view("main")

    app.start()


if __name__ == "__main__":
    main()
