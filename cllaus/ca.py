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
