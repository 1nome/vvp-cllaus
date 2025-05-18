import numpy as np
from numpy.typing import NDArray
import os

def save_to(filename: str, arr):
    i = filename.rfind("/")
    if i == -1:
        path = ""
    else:
        path = filename[:i]
    if len(path) > 0:
        try:
            os.makedirs(path)
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    # if filename[-1:-5] == ".npy":
        # np.save(filename, arr)
    # else:
    try:
        np.savetxt(filename, arr, "%d")
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return True

def load_from(filename, dtype) -> NDArray:
    # if filename[-1:-5] == ".npy":
        # return np.load(filename)
    try:
        a = np.loadtxt(filename, dtype=dtype, ndmin = 2)
    except FileNotFoundError:
        print(f"File {filename} not found")
        a = np.zeros((0, 0), dtype=dtype)
    return a