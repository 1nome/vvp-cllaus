from typing import List, Tuple
import numpy as np
from numpy.typing import NDArray
from .ca import CA, NoRule

class vizState:
    def __init__(self):
        self.screen_dims: Tuple[int, int] = (1280, 720)
        self.cell_size = 20
        self.ca: CA = NoRule()
        self.universe = np.zeros((100, 100), dtype=np.int8)
        self.dtype = np.int8
        self.fps_desired: int | float = 60
        self.ups_desired: int | float = 5
        self.kb_move = 1000
        self.show_fps = False
        self.show_ups = False
        self.paused = False
        self.colors: List[Tuple[int, int, int] | str] = ["white", "red", "yellow", "black", (40, 40, 40)]
        self.crosshair = False
        self.grid = False
        self.show_generation = True
        self.show_population = True
        
    def reset(self):
        self.__init__()

_config = vizState()

def display():
    from .ui import ui
    ui(_config)

def rule(ca: CA):
    _config.ca = ca

def window_dims(dims: Tuple[int, int]):
    _config.screen_dims = dims

def cell_size(size: int):
    if size < 1:
        raise ValueError("Expected a value >= 1")
    _config.cell_size = size

def universe_dims(dims: Tuple[int, int]):
    _config.universe.resize(dims)

def fps(fps: int | float):
    if fps <= 0:
        raise ValueError("Expected a value > 0")
    _config.fps_desired = fps

def ups(ups: int | float):
    if ups <= 0:
        raise ValueError("Expected a value > 0")
    _config.ups_desired = ups

def fps_show():
    _config.show_fps = True

def ups_show():
    _config.show_ups = True

def fps_hide():
    _config.show_fps = False

def ups_hide():
    _config.show_ups = False

def paste_vals(arr: NDArray, x: int, y: int) -> int:
    src_x = 0 if x > 0 else -x
    src_y = 0 if y > 0 else -y
    if src_x > arr.shape[0] or src_y > arr.shape[1]:
        return 0
    dest_x = x if x > 0 else 0
    dest_y = y if y > 0 else 0
    if dest_x > _config.universe.shape[0] or dest_y > _config.universe.shape[0]:
        return 0
    size_x = min(arr.shape[0] - src_x, _config.universe.shape[0] - dest_x)
    size_y = min(arr.shape[1] - src_y, _config.universe.shape[1] - dest_y)
    _config.universe[dest_x:dest_x + size_x, dest_y:dest_y + size_y] =\
        arr[src_x:src_x + size_x, src_y:src_y + size_y]
    return size_x * size_y

def pause():
    _config.paused = True

def unpause():
    _config.paused = False

def reset():
    _config.reset()

def clear():
    _config.universe.fill(0)

def bg_color(color: Tuple[int, int, int] | str):
    _config.colors[3] = color

def text_color(color: Tuple[int, int, int] | str):
    _config.colors[0] = color

def cursor_color(color: Tuple[int, int, int] | str):
    _config.colors[2] = color

def border_color(color: Tuple[int, int, int] | str):
    _config.colors[1] = color

def grid_color(color: Tuple[int, int, int] | str):
    _config.colors[4] = color

def crosshair_show():
    _config.crosshair = True

def crosshair_hide():
    _config.crosshair = False

def generation_show():
    _config.show_generation = True

def generation_hide():
    _config.show_generation = False

def population_show():
    _config.show_population = True

def population_hide():
    _config.show_population = False

def grid_show():
    _config.grid = True

def grid_hide():
    _config.grid = False