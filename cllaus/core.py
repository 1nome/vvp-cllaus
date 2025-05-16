from typing import List
import numpy as np
from numpy.typing import NDArray
from .ca import CA, NoRule

class vizState:
    def __init__(self):
        self.screen_dims = [1280, 720]
        self.cell_size = 20
        self.ca: CA = NoRule()
        self.universe = np.zeros((100, 100), dtype=np.int8)
        self.dtype = np.int8
        self.fps_desired: int | float = 60
        self.ups_desired: int | float = 5
        self.kb_move = 1000
        self.show_fps = False
        self.show_ups = False
        
    def reset(self):
        self.__init__()

_config = vizState()

def display():
    from .ui import ui
    ui(_config)

def rule(ca: CA):
    _config.ca = ca

def window_dims(dims: List[int]):
    if len(dims) != 2:
        raise ValueError("Expected a list of len 2")
    _config.screen_dims[:] = dims[:]

def cell_size(size: int):
    if size < 1:
        raise ValueError("Expected a value > 1")
    _config.cell_size = size

def universe_dims(dims: List[int]):
    if len(dims) != 2:
        raise ValueError("Expected a list of len 2")
    _config.universe.resize(dims)

def fps(fps: int | float):
    _config.fps_desired = fps

def ups(ups: int | float):
    _config.ups_desired = ups

def toggle_fps():
    _config.show_fps = not _config.show_fps

def toggle_ups():
    _config.show_ups = not _config.show_ups