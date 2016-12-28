from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton

class BetSelector(FloatLayout):
    """
        For player to select his betting strategy in four choices:
            0. Big bet
            1. Middle bet
            2. Small bet
            3. Fold (Give away the round)

        The event is raised in turn 1 to 3.
        The bet would be the average bet from players.
    """
    # default bet is "small bet"
    bet = 2

    def get_bet(self):
        # get the bet choice of player ( range(0,4) )
        return self.bet

    def _select_bet(self, bet):
        self.bet = bet

    def _state_normalize(self):
        # state of suit selector are set to normal
        for child in self.children:
            if child.__module__ == "kivy.uix.togglebutton":
                child.state = "normal"
