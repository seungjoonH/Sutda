import constants as c
import pygame as pg
import numpy as np

class Button(c.Constants):
    # data = [[x, y], [w, h]]
    def __init__(self, window, data, color, text):
        super().__init__()
        self.window = window
        self.pos = data[0]
        self.rect = pg.Rect([self.pos[0] - data[1][0] / 2, self.pos[1] - data[1][1] / 2, data[1][0], data[1][1]])
        self.color = color
        self.text = text

        self.FONT = pg.font.Font(self.font('rg'), text[1])
        self.text_surface = self.FONT.render(text[0], True, self.BLACK)

        self.surface_size = np.array([self.rect.w, self.rect.h])
        self.surface = pg.Surface(self.surface_size, pg.SRCALPHA)
        self.above_surface = pg.Surface(self.surface_size, pg.SRCALPHA)

        self.rect_in_surf = [0, 0, self.surface_size[0], self.surface_size[1]]
        pg.draw.rect(self.surface, self.color, self.rect_in_surf, 0)

        self.above_surface.fill(self.BLACK)
        self.above_surface.set_alpha(50)

        self.active = False

    def update_text(self, text, color):
        self.text[0] = text
        self.text_surface = self.FONT.render(self.text[0], True, color)

    def visualize(self):
        shape_rect = self.surface.get_rect(center = self.pos)
        text_rect = self.text_surface.get_rect(center = self.pos)
        self.window.blit(self.surface, shape_rect)
        self.window.blit(self.text_surface, text_rect)

    def is_cursor_above(self, mouse_pos, rect):
        return mouse_pos[0] in range(rect.x, rect.x + rect.w) \
            and mouse_pos[1] in range(rect.y, rect.y + rect.h)

    def cursor_above(self):
        mouse_pos = pg.mouse.get_pos()
        if self.is_cursor_above(mouse_pos, self.rect):
            text_rect = self.above_surface.get_rect(center = self.pos)
            self.screen.blit(self.above_surface, text_rect)

    def clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.above_surface.set_alpha(150)

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.above_surface.set_alpha(50)
            if self.rect.collidepoint(event.pos):
                self.active = True


        
