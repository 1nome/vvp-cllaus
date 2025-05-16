import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple, Literal

class CA:
    def __init__(self):
        self.name = "My CA"
    def __call__(self, universe):
        pass

class NoRule(CA):
    def __init__(self):
        self.name = "Nothing"

class ConwayNaive(CA):
    def __init__(self):
        self.name = "Conway's game of life, naive implementation"
        self.relative_neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.n_neighbours = np.zeros((100, 100), dtype=np.int8)
    
    def __call__(self, universe: NDArray[np.int8]):
        if self.n_neighbours.shape != universe.shape:
            self.n_neighbours.resize(universe.shape)

        self.n_neighbours.fill(0)

        for i in range(1, universe.shape[0] - 1):
            for j in range(1, universe.shape[1] - 1):
                for ii, jj in self.relative_neighbours:
                    if universe[i + ii, j + jj]:
                        self.n_neighbours[i, j] += 1

        for i in range(1, universe.shape[0] - 1):
            for j in range(1, universe.shape[1] - 1):
                if (self.n_neighbours[i, j] < 2 or self.n_neighbours[i, j] > 3) and universe[i, j]:
                    universe[i, j] = np.False_
                elif self.n_neighbours[i, j] == 3 and not universe[i, j]:
                    universe[i, j] = np.True_
