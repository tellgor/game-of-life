import pygame as pg


class EventManager:
    """class for getting events from user like mouse clicks of keyboard input and store it"""
    def __init__(self):
        self._run = True  # check variable that means a game loop is going on
        self._mouse_pos = None  # returns mouse position: tuple(cor_x, cor_y)
        self._mouse_clicked = None  # returns mouse event index: int()
        self._key_pressed = None  # returns keyboard inputs: dict(  key: {key_name} value: bool )

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, value: bool):
        self._run = value

    @property
    def mouse_clicked(self):
        return self._mouse_clicked

    @mouse_clicked.setter
    def mouse_clicked(self, value):
        self._mouse_clicked = value

    @property
    def key_pressed(self):
        return self._key_pressed

    @key_pressed.setter
    def key_pressed(self, value):
        self._key_pressed = value

    @property
    def mouse_pos(self):
        return self._mouse_pos

    @mouse_pos.setter
    def mouse_pos(self, value):
        self._mouse_pos = value

    def check(self):
        self.mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            else:
                if event.type == pg.KEYDOWN:
                    self.key_pressed = pg.key.get_pressed()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_clicked = event.button

    def reset(self):
        self.mouse_clicked = None
        self.key_pressed = None
        self.mouse_pos = None
