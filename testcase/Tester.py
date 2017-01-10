from random import randint


class Tester():
    def __init__(self, game):
        self.game = game
        self.player = ["player1", "player2"]

    def _run_script(self):
        """
        Would be better to build test script.
        """

        script = """
        turn1:
            player1 [0,1,2] 2
            player2 [0,2,4] 0

        turn2:
            player1 [3] 4 # fold
            player2 [3] 0
        """

    def _test_log(self, msg):
        print msg

    def run_test(self):
        # init game
        self.game.round_play()

        ''' Test on normal flow '''
        self._test_log("Test on normal flow")
        self._run_flow()

        ''' Test on 1 player lied '''
        self._test_log("Test on 1 player lied")
        self._run_flow(lie = 1)

        ''' Test on 1 player lied, 1 player suspect '''
        self._test_log("Test on 1 player lied")
        self._run_flow(lie = 1, suspect = 1)

        ''' Test on 1 player fold '''



    def _run_flow(self, lie = 0, suspect = 0):
        """
        Play game flow.
        Arg lie indicate number of player made lie.
        Arg suspect indicate number of player suspect.
        """

        for turn in range(1,5):
            # normal flow stands for player press confirm
            normalFlow = True
            for i in range(2):
                if turn == 3 and lie > 0: # if a player lied
                    if lie == 2:
                        self._call_on_player_lie(self.player[0])
                        self._call_on_player_lie(self.player[1])
                    else:
                        liar = randint(0,1)
                        self._call_on_player_lie(self.player[liar])
                        self._call_on_player_confirm(self.player[liar^1], turn)
                    lie = 0
                    normalFlow = False
                elif turn == 4 and suspect > 0: # if player suspected
                    if suspect == 2:
                        self._call_on_player_suspect(self.player[0])
                        self._call_on_player_suspect(self.player[1])
                    else:
                        suspecter = randint(0,1)
                        self._call_on_player_suspect(self.player[suspecter])
                        self._call_on_player_confirm(self.player[suspecter^1], turn)
                    suspect = 0
                    normalFlow = False
                if normalFlow:
                    self._call_on_player_confirm(self.player[i], turn)

        # start new round
        self._call_on_press_new_round()


    def _call_on_player_confirm(self, player, turn):
        """
        Generate input value for turn 1 player input event:
        on_player_confirm(self, boxid, thisPlayer, cardList, bet)
        """
        boxid = player + "_box"
        thisPlayer = int(player[-1]) -1
        cardList = [0,1,2]
        if turn > 1:
            cardList = [4]
        bet = 1
        self.game.on_player_confirm( boxid, thisPlayer, cardList, bet )

    def _call_on_player_lie(self, player):
        """
        on_player_lie(self, player, card)
        """
        card =  "Ac"
        bet = 1
        self.game.on_player_lie(player, card, bet)

    def _call_on_player_suspect(self, player):
        """
        on_player_suspect(self, player, pno)
        """
        pno = int(player[-1]) -1
        self.game.on_player_suspect(player, pno)

    def _call_on_press_new_round(self):
        """
        on_press_new_round(self)
        """
        self.game.on_press_new_round()
