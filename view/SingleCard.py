from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.image import Image

class SingleCard(FloatLayout):
    la = ObjectProperty(None)
    lb = ObjectProperty(None)
    check = ObjectProperty(None)
    enable = True
    suit = None
    rank = 0

    # TODO: where to put this?
    cardImage = {'s':"Spade.png", 'h':"Heart.png", 'd':"Diamond.png", 'c':"Club.png"}

    def reset_card(self):
        self.suit = None
        self.rank = 0
        self.la.text = ""
        self.lb.text = ""
        self._remove_suit_image()

    def set_card(self, cardStr):
        self.rank = cardStr[0]
        self.suit = cardStr[1]

    def show_card_to_self(self):
        """
        Only shows button side of card so that opponent cannot see it.
        """
        self.lb.text = str(self.rank)
        self._load_suit_image(self.lb.children[0])

    def show_card_to_all(self):
        self.la.text = str(self.rank)
        self.lb.text = self.la.text

        # test on suit image
        self._load_suit_image(self.la.children[0])
        self._load_suit_image(self.lb.children[0])

    def _load_suit_image(self, widget):
        widget.source = 'resource/' + self.cardImage[self.suit]
        widget.color = [1,1,1,1]
        #self.la.children[0].allow_stretch = True

    def _remove_suit_image(self):
        self.la.children[0].sourcee = ""
        self.la.children[0].color = [0,0,0,0]
        self.lb.children[0].sourcee = ""
        self.lb.children[0].color = [0,0,0,0]


    def round_reset(self):
        self.suit = None
        self.rank = 0
        #self.la.text = ""
        #self.lb.text = ""


    def click(self):
        # state change when button clicked
        self.check.active = not self.check.active

    def uncheck(self):
        # state change to "False"
        self.check.active = False

    def do_check(self):
        # state change to "True"
        self.check.active = True

    def enable_check(self):
        # Shows the checkbox widget
        if not self.check.parent:
            self.add_widget(self.check)
            self.enable = True

    def disable_check(self):
        # hides the checkbox widget
        self.remove_widget(self.check)
        self.enable = False

    def is_checkbox_active(self):
        return self.enable and self.check.active
