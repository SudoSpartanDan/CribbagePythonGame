import random
import math
from card import Card, CardSuit, CardValue

class Deck:
    def __init__(self):
        # populate the deck
        self.cards = []
        for suit in CardSuit:
            for value in CardValue:
                self.cards.append(Card(value, suit))
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
        self.dealIndex = 0

    def deal(self):
        if(self.dealIndex >= len(self.cards)):
            raise ValueError('No more cards are in the deck')
        self.dealIndex += 1
        return self.cards[self.dealIndex - 1]

    def cut(self):
        if(self.dealIndex >= len(self.cards)):
            raise ValueError('No more cards are in the deck')
        # To cut, take the length of the deck minus the current deal index
        # Then divide that by 2; cutting to the middle of the deck
        # Then add the deal index back in to get the cut index to align with the deck
        cutIndex = math.floor((len(self.cards) - self.dealIndex) / 2) + self.dealIndex
        return self.cards[cutIndex]