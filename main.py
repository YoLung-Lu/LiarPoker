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

from __init__ import *


class Game(FloatLayout):
    id = "root"
    turn = 1
    round = 0

    def _round_reset(self):
        # At the end of round, update data and views
        self.turn = 1
        self.round += 1
        self.deck.shuffle()
        self.player[0].round_reset()
        self.player[1].round_reset()

        # TODO: remove lie panel from playerbox
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
        # TODO: check if need this at first round ??
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
        # There are 4 turns in a round of a game. Players must confirm there cards to finish the turn
        """
        In every turn, check:
            (1) if player's confirm ligelly (turn1: 3 cards selected, turn2: 1 card, turn3: lie or not)
                -> rearrange sequence of cards and lock cards
                -> if both of players finished confirm -> enter next turn
            (2) Turn3: if player lie (implemented at "on_player_lie" method)
                -> Change card and player.state.lie
                -> if both of players finished confirm or lie -> enter next turn
            (3) Turn4: if players suspect opponent lied.
                -> decide winner and odds
        """
        print cardList
        # TODO: no betting process
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
        elif self.turn == 3:
            # TODO: implement not lie flow
            pass
        elif self.turn == 4:
            # TODO: implement not suspect flow
            pass


    def on_player_lie(self, player, card):
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

    def on_player_suspect(self, player):
        print str(player) + "suspect his opponent lied."
        pass

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

    def round_turn_4_end(self):
        pass

    def _create_liar_selector(self, player):
        # create a card selector for players to tell lie
        cs = CardSelector(id=player)
        cs.build(self)
        return cs

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
        return game


if __name__ == '__main__':
    LiarPokerApp().run()
