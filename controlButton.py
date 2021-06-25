import pygame as pg
import numpy as np
import sys
from pygame import scrap
from pygame.constants import MOUSEBUTTONDOWN, SRCALPHA
import constants as c

# pg.init()
# size = np.array([700, 700])
# screen = pg.display.set_mode(size)

class ControlButton(c.Constants):
    def __init__(self, pos, mag):
        super().__init__()
        self.pos = pos
        self.button_size = self.size * 0.15 * mag
        self.rect = pg.Rect(self.pos[0] - self.button_size[0] / 2, \
            self.pos[1] - self.button_size[1] / 2, self.button_size[0], self.button_size[1])
        self.halfrect = [
            pg.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h / 2),
            pg.Rect(self.rect.x, self.rect.y + self.rect.h / 2, self.rect.w, self.rect.h / 2)
        ]
        self.font_pos = [self.rect.centerx - self.rect.w * 0.05, self.rect.centery]
        
        self.value = 2
        self.MAX_VALUE = 6
        self.MIN_VALUE = 2

        self.FONT = pg.font.Font(self.font('rg'), int(self.size.mean() * mag / 25))

        self.font_color = self.BLACK
        self.color = self.GRAY(.7)
        self.value_surface = self.FONT.render(str(self.value), True, self.font_color)
        self.surface_size = [self.button_size[0], self.button_size[1] / 2]
        self.surface = pg.Surface(self.button_size, pg.SRCALPHA)
        self.above_surface = [pg.Surface(self.surface_size, pg.SRCALPHA), \
            pg.Surface(self.surface_size, pg.SRCALPHA)]

        pg.draw.rect(self.surface, self.color, [0, 0, self.button_size[0], self.button_size[1]], 0)
        
        self.above_surface[0].set_alpha(50)
        self.above_surface[1].set_alpha(50)

        self.tri = [Triangle(self.rect.w / 5, 1, self.button_size), Triangle(self.rect.w / 5, -1, self.button_size)]

        self.above_surface[0].fill(self.BLACK)
        self.above_surface[1].fill(self.BLACK)

    def is_cursor_above(self, mouse_pos, rect):
        return mouse_pos[0] in range(rect.x, rect.x + rect.w) \
            and mouse_pos[1] in range(rect.y, rect.y + rect.h)

    def cursor_above(self):
        mouse_pos = pg.mouse.get_pos()
        if self.is_cursor_above(mouse_pos, self.halfrect[0]):
            rect = self.above_surface[0].get_rect(center = [self.pos[0], self.pos[1] - self.rect.h / 4])
            self.screen.blit(self.above_surface[0], rect)
        elif self.is_cursor_above(mouse_pos, self.halfrect[1]):
            rect = self.above_surface[1].get_rect(center = [self.pos[0], self.pos[1] + self.rect.h / 4])
            self.screen.blit(self.above_surface[1], rect)
    
    def update(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.halfrect[0].collidepoint(event.pos):
                self.above_surface[0].set_alpha(150)
                self.above_surface[1].set_alpha(50)
            elif self.halfrect[1].collidepoint(event.pos):
                self.above_surface[0].set_alpha(50)
                self.above_surface[1].set_alpha(150)
        
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.above_surface[0].set_alpha(50)
            self.above_surface[1].set_alpha(50)
            if self.halfrect[0].collidepoint(event.pos):
                self.value = min(self.value + 1, self.MAX_VALUE) 
            elif self.halfrect[1].collidepoint(event.pos):
                self.value = max(self.value - 1, self.MIN_VALUE) 

            self.value_surface = self.FONT.render(str(self.value), True, self.font_color)

                
    def visualize(self):
        self.tri[0].visualize(self.surface)
        self.tri[1].visualize(self.surface)

        shape_rect = self.surface.get_rect(center = self.pos)
        font_rect = self.value_surface.get_rect(center = self.font_pos)
        #above_rect = [self.above_surface[0].get_rect(center = self.pos), self.above_surface[1].get_rect(center = self.pos)]
        self.screen.blit(self.surface, shape_rect)
        self.screen.blit(self.value_surface, font_rect)
        #self.screen.blit(self.above_surface[0], above_rect[0])
        #self.screen.blit(self.above_surface[1], above_rect[1])

class Triangle(c.Constants):
    def __init__(self, base, dir, button_size):
        super().__init__()
        pos = [button_size[0] * 2 / 3, button_size[1] / 2 + dir * button_size[1] / 6]
        self.base = base
        self.dir = dir

        self.p = [pos, [pos[0] + base, pos[1]], [pos[0] + base / 2, pos[1] + dir * base / 2]]
        
    def visualize(self, surface):
        pg.draw.polygon(surface, self.GRAY(.5), self.p, 0)


# c = ControlButton(size, [50, 50])
# clock = pg.time.Clock()

# while True:
#     mouse_pos = pg.mouse.get_pos()
#     screen.fill(WHITE)

#     c.draw(screen)

#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             sys.exit()
        
#         elif event.type == pg.KEYDOWN:
#             if event.key == pg.K_ESCAPE:
#                 sys.exit()

#         c.update(event, mouse_pos)

#     pg.display.flip()
#     clock.tick(30)
