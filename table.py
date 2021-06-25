from pygame.display import update
import pygame as pg
from pygame.constants import MOUSEBUTTONDOWN
import constants
import math
import cardImage
import cardhandImage
import sutda
import turnArrow
import propertyBox
import userChoiceWindow
import button
import numpy as np
import random
import time
import os

PI = math.pi
BASIC_BET = 100
SHUFFLING_CONST = 85
DEALING_CONST = 25
TURNING_CONST = 180
UPDATE_CONST = 120

class Table(constants.Constants):
    def __init__(self):
        super().__init__()
        self.radius = self.size[0] * DEALING_CONST / 100
        self.circle = [self.size * 0.5, self.radius]
        self.mypos = np.array([self.size[0] * 0.5, self.size[1] * 0.5 + self.radius])
        self.place = [self.mypos]
        self.cardhandImages = []
        self.n_player = 2
        self.table_color = self.GREEN

        self.cur_hour = int(time.strftime('%H'))
        self.time_of_day = 'Night'
        if 5 <= self.cur_hour < 17:
            self.time_of_day = 'Daytime'

        self.rect_color = lambda s: self.WHITE if s == 'Night' else self.BLACK 

        self.basic_bet = BASIC_BET
        self.highest_bet = 0

        self.highest_pos = [self.size[0] * 0.3, self.size[1] * 0.1]
        self.highest_size = np.array([self.size[0] * 0.15, self.size[1] * 0.05])
        self.highest_surface = pg.Surface(self.highest_size, pg.SRCALPHA)
        pg.draw.rect(self.highest_surface, self.GRAY(.5), \
            (0, 0, self.highest_size[0], self.highest_size[1]), 0)
        pg.draw.rect(self.highest_surface, self.rect_color(self.time_of_day), \
            (0, 0, self.highest_size[0], self.highest_size[1]), 2)

        self.HIGHEST_FONT = pg.font.Font(self.font('rg'), int(self.size.mean() / 35))
        self.highest_font_surface = self.HIGHEST_FONT.render(str(round(self.highest_bet)), True, self.BLUE)
        self.highest_rect = self.highest_font_surface.get_rect(center = self.highest_size / 2)
        self.highest_surface.blit(self.highest_font_surface, self.highest_rect)

        self.shuffle = False
        self.shuffling = False
        self.img_size = np.array([500, 500]) * 0.22
        self.cards_img = pg.image.load(os.getcwd() + '/data/bundle.png')
        self.cards_img = pg.transform.scale(self.cards_img, np.array(self.img_size).astype(int)).convert_alpha()
        self.cards_img.set_colorkey(self.WHITE)

        self.img_surface_size = np.array([500, 500]) * 0.22
        self.img_surface = pg.Surface(self.img_surface_size, pg.SRCALPHA)
        self.img_surface.fill(self.table_color)

        self.img_surface.blit(self.cards_img, [0, 0])
        
        self.oc = []

        # Clockwise
        self.order_dir = 1
        self.order = False
        self.ordering = False
        self.order_cards = []
        self.order_cardImages = []

        self.display = False

        self.merge = False
        self.merging = False

        self.deal = False
        self.dealing = False
        self.deal_player = [0] * self.n_player
        self.cur_t = 0
        self.c = []

        self.propertyBoxes = []
        self.bet = 0
        self.cost = 0
        self.bet_pos = [self.size[0] * 0.6, self.size[1] * 0.5]
        self.BET_FONT = pg.font.Font(self.font('rg'), int(self.size.mean() / 35))
        self.betBox_surface = self.BET_FONT.render(str(self.bet), True, self.BLACK)
        self.bet_t = 0

        self.NUM_FONT = pg.font.Font(self.font('rg'), int(self.size.mean() / 30))
        self.num_surfaces = []

        self.w = userChoiceWindow.UserChoiceWindow()

        self.basic_betting = False
        self.progress = False
        self.end = False

        self.restart_pos = self.size / 2
        self.restart_size = [self.size[0] * 0.2, self.size[1] * 0.1]
        self.restart_text = ['RESTART', int(self.size.mean() / 35)]
        self.rb = button.Button(self.screen, [self.restart_pos, self.restart_size], self.L_SBLUE, self.restart_text)

        self.game_count = 1
        self.properties = []

    def calc_pos(self, deg):
        return np.array([self.circle[0][0] + self.radius * math.sin(deg), \
            self.circle[0][1] + self.radius * math.cos(deg)])

    def visualize_table(self):
        pg.draw.circle(self.screen, self.table_color, self.circle[0], self.circle[1], 0)
        pg.draw.circle(self.screen, self.BLACK, self.circle[0], self.circle[1], 1)
        
    def update_players(self, n):
        self.n_player = n

        self.s = sutda.Sutda(self.n_player, self.basic_bet)
        if self.game_count > 1:
            for i in range(self.n_player):
                self.s.p[i].property = self.properties[i]

        self.shuffle_cards()
        self.order_player = [False for i in range(self.n_player)]
        self.deal_player = [[False, False] for i in range(self.n_player)]
        self.arrow = turnArrow.TurnArrow(self.n_player)
                
        for i in range(self.n_player - 1):
            self.place.append(self.calc_pos(2 * PI * (i + 1) / self.n_player))

        for d in range(2):
            for i in range(self.n_player):
                self.s.player_deal_card(i)

        self.order_cards = random.sample(self.s.cards, self.n_player)

        for i in range(self.n_player):
            pos = self.circle[0]

            self.oc.append(cardImage.CardImage([0, 0], 0.6))
            self.oc[i].set_pos([pos[0], pos[1]])
            self.oc[i].set_pos([pos[0], pos[1]])

            self.order_cardImages.append(cardImage.CardImage(self.order_cards[i], 0.6))
            self.order_cardImages[i].set_pos((pos[0] + self.radius * math.sin(math.radians(i * 360 / self.n_player)), \
                pos[1] + self.radius * math.cos(math.radians(i * 360 / self.n_player))))
            self.order_cardImages[i].rotate(i * 360 / self.n_player)

            self.c.append([cardImage.CardImage([0, 0], 0.6), cardImage.CardImage([0, 0], 0.6)])
            self.c[i][0].set_pos([pos[0], pos[1]])
            self.c[i][1].set_pos([pos[0], pos[1]])

            self.cardhandImages.append(
                cardhandImage.CardhandImage(self.s.card_hands[i], i, self.place, i * 360 / self.n_player)
            )

            self.propertyBoxes.append(propertyBox.PropertyBox(self.s.p[i], self.n_player))

    def visualize_betBox(self):
        rect = self.betBox_surface.get_rect(center = self.bet_pos)
        self.screen.blit(self.betBox_surface, rect)

    def update_betBox(self, cost, t):
        self.cost = cost
        self.bet += cost
        self.bet_t = t
        self.betBox_surface = self.BET_FONT.render(str(self.bet), True, self.BLACK)

    def betBox_update_motion(self, t):
        if t - self.bet_t < UPDATE_CONST:
            if self.cost != 0:
                color = lambda x: self.GRAY(.3) if x > 0 else self.RED
                num_with_sign = lambda x: '+' + str(x) if x > 0 else str(x)
                surface = self.BET_FONT.render(num_with_sign(self.cost), True, color(self.cost))
                rect = surface.get_rect(center = [self.bet_pos[0], self.bet_pos[1] - \
                    self.size[0] * 0.05 * (t - self.bet_t) / UPDATE_CONST])
                self.screen.blit(surface, rect)

        elif t - self.bet_t == UPDATE_CONST:
            self.bet_t = 0

    def visualize_highest_bet(self):
        rect = self.highest_surface.get_rect(center = self.highest_pos)
        self.screen.blit(self.highest_surface, rect)
    
    def update_highest_bet(self, cost):
        self.highest_bet = cost

        pg.draw.rect(self.highest_surface, self.GRAY(.5), \
            (0, 0, self.highest_size[0], self.highest_size[1]), 0)
        pg.draw.rect(self.highest_surface, self.rect_color(self.time_of_day), \
            (0, 0, self.highest_size[0], self.highest_size[1]), 2)

        self.highest_font_surface = self.HIGHEST_FONT.render(str(round(cost)), True, self.BLUE)
        self.highest_rect = self.highest_font_surface.get_rect(center = self.highest_size / 2)
        self.highest_surface.blit(self.highest_font_surface, self.highest_rect)

    def visualize_cardsbundle(self):
        if not self.shuffling:
            rect = self.img_surface.get_rect(center = self.size / 2)
            self.screen.blit(self.img_surface, rect)

    def shuffle_cards(self):
        self.s.shuffle_cards()

        self.cards_img = pg.image.load(os.getcwd() + '/data/bundle.png')
        self.img_size = np.array([500, 500]) * 0.22
        self.cards_img = pg.transform.scale(self.cards_img, np.array(self.img_size).astype(int)).convert_alpha()
        self.cards_img.set_colorkey(self.WHITE)
    
    def start_shuffling(self, event, t):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.cur_t == 0 and not self.shuffle and not self.shuffling:
                self.cur_t = t
                self.shuffling = True

    def shuffling_motion(self, t):
        if self.shuffling:
            if t - self.cur_t >= SHUFFLING_CONST:
                self.cur_t = 0
                self.shuffling = False
                self.shuffle = True
                self.cards_img = pg.image.load(os.getcwd() + '/data/bundle.png')
                return 

            pg.draw.rect(self.img_surface, self.table_color, [0, 0, self.img_surface_size[0], self.img_surface_size[1]], 0)
            if (t - self.cur_t) // 5 % 4 == 0: self.cards_img = pg.image.load(os.getcwd() + '/data/bundle.png')
            else: self.cards_img = pg.image.load(os.getcwd() + '/data/shuffle' + str((t - self.cur_t) // 5 % 4) + '.png')
            
            self.cards_img.set_colorkey(self.WHITE)
            self.cards_img = pg.transform.scale(self.cards_img, np.array(self.img_size).astype(int)).convert_alpha()
            self.img_surface.blit(self.cards_img, [0, 0])
            rect = self.img_surface.get_rect(center = self.size / 2)
            self.screen.blit(self.img_surface, rect)

    def start_ordering(self, event, t):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.cur_t == 0 and not self.order and not self.ordering:
                self.cur_t = t
                self.ordering = True

    def ordering_motion(self, t):
        if self.ordering and not self.display and not self.deal:
            for i in range(self.n_player):
                if t - self.cur_t < DEALING_CONST * (i + 1):
                    self.ordering_player_motion(t, i)
                    break

        self.visualize_ordering_realtime_cardhands()
    
    def ordering_player_motion(self, t, n):
        dir = np.array((self.place[n % self.n_player] - self.circle[0]) / \
            np.linalg.norm(self.place[n % self.n_player] - self.circle[0]))

        if t - self.cur_t == DEALING_CONST * n:
            self.oc[n % self.n_player].rotate(n * 360 / self.n_player)
            self.oc[n % self.n_player].set_pos((self.circle[0][0], self.circle[0][1]))
        self.oc[n % self.n_player].visualize()
        self.oc[n % self.n_player].move(dir * 6)

        if t - self.cur_t == DEALING_CONST * (n + 1) - 1:
            self.order_player[n % self.n_player] = True

    def visualize_ordering_realtime_cardhands(self):
        if self.ordering:
            for i in range(self.n_player):
                if self.order_player[i]:
                    self.oc[i].visualize()

    def ordering_card_open_control(self, event, t, time_of_day):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if t - self.cur_t > DEALING_CONST * self.n_player and not self.display:
                for i in range(self.n_player):
                    self.order_cardImages[i].flip()
                self.cur_t = t
                self.order = True
                self.ordering = False
                self.deal_player = [[False, False] for i in range(self.n_player)]

                self.update_first(time_of_day)
                self.arrow.update_turn(self.s.turn)

    def ordering_card_open(self):
        if self.order and not (self.merge or self.merging):
            for i in range(self.n_player):
                self.order_cardImages[i].visualize()

    def visualize_numbers(self, t):
        if self.order and not (self.merge or self.merging):
            for i in range(self.n_player):
                self.num_surfaces.append(self.NUM_FONT.render(str(self.order_cards[i][0]), True, self.PURPLE))

            for i in range(self.n_player):
                radius = self.size[0] * 0.15
                cent = self.size / 2
                deg = i * 360 / self.n_player
                pos = cent + radius * np.array([np.sin(np.radians(deg)), np.cos(np.radians(deg))])
                rect = self.num_surfaces[i].get_rect(center = pos)
                self.screen.blit(self.num_surfaces[i], rect)

            if t - self.cur_t == 60 and not self.display:
                self.display = True
                self.cur_t = 0
            
    def update_first(self, time_of_day):
        temp_list = []
        for card in self.order_cards:
            temp_list.append([card[0], 1 - card[1]])

        if self.order and not self.deal:
            if time_of_day == 'Night':
                self.s.turn = temp_list.index(max(temp_list))
                
            elif time_of_day == 'Daytime':
                self.s.turn = temp_list.index(max(temp_list))

            self.s.turn = 1
            self.s.p[self.s.turn].is_first = True

    def display_arrow(self, t):
        if self.display and not self.end:
            self.arrow.visualize(t)

    def start_merging(self, event, t):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.cur_t == 0 and self.order and not self.merge:
                self.cur_t = t
                self.merging = True

    def merging_motion(self, t):
        if not self.merge and self.merging and not self.deal:
            for i in range(self.n_player):
                if t - self.cur_t < DEALING_CONST * (i + 1):
                    self.merging_player_motion(t, i)
                    break
        
        if t - self.cur_t == DEALING_CONST * self.n_player and self.merging:
            self.merge = True
            self.merging = False

            self.cur_t = t
            self.shuffling = True

        self.visualize_merging_realtime_cardhands()
    
    def merging_player_motion(self, t, n):
        dir = -np.array((self.place[n % self.n_player] - self.circle[0]) / \
            np.linalg.norm(self.place[n % self.n_player] - self.circle[0]))

        self.oc[n % self.n_player].visualize()
        self.oc[n % self.n_player].move(dir * 6)

        if t - self.cur_t == DEALING_CONST * (n + 1) - 1:
            self.order_player[n % self.n_player] = False
            
    def visualize_merging_realtime_cardhands(self):
        if self.merging:
            for i in range(self.n_player):
                if self.order_player[i]:
                    self.oc[i].visualize()

    def start_dealing(self, event, t):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.cur_t == 0 and not self.deal and not self.dealing:
                self.cur_t = t
                self.dealing = True

    def dealing_motion(self, t):
        if self.dealing and not self.deal:
            for i in range(self.n_player):
                if t - self.cur_t < DEALING_CONST * (i + 1):
                    self.dealing_player_motion(t, i)
                    break
            
            for i in range(self.n_player, self.n_player * 2):
                if DEALING_CONST * i <= t - self.cur_t < DEALING_CONST * (i + 1):
                    self.dealing_player_motion(t, i)
                    break

            if t - self.cur_t == DEALING_CONST * self.n_player * 2:
                self.dealing = False
                self.deal = True
                self.cur_t = t

            self.visualize_dealing_realtime_cardhands()

    def dealing_player_motion(self, t, n):
        dir = np.array((self.place[n % self.n_player] - self.circle[0]) / \
            np.linalg.norm(self.place[n % self.n_player] - self.circle[0]))

        if t - self.cur_t == DEALING_CONST * n + 1:
            self.c[n % self.n_player][n // self.n_player].rotate(n * 360 / self.n_player)
            self.c[n % self.n_player][n // self.n_player].set_pos((self.circle[0][0], self.circle[0][1]))

        self.c[n % self.n_player][n // self.n_player].visualize()
        self.c[n % self.n_player][n // self.n_player].move(dir * 6)

        if t - self.cur_t == DEALING_CONST * (n + 1) - 1:
            self.deal_player[n % self.n_player][n // self.n_player] = True

    def visualize_dealing_realtime_cardhands(self):
        if not self.deal:
            for i in range(self.n_player):
                for j in range(2):
                    if self.deal_player[i][j]:
                        self.c[i][j].visualize()

    def visualize_cards(self):
        if self.deal and self.basic_betting and not self.end:
            for i in range(self.n_player):
                self.cardhandImages[i].visualize()

    def activate_user_window(self):
        if self.progress and self.s.turn == 0:
                self.w.active = True
                self.w.property = self.s.p[0].property
                self.w.before_bet = self.s.p[0].before_bet
                self.w.highest_bet = self.s.highest_bet

    def visualize_user_window(self):
        if self.w.active:
            self.w.visualize()
    
    def start_progress(self, t):
        if self.deal:
            if t - self.cur_t < TURNING_CONST:
                if t - self.cur_t < UPDATE_CONST:
                    self.basic_betting = True

                    if t - self.cur_t == 0:
                        self.update_betBox(self.basic_bet * self.n_player, t)
                    else:
                        self.betBox_update_motion(t)

                    for i in range(self.n_player):
                        if t - self.cur_t == 0:
                            self.propertyBoxes[i].update(-self.basic_bet)
                            self.s.p[i].property -= self.basic_bet

                        else:
                            self.propertyBoxes[i].update_motion(t - self.cur_t, UPDATE_CONST)

            elif not self.end and t - self.cur_t == TURNING_CONST:
                self.progress = True

    def visualize_choice(self, t):
        if self.progress:
            state = ''
            color = {'first bet': self.L_ORANGE, 'die': self.L_RED, \
                'call': self.L_GREEN, 'raise': self.L_BLUE, 'all-in': self.RED}
            
            if (t - self.cur_t) % TURNING_CONST == 0:
                if self.s.turn == 0:
                    self.activate_user_window()
                    act_but = self.w.active_button
                    self.w.active_button = -1

                    if act_but == 0:
                        self.s.p[0].die()

                    elif act_but == 1:
                        print(self.highest_bet - self.s.p[0].before_bet)
                        self.s.p[0].betting(self.highest_bet - self.s.p[0].before_bet)

                    elif act_but == 2:
                        call = self.highest_bet - self.s.p[0].before_bet
                        self.s.p[0].betting(round(call + (self.w.property - call) * self.w.value))

                    if act_but >= 0:
                        self.s.p[0].choice_str = self.w.b[act_but].text[0].lower()
                        self.w.active = False
                        
                else:
                    self.s.p[self.s.turn].auto_bet()
                
                bet = round(self.s.p[self.s.turn].bet)

                self.propertyBoxes[self.s.turn].update(-bet)
                self.update_betBox(bet, t)
                self.s.update_first_bet()
                self.s.update_highest_bet()
                self.update_highest_bet(self.s.highest_bet)
                
            if not self.w.active:
                state = self.s.p[self.s.turn].choice_str
                if state in ['first bet', 'raise', 'all-in']:
                    self.s.highest_player = self.s.turn

                FONT = pg.font.Font(self.font('rg'), int(self.size.mean() / 30))
                surface = FONT.render(state, True, color[state])

                rect = surface.get_rect(center = self.place[self.s.turn])
                self.screen.blit(surface, rect)

                self.propertyBoxes[self.s.turn].update_motion(t - self.bet_t, UPDATE_CONST) 
                self.betBox_update_motion(t)

                if (t - self.cur_t) % TURNING_CONST == TURNING_CONST - 1:
                    self.s.next_turn()
                    self.arrow.update_turn(self.s.turn)
                    self.s.update_highest_bet()
                    self.update_highest_bet(self.s.highest_bet)
                    #print(self.s.bets)
                
                    self.terminate_game(t)
    
    def visualize_dead_player(self):
        if self.progress:
            for i in range(self.n_player):
                if not self.s.p[i].state:
                    FONT = pg.font.Font(self.font('rg'), int(self.size.mean() / 30))
                    surface = FONT.render('die', True, self.L_RED)

                    rect = surface.get_rect(center = self.place[i])
                    self.screen.blit(surface, rect)

    def terminate_game(self, t):
        if self.progress:
            winner = self.s.game_winner()
            if winner >= 0:
                self.cur_t = t
                self.bet_t = t
                self.progress = False
                self.end = True
                self.update_highest_bet(0)
                self.propertyBoxes[winner].update(self.bet)
                self.update_betBox(-self.bet, t)

                for i in range(self.n_player):
                    if i > 0 and self.s.p[i].state:
                        self.cardhandImages[i].flip()
                    self.properties.append(self.s.p[i].property)
                print(self.properties)

                self.game_count += 1
                self.update_players(self.n_player)
            
    def ending_game_motion(self, t):
        if self.end:
            self.propertyBoxes[self.s.turn].update_motion(t - self.bet_t, UPDATE_CONST) 
            self.betBox_update_motion(t)

    def visualize_restart_button(self):
        if self.end:
            self.rb.visualize()
            self.rb.cursor_above()

    def restart_button_clicked(self, event):
        if self.end:
            self.rb.clicked(event)

    def start_new_game(self):
        if self.end and self.rb.active:
            self.cur_t = 0
            self.shuffle = False
            self.order = False
            self.display = False
            self.merge = False
            self.deal = False
            self.basic_betting = False
            self.progress = False
            self.end = False
            self.rb.active = False

    
    # def speck_point(self):
    #     for pos in self.place:
    #         pg.draw.circle(self.screen, self.L_RED, pos, 20)
