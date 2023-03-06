"""A main that implements all the visual stuff and processing"""

import time
from queue import PriorityQueue
from threading import Thread, active_count as threads_count
import pygame
import cubes

pygame.init()


def heuristic(cube, objective):
    """A heuristic function, using Manhattan method."""

    objt_x, objt_y = objective.get_pos()
    cub_x, cub_y = cube.get_pos()
    return (abs((objt_x - cub_x)) + abs((objt_y - cub_y))) // 40


def reconstruct_path(came_from, current):
    """Reconstruct all the good path."""

    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def astar(cube, paths):  # Thread
    """At this part of the program, the character will start walking through
    the paths up to the objective."""

    open_queue = PriorityQueue()

    # cameFrom[n] is the node immediately preceding it on the cheapest path
    # from start to n currently known.
    came_from = dict()

    g_score = {path: float("inf") for path in paths}
    f_score = {path: float("inf") for path in paths}

    # Defining the start pathcube f_cost and putting in the queue
    start = paths.find_path(cube)
    g_score[start] = 0
    start.f = f_score[start] = heuristic(start, paths.get_objective())
    open_queue.put(start)

    # The priority queue has no way to analyze if it has an element inside.
    # So a set is much better .
    open_set = {start}

    g = 1  # g == n + 1
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
            tentative_gscore = g_score[current] + g

            if tentative_gscore < g_score[neighbor] and not \
                    neighbor.is_blocked:
                # This path is better. Record It !
                came_from[neighbor] = current
                g_score[neighbor] = tentative_gscore
                f_score[neighbor] = g_score[neighbor] + \
                    heuristic(neighbor, paths.get_objective())
                neighbor.f = f_score[neighbor]

                if neighbor not in open_set:
                    open_queue.put(neighbor)
                    open_set.add(neighbor)
            else:
                # This is not a good idea, let's see others...
                if not (neighbor.is_blocked or neighbor.is_objective):
                    neighbor.rect_color = (255, 0, 255)
        g += 1

    # print this if the path just dont exist. :(
    print("The path doesn't exist")
    return False


def get_keydown_events(event, paths, cube):
    """Catch the buttons clicked by user."""

    if event.key == pygame.K_r:
        paths.reset_all()
        cube.reset_pos()
    elif event.key == pygame.K_s:
        # TODO: The character starts running on the better way.
        # Implementing a daemon thread, so when the user click the exit
        # button, the process is immediatelly killed.
        if threads_count() == 1 and paths.have_objective():
            Thread(target=astar, args=(cube, paths), daemon=True).start()

    # Catching the directions clicks.
    elif event.key == pygame.K_UP:
        cube.rect.y -= 40
    elif event.key == pygame.K_DOWN:
        cube.rect.y += 40
    elif event.key == pygame.K_RIGHT:
        cube.rect.x += 40
    elif event.key == pygame.K_LEFT:
        cube.rect.x -= 40


def main():
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pathfinding app")

    cube = cubes.CharacterCube(screen)
    paths = cubes.PathCubeList(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                get_keydown_events(event, paths, cube)

        # TODO: Draw and update the screen
        screen.fill((255, 255, 255))
        paths.update_paths()
        cube.draw()

        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main()
