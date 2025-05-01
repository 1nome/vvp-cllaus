import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple

def conwayNaive(universe: NDArray[np.bool_]):
    nNeighbours: NDArray[np.int8] = np.zeros_like(universe, dtype=np.int8)

    relativeNeighbours: List[Tuple] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for i in range(1, universe.shape[0] - 1):
        for j in range(1, universe.shape[1] - 1):
            for ii, jj in relativeNeighbours:
                if universe[i + ii, j + jj]:
                    nNeighbours[i, j] += 1

    for i in range(1, universe.shape[0] - 1):
        for j in range(1, universe.shape[1] - 1):
            if (nNeighbours[i, j] < 2 or nNeighbours[i, j] > 3) and universe[i, j]:
                universe[i, j] = np.False_
            elif nNeighbours[i, j] == 3 and not universe[i, j]:
                universe[i, j] = np.True_

universe = np.array([[True, True, True], [True, True, True], [True, True, True]], dtype=np.bool_)
universe = np.pad(universe, 4)

# print(universe)
# for _ in range(10):
#     conwayNaive(universe)
#     print(universe)


