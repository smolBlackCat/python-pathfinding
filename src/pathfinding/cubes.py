"""Cubes module."""

from pygame import draw, rect, mouse

SIDE_LENGTH = 40  # In pixels


class Cube:
    """Base class for implementing Cube classes."""

    def __init__(self, screen):
        """Initialise the object.

        Args:
            screen: pygame.surface.Surface object from where the cube will be
                    drawn on.
        """

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect = rect.Rect(0, 0, SIDE_LENGTH, SIDE_LENGTH)
        self.rect_color = ()
        self.pos = self.rect.x, self.rect.y

    def draw(self):
        """Draws the cube."""

        draw.rect(self.screen, self.rect_color, self.rect)

    def get_pos(self):
        """Gets a tuple corresponding to the cube x and y coordinates."""

        return self.rect.x, self.rect.y


class CharacterCube(Cube):
    """CharacterCube class."""

    def __init__(self, screen):
        super().__init__(screen)
        self.rect_color = (0, 0, 255)

    def move(self, path_obj):
        """Moves the Character to a specified path.
        
        Args:
            path_obj: PathCube object from which this CharacterCube object will
                      go to.
        """

        self.rect.x = path_obj.rect.x
        self.rect.y = path_obj.rect.y

    def draw(self):
        draw.rect(self.screen, self.rect_color, self.rect, border_radius=3)

    def reset_pos(self):
        """Resets the position to (0,0)."""

        self.rect.x = self.rect.y = 0


class PathCube(Cube):
    """Cube subclass working as a path block in the game's surface."""

    ID = 0

    BLOCKED_COLOUR = (10, 195, 138)
    OPEN_COLOUR = (43, 218, 127)
    OBJECTIVE_COLOUR = (255, 225, 45)

    def __init__(self, screen, pos):
        """Initialise the object.

        Args:
            screen: pygame.surface.Surface object from where the cube will be
                    drawn on.
            
            pos: tuple containing the x and y coordinates.
        """

        super().__init__(screen)
        self.rect_color = self.OPEN_COLOUR
        self.is_blocked = False
        self.is_objective = False
        self.f_cost = 0

        self.rect.x, self.rect.y = pos  # (x, y)
        PathCube.ID += 1

    def block(self):
        """Change the status of the path to blocked and change the color
        (red).
        """

        self.rect_color = self.BLOCKED_COLOUR
        self.is_blocked = True
        self.is_objective = False

    def unblock(self):
        """Change the status of the path to unblocked and change the color
        (green).
        """

        self.rect_color = self.OPEN_COLOUR
        self.is_blocked = False
        self.is_objective = False

    def set_objective(self):
        """Change the status of the path to be the objective from which the
        CharacterCube object will go to in the most optimal way.
        """

        self.rect_color = self.OBJECTIVE_COLOUR
        self.is_blocked = False
        self.is_objective = True

    def draw(self):
        draw.rect(self.screen, self.rect_color, self.rect)

    def __repr__(self):
        return f"Path({PathCube.ID}) at {self.get_pos()}"

    def __lt__(self, other):
        """The comparison is based on the f cost."""

        return self.f_cost < other.f_cost


class PathCubeList(list):
    """Subclass of list to organise all paths objects and interact with them."""

    def __init__(self, screen, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scr = screen
        self.gen_paths()

    def get_neighbors(self, path_: PathCube):
        """Get the neighbors of the given path.

        Args:
            path_: PathCube object from which the neighbors will be gotten from.
        
        Returns:
            A list containing all the path_ neighbors.
        """

        neighbors = []
        pathx, pathy = path_.get_pos()
        for path in self:
            is_neighbor = any([path.rect.collidepoint(pathx, pathy-SIDE_LENGTH),
                               path.rect.collidepoint(
                                   pathx, pathy+SIDE_LENGTH),
                               path.rect.collidepoint(
                                   pathx-SIDE_LENGTH, pathy),
                               path.rect.collidepoint(pathx+SIDE_LENGTH, pathy)])
            if is_neighbor:
                neighbors.append(path)
        return neighbors

    def gen_paths(self):
        """Creates the path objects according to the screen size."""

        n_columns = self.scr.get_width() // SIDE_LENGTH
        n_rows = self.scr.get_height() // SIDE_LENGTH

        for x_pos in range(n_rows):
            for y_pos in range(n_columns):
                self.append(
                    PathCube(self.scr, (y_pos*SIDE_LENGTH, x_pos*SIDE_LENGTH)))
    
    def draw(self):
        """Draws the grid onto screen."""

        for path in self:
            path.draw()

    def update(self):
        """Update their colours if they're pressed."""

        for path in self:
            if mouse.get_pressed()[0] and \
                    path.rect.collidepoint(mouse.get_pos()):
                path.block()
            elif mouse.get_pressed()[2] and \
                    path.rect.collidepoint(mouse.get_pos()) and \
                    self.get_objective() is None:
                path.set_objective()

    def get_objective(self):
        """Get a CubePath object which its is_objective attribute is set to
        True. 

        Returns:
            CubePath object that's an objective.
        """

        for path in self:
            if path.is_objective:
                return path
        return None

    def unblock_all(self):
        """Set all the PathCube(s) status to unblocked."""

        for path in self:
            path.unblock()

    def find_path(self, cube):
        """Get the PathCube that's being covered by the given cube.

        Args:
            cube: Any cube object.
        
        Returns:
            PathCube object that's being covered by the given cube. If that
            isn't the case, None is returned.
        """

        for path in self:
            if cube.get_pos() == path.get_pos():
                return path
        return None
