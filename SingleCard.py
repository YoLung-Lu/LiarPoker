from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

class SingleCard(FloatLayout):
    la = ObjectProperty(None)
    lb = ObjectProperty(None)
    check = ObjectProperty(None)
    enable = True

    def get_widget_by_id(self, w_id):
        #print self.ids[w_id]
        pass

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
