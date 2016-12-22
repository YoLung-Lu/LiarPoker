
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from SingleCard import SingleCard
from kivy.uix.widget import Widget
from deuces import Card, Evaluator, Deck

class PlayerDeck_Top(BoxLayout):
    id = "player2_box"
    but_2 = ObjectProperty(None)

    def init_deck(self):
        # create widgets of player deck
        for i in range(5):
            c = SingleCard(id = 'player2_card' + str(i))
            self.ids[c.id] = c
            self.add_widget(c)
            self.add_widget(Widget(size_hint= (0.01, 1)) )

    def round_reset(self):
        for i in range(5):
            self.ids['player2_card'+str(i)].enable_check()

    def update_hand(self, hand, turn = 1):
        # give cards to player by setting text on card
        # input hand of player, update to widget base on current turn
        # openCard stands for card that can be seen by opponent
        openCardIndex={1:5, 2:1, 3:0, 4:-1}
        for i in range(5):
            self.ids['player2_card'+str(i)].la.text = Card.int_to_pretty_str( hand[i] )
            if i > openCardIndex[turn]:
                self.ids['player2_card'+str(i)].lb.text = Card.int_to_pretty_str( hand[i] )

    def set_button_message(self, msg):
        self.ids.but_2.text = msg

    def press_player_confirm(self):
        # Notify the selected cards
        pickedCards = []
        for i in range(5):
            if self.ids['player2_card'+str(i)].check.active:
                pickedCards.append(i)
        self.parent.on_player_confirm(self.id, 1, pickedCards)

    def update_turn(self, turn):
        # cancel selection and remove last 3 checkbox
        openCardIndex={1:5, 2:1, 3:0, 4:-1}
        for i in range(5):
            self.ids['player2_card'+str(i)].uncheck()
            if i > openCardIndex[turn]:
                self.ids['player2_card'+str(i)].disable_check()

    def add_lie_widget(self, widget):
        print self.children
        self.add_widget(widget, index=(self.children) )
        self.ids[widget.id] = widget
        self.size_hint_x = 1
        print self.children
