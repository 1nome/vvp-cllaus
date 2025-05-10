import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple

def conwayNaive(universe: NDArray[np.bool_]):
    n_neighbours: NDArray[np.int8] = np.zeros_like(universe, dtype=np.int8)

    relative_neighbours: List[Tuple] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for i in range(1, universe.shape[0] - 1):
        for j in range(1, universe.shape[1] - 1):
            for ii, jj in relative_neighbours:
                if universe[i + ii, j + jj]:
                    n_neighbours[i, j] += 1

    for i in range(1, universe.shape[0] - 1):
        for j in range(1, universe.shape[1] - 1):
            if (n_neighbours[i, j] < 2 or n_neighbours[i, j] > 3) and universe[i, j]:
                universe[i, j] = np.False_
            elif n_neighbours[i, j] == 3 and not universe[i, j]:
                universe[i, j] = np.True_

universe = np.zeros((100, 100), dtype=np.bool_)

# glider
universe[[2, 3, 1, 2, 3], [1, 2, 3, 3, 3]] = True

import pygame

screen_dims = (1280, 720)

pygame.init()
screen = pygame.display.set_mode(screen_dims)
clock = pygame.time.Clock()
running = True

size = 20
x_offset = 100
y_offset = 100

ups_desired = 5
fps_desired = 180
time_since_last_update = 0

mouse_down = False
mouse_move = False
paused = False

while running:

    # calculate the visible area offsets
    base_offset = ((-x_offset if x_offset < 0 else 0) // size, (-y_offset if y_offset < 0 else 0) // size)
    visible_dims = ((screen_dims[0] // size + 1), (screen_dims[1] // size + 1))

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # stops the loop (thus pygame)
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            if mouse_down and not mouse_move:
                # toggle cell under cursor
                x = (-x_offset + event.pos[0]) // size
                y = (-y_offset + event.pos[1]) // size
                if 0 < x < universe.shape[0] and 0 < y < universe.shape[1]:
                    universe[x, y] = not universe[x, y]
            mouse_down = False
            mouse_move = False
        if event.type == pygame.MOUSEMOTION:
            if mouse_down:
                mouse_move = True
                x_offset += event.rel[0]
                y_offset += event.rel[1]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    # clear image
    screen.fill("black")

    def clamp(a, max):
        return a if a < max else max

    # rendering
    pygame.draw.rect(screen, "red", (x_offset, y_offset, universe.shape[0] * size, universe.shape[1] * size), 1)
    for x in range(base_offset[0], clamp(base_offset[0] + visible_dims[0], universe.shape[0])):
        for y in range(base_offset[1], clamp(base_offset[1] + visible_dims[1], universe.shape[1])):
            if universe[x, y]:
                pygame.draw.rect(screen, "white",
                                 (x * size + x_offset, y * size + y_offset, size, size))
    
    # updating CA
    if time_since_last_update > 1 / ups_desired:
        conwayNaive(universe)
        time_since_last_update -= 1 / ups_desired

    # presenting image
    pygame.display.flip()

    # time step
    # too bad now:
    #   if the CA can't update in less than 1/fps_desired, fps will drop (and the app will become unresponsive)
    #   UPS can't be higher than FPS
    dt = clock.tick(fps_desired) / 1000
    if not paused:
        time_since_last_update += dt

pygame.quit()

