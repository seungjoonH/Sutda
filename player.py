from math import e
import random
import numpy as np

class Player:
    def __init__(self, n):
        self.my_turn = n
        self.is_first = False
        self.card_hand = []
        self.card_visible = [False, False, False]
        self.state = True
        self.choice_str = ''

        self.property = 10000
        self.bet = 0
        self.total_bet = 0
        self.highest_bet = 0
        self.before_bet = 0
        self.score_list = []
    
    def deal_card(self, card):
        if self.state:
            self.card_hand.append(card)
            self.card_visible[self.card_visible.count(True)] = True

    def abandon_card(self, n):
        self.card_hand.remove(n)

    def die(self):
        self.state = False
        self.choice_str = 'die'

    def betting(self, cost):
        self.bet += cost
        self.property -= cost

    def load_total_bet(self, bet):
        self.total_bet = bet

    def auto_choice(self):
        if self.highest_bet - self.before_bet > self.property:
            choice = 0

        elif self.highest_bet - self.before_bet == self.property:
            # die / +0%
            ap = [0.70, 0.30]
            slope = np.array([], dtype = float)

            for i in range(len(ap)):
                slope = np.append(slope, np.array([ap[len(ap) - i - 1] - ap[i]]))

            slope = slope / 27
            score = self.score_list[0]
            prob = [slope[i] * score + ap[i] for i in range(len(ap))]

            prob_accum = np.cumsum(prob)

            rn = random.random()
            choice = -1
            for i in range(len(ap)):
                if rn < prob_accum[i]:
                    choice = i
                    break

        else:
            # die / +0% / +20% / +40% / +60% / +80% / all-in
            bp = [0.27, 0.23, 0.19, 0.16, 0.09, 0.05, 0.01]
            slope = np.array([], dtype = float)

            for i in range(len(bp)):
                slope = np.append(slope, np.array([bp[len(bp) - i - 1] - bp[i]]))

            slope = slope / 27
            score = self.score_list[0]
            prob = [slope[i] * score + bp[i] for i in range(len(bp))]

            if self.is_first:
                prob = [prob[0] + prob[1], 0, prob[2], prob[3], prob[4], prob[5], prob[6]]

            # print(prob, sum(prob))
            prob_accum = np.cumsum(prob)

            rn = random.random()
            choice = -1
            for i in range(len(bp)):
                if rn < prob_accum[i]:
                    choice = i
                    break
        
        if choice == 1:
            self.choice_str = 'call'
        else:
            self.choice_str = 'raise'

        if self.is_first and choice > 0:
            self.choice_str = 'first bet'
            self.is_first = False

        if choice == 6:
            self.choice_str = 'all-in'

        return choice

    def update_highest_bet(self, cost):
        self.highest_bet = cost

    def auto_bet(self):
        choice = self.auto_choice()
        #print(self.my_turn, choice)

        if choice == 0:
            self.die()
        else:
            if self.highest_bet - self.before_bet > self.property:
                self.die()

            self.betting(self.highest_bet - self.before_bet)
            self.betting(self.property * (choice - 1) * 0.2)