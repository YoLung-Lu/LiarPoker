
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from deuces import Card, Evaluator, Deck
from SingleCard import SingleCard
from CardSelector import CardSelector
from functools import partial

class PlayerDeck_Bottom(BoxLayout):
    id = "player1_box"
    but_1 = ObjectProperty(None)
    player = "player1"

    def init_deck(self):
        b = self.children[0]
        self.remove_widget(b)
        for i in range(5):
            c = SingleCard(id = 'player1_card' + str(i))
            self.ids[c.id] = c
            self.add_widget(c)
            self.add_widget(Widget(size_hint= (0.01, 1)) )

        self.add_widget(b)

    def round_reset(self, testMode = False):
        for i in range(5):
            self.ids['player1_card'+str(i)].enable_check()
            self.ids['player1_card'+str(i)].la.text = ""
            if testMode and i>1:
                self.ids['player1_card'+str(i)].do_check()
            else:
                self.ids['player1_card'+str(i)].uncheck()

    def update_hand(self, hand, turn = 1):
        # input hand of player, update to widget base on current turn
        openCardIndex={1:5, 2:1, 3:0, 4:-1}
        for i in range(5):
            self.ids['player1_card'+str(i)].lb.text = Card.int_to_pretty_str( hand[i] )
            if i > openCardIndex[turn]:
                self.ids['player1_card'+str(i)].la.text = Card.int_to_pretty_str( hand[i] )

    def update_turn(self, turn, testMode = False):
        # cancel selection and remove last 3 checkbox
        openCardIndex={1:5, 2:1, 3:0, 4:-1}
        for i in range(5):
            self.ids['player1_card'+str(i)].uncheck()
            if i > openCardIndex[turn]:
                self.ids['player1_card'+str(i)].disable_check()
            elif testMode and i == openCardIndex[turn]:
                self.ids['player1_card'+str(i)].do_check()

        if turn == 3:
            self.ids['player1_card0'].do_check()

    def set_button_message(self, msg):
        self.ids.but_1.text = msg

    def press_player_confirm(self):
        # Notify the selected cards
        pickedCards = []
        for i in range(5):
            if self.ids['player1_card'+str(i)].check.active:
                pickedCards.append(i)
        self.parent.on_player_confirm(self.id, 0, pickedCards)

    def round_turn_2_end(self):
        self._add_lie_widget()

    def round_turn_3_end(self):
        self._remove_lie_widget()
        b = Button(text="Suspect", size_hint_y=0.8)
        #b.bind(on_press=self.parent.on_player_suspect(self.player) )
        buttoncallback = partial(self.parent.on_player_suspect, self.player)
        b.bind(on_press = buttoncallback)

        self.add_widget(b, index=len(self.children))

    def round_end(self):
        # remove suspect widget
        self.remove_widget(self.children[-1])

    def _add_lie_widget(self):
        cs = CardSelector(id="player1_cs")
        cs.build(self.parent)
        self.add_widget(cs, index=len(self.children) )
        self.ids[cs.id] = cs
        self.size_hint_x = 1

    def _remove_lie_widget(self):
        self.remove_widget(self.children[-1])
