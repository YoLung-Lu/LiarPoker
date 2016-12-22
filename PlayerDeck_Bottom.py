
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from SingleCard import SingleCard
from kivy.uix.widget import Widget
from deuces import Card, Evaluator, Deck

class PlayerDeck_Bottom(BoxLayout):
    id = "player1_box"
    but_1 = ObjectProperty(None)

    def init_deck(self):
        b = self.children[0]
        self.remove_widget(b)
        for i in range(5):
            c = SingleCard(id = 'player1_card' + str(i))
            self.ids[c.id] = c
            self.add_widget(c)
            self.add_widget(Widget(size_hint= (0.01, 1)) )

        self.add_widget(b)

    def round_reset(self):
        for i in range(5):
            self.ids['player1_card'+str(i)].enable_check()

    def update_hand(self, hand, turn = 1):
        # input hand of player, update to widget base on current turn
        openCardIndex={1:5, 2:1, 3:0, 4:-1}
        for i in range(5):
            self.ids['player1_card'+str(i)].lb.text = Card.int_to_pretty_str( hand[i] )
            if i > openCardIndex[turn]:
                self.ids['player1_card'+str(i)].la.text = Card.int_to_pretty_str( hand[i] )

    def set_button_message(self, msg):
        self.ids.but_1.text = msg

    def press_player_confirm(self):
        # Notify the selected cards
        pickedCards = []
        for i in range(5):
            if self.ids['player1_card'+str(i)].check.active:
                pickedCards.append(i)
        self.parent.on_player_confirm(self.id, 0, pickedCards)

    def update_turn(self, turn):
        # cancel selection and remove last 3 checkbox
        openCardIndex={1:5, 2:1, 3:0, 4:-1}
        for i in range(5):
            self.ids['player1_card'+str(i)].uncheck()
            if i > openCardIndex[turn]:
                self.ids['player1_card'+str(i)].disable_check()

    def add_lie_widget(self, widget):
        self.add_widget(widget)
        self.ids[widget.id] = widget
        self.size_hint_x = 1
