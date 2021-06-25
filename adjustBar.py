import constants as c
import pygame as pg
import math

class AdjustBar(c.Constants):
    def __init__(self, window, pos):
        super().__init__()
        self.pos = pos
        self.window = window
        self.surface_size = [self.size[0] * 0.5, self.size[1] * 0.1]
        self.surface = pg.Surface(self.surface_size, pg.SRCALPHA)

        self.drag = False
        self.value = 0.0
        
        self.rect = pg.Rect(self.surface_size[0] * 0.1, self.surface_size[1] * 0.48, \
            self.surface_size[0] * 0.8, self.surface_size[1] * 0.04)
        pg.draw.rect(self.surface, tuple(self.BLACK) + (0,), [0, 0, self.surface_size[0], self.surface_size[1]], 0)
        pg.draw.rect(self.surface, self.GRAY(.5), self.rect, 0)

        self.radius = self.size[0] * 0.015
        self.cirx_range = [self.surface_size[0] * 0.1, self.surface_size[0] * 0.9]
        self.cir_pos = [self.surface_size[0] * 0.1, self.rect.y + self.rect.h / 2]

        pg.draw.circle(self.surface, self.L_PURPLE, self.cir_pos, self.radius, 3)

        rect = self.surface.get_rect(center = self.pos)
        self.window.blit(self.surface, rect)

    def calc_x_perc(self, x):
        return (x - self.cirx_range[0]) / (self.cirx_range[1] - self.cirx_range[0])
    
    def restrict_x_range(self, x):
        if self.calc_x_perc(x) < 0:
            return self.cirx_range[0]

        elif self.calc_x_perc(x) > 1:
            return self.cirx_range[1]

        return x

    def visualize(self):
        rect = self.surface.get_rect(center = self.pos)
        self.window.blit(self.surface, rect)

    def adjust_circle(self, event):
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP or event.type == pg.MOUSEMOTION:
            real_pos = [event.pos[0] - self.pos[0] + self.surface_size[0] * 0.5, \
                event.pos[1] - self.pos[1] + self.surface_size[1] * 0.5]

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if math.dist(self.cir_pos, real_pos) < self.radius:
                    self.drag = True
                    pg.draw.circle(self.surface, self.L_PURPLE, self.cir_pos, self.radius, 3)
                    pg.draw.circle(self.surface, tuple(self.BLACK) + (150,), self.cir_pos, self.radius, 3)

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.drag = False
                pg.draw.circle(self.surface, self.L_PURPLE, self.cir_pos, self.radius, 3)

            if event.type == pg.MOUSEMOTION:
                if self.drag:
                    self.cir_pos[0] = self.restrict_x_range(real_pos[0])
                    pg.draw.rect(self.surface, tuple(self.BLACK) + (0,), [0, 0, self.surface_size[0], self.surface_size[1]], 0)
                    pg.draw.rect(self.surface, self.GRAY(.5), self.rect, 0)
                    pg.draw.circle(self.surface, self.L_PURPLE, self.cir_pos, self.radius, 3)
                    pg.draw.circle(self.surface, tuple(self.BLACK) + (150,), self.cir_pos, self.radius, 3)
                    self.value = self.calc_x_perc(self.cir_pos[0])
            
            