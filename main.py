import pygame as pg
from input import EventManager
import cell
from button import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DROP_BTN_WIDTH = 68
DROP_BTN_HEIGHT = 25
DROP_BTN_X = WINDOW_WIDTH - DROP_BTN_WIDTH - 7
DROP_BTN_Y = 5
REDACTOR_WIDTH = 240
REDACTOR_HEIGHT = 220
REDACTOR_X = WINDOW_WIDTH - REDACTOR_WIDTH - 7
REDACTOR_Y = DROP_BTN_Y + DROP_BTN_HEIGHT
CELL_SIZE_TEXT = 10
TURN_DELAY_TEXT = 5

pg.init()

event = EventManager()
window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)  # window setup

# creating redactor menu and buttons
drop_button = Button(DROP_BTN_WIDTH, DROP_BTN_HEIGHT, DROP_BTN_X, DROP_BTN_Y)
drop_button.text_parameters((2, 0), "show", 35)
drop_button_group = pg.sprite.Group()
drop_button_group.add(drop_button)

redactor_buttons = pg.sprite.Group()
clear_button = Button(60, 30, 10, 170)
clear_button.text_parameters((10, 7), "clear", 24)
redactor_buttons.add(clear_button)
random_button = Button(60, 30, 90, 170)
random_button.text_parameters((2, 7), "random", 23)
redactor_buttons.add(random_button)
submit_button = Button(60, 30, 170, 170)
submit_button.text_parameters((2, 7), "submit", 24)
redactor_buttons.add(submit_button)
size_increment_btn = Button(20, 20, 210, 55)
size_increment_btn.text_parameters((5, 0), "+", 24)
redactor_buttons.add(size_increment_btn)
size_decrease_btn = Button(20, 20, 152, 55)
size_decrease_btn.text_parameters((7, 0), "-", 24)
redactor_buttons.add(size_decrease_btn)

delay_increment_btn = Button(20, 20, 210, 95)
delay_increment_btn.text_parameters((5, 0), "+", 24)
redactor_buttons.add(delay_increment_btn)
delay_decrease_btn = Button(20, 20, 152, 95)
delay_decrease_btn.text_parameters((7, 0), "-", 24)
redactor_buttons.add(delay_decrease_btn)

redactor_menu = window.subsurface(REDACTOR_X, REDACTOR_Y, REDACTOR_WIDTH, REDACTOR_HEIGHT)


def draw_redactor(cell_size: int, turn_delay: int):
    """redactor menu init"""
    mouse_pos_x = event.mouse_pos[0] - REDACTOR_X if event.mouse_pos[0] > REDACTOR_X else 0
    mouse_pos_y = event.mouse_pos[1] - REDACTOR_Y if event.mouse_pos[1] > REDACTOR_Y else 0
    menu_mouse_cor = (mouse_pos_x, mouse_pos_y)
    redactor_menu.fill((255, 255, 255))
    generate_text(redactor_menu, (56, 3), "Redactor", 45, (0, 0, 0))
    generate_text(redactor_menu, (10, 55), "cell size", 30, (0, 0, 0))
    generate_text(redactor_menu, (180, 55), str(CELL_SIZE_TEXT), 30, (0, 0, 0))
    generate_text(redactor_menu, (10, 95), "turn delay", 30, (0, 0, 0))
    generate_text(redactor_menu, (180, 95), str(TURN_DELAY_TEXT), 30, (0, 0, 0))
    redactor_buttons.update(menu_mouse_cor)
    redactor_buttons.draw(redactor_menu)
    pg.draw.line(redactor_menu, (0, 0, 0), (0, 0), (REDACTOR_WIDTH, 0))
    pg.draw.line(redactor_menu, (0, 0, 0), (0, 0), (0, REDACTOR_HEIGHT))
    pg.draw.line(redactor_menu, (0, 0, 0), (REDACTOR_WIDTH - 1, 0), (REDACTOR_WIDTH - 1, REDACTOR_HEIGHT))
    pg.draw.line(redactor_menu, (0, 0, 0), (0, REDACTOR_HEIGHT - 1), (REDACTOR_WIDTH, REDACTOR_HEIGHT - 1))


def main():
    """organization of all scripts into main program"""
    global TURN_DELAY_TEXT, CELL_SIZE_TEXT
    # creating parameters and check variables
    cell_side = 10
    turn_delay = 5
    turn_mode = "normal"
    frame_counter = 0
    game_stop = False
    redactor_active = False
    cells_created = False
    cells_group = pg.sprite.Group()
    cells = cell.Cell.all_cells
    # game loop
    while event.run:
        event.check()
        # creating cells
        if not cells_created:
            cell.create_cells(WINDOW_WIDTH, WINDOW_HEIGHT, cell_side, cells, cells_group)
            cells_created = True

        # if game is not in pause mode
        if not game_stop:
            cell.next_turn(turn_mode)

        turn_mode = "normal"
        # if space clicked - pause
        if event.key_pressed is not None:
            if event.key_pressed[pg.K_SPACE]:
                game_stop = True if game_stop == False else False
        # event,mouse_clicked returns index of mouse button. index "1" is index for left mouse button
        if event.mouse_clicked == 1:
            # converting window coordinates into redactor surface coordinates
            menu_click_pos_x = event.mouse_pos[0] - REDACTOR_X if event.mouse_pos[0] > REDACTOR_X else 0
            menu_click_pos_y = event.mouse_pos[1] - REDACTOR_Y if event.mouse_pos[1] > REDACTOR_Y else 0
            redactor_click_cor = (menu_click_pos_x, menu_click_pos_y)
            if drop_button.clicked(event.mouse_pos):
                redactor_active = True if redactor_active is False else False
                if redactor_active is True:
                    drop_button.text = "hide"
                    drop_button.rect.y += REDACTOR_HEIGHT + DROP_BTN_HEIGHT
                else:
                    drop_button.text = "show"
                    drop_button.rect.y -= REDACTOR_HEIGHT + DROP_BTN_HEIGHT
                    CELL_SIZE_TEXT = cell_side
                    TURN_DELAY_TEXT = turn_delay
            elif size_increment_btn.clicked(redactor_click_cor):
                CELL_SIZE_TEXT += 1 if CELL_SIZE_TEXT < 25 else 0
            elif size_decrease_btn.clicked(redactor_click_cor):
                CELL_SIZE_TEXT -= 1 if 5 < CELL_SIZE_TEXT else 0
            elif delay_increment_btn.clicked(redactor_click_cor):
                TURN_DELAY_TEXT += 1 if TURN_DELAY_TEXT < 30 else 0
            elif delay_decrease_btn.clicked(redactor_click_cor):
                TURN_DELAY_TEXT -= 1 if 0 < TURN_DELAY_TEXT else 0
            elif clear_button.clicked(redactor_click_cor):
                turn_mode = "clear"
            elif random_button.clicked(redactor_click_cor):
                turn_mode = "random"
            elif submit_button.clicked(redactor_click_cor):
                turn_delay = TURN_DELAY_TEXT
                if cell_side != CELL_SIZE_TEXT:
                    cell_side = CELL_SIZE_TEXT
                    cells_group.empty()
                    cell.Cell.all_cells = dict()
                    cells = cell.Cell.all_cells
                    cells_created = False
            # if no beutton is clicked finding which cell is clicked and using {Cell_object}.clicked() method
            else:
                for key in cells:
                    mouse_x = event.mouse_pos[0]
                    mouse_y = event.mouse_pos[1]
                    if key[0] != int(mouse_x / cell_side):  # finding column of cell
                        continue
                    if key[1] != int(mouse_y / cell_side):  # finding row of cell
                        continue
                    current_cell = cells[(key[0] + 1), key[1]]
                    current_cell.clicked()

        # checking delay between turns
        if turn_delay == 0 or frame_counter % turn_delay == 0:
            cells_group.update(True, game_stop)
        else:
            cells_group.update(False, game_stop)

        # rendering screen frame
        cells_group.draw(window)
        drop_button_group.update(event.mouse_pos)
        drop_button_group.draw(window)

        if redactor_active:
            draw_redactor(cell_side, turn_delay)

        pg.display.flip()
        frame_counter += 1
        event.reset()

    pg.quit()


if __name__ == "__main__":
    main()
