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
x_offset = 10
y_offset = 10

ups_desired = 5
fps_desired = 180
time_since_last_update = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    visible_dims = (screen_dims[0] // size + 1, screen_dims[1] // size + 1)
    visible = universe[x_offset:x_offset + visible_dims[0], y_offset:y_offset + visible_dims[1]]
    for x in range(visible.shape[0]):
        for y in range(visible.shape[1]):
            if visible[x, y]:
                pygame.draw.rect(screen, "white",
                                 (x * size, y * size, size, size))
    
    if time_since_last_update > 1 / ups_desired:
        conwayNaive(universe)
        time_since_last_update -= 1 / ups_desired

    pygame.display.flip()

    dt = clock.tick(fps_desired) / 1000
    time_since_last_update += dt

pygame.quit()

