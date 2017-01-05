from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from SingleCard import SingleCard
from kivy.uix.widget import Widget
from deuces import Card, Evaluator, Deck
from kivy.uix.label import Label

class Public_Area(BoxLayout):
    id = "public_area"
    round = 1
    turn = 1
    betString = {0:"Large bet", 1:"Middle bet", 2:"Small bet", 3:"Fold"}


    def init_deck(self):
        self._init_child_widget()

    def _init_child_widget(self):
        # put 2 public cards before player2_score and button
        for i in range(2):
            c = SingleCard(id = 'public_card' + str(i))
            c.disable_check()

            self.add_widget(c, index = 2)
            self.ids[c.id] = c
            # space between cards
            self.add_widget(Widget(size_hint= (0.01, 1)), index = 2 )

    def update_turn(self, turn):
        self.turn = turn

    def update_round(self, round):
        self.round = round
        self.turn  = 1

    def update_hand(self, hand):
        for i in range(2):
            card = Card.int_to_str(hand[i])
            self.ids["public_card" + str(i)].set_card(card[0], card[1])
            self.ids["public_card" + str(i)].show_card_to_all()
        #self.ids.public_card0.la.text = Card.int_to_pretty_str( hand[0] )
        #self.ids.public_card0.lb.text = self.ids.public_card0.la.text
        #self.ids.public_card1.la.text = Card.int_to_pretty_str( hand[1] )
        #self.ids.public_card1.lb.text = self.ids.public_card1.la.text

    def set_info(self, msg = ""):
        info = "<< Information >>\n"
        info = info + "Round: " + str(self.round) + ", turn: " + str(self.turn) + "\n"
        info = info + msg
        self.ids['info_label_id'].text = info

    def set_chip_info(self, c1, c2, bonus):
        info = "<< Chip >>\n" + \
               "Player1: " + str(c1)  + "\n" + "Player2: " + str(c2) + "\n" +\
               "Bonus: " + str(bonus)
        self.ids['chip_label_id'].text = info

    def set_bet_info(self, b1, b2, avgBet, chip):
        info = "<< Bet >>\n" + \
               "Player1: " + self.betString[b1]  + "\n" + "Player2: " + self.betString[b2] + "\n" + \
               self.betString[avgBet] +"\n" + \
               "Chip: " + str(chip)
        self.ids['bet_label_id'].text = info

    def set_message(self, msg):
        # TODO: replace the function of this method with "set_info"
        self.ids['public_button_id'].text = msg
        pass

    def press_new_round(self):
        self.parent.press_new_round()
        pass

    def _test_msg(self):
        self.set_info("Game Start !!")
        self.set_chip_info(500, 500)
        self.set_bet_info(100, 100)
