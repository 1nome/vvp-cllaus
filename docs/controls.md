# Visualizer controls:

## Keyboard:
 - `Space`: pauses/unpauses the simulation
 - `r`: resets the universe and generation counter
 - `-`: zooms out
 - `+`/`=`: zooms in
 - `h`/`left arrow`: moves left
 - `j`/`down arrow`: moves down
 - `k`/`up arrow`: moves up
 - `l`/`right arrow`: moves right
 - `a`: increment value under cursor
 - `p`/`C-v`: pastes from register
 - `y`/`C-c`: copies under cursor
 - `d`/`C-x`: copies then resets under cursor
 - `i`: changes from normal to insert mode;
 cursor in the middle of the window
 - `v`: changes from normal to visual mode;
 first and second cursor in the middle of the window
 - **`Esc`: changes back to normal mode/cancels saving/loading**
 - `w`/`C-s`: Saves under cursor/entire universe in normal mode to file
 - `e`/`C-o`: Loads from file to register
 - `C-a`: Selects entire universe
 - `1`/`2`: Increases ups by 1/10
 - `S-1`/`S-2`: Decrease ups by 1/10
 - `CR`: Confirms filename

 ## Mouse:
  - `Left button`: Hold and move mouse to move around the universe,
  click to set insert mode and move cursor to mouse curor.
  - `Right button`: Sets visual mode and first cursor to click pos,
  moves second cursor to mouse cursor while held.
  - `Mouse wheel up`: Zooms in on mouse cursor.
  - `Mouse wheel up`: Zooms out around mouse cursor.
  - `Middle button`: Increments value under mouse cursor.

## Modes:
 - NORMAL: Cursor is in the middle of the screen, keyboard pans the universe, 1x1
 - INSERT: Keyboard moves the cursor, 1x1
 - VISUAL: Keyboard moves the second cursor, rectangular cursor over multiple cells.
 Pastes to the second cursor.