import random
from card import Card, CardSuit, CardValue

class Play():
    def __init__(self):
        self.cards = []

    def append(self, card):
        self.cards.append(card)

    @property
    def points(self):
        return sum(card.valuePoints for card in self.cards)

    @property
    def pointLimit(self):
        return 31 - self.points

    def calculateExtraPoints(self):
        # Can't get extra points if nothing is there
        if(self.cards == []):
            return 0
        extraPoints = 0
        # Check for fifteen
        if(sum(card.valuePoints for card in self.cards) == 15):
            extraPoints += 2
            print("15 for 2")

        # Check for like cards
        currentCardValue = self.cards[-1].value
        pairLength = 1
        for card in reversed(self.cards[:-1]):
            if(card.value == currentCardValue):
                pairLength += 1
            else:
                break
        if(pairLength == 2):
            print('Pair for 2')
            extraPoints += 2
        elif(pairLength == 3):
            print('Royal Pair for 6')
            extraPoints += 6
        elif(pairLength == 4):
            print('Double Royal Pair for 12')
            extraPoints += 12

        # Check for runs
        # Only if the chain is 3 or more cards
        if(len(self.cards) > 2):
            # Only checking last three cards
            sortedThree = sorted(self.cards[-3:], reverse=True)
            currentCardValue = sortedThree[0].value
            if(sortedThree[0].valueInt == (sortedThree[1].valueInt+1) and sortedThree[0].valueInt == (sortedThree[2].valueInt+2)):
                print('Run for 3')
                extraPoints += 3

        return extraPoints

    def reset(self):
        self.cards = []