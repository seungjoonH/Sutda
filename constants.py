import pygame as pg
import numpy as np
import os

class Constants:
    def __init__(self):
        self.size = np.array([600, 600])
        self.screen = pg.display.set_mode(self.size)
        self.title = 'Sutda'

        font = os.getcwd() + '/fonts/unispace/unispace rg.ttf'
        self.font = lambda x: font.replace('rg', x)

        self.BLACK  = np.array((  0,   0,   0))
        self.WHITE  = np.array((255, 255, 255))
        self.GRAY   = lambda x: self.WHITE * x
        self.BROWN  = np.array((201, 107,   0))
        self.RED    = np.array((255,   0,   0))
        self.GREEN  = np.array(( 79, 175,   0))
        self.BLUE   = np.array((  0,   0, 255))
        self.ORANGE = np.array((255, 162,   0))
        self.YELLOW = np.array((255, 255,   0))
        self.PURPLE = np.array((180,   0, 180))

        self.L_RED    = np.array((255, 140, 140))
        self.L_ORANGE = np.array((255, 200, 140))
        self.L_YELLOW = np.array((255, 255, 140))
        self.L_GREEN  = np.array((140, 255, 140))
        self.L_SBLUE  = np.array((140, 255, 255))
        self.L_BLUE   = np.array((140, 140, 255))
        self.L_PURPLE = np.array((200, 140, 255))


