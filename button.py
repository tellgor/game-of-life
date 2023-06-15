import pygame as pg


def generate_text(surface, x_y: tuple, text: str, font_size: int, color: tuple):
    """generating text"""
    font = pg.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x = x_y[0]
    text_rect.y = x_y[1]
    surface.blit(text_surface, text_rect)


class Button(pg.sprite.Sprite):
    """Sprite class with button functional"""
    def __init__(self, button_width, button_height, button_x, button_y):
        pg.sprite.Sprite.__init__(self)
        self.width = button_width
        self.height = button_height
        self.color = (255, 255, 255, 255)
        self.image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = button_x
        self.rect.y = button_y
        self.text_cor = None
        self.text_size = None
        self.text = None
        self.check_mouse_point = False  # variable for checking if mouse point on button coordintes

    def backlight(self):
        if self.check_mouse_point:
            self.color = (220, 220, 220)
        else:
            self.color = (255, 255, 255)

    def clicked(self, mouse_click: tuple):
        click_x = mouse_click[0]
        click_y = mouse_click[1]
        if self.rect.collidepoint(click_x, click_y):
            return True
        else:
            return False

    def text_parameters(self, x_y: tuple, text: str, size: int):
        self.text_cor = x_y
        self.text = text
        self.text_size = size

    def update(self, mouse_pos: tuple):
        pg.sprite.Sprite.update(self)
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        self.check_mouse_point = True if self.rect.collidepoint(mouse_x, mouse_y) else False
        self.backlight()
        self.image.fill(self.color)
        generate_text(self.image, self.text_cor, self.text, self.text_size, (0, 0, 0))
        pg.draw.line(self.image, (0, 0, 0), (0, 0), (self.width, 0))
        pg.draw.line(self.image, (0, 0, 0), (0, 0), (0, self.height))
        pg.draw.line(self.image, (0, 0, 0), (self.width - 1, 0), (self.width - 1, self.width))
        pg.draw.line(self.image, (0, 0, 0), (0, self.height - 1), (self.width, self.height - 1))
