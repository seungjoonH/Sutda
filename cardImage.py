import pygame as pg
import numpy as np
import sys
import os
from pygame.constants import MOUSEBUTTONDOWN
import constants as c
import math

PI = math.pi

class CardImage(c.Constants):
    def __init__(self, card, mag):
        super().__init__()
        self.card = card
        self.mag = mag
        self.pos = np.array([0, 0], dtype = float)
        self.deg = 0
        
        self.back_img = pg.image.load(os.getcwd() + '/data/back.png')
            
        self.img = self.back_img
        if self.card != [0, 0]:
            self.img = pg.image.load(os.getcwd() + '/data/' + '{:02d}'.format(card[1] * 10 + card[0]) + '.png')

        self.img_size = np.array([int(self.size[0] * 0.1), int(self.size[1] * 0.15)]) * self.mag
        self.img = pg.transform.scale(self.img, np.array(self.img_size).astype(int))

        self.img_surface_size = np.array([self.img_size[1], self.img_size[1]])
        self.img_surface = pg.Surface(self.img_surface_size, pg.SRCALPHA)

        self.img_surface.blit(self.img, [(self.img_size[1] - self.img_size[0]) / 2, 0])
        self.rotated_surface = pg.transform.rotate(self.img_surface, math.degrees(self.deg))

        self.visible = False

    def set_pos(self, pos):
        self.pos = pos

    def visualize(self):
        self.visible = True
        rect = self.rotated_surface.get_rect(center = self.pos)
        self.screen.blit(self.rotated_surface, rect)

    def flip(self):
        self.visible = not self.visible
        self.img, self.back_img = self.back_img, self.img

    # def click_flip(self, event):
    #     if self.visible:
    #         if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
    #             size = np.array(self.img_size * self.mag).astype(int)
    #             hori = np.array([-size[0], size[0]]) * 0.5 + self.pos[0]
    #             vert = np.array([-size[1], size[1]]) * 0.5 + self.pos[1]

    #             if hori[0] < event.pos[0] < hori[1] and vert[0] < event.pos[1] < vert[1]:
    #                 self.flip()

    def move(self, pos):
        self.pos += pos

    def rotate(self, deg):
        self.deg += deg % 360
        self.rotated_surface = pg.transform.rotate(self.img_surface, self.deg)
