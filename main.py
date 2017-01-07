from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout

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
        """
        At the end of round, update data and views
        """
        self.turn = 1
        self.round += 1
        self.deck.shuffle()

        self.board.round_reset()
        self.player[0].round_reset()
        self.player[1].round_reset()

        self.ids.publicArea.round_reset(self.round)
        self.ids.player1_box.round_reset()
        self.ids.player2_box.round_reset()

    def build(self, testMode = True):
        """
        Initiate objects and views.
        """
        ''' init game objects '''
        self.deck = Deck()
        self.evaluator = Evaluator()

        self.player = []
        self.player.append( Player(0) )
        self.player.append( Player(1) )
        # board stands for public cards on board
        self.board = Board()

        # In test mode, both player select right-most cards for the turn automatically
        self.testMode = testMode


        ''' create view objects '''
        # Scatter that can be rotated to display players
        scatter_bot = ScatterLayout(do_rotation = False,do_translation = False,do_scale = False,
            			size_hint = (1, 1), pos_hint = {'x': 0, 'y': 0},
                        rotation = 0 )
        # For player on top, the widget rotates 180 degree
        scatter_top = ScatterLayout(do_rotation = False,do_translation = False,do_scale = False,
                        size_hint = (1, 1), pos_hint = {'x': 0, 'y': 0},
                        rotation = 180 )

        box = PlayerDeck()
        box2 = PlayerDeck()
        publicArea = PublicArea()
        box.build(self, "player1", 0, self.testMode)
        box2.build(self, "player2", 1, self.testMode)
        publicArea.build()

        scatter_bot.add_widget(box)
        scatter_top.add_widget(box2)

        self.add_widget(scatter_bot)
        self.add_widget(scatter_top)
        self.add_widget(publicArea)

        # register id of view objects
        self.ids[box.id] = box
        self.ids[box2.id] = box2
        self.ids[publicArea.id] = publicArea

    def round_play(self):
        """
        A game round starts here.
        """
        self.round_reset()

        # draw cards for players and board
        self.player[0].hand = self.deck.draw(5)
        self.player[1].hand = self.deck.draw(5)
        self.board.set_cards( self.deck.draw(2) )

        # update view
        self.ids.player1_box.update_hand(self.player[0].hand, self.turn)
        self.ids.player2_box.update_hand(self.player[1].hand, self.turn)
        self.ids.publicArea.round_play(self.board.get_cards())

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
        else: # No one caught
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


        # TODO: real winner, win type, chip gain
        roundMsg = "Player " + str(cardWinner + 1) + " wins."

        ''' Test Mode message '''
        # print cards for check in test mode
        if self.testMode:
            print '*'*50
            if self.player[cardWinner].caught and self.player[cardWinner^1].caught:
                print "Draw due to double caught."
            elif not self.player[cardWinner].caught and not self.player[cardWinner^1].caught:
                print "No one caught."
            print "             Player1          Player2"
            print "Lie       : ", self.player[0].lie, "          ", self.player[1].lie
            print "Suspection: ", self.player[0].suspect, "          ", self.player[1].suspect
            print "Caught    : ", self.player[0].caught, "          ",  self.player[1].caught
            if cardWinner == 0: print "             Win              Lose"
            else: print "             Lose              Win"
            print "Rate (winner/maintain/loser): ", winnerRate, maintainRate, loserRate
            print "Chip and bonus after: ", self.board.totalChip, self.board.bonus
            print "Card rank: "
            print "Player 1 hand rank = %d (%s)" % (self.player[0].cardScore, self.player[0].rank)
            print "Player 2 hand rank = %d (%s)" % (self.player[1].cardScore, self.player[1].rank)
            print '*'*50

        ''' end a game round '''
        # TODO: show at another place
        self.ids.player1_box.set_button_message( self.evaluator.class_to_string(self.player[0].rank ))
        self.ids.player2_box.set_button_message( self.evaluator.class_to_string(self.player[1].rank ))

        self.ids.publicArea.round_end("Round : " + str(self.round) +"\n" + roundMsg + "\nNew Round" )

        self.board.round_end()
        self.ids.player1_box.round_end()
        self.ids.player2_box.round_end()

    def on_player_confirm(self, boxid, thisPlayer, cardList, bet):
        """
        The event can be triggered by both players when they press "Confirm" button.
        After triggered, this method check if player's turn finished.

        Checking detail:
            (1) if player's confirm ligelly (turn1: 3 cards selected, turn2: 1 card, turn3: lie or not)
                -> rearrange sequence of cards and lock cards
                -> if both of players finished confirm -> enter next turn
            (2) Turn3: if player lie (implemented at "on_player_lie" method)
                -> Change card and player.state.lie
                -> if both of players finished confirm or lie -> enter next turn
            (3) Turn4: if players suspect opponent lied.
                -> decide winner and odds
        """
        if self.testMode:
            print "Player " + str(thisPlayer+1) + " Cards: " + str(cardList) + ", Bets: ", bet

        if bet == 3:
            # player fold
            self.player[thisPlayer].fold = True

        if self.turn == 1:
            # check if 3 cards selected
            if len(cardList) == 3 and self.player[thisPlayer].currentTurn == 1:
                self.player[thisPlayer].reorderCard(cardList)
                self.player[thisPlayer].bet = bet
                self.player[thisPlayer].currentTurn = 2
                self.ids[boxid].update_turn(2)
                # if other player already end turn, this turn is end
                if self.player[thisPlayer^1].currentTurn == 2:
                    self.turn_1_end()

        elif self.turn == 2:
            if len(cardList) == 1 and self.player[thisPlayer].currentTurn == 2:
                self.player[thisPlayer].reorderCard(cardList)
                self.player[thisPlayer].bet = bet
                self.player[thisPlayer].currentTurn = 3
                self.ids[boxid].update_turn(3)
                if self.player[thisPlayer^1].currentTurn == 3:
                    self.turn_2_end()

        elif self.turn == 3 and len(cardList) == 1 and self.player[thisPlayer].currentTurn == 3:
            self.player[thisPlayer].reorderCard(cardList)
            self.player[thisPlayer].bet = bet
            self.player[thisPlayer].currentTurn = 4
            self.ids[boxid].update_turn(4)
            if self.player[thisPlayer^1].currentTurn == 4:
                self.turn_3_end()

        elif self.turn == 4:
            self.player[thisPlayer].currentTurn = 5
            if self.player[thisPlayer^1].currentTurn == 5:
                self.round_end()

        elif self.turn == 5:
            # wait for next round?
            pass

    def on_player_lie(self, player, card):
        """
        Triggered by players in turn 3 if player decided to "lie".
        Check if the lie-card player assigned is different from his original card.
        """
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
        """
        Triggered by players in turn 4 if player decided to "suspect his opponent".
        Check if he caught his opponent on lie.
        """
        # TODO: fix the args
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

    def round_end_on_fold(self):
        msg = ""
        chip = self.board.totalChip
        if self.player[0].fold and self.player[1].fold: # both players fold
            self.board.bonus += chip
            msg = "Both players"
        elif self.player[0].fold:
            self.player[1].chip += chip
            msg = "Player1"
        else:
            self.player[0].chip += chip
            msg = "Player2"

        msg += " fold in this round."
        print msg

        # set info for fold
        self.ids.publicArea.set_info( msg )

        self.round_reset_on_fold()

    def round_reset_on_fold(self):

        # reset player box widget by end turn 3
        if self.turn == 3:
            self.ids.player1_box.turn_3_end()
            self.ids.player2_box.turn_3_end()

        self.ids.player1_box.round_end()
        self.ids.player2_box.round_end()
        self.board.round_end()


    def turn_1_end(self):
        if self.testMode:
            print ">> turn 1 end"

        if self.player[0].fold or self.player[1].fold:
            self.round_end_on_fold()
            return ""

        ''' Decide bet and chip of the turn '''
        bet, chip = self.board.set_bet(self.turn, self.player[0].bet, self.player[1].bet)
        # TODO: chip < 0
        self.player[0].chip -= chip
        self.player[1].chip -= chip

        ''' update game info '''
        self.ids.publicArea.set_bet_info( self.player[0].bet, self.player[1].bet, bet, chip)
        self.ids.publicArea.update_turn(self.turn)
        self.ids.publicArea.set_info( self.board.get_bet_string(self.turn) )

        self.turn = 2
        self.ids.player1_box.update_hand(self.player[0].hand, self.turn)
        self.ids.player2_box.update_hand(self.player[1].hand, self.turn)

    def turn_2_end(self):
        if self.testMode:
            print ">> turn 2 end"

        if self.player[0].fold or self.player[1].fold:
            self.round_end_on_fold()
            return ""

        bet, chip = self.board.set_bet(self.turn, self.player[0].bet, self.player[1].bet)
        self.player[0].chip -= chip
        self.player[1].chip -= chip

        self.ids.publicArea.set_bet_info( self.player[0].bet, self.player[1].bet, bet, chip)
        self.ids.publicArea.update_turn(self.turn)
        self.ids.publicArea.set_info( self.board.get_bet_string(self.turn) )

        self.turn = 3
        self.ids.player1_box.update_hand(self.player[0].hand, self.turn)
        self.ids.player2_box.update_hand(self.player[1].hand, self.turn)

        # set widgets for tell lie
        self.ids.player1_box.turn_2_end()
        self.ids.player2_box.turn_2_end()

    def turn_3_end(self):
        if self.testMode:
            print ">> turn 3 end"

        if self.player[0].fold or self.player[1].fold:
            self.round_end_on_fold()
            return ""

        bet, chip = self.board.set_bet(self.turn, self.player[0].bet, self.player[1].bet)
        self.player[0].chip -= chip
        self.player[1].chip -= chip

        self.ids.publicArea.set_bet_info( self.player[0].bet, self.player[1].bet, bet, chip)
        self.ids.publicArea.update_turn(self.turn)
        self.ids.publicArea.set_info( self.board.get_bet_string(self.turn) )

        self.turn = 4
        self.ids.player1_box.update_hand(self.player[0].hand, self.turn)
        self.ids.player2_box.update_hand(self.player[1].hand, self.turn)

        # Set suspect widgets for turn 4
        self.ids.player1_box.turn_3_end()
        self.ids.player2_box.turn_3_end()

    def get_turn(self):
        return self.turn

    def update(self, dt):
        pass

    def on_press_new_round(self):
        """
        Triggered by players after turn 4 if player press "New Round" button in the public area.
        Start a new round of the game.
        """
        self.round_play()

    def test_image(self):
        #img = Image(source='resource/Suspection.png', size_hint=(0.5,0.5) )
        #self.add_widget(img)
        pass

class LiarPokerApp(App):
    def build(self):
        """
        TODO:
            1. Player drop out (Fold)
            2. Player don't have enough chip
            3. Game info.
        """
        game = Game()
        game.build()
        game.round_play()
        return game


if __name__ == '__main__':
    LiarPokerApp().run()
