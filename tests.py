import cllaus
import numpy as np

# glider
glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=np.int8)

cllaus.window_dims((1920, 1080))
cllaus.rule(cllaus.ca.ConwayNaive())
cllaus.cell_size(10)
cllaus.universe_dims((100, 100))
cllaus.fps(180)
cllaus.ups(10)
cllaus.ups_show()
cllaus.paste_vals(glider, 1, 1)
cllaus.color_bg((20, 20, 20))
cllaus.show_crosshair()

cllaus.display()
