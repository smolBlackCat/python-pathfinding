"""Code for building a multi-platform binary.

WARNING: DO NOT RUN THIS SCRIPT WITHIN THE THE SCRIPTS DIRECTORY.
RUN IT IN THE PROJECT ROOT.
"""

import PyInstaller.__main__

PyInstaller.__main__.run(
    ["scripts/target.py",
     "-n", "moura-pathfinding",
     "--add-data", "src/pathfinding/data/icon.png:data"]
)