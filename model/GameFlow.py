from abc import ABCMeta, abstractmethod

class GameFlow:
    __metaclass__ = ABCMeta

    @abstractmethod
    def build(self):
        """
        init of object
        """
        pass

    @abstractmethod
    def round_play(self):
        """
        Start of each round
        """
        pass

    @abstractmethod
    def turn_1_end(self):
        pass

    @abstractmethod
    def turn_2_end(self):
        pass

    @abstractmethod
    def turn_3_end(self):
        pass

    @abstractmethod
    def round_end(self):
        """
        Called when a round end
        """
        pass

    @abstractmethod
    def round_reset(self):
        """
        Called before a new round
        """
        pass
