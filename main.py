from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty

from deuces import Card, Evaluator, Deck

class SingleCard(FloatLayout):
    la = ObjectProperty(None)
    lb = ObjectProperty(None)
    check = ObjectProperty(None)

    def get_widget_by_id(self, w_id):
        print self.ids[w_id]

class PlayerDeck_Bottom(BoxLayout):
    but_1 = ObjectProperty(None)

    def init_deck(self):
        b = self.children[0]
        self.remove_widget(b)
        cards = []
        for i in range(5):
            cards.append(SingleCard())
            cards[i].id = 'player1_card' + str(i)
            self.add_widget(cards[i])
            self.add_widget(Widget(size_hint= (0.01, 1)) )

        self.add_widget(b)

    def update_hand(self, hand, round = 1):
        # input hand of player, update to widget base on current round
        if round == 1:
            for i in range(2,12,2):
                self.children[i].lb.text = Card.int_to_pretty_str( hand[( i/2)-1 ] )
        elif round == 2:
            print round

    def press_player_confirm(self, w_id):
        print self.children[1]
        print w_id
        pass

class PlayerDeck_Top(BoxLayout):
    but_2 = ObjectProperty(None)

    def init_deck(self):
        cards = []
        for i in range(5):
            cards.append(SingleCard())
            cards[i].id = 'player2_card' + str(i)
            self.add_widget(cards[i])
            self.add_widget(Widget(size_hint= (0.01, 1)) )

    def update_hand(self, hand, round = 1):
        # input hand of player, update to widget base on current round
        if round == 1:
            for i in range(1,11,2):
                self.children[i].la.text = Card.int_to_pretty_str( hand[( i/2)-1 ] )
        elif round == 2:
            print round

    def press_player_confirm(self, w_id):
        print self.children[1]
        print w_id
        pass

class Public_Area(BoxLayout):
    but_public = ObjectProperty(None)
    player1_score = ObjectProperty(None)

    def init_deck(self):
        b,c = self.children[0], self.children[1]
        self.remove_widget(b)
        self.remove_widget(c)
        cards = []
        for i in range(2):
            cards.append(SingleCard())
            cards[i].id = 'public_card' + str(i)
            cards[i].remove_widget(cards[i].check)
            self.add_widget(cards[i])
            self.add_widget(Widget(size_hint= (0.01, 1)) )
        self.add_widget(c)
        self.add_widget(b)

    def update_hand(self, hand):
        print self.ids
        print self.ids.player1_score
        self.children[3].la.text = Card.int_to_pretty_str( hand[0] )
        self.children[3].lb.text = self.children[3].la.text
        self.children[5].la.text = Card.int_to_pretty_str( hand[1] )
        self.children[5].lb.text = self.children[5].la.text

    def set_message(self, msg):
        self.but_public.text = msg
        pass

    def press_new_round(self, w_id):
        pass

class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.score = 500

class Game(FloatLayout):
    id = "rootLayout"

    def _set_(self):
        self.deck = Deck()
        self.player = []
        self.player.append( Player(0) )
        self.player.append( Player(1) )

    def _new_round(self):
        self.deck.shuffle()
        self.player[0].hand = []
        self.player[1].hand = []


    def _get_public_area(self):
        box = BoxLayout(orientation = 'horizontal',
                        id = 'public_area',
            			size_hint= (1, 0.4),
            			pos_hint= {'center_x': 0.5, 'y': 0.3})

        p1_score = Label(id = 'p1_score',
                        text = "Player 1" + "\n  " + "500")
        box.add_widget(p1_score)

        hand = self.deck.draw(2)
        cards = []
        for i in range(2):
            cards.append(SingleCard())
            cards[i].la.text = Card.int_to_pretty_str( hand[i] )
            cards[i].lb.text = Card.int_to_pretty_str( hand[i] )
            cards[i].remove_widget(cards[i].check)
            box.add_widget(cards[i])
            box.add_widget(Widget(size_hint= (0.05, 1)) )

        p2_score = Label(id = 'p2_score',
                        text = "Player 1" + "\n  " + "500")
        box.add_widget(p2_score)

        but = Button(text="NewRound",
                    id = "but_1",
                    size_hint_y = 0.8)
        but.bind(on_press=self.press_new_round)
        box.add_widget(but)
        return box

    def build(self):

        box = PlayerDeck_Bottom()
        box.init_deck()
        box.update_hand(self.deck.draw(5))
        self.add_widget(box)

        box2 = PlayerDeck_Top()
        box2.init_deck()
        box2.update_hand(self.deck.draw(5))
        self.add_widget(box2)

        #public_area = self._get_public_area()
        public_area = Public_Area()
        public_area.init_deck()
        public_area.update_hand( self.deck.draw(2) )
        public_area.set_message("MSG")
        self.add_widget(public_area)

        print "*"*20
        #print dir(box)
        #print dir( cards[0].canvas)
        #print card.la.pos
        #print card.la.pos[0]
        print "*"*20


    def update(self, dt):
        pass

    def press_new_round(self, instance):
        # implement "new round" here
        #print instance.text
        #print instance.id
        #print instance.parent.id
        #print self.children
        self.clear_widgets()
        print dir(self)
        #self.remove_widget()

    def press_player_confirm(self, instance):
        # players confirm deck
        print instance.id

class LiarPokerApp(App):
    def build(self):
        game = Game()
        game._set_()
        game.build()
        #Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    LiarPokerApp().run()
