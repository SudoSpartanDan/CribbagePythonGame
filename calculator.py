from card import CardValue

class Calculator():
    def equalsFifteen(self, cards):
        if(sum(card.valuePoints for card in playCards) == 15):
            return True
        return False

    def getRunPoints(self, cards):
        if(len(cards) > 2):
            sortedCards = sorted(cards, reverse=True)
            currentCard = sortedCards[0]
            runLength = 1
            for card in sortedCards[1:]:
                if(currentCard.valueInt == (card.valueInt+1)):
                    runLength += 1
                    currentCard = card
                else:
                    break
            if(runLength > 2):
                return runLength
        return 0

    def getFlushPoints(self, cards, cutCard):
        currentSuit = cards[0].suit
        for card in cards[1:]:
            if(card.suit != currentSuit):
                return 0
        if(cutCard.suit == currentSuit):
            return 5
        else:
            return 4

    def findFifteens(self, cards, fifteensFound, partial=[]):
        cardsTotal = sum(card.valuePoints for card in partial)

        if cardsTotal == 15:
            fifteensFound += [partial]
        if cardsTotal >= 15:
            return
        
        for i in range(len(cards)):
            card = cards[i]
            remaining = cards[i+1:]
            self.findFifteens(remaining, fifteensFound, partial + [card])

    def findPairs(self, cards):
        pairsFound = []
        sortedHand = sorted(cards, reverse=True)
        cardPair = []
        currentCardValue = -1
        for card in sortedHand:
            if(card.value != currentCardValue):
                if(len(cardPair) > 1):
                    pairsFound += [cardPair]
                cardPair = [card]
                currentCardValue = card.value
            else:
                cardPair += [card]
        return pairsFound

    def findFlush(self, hand, cutCard):
        flush = [hand[0]]
        currentSuit = hand[0].suit
        for card in hand[1:]:
            if(card.suit != currentSuit):
                return []
            else:
                flush.append(card)
        if(cutCard.suit == currentSuit):
            flush.append(cutCard)
        return flush

    def hasNob(self, hand, cutCard):
        for card in hand:
            if(card.suit == cutCard.suit and card.value == CardValue.JACK):
                return True
        return False