import pygame
import numpy as np
from .core import vizState, clear, paste_vals

FONT_SIZE = 32
STATS_OFFSET_X = 250
STATS_PAD_Y = 5
AVG_OVER = 64
MODE_OFFSET = 5
LAST_OP_OFFSET = 200

def ui(config: vizState):

    universe = config.universe

    screen_dims = [config.screen_dims[0], config.screen_dims[1]]

    pygame.init()
    screen = pygame.display.set_mode(screen_dims, pygame.RESIZABLE)
    pygame.display.set_caption("cllaus | displaying " + config.ca.name)
    clock = pygame.time.Clock()
    running = True

    font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)

    size = config.cell_size
    x_offset = 0
    y_offset = 0

    ups_desired = config.ups_desired
    fps_desired = config.fps_desired
    kb_move = config.kb_move
    time_since_last_update = 0
    dt = clock.tick(fps_desired) / 1000 + 0e-6

    lmb_down = False
    rmb_down = False
    mouse_move = False
    paused = config.paused
    move_x = 0
    move_y = 0
    crosshair = config.crosshair
    visual = False
    insert = False
    ix = 0
    iy = 0
    vx = 0
    vy = 0
    reg = np.array([[0]], dtype=universe.dtype)

    class Long_avg:
        """
        Calculates the average value over n samples.
        """
        def __init__(self, n):
            self.idx = 0
            self.arr = np.zeros(n)
        def __call__(self):
            return np.sum(self.arr) / self.arr.shape[0]
        def add(self, val):
            self.arr[self.idx] = val
            self.idx += 1
            if self.idx == self.arr.shape[0]:
                self.idx = 0
    
    fps = Long_avg(AVG_OVER)
    ups = Long_avg(AVG_OVER)
    ups_s = ups_desired

    show_fps = config.show_fps
    show_ups = config.show_ups

    last_op = ""
    prev_op = last_op

    # text pre-rendering
    text_paused = font.render("PAUSED", True, config.colors[0])
    text_visual = font.render("VISUAL", True, config.colors[0])
    text_insert = font.render("INSERT", True, config.colors[0])
    text_normal = font.render("NORMAL", True, config.colors[0])
    text_last_op = font.render(last_op, True, config.colors[0])

    while running:

        def zoom(dir, cur_x, cur_y):
            """
            Updates cell size while keeping it above 0.
            Also updates offsets so that the cursor points to the same place.
            """
            newsize = size + (1 if dir else (-1 if size > 1 else 0))
            return ((x_offset - cur_x) // size) * newsize + cur_x, ((y_offset - cur_y) // size) * newsize + cur_y, newsize

        def arr_coords(cur_x, cur_y, clmp = False):
            """
            Translates from pixel coords to cell coords.
            Can snap to edges.
            """
            x = (-x_offset + cur_x) // size
            y = (-y_offset + cur_y) // size
            if clmp:
                return clamp(x, universe.shape[0] - 1), clamp(y, universe.shape[1] - 1)
            return x, y
        
        def clamp(a, max, min = 0):
            return min if a < min else (max if a > max else a)
        
        # centre of the creen coords
        nx, ny = arr_coords(screen_dims[0] // 2, screen_dims[1] // 2)

        def check_bounds(x, y):
            """
            Checks if x, y are inside the universe (cell coords)
            """
            return 0 <= x < universe.shape[0] and 0 <= y < universe.shape[1]

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # stops the loop (thus pygame)
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    lmb_down = True
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    x_offset, y_offset, size = zoom(False, event.pos[0], event.pos[1])
                elif event.button == pygame.BUTTON_WHEELUP:
                    x_offset, y_offset, size = zoom(True, event.pos[0], event.pos[1])
                elif event.button == pygame.BUTTON_RIGHT:
                    insert = False
                    visual = True
                    ix, iy = arr_coords(event.pos[0], event.pos[1], True)
                    vx, vy = ix, iy
                    rmb_down = True
                elif event.button == pygame.BUTTON_MIDDLE:
                    x, y = arr_coords(event.pos[0], event.pos[1])
                    if check_bounds(x, y):
                        universe[x, y] = config.ca.next_vals[universe[x, y]]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    if lmb_down and not mouse_move:
                        x, y = arr_coords(event.pos[0], event.pos[1])
                        if check_bounds(x, y):
                            visual = False
                            insert = True
                            ix, iy = x, y
                    lmb_down = False
                    mouse_move = False
                elif event.button == pygame.BUTTON_RIGHT:
                    rmb_down = False
            elif event.type == pygame.MOUSEMOTION:
                if lmb_down:
                    mouse_move = True
                    x_offset += event.rel[0]
                    y_offset += event.rel[1]
                elif rmb_down:
                    vx, vy = arr_coords(event.pos[0], event.pos[1], True)

            elif event.type == pygame.KEYDOWN:
                #pause
                if event.key == pygame.K_SPACE:
                    paused = not paused
                # restart
                elif event.key == pygame.K_r:
                    clear()
                # zoom
                elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                    x_offset, y_offset, size = zoom(True, screen_dims[0] // 2, screen_dims[1] // 2)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    x_offset, y_offset, size = zoom(False, screen_dims[0] // 2, screen_dims[1] // 2)
                # move
                elif event.key in (pygame.K_h, pygame.K_LEFT):
                    if insert:
                        ix -= 1 if ix > 0 else 0
                    elif visual:
                        vx -= 1 if vx > 0 else 0
                        pass
                    else:
                        move_x += kb_move
                elif event.key in (pygame.K_j, pygame.K_DOWN):
                    if insert:
                        iy += 1 if iy < universe.shape[1] - 1 else 0
                    elif visual:
                        vy += 1 if vy < universe.shape[1] - 1 else 0
                        pass
                    else:
                        move_y -= kb_move
                elif event.key in (pygame.K_k, pygame.K_UP):
                    if insert:
                        iy -= 1 if iy > 0 else 0
                    elif visual:
                        vy -= 1 if vy > 0 else 0
                        pass
                    else:
                        move_y += kb_move
                elif event.key in (pygame.K_l, pygame.K_RIGHT):
                    if insert:
                        ix += 1 if ix < universe.shape[0] - 1 else 0
                    elif visual:
                        vx += 1 if vx < universe.shape[0] - 1 else 0
                        pass
                    else:
                        move_x -= kb_move
                # editing
                # increment
                elif event.key == pygame.K_a:
                    if not (insert or visual):
                        if not check_bounds(nx, ny):
                            continue
                        ix, iy = nx, ny
                    if not visual:
                        vx, vy = ix, iy
                    universe[min(ix, vx):max(ix, vx) + 1, min(iy, vy):max(iy, vy) + 1] =\
                        config.ca.next_vals[universe[min(ix, vx):max(ix, vx) + 1, min(iy, vy):max(iy, vy) + 1]]
                # paste
                elif (event.key == pygame.K_p) or (event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL):
                    x = ix if insert else vx if visual else nx
                    y = iy if insert else vy if visual else ny
                    s = paste_vals(reg, x, y)
                    last_op = f"Overwritten {s} cells"
                # yank
                elif (event.key == pygame.K_y) or (event.key == pygame.K_c and event.mod & pygame.KMOD_CTRL):
                    if not (insert or visual):
                        if not check_bounds(nx, ny):
                            continue
                        ix, iy = nx, ny
                    if not visual:
                        vx, vy = ix, iy
                    reg = universe[min(ix, vx):max(ix, vx) + 1, min(iy, vy):max(iy, vy) + 1]
                    last_op = f"Yanked {reg.size} cells"
                # clear (delete)
                elif (event.key == pygame.K_d) or (event.key == pygame.K_x and event.mod & pygame.KMOD_CTRL):
                    if not (insert or visual):
                        if not check_bounds(nx, ny):
                            continue
                        ix, iy = nx, ny
                    if not visual:
                        vx, vy = ix, iy
                    reg = universe[min(ix, vx):max(ix, vx) + 1, min(iy, vy):max(iy, vy) + 1]
                    universe[min(ix, vx):max(ix, vx) + 1, min(iy, vy):max(iy, vy) + 1].fill(0)
                    last_op = f"Cleared {reg.size} cells"
                # modes
                elif event.key == pygame.K_i and not (insert or visual):
                    insert = True
                    crosshair = False
                    ix, iy = arr_coords(screen_dims[0] // 2, screen_dims[1] // 2, True)
                elif event.key == pygame.K_v and not (insert or visual):
                    ix, iy = arr_coords(screen_dims[0] // 2, screen_dims[1] // 2, True)
                    vx, vy = ix, iy
                    visual = True
                    crosshair = False
                elif event.key == pygame.K_ESCAPE:
                    insert = False
                    visual = False
                    crosshair = True if config.crosshair else False
            elif event.type == pygame.KEYUP:
                # move
                if event.key in (pygame.K_h, pygame.K_LEFT):
                    if not (insert or visual):
                        move_x -= kb_move
                elif event.key in (pygame.K_j, pygame.K_DOWN):
                    if not (insert or visual):
                        move_y += kb_move
                elif event.key in (pygame.K_k, pygame.K_UP):
                    if not (insert or visual):
                        move_y -= kb_move
                elif event.key in (pygame.K_l, pygame.K_RIGHT):
                    if not (insert or visual):
                        move_x += kb_move

        # keyboard move
        x_offset += int(move_x / fps_desired)
        y_offset += int(move_y / fps_desired)

        # stats
        stats = []
        if show_fps:
            stats.append(f"fps: {fps():.0f}/{fps_desired:.0f}")
        if show_ups:
            stats.append(f"ups: {ups():.0f}/{ups_desired:.0f}")
        
        # calculate the visible area offsets
        base_offset_x = (-x_offset if x_offset < 0 else 0) // size
        base_offset_y = (-y_offset if y_offset < 0 else 0) // size
        visible_dims_x = (screen_dims[0] // size + 1)
        visible_dims_y = (screen_dims[1] // size + 1)
        end_x = clamp(base_offset_x + visible_dims_x, universe.shape[0])
        end_y = clamp(base_offset_y + visible_dims_y, universe.shape[1])

        # clear image
        screen.fill(config.colors[3])

        # rendering
        if config.grid:
            for x in range(base_offset_x + 1, end_x):
                pygame.draw.line(screen, config.colors[4], (x * size + x_offset, y_offset),
                                 (x * size + x_offset, universe.shape[1] * size + y_offset - 1))
            for y in range(base_offset_y + 1, end_y):
                pygame.draw.line(screen, config.colors[4], (x_offset, y * size + y_offset),
                                 (universe.shape[0] * size + x_offset - 1, y * size + y_offset))
        # universe
        for x in range(base_offset_x, end_x):
            for y in range(base_offset_y, end_y):
                if universe[x, y]:
                    pygame.draw.rect(screen, config.ca.colors[universe[x, y]],
                                    (x * size + x_offset, y * size + y_offset, size, size))
        # border
        pygame.draw.rect(screen, config.colors[1], (x_offset, y_offset, universe.shape[0] * size, universe.shape[1] * size), 1)
        if crosshair:
            x = nx * size + x_offset
            y = ny * size + y_offset
            pygame.draw.line(screen, config.colors[2], (x, y), (x + size, y + size))
            pygame.draw.line(screen, config.colors[2], (x + size, y), (x, y + size))
        # cursor(s)
        if (insert or visual):
            if insert:
                vx, vy = ix, iy
            x = min(ix, vx)
            y = min(iy, vy)
            xs = (max(ix, vx) - x + 1) * size
            ys = (max(iy, vy) - y + 1) * size
            pygame.draw.rect(screen, config.colors[2], (x * size + x_offset, y * size + y_offset, xs, ys), 1)
        o = STATS_PAD_Y
        for s in stats:
            text = font.render(s, True, config.colors[0])
            rect = text.get_rect()
            rect.topleft = (screen_dims[0] - STATS_OFFSET_X, o)
            screen.blit(text, rect)
            o += FONT_SIZE
        text = text_visual if visual else text_insert if insert else text_normal
        rect = text.get_rect()
        rect.bottomleft = (MODE_OFFSET, screen_dims[1])
        screen.blit(text, rect)
        if last_op is not prev_op:
            text_last_op = font.render(last_op, True, config.colors[0])
            prev_op = last_op
        rect = text_last_op.get_rect()
        rect.bottomleft = (LAST_OP_OFFSET, screen_dims[1])
        screen.blit(text_last_op, rect)
        if paused:
            rect = text_paused.get_rect()
            rect.topleft = (MODE_OFFSET, 0)
            screen.blit(text_paused, rect)
        
        # updating CA
        if time_since_last_update > (1 / ups_desired):
            ups_s = 1 / time_since_last_update
            config.ca(universe)
            time_since_last_update = 0

        # presenting image
        pygame.display.flip()

        # record window size changes
        screen_dims[0] = screen.get_width()
        screen_dims[1] = screen.get_height()

        # time step
        # too bad now:
        #   if the CA can't update in less than 1/fps_desired, fps will drop (and the app will become unresponsive)
        #   UPS can't be higher than FPS
        dt = clock.tick(fps_desired) / 1000
        if not paused:
            time_since_last_update += dt
        fps.add(clock.get_fps())
        ups.add(ups_s)

    pygame.quit()