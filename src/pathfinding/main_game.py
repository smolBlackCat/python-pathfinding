"""A main that implements all the visual stuff and processing"""

import sys
import time
from queue import PriorityQueue
from threading import Thread, active_count as threads_count

import pygame

from . import cubes

pygame.init()


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


def astar(cube, paths):  # Thread
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
    open_queue.put(start)

    # The priority queue has no way to analyze if it has an element inside.
    # So a set is much better .
    open_set = {start}

    score = 1  # g == n + 1
    while not open_queue.empty():
        current = open_queue.get()
        if current.is_objective:
            # Starts running on the paths.
            for path in reconstruct_path(came_from, current):
                path.rect_color = (255, 165, 0)
                cube.move(path)
                time.sleep(0.1)
            print("Path Was found")
            return True

        # Removing the current one since we already worked with it, making the
        # algorithm not analyze repeated cubes.
        open_set.remove(current)
        for neighbor in paths.get_neighbors(current):
            tentative_gscore = g_score[current] + score

            if tentative_gscore < g_score[neighbor] and not \
                    neighbor.is_blocked:
                # This path is better. Record It !
                came_from[neighbor] = current
                g_score[neighbor] = tentative_gscore
                f_score[neighbor] = g_score[neighbor] + \
                    heuristic(neighbor, paths.get_objective())
                neighbor.f_cost = f_score[neighbor]

                if neighbor not in open_set:
                    open_queue.put(neighbor)
                    open_set.add(neighbor)
            else:
                # This is not a good idea, let's see others...
                if not (neighbor.is_blocked or neighbor.is_objective):
                    neighbor.rect_color = (255, 0, 255)
        score += 1

    # print this if the path just dont exist. :(
    print("The path doesn't exist")
    return False


def get_keydown_events(event, paths, cube):
    """Computes keydown events.
    
    Args:
        event: pygame.event.Event object from which the value in the \"key\"
               attribute is gotten from
        
        paths: PathCubeList object.
        
        cube: CharacterCube object.
    """

    if event.key == pygame.K_r:
        paths.reset_all()
        cube.reset_pos()
    elif event.key == pygame.K_s:
        if threads_count() == 1 and paths.get_objective() is not None:
            Thread(target=astar, args=(cube, paths), daemon=True).start()

    # Computing the directions clicks.
    elif event.key == pygame.K_UP:
        cube.rect.y -= cubes.SIDE_LENGTH
    elif event.key == pygame.K_DOWN:
        cube.rect.y += cubes.SIDE_LENGTH
    elif event.key == pygame.K_RIGHT:
        cube.rect.x += cubes.SIDE_LENGTH
    elif event.key == pygame.K_LEFT:
        cube.rect.x -= cubes.SIDE_LENGTH


def main():
    """Main Program."""

    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pathfinding app")

    cube = cubes.CharacterCube(screen)
    paths = cubes.PathCubeList(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                get_keydown_events(event, paths, cube)

        screen.fill((255, 255, 255))
        paths.update_paths()
        cube.draw()

        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main()
