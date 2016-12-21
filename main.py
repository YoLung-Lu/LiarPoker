from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty

from deuces import Card, Evaluator, Deck
from CardSelector import CardSelector


class SingleCard(FloatLayout):
    la = ObjectProperty(None)
    lb = ObjectProperty(None)
    check = ObjectProperty(None)

    def get_widget_by_id(self, w_id):
        #print self.ids[w_id]
        pass

    def uncheck(self):
        self.check.active = False

    def enable_check(self):
        if not self.check.parent:
            self.add_widget(self.check)

    def disable_check(self):
        self.remove_widget(self.check)

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

class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.chip = 500
        self.bid = 0
        self.currentTurn = 1
        self.lie = False

    def round_reset(self):
        self.hand = []
        self.bid = 0
        self.currentTurn = 1
        self.lie = False

    def bid(self, bidding):
        if bidding < self.chip:
            self.bid = bidding
            return True
        return False

    def reorderCard(self, cardList):
        delta = 0
        for i in cardList:
            self.hand.append( self.hand.pop(i-delta) )
            delta += 1

class Game(FloatLayout):
    id = "root"
    turn = 1
    round = 0


    def _round_reset(self):
        self.turn = 1
        self.round += 1
        self.deck.shuffle()
        self.player[0].round_reset()
        self.player[1].round_reset()
        self.ids.player1_box.round_reset()
        self.ids.player2_box.round_reset()
        self.board = []


    def build(self):
        # init game objects
        self.deck = Deck()
        self.evaluator = Evaluator()
        self.player = []
        self.player.append( Player(0) )
        self.player.append( Player(1) )
        # board stands for cards on board
        self.board = []

        # create view objects
        box = PlayerDeck_Bottom()
        box.init_deck()
        box2 = PlayerDeck_Top()
        box2.init_deck()
        public_area = Public_Area()
        public_area.init_deck()

        # register view objects
        self.add_widget(box)
        self.add_widget(box2)
        self.add_widget(public_area)
        self.ids[box.id] = box
        self.ids[box2.id] = box2
        self.ids[public_area.id] = public_area

    def round_play(self):
        self._round_reset()
        # deal cards
        self.player[0].hand = self.deck.draw(5)
        self.player[1].hand = self.deck.draw(5)
        self.board = self.deck.draw(2)

        # update view
        self.ids.player1_box.update_hand(self.player[0].hand)
        self.ids.player2_box.update_hand(self.player[1].hand)
        self.ids.public_area.update_hand(self.board)
        self.ids.public_area.update_score(500, 500)

        # TODO: turns in a round not implemented yet
        #self.round_finish()

    def round_finish(self):
        # evaluate cards
        self.player[0].cardScore = self.evaluator.evaluate(self.board, self.player[0].hand)
        self.player[0].rank = self.evaluator.get_rank_class(self.player[0].cardScore)

        self.player[1].cardScore = self.evaluator.evaluate(self.board, self.player[1].hand)
        self.player[1].rank = self.evaluator.get_rank_class(self.player[1].cardScore)

        print '*'*50
        print "GAME RESULT:"
        print "Player 1 hand rank = %d (%s)\n" % (self.player[0].cardScore, self.player[0].rank)
        print "Player 2 hand rank = %d (%s)\n" % (self.player[1].cardScore, self.player[1].rank)
        #evaluator.class_to_string(p1_class)

        roundMsg = ""
        if self.player[0].cardScore < self.player[1].cardScore:
            roundMsg = "Player1 wins"
        else:
            roundMsg = "Player2 wins"
        print '*'*50

        # temply shows card rank here
        self.ids.player1_box.set_button_message( self.evaluator.class_to_string(self.player[0].rank ))
        self.ids.player2_box.set_button_message( self.evaluator.class_to_string(self.player[1].rank ))

        self.ids.public_area.set_message("Round : " + str(self.round) +"\n" + roundMsg + "\nNew Round" )

    def on_player_confirm(self, boxid, thisPlayer, cardList, cardPicked = None):
        # There are 3 turns in a round of a game. Players must confirm there cards to finish the turn
        """
        In every turn, check:
            (1) if player's confirm ligelly (turn1: 3 cards selected, turn2: 1 card, turn3: lie or not)
                -> rearrange sequence of cards and lock cards
            (2) if both of players finished confirm
                -> enter next turn
        """
        print cardList
        # TODO: no bidding process
        if self.turn == 1:
            # check if 3 cards selected
            if len(cardList) == 3 and self.player[thisPlayer].currentTurn == 1:
                self.player[thisPlayer].reorderCard(cardList)
                self.player[thisPlayer].currentTurn = 2
                self.ids[boxid].update_turn(2)
                self.ids[boxid].update_hand(self.player[thisPlayer].hand)
            if self.player[thisPlayer^1].currentTurn == 2:
                # two players both finished turn 1
                self.round_turn_1_end()
        elif self.turn == 2:
            if len(cardList) == 1 and self.player[thisPlayer].currentTurn == 2:
                self.player[thisPlayer].reorderCard(cardList)
                self.player[thisPlayer].currentTurn = 3
                self.ids[boxid].update_turn(3)
                self.ids[boxid].update_hand(self.player[thisPlayer].hand)
            if self.player[thisPlayer^1].currentTurn == 3:
                # two players both finished turn 1
                self.round_turn_2_end()


    def round_turn_1_end(self):
        self.turn = 2
        self.ids.player1_box.update_hand(self.player[0].hand, self.turn)
        self.ids.player2_box.update_hand(self.player[1].hand, self.turn)

    def round_turn_2_end(self):
        self.turn = 3
        self.ids.player1_box.update_hand(self.player[0].hand, self.turn)
        self.ids.player2_box.update_hand(self.player[1].hand, self.turn)

        # set view for tell lie
        self.ids.player1_box.add_lie_widget(self._create_liar_selector('player1'))
        self.ids.player2_box.add_lie_widget(self._create_liar_selector('player2'))

    def round_turn_3_end(self):
        self.turn = 4
        self.ids.player1_box.update_hand(self.player[0].hand, self.turn)
        self.ids.player2_box.update_hand(self.player[1].hand, self.turn)
        self.round_finish()

    def _create_liar_selector(self, player):
        # create a card selector for players to tell lie
        cs = CardSelector(id=player)
        cs.build(self)
        return cs

    def on_lie(self, player, card):
        print str(player) + "made a lie to card: " + card
        card = Card.new(card)
        pno = int(player[-1]) - 1

        if self.player[pno].hand[0] != card:
            self.player[pno].hand.pop(0)
            self.player[pno].hand.insert(0, card)
            self.player[pno].currentTurn = 4
            self.ids[player+"_box"].update_turn(3)
            self.ids[player+"_box"].update_hand(self.player[pno].hand)
            if self.player[pno^1].currentTurn == 4:
                self.round_turn_3_end()

    def update(self, dt):
        pass

    def press_new_round(self):
        # implement "new round" here
        # TODO: fix removed checkbox

        self.round_play()

    def press_player_confirm(self, instance):
        # players confirm deck
        #print instance.id
        pass

class LiarPokerApp(App):
    def build(self):
        game = Game()
        game.build()
        game.round_play()
        #Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    LiarPokerApp().run()
