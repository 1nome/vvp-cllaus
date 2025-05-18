import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple, Literal

class CA:
    def __init__(self):
        self.name = "My CA"
        self.next_vals = np.array([])
        self.colors: dict[int, Tuple[int, int, int] | str] = {}
    def __call__(self, universe):
        pass

class NoRule(CA):
    def __init__(self):
        self.name = "Nothing"

class ConwayNaive(CA):
    def __init__(self):
        self.name = "Conway's game of life, naive implementation"
        self.next_vals = np.array([1, 0], dtype=np.int8)
        self.colors = {1: "white"}
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
                    universe[i, j] = 0
                elif self.n_neighbours[i, j] == 3 and not universe[i, j]:
                    universe[i, j] = 1

class LangtonsAnt(CA):
    def __init__(self):
        self.name = "Langton's ant"
        self.next_vals = np.array([1, 8, 0, 0, 0, 0, 0, 0,
                                   9, 10, 11, 12, 13, 14, 15, 0], dtype=np.int8)
        self.colors = {1: "white"}
        for i in range(8, 16):
            self.colors[i] = "red" if i % 2 else (128, 0, 0)
        self.next_dirs = {8: (-1, 0, 14), 9: (1, 0, 10), 10: (0, -1, 8), 11: (0, 1, 12),
                     12: (1, 0, 10), 13: (-1, 0, 14), 14: (0, 1, 12), 15: (0, -1, 8)}

    def __call__(self, universe: NDArray[np.int8]):
        ants = np.where(universe & 8)
        for i in range(ants[0].shape[0]):
            val = int(universe[ants[0][i], ants[1][i]])
            x, y, r = self.next_dirs[val]
            xx = ants[0][i] + x if 0 <= ants[0][i] + x < universe.shape[0] else ants[0][i]
            yy = ants[1][i] + y if 0 <= ants[1][i] + y < universe.shape[1] else ants[1][i]
            universe[ants[0][i], ants[1][i]] = 0 if universe[ants[0][i], ants[1][i]] & 1 else 1
            universe[xx, yy] = r + (universe[xx, yy] & 1)
            pass
