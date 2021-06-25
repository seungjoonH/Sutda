import constants as c
import pygame as pg
import numpy as np
import math
import time

class PropertyBox(c.Constants):
    def __init__(self, p, n_player):
        super().__init__()
        self.p = p
        self.property = p.property
        self.cost = 0
        self.n = p.my_turn
        self.deg = self.n * 360 / n_player
        self.radius = self.size[0] * 0.4
        self.circle = [self.size / 2, self.radius]

        self.cur_hour = int(time.strftime('%H'))
        self.time_of_day = 'Night'
        if 5 <= self.cur_hour < 17:
            self.time_of_day = 'Daytime'

        self.rect_color = lambda s: self.WHITE if s == 'Night' else self.BLACK 

        self.pos = np.array([self.circle[0][0] + self.radius * math.sin(math.radians(self.deg)), \
            self.circle[0][1] + self.radius * math.cos(math.radians(self.deg))])

        self.surface_size = [self.size[0] * 0.15, self.size[1] * 0.05]
        self.surface = pg.Surface(self.surface_size, pg.SRCALPHA)

        pg.draw.rect(self.surface, self.GRAY(.8), (0, 0, self.surface_size[0], self.surface_size[1]), 0)
        pg.draw.rect(self.surface, self.rect_color(self.time_of_day), (0, 0, self.surface_size[0], self.surface_size[1]), 2)

        self.FONT_PROPERTY = pg.font.Font(self.font('rg'), int(self.size.mean() / 35))
        self.font_surface = self.FONT_PROPERTY.render(str(round(self.property)), True, self.BLACK)

    def visualize(self):
        shape_rect = self.surface.get_rect(center = self.pos)
        font_rect = self.font_surface.get_rect(center = self.pos)
        self.screen.blit(self.surface, shape_rect)
        self.screen.blit(self.font_surface, font_rect)

    def update(self, cost):
        if self.p.state:
            self.cost = round(cost)
            self.property += cost
            self.font_surface = self.FONT_PROPERTY.render(str(round(self.property)), True, self.BLACK)

    def update_motion(self, t, update_const):
        if self.p.state:
            if t // update_const == 0:
                color = lambda x: self.GRAY(0.3) if x > 0 else self.RED
                num_with_sign = lambda x: '+' + str(x) if x > 0 else str(x)
                surface = self.FONT_PROPERTY.render(num_with_sign(self.cost), True, color(self.cost))
                rect = surface.get_rect(center = [self.pos[0], self.pos[1] - self.size[0] * 0.05 * (t % update_const) / update_const])
                self.screen.blit(surface, rect)

