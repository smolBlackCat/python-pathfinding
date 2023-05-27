"""Code for building a multi-platform binary.

WARNING: DO NOT RUN THIS SCRIPT WITHIN THE THE SCRIPTS DIRECTORY.
RUN IT IN THE PROJECT ROOT.
"""

import PyInstaller.__main__
import os

PyInstaller.__main__.run(
    ["scripts/target.py",
     "-w",
     "--icon", os.path.join("data", "moura-pathfinding.png"),
     "-n", "moura-pathfinding",
     "--add-data", os.path.join("src", "pathfinding", "data", "icon.png")+os.pathsep+"data"]
)