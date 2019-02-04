import random
import math
from card import Card, CardSuit, CardValue

class Deck:
    def __init__(self):
        # populate the deck
        self.__cards = []
        for suit in CardSuit:
            for value in CardValue:
                self.__cards.append(Card(value, suit))
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.__cards)
        self.__dealIndex = 0

    def deal(self):
        if(self.__dealIndex >= len(self.__cards)):
            raise ValueError('No more cards are in the deck')
        self.__dealIndex += 1
        return self.__cards[self.__dealIndex - 1]

    def cut(self):
        if(self.__dealIndex >= len(self.__cards)):
            raise ValueError('No more cards are in the deck')
        # To cut, take the length of the deck minus the current deal index
        # Then divide that by 2; cutting to the middle of the deck
        # Then add the deal index back in to get the cut index to align with the deck
        cutIndex = math.floor((len(self.__cards) - self.__dealIndex) / 2) + self.__dealIndex
        return self.__cards[cutIndex]