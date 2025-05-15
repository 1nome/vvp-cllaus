from collections.abc import Callable
from typing import List
import numpy as np
from numpy.typing import NDArray

class vizState:
    def __init__(self):
        self.screen_dims = [1280, 720]
        self.cell_size = 20
        from .ca import none
        self.ca = none
        self.universe = np.zeros((100, 100), dtype=np.int8)
        self.dtype = np.int8
        
        pass
    def reset(self):
        self.__init__()

_config = vizState()

def display():
    from .ui import ui
    ui(_config)

def rule(ca: Callable[[NDArray], None]):
    _config.ca = ca

def window_dims(dims: List[int]):
    if len(dims) != 2:
        raise ValueError("Expected a list of len 2")
    _config.screen_dims[:] = dims[:]

def cell_size(size: int):
    _config.cell_size = size

def universe_dims(dims: List[int]):
    if len(dims) != 2:
        raise ValueError("Expected a list of len 2")
    _config.universe.resize(dims)