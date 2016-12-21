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

    def build(self, board):
        self.board = board
        self.cardDict = {1:'A', 10:'T', 11:'J', 12:'Q', 13:'K'}
        for i in range(2,10): self.cardDict[i] = str(i)

    def get_card(self):
        if self.suit:
            #print self.suit + str(int(self.ids.slider_id.value))
            card = self.cardDict[ (int(self.ids.slider_id.value)) ] + self.suit.lower()

            self.board.on_lie(self.id, card)

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
