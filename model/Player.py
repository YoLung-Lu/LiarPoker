
class Player:
    def __init__(self, id):
        self.id = id
        self.chip = 500
        self.round_reset()
        
    def round_reset(self):
        self.hand = []
        self.bet = 0
        self.currentTurn = 1
        self.lie = False
        self.suspect = False
        self.caught = False

    def bet(self, betting):
        if betting < self.chip:
            self.bet = betting
            return True
        return False

    def reorderCard(self, cardList):
        delta = 0
        for i in cardList:
            self.hand.append( self.hand.pop(i-delta) )
            delta += 1
