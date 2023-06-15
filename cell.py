import pygame as pg
from random import choice


def create_cells(window_width: int, window_height: int, cell_side: int, cells_dic: dict, sprite_group):
    """creating and sorting cells"""
    start_column = int(0 - (0.10 * window_width))
    finish_column = int(window_width + (0.10 * window_width))
    start_row = int(0 - (0.10 * window_height))
    finish_row = int(window_height + (0.10 * window_height))
    cell_column = int(start_column / cell_side)
    for cell_width in range(start_column, finish_column, cell_side):
        cell_row = int(start_row / cell_side)
        for cell_height in range(start_row, finish_row, cell_side):
            cells_dic[(cell_column, cell_row)] = Cell(cell_side, cell_column, cell_row)
            sprite_group.add(cells_dic[(cell_column, cell_row)])
            cells_dic[(cell_column, cell_row)].set_neighbours(window_width, window_height)
            cell_row += 1
        cell_column += 1


def next_turn(mode: str):
    """transition between turns"""
    if mode == "normal":
        for key in Cell.all_cells:
            cell = Cell.all_cells[key]
            cell.state = cell.next_state if cell.next_state is not None else cell.state
    elif mode == "random":
        for key in Cell.all_cells:
            cell = Cell.all_cells[key]
            cell.state = choice(["alive", "unalive"])
    elif mode == "clear":
        for key in Cell.all_cells:
            cell = Cell.all_cells[key]
            cell.state = "unalive"


class Cell(pg.sprite.Sprite):
    all_cells = dict()  # cells storage. key: tuple(column, row) . value: {cell_object}

    def __init__(self, cell_side: int, column: int, row: int):
        pg.sprite.Sprite.__init__(self)
        self.side = cell_side
        self.image = pg.Surface((self.side, self.side))
        self.rect = self.image.get_rect()
        self.place = (column, row)
        self.rect.x = (column * self.side) - self.side
        self.rect.y = (row * self.side)
        self.state = "unalive"  # state that is cell color
        self.next_state = None # state in next turn
        # variables that stores neighbours of cell
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None
        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None

    def set_neighbours(self, window_width: int, window_height: int):
        """setting neighbours to cell"""
        max_column = int((window_width + (0.10 * window_width)) / self.side)
        max_row = int((window_height + (0.10 * window_height)) / self.side)
        min_column = int((0 - (0.10 * window_width)) / self.side)
        min_row = int((0 - (0.10 * window_height)) / self.side)

        self.top = (self.place[0], self.place[1] - 1) if self.place[1] > min_row else None
        self.bottom = (self.place[0], self.place[1] + 1) if self.place[1] + 1 < max_row else None
        self.left = (self.place[0] - 1, self.place[1]) if self.place[0] > min_column else None
        self.right = (self.place[0] + 1, self.place[1]) if self.place[0] + 1 < max_column else None
        self.top_left = (self.place[0] - 1, self.place[1] - 1) if self.place[1] > min_row and self.place[
            0] > min_column else None
        self.top_right = (self.place[0] + 1, self.place[1] - 1) if self.place[1] > min_row and self.place[
            0] + 1 < max_column else None
        self.bottom_left = (self.place[0] - 1, self.place[1] + 1) if self.place[0] > min_column and self.place[
            1] + 1 < max_row else None
        self.bottom_right = (self.place[0] + 1, self.place[1] + 1) if self.place[0] + 1 < max_column and self.place[
            1] + 1 < max_row else None

    def get_neighbours(self):
        lst = (self.top, self.bottom, self.left, self.right, self.top_left, self.top_right, self.bottom_left,
               self.bottom_right)
        return lst

    def clicked(self):
        self.state = "alive" if self.state == "unalive" else "unalive"

    def set_next_state(self):
        """setting state on next turn"""
        neighbours = self.get_neighbours()
        counter = 0
        for place in neighbours:  # loop for counting neighbours
            if place is None:
                continue
            neighbour = Cell.all_cells[place]
            if neighbour.state == "alive":
                counter += 1
            if counter >= 4: # if it reaches 4 then the counting makes no sens because after 4 nothing will change
                break

        # cell became alive if cell is unalive and haves 3 neighbours
        if self.state == "unalive":
            if counter == 3:
                self.next_state = "alive"
            else:
                self.next_state = "unalive"
        # if cell alive and have 2 or 3 neighbours then cell stays alive
        elif self.state == "alive":
            if counter < 2 or counter > 3:
                self.next_state = "unalive"

    def update(self, new_turn: bool, pause: bool):
        """update method is pygame built-in method for updating {Sprite_class} on screen """
        pg.sprite.Sprite.update(self)
        if not pause:
            if new_turn:
                self.set_next_state()
            else:
                self.next_state = self.state
        if self.state == "unalive":
            self.image.fill((255, 255, 255, 255))
            pg.draw.line(self.image, (0, 0, 0), (0, 0), (self.side, 0))
            pg.draw.line(self.image, (0, 0, 0), (0, 0), (0, self.side))
            pg.draw.line(self.image, (0, 0, 0), (self.side - 1, 0), (self.side - 1, self.side))
            pg.draw.line(self.image, (0, 0, 0), (0, self.side - 1), (self.side, self.side - 1))
        elif self.state == "alive":
            self.image.fill((0, 0, 0, 255))
