from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton

class CardSelector(FloatLayout):
    suit = None
    cardDict = {}
    player = ""

    def build(self, board):
        self.player = self.id[0:7]
        #self.parent = board
        self.cardDict = {1:'A', 10:'T', 11:'J', 12:'Q', 13:'K'}
        for i in range(2,10): self.cardDict[i] = str(i)

    def get_card(self):
        """
        Player lies about his card and trigger event of board.
        return type: str with 2 digit (Rank + Suit), rank in upper, suit in lower
        E.g.: As or 7d
        """
        # TODO: trigger event of PlayerDeck instead of board
        if self.suit:
            #print self.suit + str(int(self.ids.slider_id.value))
            card = self.cardDict[ (int(self.ids.slider_id.value)) ] + self.suit.lower()

            self.parent.press_player_lie(self.player, card)

    def _select_suit(self, suit):
        self.suit = suit

    def _state_normalize(self):
        # state of suit selector are set to normal
        for child in self.children:
            if child.__module__ == "kivy.uix.togglebutton":
                child.state = "normal"
"""
class Game(Widget):
    Color = [1,255,1,1]

    def build(self):
        s = Selector()
        s.build()
        self.add_widget(s)
        pass

class CardSelectorApp(App):
    def build(self):
        game = Game()
        game.build()
        return game


if __name__ == '__main__':
    CardSelectorApp().run()
"""
