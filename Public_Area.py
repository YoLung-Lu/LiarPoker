from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from SingleCard import SingleCard
from kivy.uix.widget import Widget
from deuces import Card, Evaluator, Deck

class Public_Area(BoxLayout):
    id = "public_area"
    but_public = ObjectProperty(None)
    player1_score = ObjectProperty(None)

    def init_deck(self):
        b,b2 = self.children[0], self.children[1]
        self.remove_widget(b)
        self.remove_widget(b2)

        # put 2 public cards before player2_score and button
        for i in range(2):
            c = SingleCard(id = 'public_card' + str(i))
            # Register ids for public cards
            self.ids[c.id] = c
            c.disable_check()
            self.add_widget(c)
            # space between cards
            self.add_widget(Widget(size_hint= (0.01, 1)) )
        self.add_widget(b2)
        self.add_widget(b)

    def update_hand(self, hand):
        self.ids.public_card0.la.text = Card.int_to_pretty_str( hand[0] )
        self.ids.public_card0.lb.text = self.ids.public_card0.la.text
        self.ids.public_card1.la.text = Card.int_to_pretty_str( hand[1] )
        self.ids.public_card1.lb.text = self.ids.public_card1.la.text

    def set_message(self, msg):
        self.but_public.text = msg
        pass

    def update_score(self, p1_score, p2_score):
        # TODO: using binding to handle this??
        self.ids.player1_score.text = str(p1_score)
        self.ids.player2_score.text = str(p2_score)

    def press_new_round(self, w_id):
        self.parent.press_new_round()
        pass
