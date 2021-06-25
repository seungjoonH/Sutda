import pygame as pg
import sys
import constants as c
import controlButton
import cardImage
import button
import table
import time
import sunOrMoon

class Main(c.Constants):
    def __init__(self):
        super().__init__()
        self.n_player = 2

    def main(self):
        pg.init()
        pg.display.set_caption(self.title)

        self.clock = pg.time.Clock()
        self.ms = MainScreen()
        self.ps = PlayScreen()

        t = 0 
        while True:
            self.screen.fill(self.WHITE)
            
            if self.ms.active:
                self.ms.cb.visualize()
                self.ms.cb.cursor_above()
                self.ms.play_bt.cursor_above()

                self.ms.samgwang.set_pos([self.size[0] * 0.4, self.size[1] * 0.2])
                self.ms.palgwang.set_pos([self.size[0] * 0.6, self.size[1] * 0.2])
                self.ms.samgwang.visualize()
                self.ms.palgwang.visualize()

                self.ms.play_bt.visualize()
                self.ms.play_bt.cursor_above()

                self.ms.display_text()
            
            elif self.ps.active:
                self.ps.update_background_color()
                self.ps.update_clock(t)
                self.ps.visualize_clock()

                self.ps.sm.visualize()

                self.ps.tb.visualize_table()
                
                self.ps.tb.visualize_cardsbundle()
                self.ps.tb.shuffling_motion(t)
                self.ps.tb.visualize_betBox()
                self.ps.tb.visualize_highest_bet()

                self.ps.tb.ordering_motion(t)
                self.ps.tb.ordering_card_open()
                self.ps.tb.visualize_numbers(t)
                self.ps.tb.display_arrow(t)

                self.ps.tb.merging_motion(t)
                self.ps.tb.dealing_motion(t)
                self.ps.tb.visualize_cards()

                for i in range(self.ps.tb.s.n_player):
                    self.ps.tb.propertyBoxes[i].visualize()

                self.ps.tb.visualize_dead_player()
                self.ps.tb.visualize_user_window()

                self.ps.tb.w.visualize()
                self.ps.tb.w.cursor_above()

                self.ps.tb.start_progress(t)
                self.ps.tb.visualize_choice(t)

                self.ps.tb.ending_game_motion(t)

                self.ps.tb.visualize_restart_button()
                self.ps.tb.start_new_game()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        sys.exit()

                if self.ms.active:
                    self.ms.cb.update(event)
                    self.ms.play_bt.clicked(event)
                    self.n_player = self.ms.cb.value

                    self.ms.active = not self.ms.play_bt.active
                    self.ps.active = not self.ms.active
                    
                    if self.ps.active:
                        self.ps.tb.update_players(self.n_player)

                elif self.ps.active:
                    self.ps.tb.start_shuffling(event, t)
                    self.ps.tb.start_ordering(event, t)
                    self.ps.tb.ordering_card_open_control(event, t, self.ps.time_of_day)
                    self.ps.tb.start_merging(event, t)
                    self.ps.tb.start_dealing(event, t)
                    self.ps.tb.w.button_clicked(event)
                    self.ps.tb.w.control_adjustBar(event)
                    self.ps.tb.restart_button_clicked(event)

            t += 1

            pg.display.flip()
            self.clock.tick(60)

class MainScreen(c.Constants):
    def __init__(self):
        super().__init__()
        self.font_color = self.BLACK
        self.background_color = self.WHITE

        self.FONT_TITLE = pg.font.Font(self.font('bd'), int(self.size.mean() / 15))
        self.FONT_TEXT = pg.font.Font(self.font('bd'), int(self.size.mean() / 25))

        self.title = 'Sutda Game'
        self.text = 'number of players'

        self.title_pos = [self.size[0] * 0.5, self.size[1] * 0.43]
        self.text_pos = [self.size[0] * 0.4, self.size[1] * 0.6]

        self.title_surface = self.FONT_TITLE.render(self.title, True, self.font_color)
        self.text_surface = self.FONT_TEXT.render(self.text, True, self.font_color)

        self.play_bt = button.Button(
            self.screen, [[self.size[0] * 0.5, self.size[1] * 0.8], [self.size[0] * 0.2, self.size[1] * 0.1]],
            self.L_RED, ['Play Game', int(self.size.mean() / 35)]
        )
        
        self.active = True

        self.cb_pos = [self.size[0] * 0.7, self.size[1] * 0.6]

        self.cb = controlButton.ControlButton(self.cb_pos, .7)
        self.samgwang = cardImage.CardImage([3, 0], 1)
        self.palgwang = cardImage.CardImage([8, 0], 1)

    def display_text(self):
        title_pos = self.title_surface.get_rect(center = self.title_pos)
        self.screen.blit(self.title_surface, title_pos)
        text_pos = self.text_surface.get_rect(center = self.text_pos)
        self.screen.blit(self.text_surface, text_pos)

class PlayScreen(c.Constants):
    def __init__(self):
        super().__init__()
        self.active = False

        self.FONT_CLOCK = pg.font.Font(self.font('rg'), int(self.size.mean() / 40))
        self.clock_str = '%y.%m.%d %H:%M'
        self.clock_surface = self.FONT_CLOCK.render(self.clock_str, True, self.BLACK)

        self.cur_hour = int(time.strftime('%H'))
        self.time_of_day = 'Night'
        if 5 <= self.cur_hour < 17:
            self.time_of_day = 'Daytime'

        self.bg_color = self.GRAY((12 - abs(12 - self.cur_hour)) / 12)
        color = lambda x: self.BLACK if x == 'Daytime' else self.WHITE
        self.clock_color = color(self.time_of_day)

        self.sm = sunOrMoon.SunOrMoon(self.time_of_day)

        self.tb = table.Table()

    def update_background_color(self):
        self.bg_color = self.GRAY((12 - abs(12 - self.cur_hour)) / 12)
        self.screen.fill(self.bg_color)

    def visualize_clock(self):
        rect = self.clock_surface.get_rect(center = [self.size[0] * 0.85, self.size[1] * 0.05])
        self.screen.blit(self.clock_surface, rect)

    def update_clock(self, t):
        if (t // 30) % 2: self.clock_str = '%y.%m.%d %H %M'
        else: self.clock_str = '%y.%m.%d %H:%M'

        self.clock_surface = self.FONT_CLOCK.render(time.strftime(self.clock_str), True, self.clock_color)

m = Main()
m.main()



