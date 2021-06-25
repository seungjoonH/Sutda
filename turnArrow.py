from pygame.constants import MOUSEBUTTONDOWN
import constants as c
import pygame as pg
import numpy as np
import math

class TurnArrow(c.Constants):
    def __init__(self, n_player):
        super().__init__()
        self.radius = self.size[0] * 0.1
        self.circle = [self.size / 2, self.radius]

        self.surface_size = self.size * 0.04
        self.surface = pg.Surface(self.surface_size, pg.SRCALPHA)

        self.n_player = n_player
        self.deg = 0

        w, h = self.surface_size[0], self.surface_size[1]
        p = [[(0, 0), (w / 2, h / 3), (w / 2, h)], [(w, 0), (w / 2, h / 3), (w / 2, h)]]
        pg.draw.polygon(self.surface, self.L_ORANGE, p[0], 0)
        pg.draw.polygon(self.surface, self.ORANGE, p[1], 0)
        
    def update_turn(self, n):
        self.deg = n * 360 / self.n_player
        self.pos = np.array([self.circle[0][0] + self.radius * math.sin(math.radians(self.deg)), \
            self.circle[0][1] + self.radius * math.cos(math.radians(self.deg))])

        self.rotated_surface = pg.transform.rotate(self.surface, self.deg)

    def visualize(self, t):
        self.dynamic_movement(t)
        rect = self.rotated_surface.get_rect(center = self.pos)
        self.screen.blit(self.rotated_surface, rect)
    
    def dynamic_movement(self, t):
        dir = (self.pos - self.circle[0]) / np.linalg.norm(self.pos - self.circle[0])
        self.pos += dir * np.sign((t % 30) - 14.5)
