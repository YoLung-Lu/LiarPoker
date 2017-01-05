from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.image import Image

class SingleCard(FloatLayout):
    la = ObjectProperty(None)
    lb = ObjectProperty(None)
    image_top_id = ObjectProperty(None)
    check = ObjectProperty(None)
    enable = True
    suit = None
    rank = 0

    # TODO: where to put this?
    cardImage = {'s':"Spade.png", 'h':"Heart.png", 'd':"Diamond.png", 'c':"Club.png"}

    def set_card(self, rank, suit):
        self.suit = suit
        self.rank = rank

    def show_card_to_self(self):
        """
        Only shows button side of card so that opponent cannot see it.
        """
        self.la.text = self.suit + str(self.rank)

    def show_card_to_all(self):
        self.la.text = self.suit + str(self.rank)
        self.lb.text = self.la.text

        # test on suit image
        self._load_suit_image(self.la.children[0])

    def _load_suit_image(self, widget):
        widget.source = 'resource/' + self.cardImage[self.suit]
        widget.color = [1,1,1,1]
        #self.la.children[0].allow_stretch = True

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
