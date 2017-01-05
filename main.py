from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty

from view import BetSelector, CardSelector, PlayerDeck, PublicArea, SingleCard
from model import GameFlow, Board, Player
from deuces import Card, Evaluator, Deck
from abc import ABCMeta


class Game(GameFlow, FloatLayout):
    # give the type of game to a self-created type inheritence from both "FloatLayout" and "ABCMeta"
    __metaclass__ = type( 'GameMeta', (type(FloatLayout), ABCMeta), {})
    id = "root"
    turn = 1
    round = 0

    def round_reset(self):
        # At the end of round, update data and views
        self.turn = 1
        self.round += 1
        self.deck.shuffle()
        self.player[0].round_reset()
        self.player[1].round_reset()

        # TODO: remove lie panel from playerbox
        self.ids.player1_box.round_reset()
        self.ids.player2_box.round_reset()
        self.board.round_reset()


    def build(self, testMode = True):
        """
        Initiate objects and views.
        """
        # init game objects
        self.deck = Deck()
        self.evaluator = Evaluator()

        self.player = []
        self.player.append( Player(0) )
        self.player.append( Player(1) )
        # board stands for public cards on board
        self.board = Board()

        # In test mode, both player select right-most cards for the turn automatically
        self.testMode = testMode


        # create view objects

        # Scatter that can be rotated to display players
        scatter_but = ScatterLayout(do_rotation = False,do_translation = False,do_scale = False,
            			size_hint = (1, 1), pos_hint = {'x': 0, 'y': 0},
                        rotation = 0 )
        # For player on top, the widget rotates 180 degree
        scatter_top = ScatterLayout(do_rotation = False,do_translation = False,do_scale = False,
                        size_hint = (1, 1), pos_hint = {'x': 0, 'y': 0},
                        rotation = 180 )

        box = PlayerDeck()
        box.init_deck(self, "player1", 0, self.testMode)
        box2 = PlayerDeck()
        box2.init_deck(self, "player2", 1, self.testMode)
        publicArea = PublicArea()
        publicArea.init_deck()

        scatter_but.add_widget(box)
        self.add_widget(scatter_but)
        scatter_top.add_widget(box2)
        self.add_widget(scatter_top)
        self.add_widget(publicArea)

        # register view objects
        self.ids[box.id] = box
        self.ids[box2.id] = box2
        self.ids[publicArea.id] = publicArea

    def round_play(self):
        """
        A game round starts here.
        """
        self.round_reset()
        self.ids.publicArea.update_round(self.round)

        # draw cards for players and board
        self.player[0].hand = self.deck.draw(5)
        self.player[1].hand = self.deck.draw(5)
        self.board.set_cards( self.deck.draw(2) )

        # update view
        self.ids.player1_box.update_hand(self.player[0].hand)
        self.ids.player2_box.update_hand(self.player[1].hand)
        self.ids.publicArea.update_hand(self.board.get_cards())

        # TODO: fix bet
        self.ids.publicArea.set_chip_info(self.player[0].chip, self.player[1].chip, self.board.bonus)
        self.ids.publicArea.set_info( self.board.get_bet_string(self.turn) )

    def round_end(self):
        """
        The end of a game round. Decide winner of the round and chip shift based on:
            (1) If any lier caught
            (2) Card score
        """
        self.turn = 5

        ''' Evaluation card rank '''
        self.player[0].cardScore = self.evaluator.evaluate(self.board.get_cards(), self.player[0].hand)
        self.player[1].cardScore = self.evaluator.evaluate(self.board.get_cards(), self.player[1].hand)
        self.player[0].rank = self.evaluator.get_rank_class(self.player[0].cardScore)
        self.player[1].rank = self.evaluator.get_rank_class(self.player[1].cardScore)

        ''' Card winner '''
        cardWinner = 1
        if self.player[0].cardScore < self.player[1].cardScore:
            cardWinner = 0 # Player1

        ''' Decide chip gain rate for winner, loser and board '''
        winnerRate = 1.0    # The chip to handover to the card winner
        loserRate = 0.0     # The chip to handover to the card loser
        maintainRate = 0.0  # The chip left on the table

        if self.player[cardWinner].caught and self.player[cardWinner^1].caught:
            # Both of players lied, and caught.
            print "Draw due to double caught."
            winnerRate, maintainRate, loserRate = 0, 1, 0
        elif self.player[cardWinner].caught:
            # Only winner caught
            if self.player[cardWinner].suspect:
                winnerRate, maintainRate, loserRate = -1, 1.5, 0.5
            else:
                winnerRate, maintainRate, loserRate = -0.5, 1, 0.5
        elif self.player[cardWinner^1].caught:
            # Only loser caught
            if self.player[cardWinner^1].suspect:
                winnerRate, maintainRate, loserRate = 1.5, 0.5, -1
            else:
                winnerRate, maintainRate, loserRate = 1.5, 0, -0.5
        else:
            print "No one caught"
            winnerRate, maintainRate, loserRate = 1, 0, 0
            if self.player[cardWinner].suspect:
                winnerRate -= 0.5
                maintainRate += 0.5
            if self.player[cardWinner^1].suspect:
                loserRate -= 0.5
                maintainRate += 0.5

        """
                    Winner   Host    Loser
        winnerPrize       <--1.0            ( Stay at host if winner caught )
        LieCost       0.5 <--------> 0.5    ( Pay to opponent if caught )
        SuspectCost   0.5->        <-0.5    ( Pay to host if suspect not stand )
        """

        ''' Calculate chip gain '''
        stacks = self.board.totalChip
        bonus  = self.board.bonus

        self.player[cardWinner].chip += int(stacks * winnerRate)
        self.player[cardWinner^1].chip += int(stacks * loserRate)

        if winnerRate > 0: # winner gets bonus
            self.player[cardWinner].chip += bonus
            bonus = stacks * maintainRate
        elif winnerRate < 0 and loserRate > 0: # loser gets bonus
            self.player[cardWinner^1].chip += bonus
            bonus = stacks * maintainRate
        else: # no one gets bonus due to double caught
            bonus = bonus + stacks * maintainRate

        self.board.set_bonus(int(bonus))
        self.board.round_end()

        # print cards for check
        print winnerRate, maintainRate, loserRate
        print '*'*50
        print "GAME RESULT:"
        print "Player 1 hand rank = %d (%s)\n" % (self.player[0].cardScore, self.player[0].rank)
        print "Player 2 hand rank = %d (%s)\n" % (self.player[1].cardScore, self.player[1].rank)

        roundMsg = "Player " + str(cardWinner + 1) + " wins."
        print roundMsg
        print '*'*50

        # temply shows card rank here
        self.ids.player1_box.set_button_message( self.evaluator.class_to_string(self.player[0].rank ))
        self.ids.player2_box.set_button_message( self.evaluator.class_to_string(self.player[1].rank ))

        self.ids.publicArea.set_message("Round : " + str(self.round) +"\n" + roundMsg + "\nNew Round" )

        # Remove suspect widget
        # TODO: move 2 right place
        self.ids.player1_box.round_end()
        self.ids.player2_box.round_end()

    def on_player_confirm(self, boxid, thisPlayer, cardList, bet):
        # There are 4 turns in a round of a game. Players must confirm their cards to finish the turn
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
        # TODO: no betting process
        if self.testMode:
            print "Player " + str(thisPlayer+1) + " Cards: " + str(cardList)

        if self.turn == 1:
            # check if 3 cards selected
            if len(cardList) == 3 and self.player[thisPlayer].currentTurn == 1:
                self.player[thisPlayer].reorderCard(cardList)
                self.player[thisPlayer].bet = bet
                self.player[thisPlayer].currentTurn = 2
                self.ids[boxid].update_turn(2)
                #self.ids[boxid].update_hand(self.player[thisPlayer].hand, self.turn)
                # if other player already end turn, this turn is end
                if self.player[thisPlayer^1].currentTurn == 2:
                    self.turn_1_end()

        elif self.turn == 2:
            if len(cardList) == 1 and self.player[thisPlayer].currentTurn == 2:
                self.player[thisPlayer].reorderCard(cardList)
                self.player[thisPlayer].bet = bet
                self.player[thisPlayer].currentTurn = 3
                self.ids[boxid].update_turn(3)
                #self.ids[boxid].update_hand(self.player[thisPlayer].hand, self.turn)
                if self.player[thisPlayer^1].currentTurn == 3:
                    self.turn_2_end()
        elif self.turn == 3 and len(cardList) == 1 and self.player[thisPlayer].currentTurn == 3:
            self.player[thisPlayer].reorderCard(cardList)
            self.player[thisPlayer].bet = bet
            self.player[thisPlayer].currentTurn = 4
            self.ids[boxid].update_turn(4)
            #self.ids[boxid].update_hand(self.player[thisPlayer].hand, self.turn)
            if self.player[thisPlayer^1].currentTurn == 4:
                self.turn_3_end()

        elif self.turn == 4:
            self.player[thisPlayer].currentTurn = 5
            if self.player[thisPlayer^1].currentTurn == 5:
                self.round_end()

        elif self.turn == 5:
            # wait for next round
            pass

    def on_player_lie(self, player, card):
        print str(player) + " made a lie to card: " + card
        card = Card.new(card)
        pno = int(player[6]) - 1

        if self.player[pno].hand[0] != card:
            self.player[pno].lie = True
            self.player[pno].hand.pop(0)
            self.player[pno].hand.insert(0, card)
            self.player[pno].currentTurn = 4
            self.ids[player+"_box"].update_turn(4)
            self.ids[player+"_box"].update_hand(self.player[pno].hand, self.turn)
            if self.player[pno^1].currentTurn == 4:
                self.turn_3_end()

    def on_player_suspect(self, *args):
        print args[0] + " suspect his opponent lied."
        player = args[0]
        pno = int(args[0][-1])-1
        self.player[pno].suspect = True
        if self.player[pno^1].lie:
            self.player[pno^1].caught = True
            print player + " caught his opponent lied"

        self.player[pno].currentTurn = 5
        if self.player[pno^1].currentTurn == 5:
            self.round_end()

    def turn_1_end(self):
        print ">> turn 1 end"
        bet, chip = self.board.set_bet(self.turn, self.player[0].bet, self.player[1].bet)
        #set_bet_info
        # TODO: chip < 0
        self.ids.publicArea.set_bet_info( self.player[0].bet, self.player[1].bet, bet, chip)
        self.ids.publicArea.update_turn(self.turn)
        self.ids.publicArea.set_info( self.board.get_bet_string(self.turn) )

        self.player[0].chip -= chip
        self.player[1].chip -= chip

        self.turn = 2
        self.ids.player1_box.update_hand(self.player[0].hand, self.turn)
        self.ids.player2_box.update_hand(self.player[1].hand, self.turn)


    def turn_2_end(self):
        print ">> turn 2 end"
        bet, chip = self.board.set_bet(self.turn, self.player[0].bet, self.player[1].bet)
        #set_bet_info
        # TODO: chip < 0
        self.ids.publicArea.set_bet_info( self.player[0].bet, self.player[1].bet, bet, chip)
        self.ids.publicArea.update_turn(self.turn)
        self.ids.publicArea.set_info( self.board.get_bet_string(self.turn) )

        self.player[0].chip -= chip
        self.player[1].chip -= chip

        self.turn = 3
        self.ids.player1_box.update_hand(self.player[0].hand, self.turn)
        self.ids.player2_box.update_hand(self.player[1].hand, self.turn)

        # set widgets for tell lie
        self.ids.player1_box.round_turn_2_end()
        self.ids.player2_box.round_turn_2_end()

    def turn_3_end(self):
        print ">> turn 3 end"
        bet, chip = self.board.set_bet(self.turn, self.player[0].bet, self.player[1].bet)
        #set_bet_info
        # TODO: chip < 0
        self.ids.publicArea.set_bet_info( self.player[0].bet, self.player[1].bet, bet, chip)
        self.ids.publicArea.update_turn(self.turn)
        self.ids.publicArea.set_info( self.board.get_bet_string(self.turn) )

        self.player[0].chip -= chip
        self.player[1].chip -= chip

        self.turn = 4
        self.ids.player1_box.update_hand(self.player[0].hand, self.turn)
        self.ids.player2_box.update_hand(self.player[1].hand, self.turn)

        # Set suspect widgets for turn 4
        self.ids.player1_box.round_turn_3_end()
        self.ids.player2_box.round_turn_3_end()

    def get_turn(self):
        return self.turn

    def update(self, dt):
        pass

    def press_new_round(self):
        # implement "new round" here
        # TODO: fix removed checkbox

        self.round_play()

    def test_image(self):
        #img = Image(source='resource/Suspection.png', size_hint=(0.5,0.5) )
        #self.add_widget(img)
        pass

class LiarPokerApp(App):
    def build(self):
        """
        TODO:
            1. Betting
            2. End game strategy
            3. Player drop out
            4. Flow problem (potential bug): end game using button before turn 5
            5.
        """
        game = Game()
        game.build()
        game.round_play()
        return game


if __name__ == '__main__':
    LiarPokerApp().run()
