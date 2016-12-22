from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

class SingleCard(FloatLayout):
    la = ObjectProperty(None)
    lb = ObjectProperty(None)
    check = ObjectProperty(None)

    def get_widget_by_id(self, w_id):
        #print self.ids[w_id]
        pass

    def uncheck(self):
        self.check.active = False

    def enable_check(self):
        if not self.check.parent:
            self.add_widget(self.check)

    def disable_check(self):
        self.remove_widget(self.check)