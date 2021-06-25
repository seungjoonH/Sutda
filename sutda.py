import random
import player

class Sutda():
    def __init__(self, n, cost):
        self.n_player = n
        self.basic_bet = cost
        self.total_bet = 0
        self.highest_bet = 0
        self.highest_player = -1

        self.bets = []
        self.p = []
        for i in range(n):
            self.bets.append(0)
            self.p.append(player.Player(i))

        self.turn = 0
        
        self.cards = []
        for i in range(1, 11):
            for j in range(2):
                self.cards.append([i, j])

        self.card_hands = [[]] * n

        self.winner = -1
        self.open_ending = False

    def update_first_bet(self):
        if self.p[self.turn].is_first:
            bet = round(self.p[self.turn].bet)
            if bet == 0:
                self.p[self.turn].is_first = False
                self.p[(self.turn + 1) % self.n_player].is_first = True

    def update_highest_bet(self):
        bet = round(self.p[self.turn].bet)
        self.p[self.turn].bet = 0

        self.bets[self.turn] = bet
        self.p[self.turn].before_bet += bet
        self.highest_bet = max(self.p[self.turn].before_bet, self.highest_bet)

        self.p[self.turn].update_highest_bet(self.highest_bet)

    def next_turn(self):
        while True:
            self.turn = (self.turn + 1) % self.n_player

            if self.p[self.turn].state:
                break

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)
    
    def player_deal_card(self, n):
        self.p[n].card_hand.append(self.deal_card())
        self.card_hands[n] = self.p[n].card_hand
        
        if len(self.card_hands[n]) > 1:
            self.p[n].score_list = self.score_card_hand(self.card_hands[n])

    def score_card_hand(self, card_hand):
        ordinal_list = [['영', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉'], \
            ['일', '이', '삼', '사', '오', '육', '칠', '팔', '구', '장']]

        gwang_list = [[1, 0], [3, 0], [8, 0]]

        score = 0
        case_str = ''
        spec_str = ''

        # mangtong & keut & gabo
        score = (card_hand[0][0] + card_hand[1][0]) % 10
        case_str = ordinal_list[0][score] + '끗'
        if score == 0: case_str = '망통'
        elif score == 9: case_str = '갑오'

        # seryuk
        if score == 0 and (card_hand[0][0] == 4 or card_hand[0][0] == 6):
            score = 10
            case_str = '세륙'

        # jangsa
        if score == 4 and (card_hand[0][0] == 4 or card_hand[0][0] == 10):
            score = 11
            case_str = '장사'
        
        # jangping
        if score == 1 and (card_hand[0][0] == 1 or card_hand[0][0] == 10):
            score = 12
            case_str = '장삥'
        
        # guping
        if score == 0 and (card_hand[0][0] == 1 or card_hand[0][0] == 9):
            score = 13
            case_str = '구삥'
        
        # doksa
        if score == 5 and (card_hand[0][0] == 1 or card_hand[0][0] == 4):
            score = 14
            case_str = '독사'

        # ali
        if score == 3 and (card_hand[0][0] == 1 or card_hand[0][0] == 2):
            score = 15
            case_str = '알리'

        # taeng
        if card_hand[0][0] == card_hand[1][0]:
            score = 15 + card_hand[0][0]
            case_str = ordinal_list[1][card_hand[0][0] - 1] + '땡'

        # gwangtaeng
        if card_hand[0][1] == card_hand[1][1] == 0:
            if card_hand[0] in gwang_list and card_hand[1] in gwang_list:
                # sampal
                if not [1, 0] in card_hand:
                    score = 27
                    case_str = '삼팔'
                
                # ilsam & ilpal
                else:
                    score = 26
                    if not [3, 0] in card_hand:
                        case_str = '일팔'
                    else:
                        case_str = '일삼'
                
                case_str += '광땡'

        # taengjabi
        if score < 10 and card_hand[0][0] in [3, 7] and card_hand[1][0] in [3, 7]:
            spec_str = '땡잡이'
        
        # gusa
        if score < 10 and card_hand[0][0] in [4, 9] and card_hand[1][0] in [4, 9]:
            # meongteongguri
            if card_hand[0][1] == card_hand[1][1] == 0:
                spec_str = '멍텅구리'
            spec_str += '구사'
        
        # amhaengeosa
        if score < 10 and card_hand[0][0] in [4, 7] and card_hand[1][0] in [4, 7]:
            if card_hand[0][1] == card_hand[1][1] == 0:
                spec_str = '암행어사'
            
        return score, case_str, spec_str
            
    def who_wins(self, card_hands):
        score_list = []

        for card_hand in card_hands:
            score_list.append(self.score_card_hand(card_hand))
        print(score_list)

        # taengjabi > ilsam or ilpal
        if '땡잡이' in [i[2] for i in score_list]:
            if '일삼광땡' in [i[1] for i in score_list] or '일팔광땡' in [i[1] for i in score_list]:
                return [i[2] for i in score_list].index('땡잡이')

        # meongteongguri gusa
        if '멍텅구리구사' in [i[2] for i in score_list]:
            if max([j[0] for j in score_list]) < 26:
                return -1
        
        # gusa
        if '구사' in [i[2] for i in score_list]:
            if max([j[0] for j in score_list]) < 16:
                return -1

        # amhaengeosa
        if '암행어사' in [i[2] for i in score_list]:
            if max([j[0] for j in score_list]) == 26:
                return [i[2] for i in score_list].index('암행어사')

        if [j[0] for j in score_list].count(max([j[0] for j in score_list])) == 1:
            return [j[0] for j in score_list].index(max([j[0] for j in score_list]))
        
        return -1

    def game_winner(self):
        state_list = []

        for i in range(self.n_player):
            state_list.append(self.p[i].state)    

        if state_list.count(False) == self.n_player - 1:
            return state_list.index(True)

        print('#', self.highest_player)
        if self.highest_player == self.turn:
            self.open_ending = True
            
            card_hands = []

            for i in range(self.n_player):
                if self.p[i].state:
                    card_hands.append(self.card_hands[i])

            winner_of_survivors = self.who_wins(card_hands)

            cnt = 0
            for i in range(self.n_player):
                if self.p[i].state:
                    if cnt == winner_of_survivors:
                        print(self.turn, i)
                        return i
                    cnt += 1

        return -1

        
# n = 5
# s = Sutda(n, 100)

# s.shuffle_cards()

# for i in range(n):
#     s.player_deal_card(i)
#     s.player_deal_card(i)

# print(s.card_hands)
