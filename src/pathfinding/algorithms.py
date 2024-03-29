"""algorithms.py module"""

import time
from queue import PriorityQueue, Queue, LifoQueue

from . import cubes

TIME_INTERVAL = 0.01


def heuristic(cube, objective):
    """Produces the cost based on the cube position and the objective position
    using the manhattan method.

    Args:
        cube: Character cube object that will go through the most optimal path.

        objective: PathCube object which is_objective attribute is true.

    Returns:
        The cost based on the cube position and the objective position.
    """

    objt_x, objt_y = objective.get_pos()
    cub_x, cub_y = cube.get_pos()
    return (abs((objt_x - cub_x)) + abs((objt_y - cub_y))) // cubes.SIDE_LENGTH


def reconstruct_path(came_from, current):
    """Produces a list containing the most optimal nodes.

    Args:
        came_from: dict object used to keep track of the node immediately
                   preceding each node on the cheapest path from the start node
                   to that node.

        current: Starting node. the value will change to the next node linked
                 to this node.

    Returns:
        list object containing the most optimal nodes.
    """

    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def walk(app_scene, cube, to_walk):
    """Make cube walk through all the given pathcubes.

     Args:
        app_scene: scene holding the state 'traversing'

        cube: Character cube object instance

        tO_walk: list of PathCube objects to go to in an interval of
                 0.1 second

    Returns:
        True whenever the cube finish traversing. False might be
        returned if the process was canceled by the user in the main
        thread.
    """

    for path in to_walk:
        if not app_scene.traversing:
            return False

        path.rect_color = (255, 165, 0)
        cube.move(path)
        time.sleep(0.1)
    return True


def astar(app_scene, cube, paths):  # Thread
    """A* Algorithm. Produces the most optimal path.

    Args:
        cube: Character cube object that will go through the most optimal path.

        paths: PathCubeList object.

    Returns:
        True when the algorithm was able to find a optimal path. Otherwise
        False.
    """

    open_queue = PriorityQueue()

    # cameFrom[n] is the node immediately preceding it on the cheapest path
    # from start to n currently known.
    came_from = {}

    g_score = {path: float("inf") for path in paths}
    f_score = {path: float("inf") for path in paths}

    # Defining the start pathcube f_cost and putting in the queue
    start = paths.find_path(cube)
    g_score[start] = 0
    start.f_cost = f_score[start] = heuristic(start, paths.get_objective())
    open_queue.put((0, start))

    visited = set()

    while not open_queue.empty():
        if not app_scene.traversing:
            return False

        _, current_node = open_queue.get()
        if current_node in visited:
            continue
        if current_node.is_objective:
            # Starts running on the paths.
            path = reconstruct_path(came_from, current_node)
            return walk(app_scene, cube, path), len(visited), len(path), sum(map(lambda p: p.weight, path))

        for neighbor in paths.get_neighbors(current_node):
            tentative_gscore = g_score[current_node] + current_node.weight

            if tentative_gscore < g_score[neighbor] and not neighbor.is_blocked:
                # This path is better. Record It !
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_gscore
                f_score[neighbor] = g_score[neighbor] + heuristic(
                    neighbor, paths.get_objective())

                open_queue.put((f_score[neighbor], neighbor))
                neighbor.rect_color = (180, 0, 0)

        current_node.rect_color = (255, 0, 255)
        visited.add(current_node)
        time.sleep(TIME_INTERVAL)

    # print this if the path just dont exist. :(
    print("The path doesn't exist")
    return False, len(visited), 0, 0


def _search(app_scene, cube: cubes.CharacterCube, paths: cubes.PathCubeList, container_class):
    """General function for searching."""
    start_node = paths.find_path(cube)
    came_from = {}

    queue = container_class()
    visited = set()
    queue.put(start_node)

    start_node.rect_colour = (255, 0, 255)

    while not queue.empty():
        current_node = queue.get()

        if not app_scene.traversing:
            break

        if current_node.is_objective:
            path = reconstruct_path(came_from, current_node)
            return (walk(app_scene, cube, path), len(visited), len(path),
                    sum(map(lambda p: p.weight, path)))
        elif current_node in visited:
            continue

        for neighbour in paths.get_neighbors(current_node):
            if not (neighbour.is_blocked or neighbour in visited):
                queue.put(neighbour)
                came_from[neighbour] = current_node
                neighbour.rect_color = (180, 0, 0)

        visited.add(current_node)
        current_node.rect_color = (255, 0, 255)
        time.sleep(TIME_INTERVAL)
    return False, len(visited), 0, 0


def dfs(app_scene, cube: cubes.CharacterCube, paths: cubes.PathCubeList) -> bool:
    """Finds a path from the starting node to the end node.

    The start node is defined by the current cube's position and the
    end node is defined by the pathcube which its is_objective attribute is true.

    The algorithm finds a path using the depth-first search algorithm.

    Returns:
        True if the a path was found, othewise False.
    """

    return _search(app_scene, cube, paths, LifoQueue)


def bfs(app_scene, cube: cubes.CharacterCube, paths: cubes.PathCubeList):
    """Breadth-first search algorithm."""

    return _search(app_scene, cube, paths, Queue)


def dijkstra(app_scene, cube: cubes.CharacterCube, paths: cubes.PathCubeList):
    initial_node = paths.find_path(cube)
    distances = {node: float("inf") for node in paths}
    distances[initial_node] = 0

    came_from = {initial_node: None}
    visited = set()

    priority_queue = PriorityQueue()
    priority_queue.put((0, initial_node))

    while not priority_queue.empty():
        if not app_scene.traversing:
            return False
        current_distance, current_node = priority_queue.get()

        if current_node.is_objective:
            found_path = reconstruct_path(came_from, current_node)
            found_path.pop(0)
            return walk(app_scene, cube, found_path), len(visited), len(found_path), sum(map(lambda p: p.weight, found_path))
        elif current_node in visited:
            continue

        for neighbour in paths.get_neighbors(current_node):
            if neighbour.is_blocked:
                continue

            tentative_distance = distances[current_node] + neighbour.weight

            if tentative_distance < distances[neighbour]:
                distances[neighbour] = tentative_distance
                came_from[neighbour] = current_node
                if neighbour not in visited:
                    priority_queue.put((tentative_distance, neighbour))
                    neighbour.rect_color = (180, 0, 0)
        
        visited.add(current_node)
        current_node.rect_color = (255, 0, 255)
        time.sleep(TIME_INTERVAL)

    return False, len(visited), 0, 0
