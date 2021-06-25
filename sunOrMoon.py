import pygame as pg
import constants as c
import time
import numpy as np
import math

class SunOrMoon(c.Constants):
    def __init__(self, time_of_day):
        super().__init__()
        self.surface_size = self.size * 0.15
        self.surface = pg.Surface(self.surface_size, pg.SRCALPHA)
        self.time_of_day = time_of_day
        self.pos = self.size * 0.1

        self.cur_hour = int(time.strftime('%H'))
        self.bg_color = self.GRAY((12 - abs(12 - self.cur_hour)) / 12)

        self.radius = self.surface_size[0] * 0.35
        t = [np.array([0, -self.surface_size[1] / 2]), \
            np.array([-self.radius / 6, -self.surface_size[1] * 0.4]), \
            np.array([ self.radius / 6, -self.surface_size[1] * 0.4])]

        if time_of_day == 'Night':
            pg.draw.circle(self.surface, self.YELLOW, self.surface_size / 2, self.radius)
            pg.draw.circle(self.surface, self.bg_color, \
                self.surface_size / 2 + np.array([1, -1]) * self.radius / 3, self.radius)
        
        elif time_of_day == 'Daytime':
            pg.draw.circle(self.surface, self.ORANGE, self.surface_size / 2, self.radius)
            
            flare_count = 10
            for i in range(flare_count):
                deg = i * 360 / flare_count
                
                v = self.surface_size / 2
                rot = np.array([[math.cos(math.radians(deg)), -math.sin(math.radians(deg))], \
                    [math.sin(math.radians(deg)), math.cos(math.radians(deg))]])

                pg.draw.polygon(self.surface, self.ORANGE, [v + np.dot(rot, t[0]), \
                    v + np.dot(rot, t[1]), v + np.dot(rot, t[2])], 0)


    def visualize(self):
        rect = self.surface.get_rect(center = self.pos)
        self.screen.blit(self.surface, rect)