
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from functools import partial

from deuces import Card, Evaluator, Deck
from SingleCard import SingleCard
from CardSelector import CardSelector
from BetSelector import BetSelector

from model import GameFlow
from abc import ABCMeta

class PlayerDeck(GameFlow, BoxLayout):
    __metaclass__ = type( 'GameMeta', (type(BoxLayout), ABCMeta), {})
    widget_storage = {}

    def build(self, parent, pname, pno, testMode):
        self.root = parent
        self.name = pname
        self.no = pno
        self.testMode = testMode
        self.id = pname + "_box"
        self.turn = 0
        # betting strategy decided by "BetSelector". Set to 1 as default
        self.bet = 1

        # register 5 cards
        for i in range(5):
            c = SingleCard(id = self.name + '_card' + str(i))
            #c.la.pos = (20, 0)
            self.ids[c.id] = c
            self.add_widget(c)
            self.add_widget(Widget(size_hint= (0.01, 1)) )

        self._init_child_widget()


    def round_play(self):
        # update_hand
        pass

    def turn_2_end(self):
        self._remove_empty_widget()
        self._add_lie_widget()

    def turn_3_end(self):
        self._remove_lie_widget()
        self._add_suspect_widget()

    def round_end(self):
        # remove suspect widget
        self._remove_suspect_widget()
        self._add_empty_widget()

    def round_reset(self):
        for i in range(5):
            self.ids[self.name + '_card'+str(i)].enable_check()
            self.ids[self.name + '_card'+str(i)].reset_card()
            if self.testMode and i > 1:
                self.ids[self.name + '_card'+str(i)].do_check()
            else:
                self.ids[self.name + '_card'+str(i)].uncheck()

    def update_hand(self, hand, turn):
        # input hand of player, update to widget base on current turn
        openCardIndex = {1:5, 2:1, 3:0, 4:-1}
        for i in range(5):
            self.ids[self.name + '_card'+str(i)].set_card( Card.int_to_str(hand[i]) )
            if i > openCardIndex[turn]:
                self.ids[self.name + '_card'+str(i)].show_card_to_all()
            else:
                self.ids[self.name + '_card'+str(i)].show_card_to_self()
            '''
            self.ids[self.name + '_card'+str(i)].lb.text = Card.int_to_pretty_str( hand[i] )
            if i > openCardIndex[turn]:
                self.ids[self.name + '_card'+str(i)].la.text = Card.int_to_pretty_str( hand[i] )
            '''

    def update_turn(self, turn):
        # Cards revealed after each turn
        # Also, checkboxs for revealed cards are removed.
        self.turn = turn
        openCardIndex = {1:5, 2:1, 3:0, 4:-1}
        for i in range(5):
            self.ids[self.name + '_card'+str(i)].uncheck()
            if i > openCardIndex[turn]:
                self.ids[self.name + '_card'+str(i)].disable_check()
            elif self.testMode and i == openCardIndex[turn]:
                self.ids[self.name + '_card'+str(i)].do_check()

        if turn == 3:
            self.ids[self.name + '_card0'].do_check()

    def set_button_message(self, msg):
        self.ids[self.name + "_but_confirm"].text = msg

    def insert_button_message(self, msg):
        m = self.ids[self.name + "_but_confirm"].text
        self.ids[self.name + "_but_confirm"].text = m + "\n" + msg

    def press_player_suspect(self, *kargs):
        self.root.on_player_suspect(self.name)

    def press_player_confirm(self, *kargs):
        # Notify the selected cards
        #print self.id

        # Check if other player done current turn
        if self.root.get_turn() < self.turn:
            self.insert_button_message("Please wait ...")

        pickedCards = []
        for i in range(5):
            if self.ids[self.name + '_card'+str(i)].is_checkbox_active():
                pickedCards.append(i)

        bet = self.ids[self.name+"_bs"].get_bet()
        self.root.on_player_confirm(self.id, self.no, pickedCards, bet)


    def _init_child_widget(self):
        # bet selector
        bs = BetSelector(id = self.name + "_bs")
        for child in bs.children:
            child.group = self.name + "_bet"

        # card selector
        cs = CardSelector(id = self.name + "_cs")
        cs.build(self.root)
        for child in cs.children:
            child.group = self.name + "_suit"

        # confirm button
        b = Button( id = self.name + "_but_confirm",
                    text = 'Confirm',
                    size_hint_y = 0.8,
                    on_press = self.press_player_confirm )

        # suspect button
        s = Button( id = self.name + "_but_suspect",
                    text = "Suspect",
                    size_hint_y = 0.8,
                    on_press = self.press_player_suspect )
        #b.bind(on_press=self.parent.on_player_suspect(self.player) )
        #buttoncallback = partial(self.root.on_player_suspect, self.name)
        #s.bind(on_press = buttoncallback)

        # show empty widget when lie widget not on screen
        emptyWidget = Widget(   id = self.name + "_empty",
                                size_hint= (1, 1))

        # store child widgets
        self.widget_storage[emptyWidget.id] = emptyWidget
        self.widget_storage[b.id] = b
        self.widget_storage[s.id] = s
        self.widget_storage[bs.id] = bs
        self.widget_storage[cs.id] = cs

        # put child widgets onto screen
        self._add_confirm_button()
        self._add_bet_widget()
        self._add_empty_widget()

    def _add_empty_widget(self):
        e = self.widget_storage[self.name + "_empty"]
        self.add_widget(e, index = len(self.children))

    def _add_suspect_widget(self):
        s = self.widget_storage[self.name + "_but_suspect"]
        self.add_widget(s, index = len(self.children))
        self.ids[s.id] = s

    def _add_confirm_button(self):
        b = self.widget_storage[self.name + "_but_confirm"]
        self.add_widget(b)
        self.ids[b.id] = b

    def _add_bet_widget(self):
        bs = self.widget_storage[self.name + "_bs"]
        self.add_widget(bs, index=len(self.children) )
        self.ids[bs.id] = bs

    def _add_lie_widget(self):
        cs = self.widget_storage[self.name + "_cs"]
        self.add_widget(cs, index=len(self.children) )
        self.ids[cs.id] = cs

    def _remove_empty_widget(self):
        e = self.widget_storage[self.name + "_empty"]
        self.remove_widget(e)

    def _remove_bet_widget(self):
        bs = self.ids[self.name + "_bs"]
        self.remove_widget(bs)

    def _remove_lie_widget(self):
        cs = self.ids[self.name + "_cs"]
        self.remove_widget(cs)

    def _remove_suspect_widget(self):
        s = self.widget_storage[self.name + "_but_suspect"]
        self.remove_widget(s)

    def _set_size_hint_x(self, size_hint_x):
        self.size_hint_x = size_hint_x
