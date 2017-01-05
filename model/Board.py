

class Board:
    """
    Control game betting and public information.
    """
    cards = []

    betting = 0
    totalChip = 0
    bonus = 0
    lastBet = 0
    betString = {0:"Large bet", 1:"Middle bet", 2:"Small bet", 3:"Fold"}
    # turn : large, mid, small
    betTable = {1:[30,20,10],
                2:[40,20,10],
                3:[50,30,20]
                }

    def set_cards(self, cards):
        self.cards = cards

    def set_msg(self, msg):
        pass

    def set_bet_on_chip_lack(self, turn, bet):
        pass

    def set_bet(self, turn, player1_bet, player2_bet):
        avgBet = 1
        if player1_bet == 2 and player2_bet == 2:
            avgBet = 2
        elif player1_bet == 0 and player2_bet == 0:
            avgBet = 0
        self.betting = self.betTable[turn][avgBet]
        self.lastBet = avgBet
        self.totalChip += 2 * self.betting

        return avgBet, self.betting

    def get_cards(self):
        return self.cards

    def get_bet(self):
        return self.betting

    def get_last_bet_string(self):
        msg = self.betString[self.lastBet] + " in last turn.\n" + \
              str(2*self.betting) + " added to the bet.\n" + \
              "Total bet: " + str(self.totalChip)
        return msg

    def get_bet_string(self, turn):
        msg = "Large bet   : " + str(self.betTable[turn][0]) + "\n" + \
              "Middle bet: " + str(self.betTable[turn][1]) + "\n" + \
              "Small bet : " + str(self.betTable[turn][2])
        return msg

    def set_bonus(self, bonus):
        self.bonus = bonus

    def round_end(self):
        self.betting = 0
        self.totalChip = 0

    def round_reset(self):
        self.cards = []
        #self.betting = 0
        pass
