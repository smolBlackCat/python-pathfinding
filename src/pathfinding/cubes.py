"""Cubes module."""

from pygame import draw, rect, mouse


# Super Class
class Cube:
    """A class that will represent the cubes used for simulating,
    walls, objectives and the main character"""

    def __init__(self, screen):
        """Initialize all the instance attributes for this object."""

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect = rect.Rect(0, 0, 40, 40)
        self.rect_color = ()
        self.pos = self.rect.x, self.rect.y

    def draw(self):
        """Draws the cube"""

        draw.rect(self.screen, self.rect_color, self.rect)

    def get_pos(self):
        """Returns a tuple corresponding the path coordinates."""

        return self.rect.x, self.rect.y


class CharacterCube(Cube):
    """A class that represents the cube character.

    His objective is going to the objective with a faster and better way."""

    def __init__(self, screen):
        super().__init__(screen)
        self.rect_color = (0, 0, 255)

    def move(self, path_obj):
        """Moves the Character to a specified path."""

        self.rect.x = path_obj.rect.x
        self.rect.y = path_obj.rect.y

    def reset_pos(self):
        """Resets the character cube."""

        self.rect.x = self.rect.y = 0


class PathCube(Cube):
    """A class that represents the wall.

    In the initial, the user will put the cubes for difficulting the 
    passage of the charater cube."""

    ID = 0

    def __init__(self, screen, pos):
        super().__init__(screen)
        self.rect_color = (0, 255, 0)
        self.is_blocked = False
        self.is_objective = False
        self.f_cost = 0

        self.rect.x, self.rect.y = pos  # (x, y)
        PathCube.ID += 1

    def block(self):
        """Change the status of the path to blocked and change the 
        color (red).
        """

        self.rect_color = (255, 0, 0)
        self.is_blocked = True
        self.is_objective = False

    def unblock(self):
        """Change the status of the path to unblocked and change the 
        color (green)"""

        self.rect_color = (0, 255, 0)
        self.is_blocked = False
        self.is_objective = False

    def set_objective(self):
        """Sets where the character must appear"""

        self.rect_color = (255, 225, 45)
        self.is_blocked = False
        self.is_objective = True

    def draw(self):
        """Draw the Path Grid on the screen."""

        draw.rect(self.screen, self.rect_color, self.rect)

    def __repr__(self):
        return f"Path({PathCube.ID}) at {self.get_pos()}"

    def __lt__(self, other):
        """The comparing is based on the f cost"""

        return self.f_cost < other.f_cost


class PathCubeList(list):
    """A class that inherit list class, to organize all paths objects"""

    def __init__(self, screen, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scr = screen
        self.gen_paths()

    def get_neighbors(self, path_: PathCube):
        """Get neighbors from a path.

        Returns a empty list if the path specified doesnt exists.
        """

        neighbors = []
        pathx, pathy = path_.get_pos()
        for path in self:
            is_neighbor = any([path.rect.collidepoint(pathx, pathy-40),
                               path.rect.collidepoint(pathx, pathy+40),
                               path.rect.collidepoint(pathx-40, pathy),
                               path.rect.collidepoint(pathx+40, pathy)])
            if is_neighbor:
                neighbors.append(path)
        return neighbors

    def gen_paths(self):
        """Creates the path objects depending on the screen size."""

        n_columns = self.scr.get_width() // 40
        n_rows = self.scr.get_height() // 40

        for x_pos in range(n_rows):
            for y_pos in range(n_columns):
                self.append(PathCube(self.scr, (y_pos*40, x_pos*40)))

    def update_paths(self):
        """Updates the CubePath objects on the screen. 

        Tasks such as drawing and color update.
        """

        for path in self:
            path.draw()
            if mouse.get_pressed()[0] and \
                    path.rect.collidepoint(mouse.get_pos()):
                path.block()
            elif mouse.get_pressed()[2] and \
                    path.rect.collidepoint(mouse.get_pos()) and \
                    not self.have_objective():
                path.set_objective()

    def get_objective(self):
        """Returns the pathCube object that the attribute is_objective is 
        True.

        Returns None if the objective doesnt exists.
        """

        for path in self:
            if path.is_objective:
                return path
        return None

    def have_objective(self):
        """It returns True if the objective is in the List"""

        return self.get_objective() is not None

    def reset_all(self):
        """Resets all the program to the factory."""

        for path in self:
            path.unblock()

    def find_path(self, cube):
        """Returns the path object from pos.

        None is returned if the path was not found.
        """

        for path in self:
            if cube.get_pos() == path.get_pos():
                return path
        return None
