import cllaus
import numpy as np

# glider
glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=np.int8)

cllaus.window_dims((1920, 1080))
cllaus.rule(cllaus.ca.ConwayNaive())
# cllaus.rule(cllaus.LangtonsAnt())
cllaus.cell_size(10)
cllaus.universe_dims((100, 150))
cllaus.fps(180)
cllaus.ups(10)
cllaus.ups_show()
cllaus.paste_vals(glider, 1, 1)
# cllaus.paste_vals(np.array([[8]], dtype=np.int8), 30, 50)
cllaus.bg_color((20, 20, 20))
cllaus.crosshair_show()
cllaus.grid_show()

# cllaus.simulate(11000)
cllaus.display()
