import pygame
import numpy as np
from .core import vizState, clear

FONT_SIZE = 32
STATS_OFFSET_X = 250
STATS_PAD_Y = 5
AVG_OVER = 64
MODE_OFFSET = 5

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

    mouse_down = False
    mouse_move = False
    paused = config.paused
    move_x = 0
    move_y = 0
    crosshair = False
    visual = False
    insert = False

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

    while running:

        def zoom(dir, cur_x, cur_y):
            """
            Updates cell size while keeping it above 0.
            Also updates offsets so that the cursor points to the same place.
            """
            newsize = size + (1 if dir else (-1 if size > 1 else 0))
            return ((x_offset - cur_x) // size) * newsize + cur_x, ((y_offset - cur_y) // size) * newsize + cur_y, newsize

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # stops the loop (thus pygame)
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_down = True
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    x_offset, y_offset, size = zoom(False, event.pos[0], event.pos[1])
                elif event.button == pygame.BUTTON_WHEELUP:
                    x_offset, y_offset, size = zoom(True, event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    if mouse_down and not mouse_move:
                        # toggle cell under cursor
                        x = (-x_offset + event.pos[0]) // size
                        y = (-y_offset + event.pos[1]) // size
                        if 0 <= x < universe.shape[0] and 0 <= y < universe.shape[1]:
                            universe[x, y] = config.ca.next_vals[universe[x, y]]
                    mouse_down = False
                    mouse_move = False
            elif event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    mouse_move = True
                    x_offset += event.rel[0]
                    y_offset += event.rel[1]
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
                    move_x += kb_move
                elif event.key in (pygame.K_j, pygame.K_DOWN):
                    move_y -= kb_move
                elif event.key in (pygame.K_k, pygame.K_UP):
                    move_y += kb_move
                elif event.key in (pygame.K_l, pygame.K_RIGHT):
                    move_x -= kb_move
                elif event.key == pygame.K_a:
                    crosshair = True
                elif event.key == pygame.K_i and not visual:
                    insert = True
                elif event.key == pygame.K_v and not insert:
                    visual = True
                elif event.key == pygame.K_ESCAPE:
                    insert = False
                    visual = False
            elif event.type == pygame.KEYUP:
                # move
                if event.key in (pygame.K_h, pygame.K_LEFT):
                    move_x -= kb_move
                elif event.key in (pygame.K_j, pygame.K_DOWN):
                    move_y += kb_move
                elif event.key in (pygame.K_k, pygame.K_UP):
                    move_y -= kb_move
                elif event.key in (pygame.K_l, pygame.K_RIGHT):
                    move_x += kb_move
                # modyfying the universe
                elif event.key == pygame.K_a:
                    x = (-x_offset + screen_dims[0] // 2) // size
                    y = (-y_offset + screen_dims[1] // 2) // size
                    if 0 <= x < universe.shape[0] and 0 <= y < universe.shape[1]:
                        universe[x, y] = config.ca.next_vals[universe[x, y]]
                    crosshair = False

        # keyboard move
        x_offset += int(move_x / fps_desired)
        y_offset += int(move_y / fps_desired)

        # stats
        stats = []
        if show_fps:
            stats.append(f"fps: {fps():.0f}/{fps_desired:.0f}")
        if show_ups:
            stats.append(f"ups: {ups():.0f}/{ups_desired:.0f}")

        def clamp(a, max):
            return a if a < max else max
        
        # calculate the visible area offsets
        base_offset_x = (-x_offset if x_offset < 0 else 0) // size
        base_offset_y = (-y_offset if y_offset < 0 else 0) // size
        visible_dims_x = (screen_dims[0] // size + 1)
        visible_dims_y = (screen_dims[1] // size + 1)

        # clear image
        screen.fill(config.colors[3])

        # rendering
        for x in range(base_offset_x, clamp(base_offset_x + visible_dims_x, universe.shape[0])):
            for y in range(base_offset_y, clamp(base_offset_y + visible_dims_y, universe.shape[1])):
                if universe[x, y]:
                    pygame.draw.rect(screen, config.ca.colors[universe[x, y]],
                                    (x * size + x_offset, y * size + y_offset, size, size))
        pygame.draw.rect(screen, config.colors[1], (x_offset, y_offset, universe.shape[0] * size, universe.shape[1] * size), 1)
        if crosshair:
            x = (-x_offset + screen_dims[0] // 2) // size
            y = (-y_offset + screen_dims[1] // 2) // size
            pygame.draw.rect(screen, config.colors[2], (x * size + x_offset, y * size + y_offset, size, size), 1)
        o = STATS_PAD_Y
        for s in stats:
            text = font.render(s, True, config.colors[0])
            rect = text.get_rect()
            rect.topleft = (screen_dims[0] - STATS_OFFSET_X, o)
            screen.blit(text, rect)
            o += FONT_SIZE
        text = font.render("VISUAL" if visual else "INSERT" if insert else "NORMAL", True, config.colors[0])
        rect = text.get_rect()
        rect.bottomleft = (MODE_OFFSET, screen_dims[1])
        screen.blit(text, rect)
        
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