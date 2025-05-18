from typing import List, Tuple
import numpy as np
from numpy.typing import NDArray
from .ca import CA, NoRule
from .io import save_to, load_from

class vizState:
    def __init__(self):
        self.screen_dims: Tuple[int, int] = (1280, 720)
        self.cell_size = 20
        self.ca: CA = NoRule()
        self.universe: NDArray = np.zeros((100, 100), dtype=np.int8)
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
        self.generation = 0
        
    def reset(self):
        self.__init__()

_config = vizState()

def display():
    """
    Starts the visualizer.
    """
    from .ui import ui
    ui(_config)

def rule(ca: CA):
    """
    Sets the rule to be used.

    ca: CA object
    """
    _config.ca = ca
    _config.universe = np.astype(_config.universe, ca.dtype)

def window_dims(dims: Tuple[int, int]):
    """
    Sets the initial window dimensions.
    """
    _config.screen_dims = dims

def cell_size(size: int):
    """
    Sets the initial cell size.

    size: Positive integer
    """
    if size < 1:
        raise ValueError("Expected a value >= 1")
    _config.cell_size = size

def universe_dims(dims: Tuple[int, int]):
    """
    Resizes the universe to the new dimensions.
    """
    _config.universe.resize(dims)

def fps(fps: int | float):
    """
    Sets the fps limit.
    """
    if fps <= 0:
        raise ValueError("Expected a value > 0")
    _config.fps_desired = fps

def ups(ups: int | float):
    """
    Sets the initial ups limit.
    """
    if ups <= 0:
        raise ValueError("Expected a value > 0")
    _config.ups_desired = ups

def fps_show():
    """
    Displays fps.
    """
    _config.show_fps = True

def ups_show():
    """
    Displays ups.
    """
    _config.show_ups = True

def fps_hide():
    """
    Hides fps.
    """
    _config.show_fps = False

def ups_hide():
    """
    Hides ups.
    """
    _config.show_ups = False

def paste_vals(arr: NDArray, x: int, y: int) -> int:
    """
    Pastes values from arr to the universe. Has bounds checking.
    Will crop out the cells outside the visible range.
    """
    src_x = 0 if x > 0 else -x
    src_y = 0 if y > 0 else -y
    if src_x > arr.shape[0] or src_y > arr.shape[1]:
        return 0
    dest_x = x if x > 0 else 0
    dest_y = y if y > 0 else 0
    if dest_x > _config.universe.shape[0] or dest_y > _config.universe.shape[1]:
        return 0
    size_x = min(arr.shape[0] - src_x, _config.universe.shape[0] - dest_x)
    size_y = min(arr.shape[1] - src_y, _config.universe.shape[1] - dest_y)
    _config.universe[dest_x:dest_x + size_x, dest_y:dest_y + size_y] =\
        arr[src_x:src_x + size_x, src_y:src_y + size_y]
    return size_x * size_y

def paste_from(filename: str, x: int, y: int):
    """
    Pastes values from a file to the universe. Has bounds checking.
    Will crop out the cells outside the visible range.
    """
    paste_vals(load_from(filename, dtype=_config.universe.dtype), x, y)

def pause():
    """
    Initially pauses the simulation.
    """
    _config.paused = True

def unpause():
    """
    Unpauses the simulation.
    """
    _config.paused = False

def reset():
    """
    Resets everything to their default values.
    """
    _config.reset()

def clear():
    """
    Sets the universe and generation counter to zeros.
    """
    _config.universe.fill(0)
    _config.generation = 0

def bg_color(color: Tuple[int, int, int] | str):
    """
    Sets the background color. Takes a pygame color value.
    """
    _config.colors[3] = color

def text_color(color: Tuple[int, int, int] | str):
    """
    Sets the text color. Takes a pygame color value.
    """
    _config.colors[0] = color

def cursor_color(color: Tuple[int, int, int] | str):
    """
    Sets the cursor and crosshair color. Takes a pygame color value.
    """
    _config.colors[2] = color

def border_color(color: Tuple[int, int, int] | str):
    """
    Sets the universe border color. Takes a pygame color value.
    """
    _config.colors[1] = color

def grid_color(color: Tuple[int, int, int] | str):
    """
    Sets the grid color. Takes a pygame color value.
    """
    _config.colors[4] = color

def crosshair_show():
    """
    Shows crosshair where actions in normal mode will happen.
    """
    _config.crosshair = True

def crosshair_hide():
    """
    Hides crosshair.
    """
    _config.crosshair = False

def generation_show():
    """
    Shows generation counter.
    """
    _config.show_generation = True

def generation_hide():
    """
    Hides generation counter.
    """
    _config.show_generation = False

def population_show():
    """
    Shows population counter.
    """
    _config.show_population = True

def population_hide():
    """
    Hides population counter.
    """
    _config.show_population = False

def grid_show():
    """
    Shows the grid.
    """
    _config.grid = True

def grid_hide():
    """
    Hides the grid.
    """
    _config.grid = False

def simulate(n: int):
    """
    Simulates n generations of the CA.
    """
    print("simulating...")
    for i in range(n):
        _config.ca(_config.universe)
        _config.generation += 1
    print("done")

def save_universe(filename: str):
    """
    Saves the entire universe to a file.
    """
    save_to(filename, _config.universe)

def load_universe(filename: str):
    """
    Overwrites the current universe with the one from a file.
    """
    _config.universe = load_from(filename, dtype=_config.universe.dtype)
