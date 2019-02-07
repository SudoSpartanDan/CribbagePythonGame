import random
import copy
from player import Player
from card import Card, CardSuit, CardValue
from deck import Deck
from play import Play

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

    def discard(self):
        # Player discard
        # First
        self.crib.append(selectCardToDiscard(self.player.hand))
        # Second
        self.crib.append(selectCardToDiscard(self.player.hand))
        # CPU Discard
        # First
        self.crib.append(self.cpu.hand.pop(random.randrange(len(self.cpu.hand))))
        # Second
        self.crib.append(self.cpu.hand.pop(random.randrange(len(self.cpu.hand))))

    def playRound(self):
        play = Play()
        playerHand = copy.deepcopy(self.player.hand)
        cpuHand = copy.deepcopy(self.cpu.hand)
        # Allows switching who goes first
        if(self.currentDealer == self.cpu):
            play.takeCPUTurn(cpuHand)
            print(play.points)
        while(len(playerHand) > 0 or len(cpuHand) > 0):
            # User input
            if(play.canHandPlay(playerHand)):
                play.takePlayerTurn(playerHand)
                self.player.score += play.calculateExtraPoints()
                print(play.points, end='')
                if(play.points == 31):
                    print(' for 2')
                    self.player.score += 2
                    play.reset()
                print()
            else:
                play.playerPasses = True
                if(play.everyonePassed()):
                    print('One for last')
                    self.player.score += 1
                    play.reset()
                else:
                    print('Player "GO"')

            # CPU Turn
            if(play.canHandPlay(cpuHand)):
                play.takeCPUTurn(cpuHand)
                self.cpu.score += play.calculateExtraPoints()
                print(play.points, end='')
                if(play.points == 31):
                    print(' for 2')
                    self.cpu.score += 2
                    play.reset()
                print()
            else:
                play.cpuPasses = True
                if(play.everyonePassed()):
                    print('One for last')
                    self.cpu.score += 1
                    play.reset()
                else:
                    print('CPU "GO"')
                

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

    def isComplete(self):
        if(self.player.score >= 121 or self.cpu.score >= 121):
            return True
        return False

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

def selectCardToDiscard(hand):
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
        else:
            return hand.pop(cardIndex)

def findFifteens(cards, fifteensFound, partial=[]):
    cardsTotal = sum(card.valuePoints for card in partial)

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
    lastCardValue = -1
    for card in sortedHand:
        if(card.valueInt != lastCardValue-1):
            if(len(run) > 2):
                return run
            run = [card]
        else:
            run.append(card)
        lastCardValue = card.valueInt
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
        print('15 for {0}'.format(scoreThisRound))
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
    # Find and print runs
    runFound = findRun(playerHand)
    runLength = len(runFound)
    if(runLength > 2):
        scoreThisRound += runLength
        print('Run of {0} for {1}'.format(runLength, scoreThisRound))
    # Find flushes
    flushFound = findFlush(hand, cutCard)
    flushLength = len(flushFound)
    if(flushLength > 3):
        scoreThisRound += flushLength
        print('Flush of {0} for {1}'.format(flushLength, scoreThisRound))
    # Find the nob
    hasNob = findNob(hand, cutCard)
    if(hasNob):
        scoreThisRound += 1
        print('Nobs for {0}'.format(scoreThisRound))
    
    return scoreThisRound