import cllaus
import numpy as np

# glider
glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=np.int8)

cllaus.window_dims([1920, 1080])
cllaus.rule(cllaus.ca.ConwayNaive())
cllaus.cell_size(10)
cllaus.universe_dims([100, 100])
cllaus.fps(180)
cllaus.ups(10)
cllaus.ups_show()
cllaus.paste_vals(glider, 1, 1)
# cllaus.pause()

# arrs = [np.ones((50, 50), dtype=np.int8),
#         np.ones((100, 100), dtype=np.int8),
#         np.ones((150, 150), dtype=np.int8)]

# os = [-1.5, -1, -0.5, 0, 0.5, 1, 1.5]

# for a in arrs:
#     for x in os:
#         for y in os:
#             cllaus.paste_vals(a, int(a.shape[0] * x), int(a.shape[1] * y))
#             cllaus.display()
#             cllaus.clear()

cllaus.display()
