import random
import constants as c
import pygame as pg
import numpy as np
import button
import adjustBar

class UserChoiceWindow(c.Constants):
    def __init__(self):
        super().__init__()
        self.active = False
        self.first = False

        window_size = self.size
        self.window = pg.Surface(window_size, pg.SRCALPHA)
        self.rect = pg.Rect(window_size[0] * 0.1, window_size[1] * 0.1, \
            window_size[0] * 0.8, window_size[1] * 0.8)

        pg.draw.rect(self.window, tuple(self.GRAY(.5)) + (150,), self.rect, 0)

        self.b = []
        button_color = [self.L_RED, self.L_GREEN, self.L_BLUE]
        button_text = ['DIE', 'CALL', 'RAISE']
        
        self.active_button = -1
        for i in range(3):
            self.b.append(button.Button(
                self.window, [np.array([self.size[0] * 0.5, self.size[1] * (0.5 + 0.1 * (i - 1))]), \
                    [self.size[0] * 0.2, self.size[1] * 0.08]], button_color[i], [button_text[i], int(self.size.mean() / 35)])
            )
            self.b[i].visualize()

        self.ab = adjustBar.AdjustBar(self.window, [self.size[0] * 0.5, self.size[1] * 0.7])

        self.property = 0
        self.before_bet = 0 
        self.highest_bet = 0
        self.value = 0

        self.FONT = pg.font.Font(self.font('rg'), int(self.size.mean() / 35))
        self.FONT_VALUE = pg.font.Font(self.font('rg'), int(self.size.mean() / 45))
        self.highest_surface = self.FONT.render(str(round(self.highest_bet)), True, self.L_GREEN)
        self.raise_surface = self.FONT.render('+' + str(round(( \
            self.property - self.highest_bet) * self.value)), True, self.L_BLUE)
        self.bet_surface = self.FONT.render('=' + str(round(
            self.highest_bet + (self.property - self.highest_bet) * self.value)), True, self.WHITE)
        self.value_surface = self.FONT_VALUE.render('+' + str(round(self.value * 100, 1)) + '%', True, self.RED)

        self.highest_rect = self.highest_surface.get_rect(center = [self.size[0] * 0.35, self.size[1] * 0.3])
        self.raise_rect = self.raise_surface.get_rect(center = [self.size[0] * 0.5, self.size[1] * 0.3])
        self.bet_rect = self.bet_surface.get_rect(center = [self.size[0] * 0.65, self.size[1] * 0.3])
        self.value_rect = self.value_surface.get_rect(center = [self.size[0] * 0.5, self.size[1] * 0.27])

        self.window.blit(self.highest_surface, self.highest_rect)
        self.window.blit(self.raise_surface, self.raise_rect)
        self.window.blit(self.value_surface, self.value_rect)

    def visualize(self):
        pg.draw.rect(self.window, tuple(self.BLACK) + (100,), self.rect, 0)

        if self.active:
            self.ab.visualize()
            self.visualize_costs()

            if self.value == 0:
                self.b[2].update_text('CALL', self.L_GREEN)
            elif self.value == 1:
                self.b[2].update_text('ALL-IN', self.RED)
            else:
                self.b[2].update_text('RAISE', self.BLACK)

            for i in range(3):
                self.b[i].visualize()

            rect = self.window.get_rect(center = self.size / 2)
            self.screen.blit(self.window, rect)

    def cursor_above(self):
        if self.active:
            for i in range(3):
                self.b[i].cursor_above()

    def button_clicked(self, event):
        if self.active:
            for i in range(3):
                self.b[i].clicked(event)
                
                if self.b[i].active:
                    self.b[i].active = False

                    self.active_button = i
                    if self.b[i].text[0] == 'CALL':
                        self.active_button = 1
                    break

    def control_adjustBar(self, event):
        if self.active:
            self.ab.adjust_circle(event)

    def visualize_costs(self):
        self.value = self.ab.value

        call = self.highest_bet - self.before_bet
        self.highest_surface = self.FONT.render(str(round(call)), True, self.L_GREEN)
        self.raise_surface = self.FONT.render('+' + str(round(( \
            self.property - call) * self.value)), True, self.L_BLUE)
        self.bet_surface = self.FONT.render('=' + str(round(
            call + (self.property - call) * self.value)), True, self.WHITE)
        self.value_surface = self.FONT_VALUE.render('+' + str(round(self.value * 100, 1)) + '%', True, self.RED)

        self.highest_rect = self.highest_surface.get_rect(center = [self.size[0] * 0.35, self.size[1] * 0.3])
        self.raise_rect = self.raise_surface.get_rect(center = [self.size[0] * 0.5, self.size[1] * 0.3])
        self.bet_rect = self.bet_surface.get_rect(center = [self.size[0] * 0.65, self.size[1] * 0.3])
        self.value_rect = self.value_surface.get_rect(center = [self.size[0] * 0.5, self.size[1] * 0.27])

        self.window.blit(self.highest_surface, self.highest_rect)
        self.window.blit(self.raise_surface, self.raise_rect)
        self.window.blit(self.bet_surface, self.bet_rect)
        self.window.blit(self.value_surface, self.value_rect)

        # rect = self.window.get_rect(center = self.size / 2)
        # self.screen.blit(self.window, rect)
