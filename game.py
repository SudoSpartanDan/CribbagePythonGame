import random
import copy
from player import Player
from card import Card, CardSuit, CardValue
from deck import Deck

def findFifteens(cards, fifteensFound, partial=[]):
    cardsTotal = sum(min(card.value.value, 10) for card in partial)

    if cardsTotal == 15:
        fifteensFound += [partial]
    if cardsTotal >= 15:
        return
    
    for i in range(len(cards)):
        card = cards[i]
        remaining = cards[i+1:]
        findFifteens(remaining, fifteensFound, partial + [card])

def findPairs(cards):
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

def findRun(cards):
    sortedHand = sorted(cards, reverse=True)
    run = []
    ## Make it negative 2 in the case of an ace which equal 0
    lastCardValue = -2
    for card in sortedHand:
        if(card.value.value != lastCardValue-1):
            if(len(run) > 2):
                return run
            run = [card]
        else:
            run.append(card)
        lastCardValue = card.value.value
    return run

def findFlush(hand, cutCard):
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

def findNob(hand, cutCard):
    for card in hand:
        if(card.suit == cutCard.suit and card.value == CardValue.JACK):
            return True
    return False

def calculateScoreForHand(hand, cutCard):
    # We're going to play with this a lot, so don't want to affect the original
    playerHand = copy.deepcopy(hand)
    playerHand.append(cutCard)
    scoreThisRound = 0
    # Find and print fifteens
    fifteensFound = []
    findFifteens(playerHand, fifteensFound)
    for fifteen in fifteensFound:
        scoreThisRound += 2
        print('15 - {0}'.format(scoreThisRound))
        #print(' '.join(['%s' % c for c in fifteen]))
    # Find and print pairs
    pairsFound = findPairs(playerHand)
    for pair in pairsFound:
        ## I WANT SWITCH STATEMENTS IN PYTHON
        if(len(pair) == 2):
            scoreThisRound += 2
            print('Pair for {0}'.format(scoreThisRound))
        elif(len(pair) == 3):
            scoreThisRound += 6
            print('Royal Pair {0}'.format(scoreThisRound))
        elif(len(pair) == 4):
            scoreThisRound += 12
            print('Double Royal Pair for {0}'.format(scoreThisRound))
        else:
            print('YOU MADE A BOO BOO')
        #print(' '.join(['%s' % c for c in pair]))
    # Find and print runs
    runFound = findRun(playerHand)
    runLength = len(runFound)
    if(runLength > 2):
        scoreThisRound += runLength
        print('Run of {0} for {1}'.format(runLength, scoreThisRound))
        #print(' '.join(['%s' % c for c in runFound]))
    # Find flushes
    flushFound = findFlush(hand, cutCard)
    flushLength = len(flushFound)
    if(flushLength > 3):
        scoreThisRound += flushLength
        print('Flush of {0} for {1}'.format(flushLength, scoreThisRound))
        #print(' '.join(['%s' % c for c in runFound]))
    # Find the nob
    hasNob = findNob(hand, cutCard)
    if(hasNob):
        scoreThisRound += 1
        print('Nobs for {0}'.format(scoreThisRound))
    
    return scoreThisRound

class Game:
    def __init__(self):
        self.player = Player('Player')
        self.cpu = Player('CPU')
        self.cutCard = None
        self.currentDealer = None
        self.deck = Deck()
        self.crib = []

    def determineDealer(self):
        r = random.randrange(1)
        self.currentDealer = self.player if r==1 else self.cpu

    def switchDealer(self):
        if(self.currentDealer == self.player):
            self.currentDealer = self.cpu
        else:
            self.currentDealer = self.player

    def dealCards(self):
        self.deck.shuffle()
        for i in range(6):
            self.player.hand.append(self.deck.deal())
            self.cpu.hand.append(self.deck.deal())
        self.cutCard = self.deck.cut()

    def calculatePlayerScore(self):
        self.player.score += calculateScoreForHand(self.player.hand, self.cutCard)

    def calculateCPUScore(self):
        self.cpu.score += calculateScoreForHand(self.cpu.hand, self.cutCard)

    def calculateCribScore(self):
        self.currentDealer.score += calculateScoreForHand(self.crib, self.cutCard)

    def endRound(self):
        self.crib = []
        self.cutCard = None
        self.player.hand = []
        self.cpu.hand = []

    def getScoreBoardString(self):
        playerScore = '{0:16s}: {1:3d}'.format(self.player.name, self.player.score)
        cpuScore = '{0:16s}: {1:3d}'.format(self.cpu.name, self.cpu.score)
        return '{0}\n{1}'.format(playerScore, cpuScore)

    def getPlayerHandString(self):
        return ' '.join(['%s' % c for c in self.player.hand])

    def getCPUHandString(self):
        return ' '.join(['%s' % c for c in self.cpu.hand])
    
    def getCribHandString(self):
        return ' '.join(['%s' % c for c in self.crib])