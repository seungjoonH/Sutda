import constants as c
import os
import pygame as pg
import numpy as np

class CardhandImage(c.Constants):
    def __init__(self, card_hand, n, place, deg):
        super().__init__()
        self.card_hand = card_hand
        self.n = n

        self.place = place
        self.pos = np.array(self.place[n])
        self.mag = 0.6
        self.deg = deg
        
        self.imgs = [pg.image.load(os.getcwd() + '/data/' + '{:02d}'.format(card_hand[0][1] * 10 + card_hand[0][0]) + '.png'), \
            pg.image.load(os.getcwd() + '/data/' + '{:02d}'.format(card_hand[1][1] * 10 + card_hand[1][0]) + '.png')]
        self.back_img = pg.image.load(os.getcwd() + '/data/back.png')
        
        self.visible = False
        if self.n == 0: self.visible = True

        for i in range(2):
            if not self.visible:
                self.imgs[i] = self.back_img
        
        self.img_size = np.array([int(self.size[0] * 0.1), int(self.size[1] * 0.15)])
        self.img_size = np.array(self.img_size * self.mag).astype(int)
        self.surface_size = np.array([self.img_size[0] * 2.2, self.img_size[0] * 2.2], dtype = int)
        self.imgs[0] = pg.transform.scale(self.imgs[0], self.img_size)
        self.imgs[1] = pg.transform.scale(self.imgs[1], self.img_size)

        self.img_surface = pg.Surface(self.surface_size, pg.SRCALPHA)
        self.rect = self.img_surface.get_rect()

        self.img_surface.blit(self.imgs[0], [0, (self.surface_size[1] - self.img_size[1]) * 0.5])
        self.img_surface.blit(self.imgs[1], [int(self.img_size[0] * 1.2), (self.surface_size[1] - self.img_size[1]) * 0.5])
        self.img_surface = pg.transform.rotate(self.img_surface, self.deg)
    
    def flip(self):
        self.visible = not self.visible

    def visualize(self):
        for i in range(2):
            if not self.visible:
                self.imgs[i] = self.back_img
        
        self.img_size = np.array([int(self.size[0] * 0.1), int(self.size[1] * 0.15)])
        self.img_size = np.array(self.img_size * self.mag).astype(int)
        self.surface_size = np.array([self.img_size[0] * 2.2, self.img_size[0] * 2.2], dtype = int)
        self.imgs[0] = pg.transform.scale(self.imgs[0], self.img_size)
        self.imgs[1] = pg.transform.scale(self.imgs[1], self.img_size)

        self.img_surface = pg.Surface(self.surface_size, pg.SRCALPHA)
        self.rect = self.img_surface.get_rect()

        self.img_surface.blit(self.imgs[0], [0, 0])
        self.img_surface.blit(self.imgs[1], [int(self.img_size[0] * 1.2), 0])
        self.img_surface = pg.transform.rotate(self.img_surface, self.deg)

        rect = self.img_surface.get_rect(center = self.pos)
        self.screen.blit(self.img_surface, rect)
