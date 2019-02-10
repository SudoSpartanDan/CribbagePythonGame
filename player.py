import copy
from abc import ABC, abstractclassmethod
from calculator import Calculator
class Player(ABC):
    def __init__(self, name: str):
        self.score = 0
        self.name = name
        self.hand = None
        self.playHand = None

    @abstractclassmethod
    def discard(self):
        pass

    def createPlayHand(self):
        self.playHand = copy.deepcopy(self.hand)

    def canPlay(self, pointLimit):
        if(len(self.playHand) > 0):
            for card in self.playHand:
                if(card.valuePoints <= pointLimit):
                    return True
        return False

    @abstractclassmethod
    def play(self, currentPlayPointLimit):
        pass

    def show(self, cutCard):
        self.score += self.hand.getPoints(cutCard)