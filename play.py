import random
from card import Card, CardSuit, CardValue

class Play():
    def __init__(self):
        self.cards = []
        self._points = None
        self.pointLimit = 31
        self.playerPasses = False
        self.cpuPasses = False

    @property
    def points(self):
        return sum(card.valuePoints for card in self.cards)

    def canHandPlay(self, hand):
        if(len(hand) > 0):
            for card in hand:
                if(card.valuePoints+self.points <= 31):
                    return True
        return False

    def takeCPUTurn(self, cpuHand):
        # First find playable cards
        playableCardIndexes = []
        pointLimit = self.pointLimit-self.points
        for i, card in enumerate(cpuHand):
            if(card.valuePoints <= pointLimit):
                playableCardIndexes.append(i)
        # Select a random card for now
        cpuCardPlayed = cpuHand.pop(random.choice(playableCardIndexes))
        self.cards.append(cpuCardPlayed)
        print('CPU plays {0}'.format(cpuCardPlayed))

    def takePlayerTurn(self, playerHand):
        # Auto Play
        if(len(playerHand) == 1):
            playerCardPlayed = playerHand.pop(0)
        else:
            playerCardPlayed = selectCardToPlay(playerHand, self.pointLimit-self.points)
        self.cards.append(playerCardPlayed)
        print('Player plays {0}'.format(playerCardPlayed))

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
            if(sortedThree[0].value == (sortedThree[1].valueInt-1) and sortedThree[0].value == (sortedThree[2].valueInt-2)):
                print('Run for 3')
                extraPoints += 3

        return extraPoints

    def everyonePassed(self):
        return (self.playerPasses and self.cpuPasses)

    def reset(self):
        self.cards = []
        playerPasses = False
        cpuPasses = False

def selectCardToPlay(hand, pointLimit):
    print('Player Hand: {0}'.format(' '.join(['%s' % c for c in hand])))
    while True:
        try:
            cardIndex = int(input('Choose card (1-{0}): '.format(len(hand)))) - 1
        except ValueError:
            print('Error: Please enter a number 1-{0}.'.format(len(hand)))
            continue
        if(cardIndex < 0 or cardIndex >= len(hand)):
            print('Error: Please enter a number 1-{0}.'.format(len(hand)))
            continue
        if(hand[cardIndex].valuePoints > pointLimit):
            print('Error: That card cannot be played. Please enter a different number 1-{0}.'.format(len(hand)))
            continue
        else:
            return hand.pop(cardIndex)