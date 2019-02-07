import random
import copy
from player import Player
from card import Card, CardSuit, CardValue
from deck import Deck

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
        self.crib.append(selectCard(self.player.hand))
        # Second
        self.crib.append(selectCard(self.player.hand))
        # CPU Discard
        # First
        self.crib.append(self.cpu.hand.pop(random.randrange(len(self.cpu.hand))))
        # Second
        self.crib.append(self.cpu.hand.pop(random.randrange(len(self.cpu.hand))))

    def play(self):
        currentChain = []
        currentChainPoints = 0
        playerPasses = False
        cpuPasses = False
        playerHand = copy.deepcopy(self.player.hand)
        cpuHand = copy.deepcopy(self.cpu.hand)
        # Allows switching who goes first
        if(self.currentDealer == self.cpu):
            currentChainPoints += cpuPlay(cpuHand, currentChain, currentChainPoints)
            print('{0:^50s}'.format('Tally: ' + str(currentChainPoints)))
        while(len(playerHand) > 0 or len(cpuHand) > 0):
            # User input
            if(canPlay(playerHand, currentChainPoints)):
                currentChainPoints += playerPlay(playerHand, currentChain, currentChainPoints)
                self.player.score += checkChainForExtraPoints(currentChain)
                print('{0:^50s}'.format('Tally: ' + str(currentChainPoints)))
                if(currentChainPoints == 31):
                    print('31 for 2')
                    self.player.score += 2
                    currentChain = []
                    currentChainPoints = 0
                    playerPasses = False
                    cpuPasses = False
            else:
                playerPasses = True
                if(playerPasses and cpuPasses):
                    print('One for last')
                    self.player.score += 1
                    currentChain = []
                    currentChainPoints = 0
                    playerPasses = False
                    cpuPasses = False
                else:
                    print('Player "GO"')

            # CPU Turn
            if(canPlay(cpuHand, currentChainPoints)):
                currentChainPoints += cpuPlay(cpuHand, currentChain, currentChainPoints)
                self.cpu.score += checkChainForExtraPoints(currentChain, '>')
                print('{0:^50s}'.format('Tally: ' + str(currentChainPoints)))
                if(currentChainPoints == 31):
                    print('31 for 2')
                    self.cpu.score += 2
                    currentChain = []
                    currentChainPoints = 0
                    playerPasses = False
                    cpuPasses = False
            else:
                cpuPasses = True
                if(playerPasses and cpuPasses):
                    print('{:>50s}'.format('One for last'))
                    self.cpu.score += 1
                    currentChain = []
                    currentChainPoints = 0
                    playerPasses = False
                    cpuPasses = False
                else:
                    print('{:>50s}'.format('CPU "GO"'))
                

    def calculatePlayerScore(self):
        self.player.score += calculateScoreForHand(self.player.hand, self.cutCard, '<')

    def calculateCPUScore(self):
        self.cpu.score += calculateScoreForHand(self.cpu.hand, self.cutCard, '>')

    def calculateCribScore(self):
        if(self.currentDealer == self.cpu):
            printAlign = '>'
        else:
            printAlign = '<'
        self.currentDealer.score += calculateScoreForHand(self.crib, self.cutCard, printAlign)

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
        return '{0:<25s}{1:>25s}'.format(playerScore, cpuScore)

    def getPlayerHandString(self):
        return ' '.join(['%s' % c for c in self.player.hand])

    def getCPUHandString(self):
        return ' '.join(['%s' % c for c in self.cpu.hand])
    
    def getCribHandString(self):
        return ' '.join(['%s' % c for c in self.crib])

def selectCard(hand, pointLimit=0):
    print('Player Hand: {0}'.format(' '.join(['%s' % c for c in hand])))
    while True:
        try:
            cardIndex = int(input('Choose card (1-{0}): '.format(len(hand))))
        except ValueError:
            print('Error: Please enter a number 1-{0}.'.format(len(hand)))
            continue
        if(cardIndex < 1 or cardIndex > len(hand)):
            print('Error: Please enter a number 1-{0}.'.format(len(hand)))
            continue
        if(pointLimit > 0 and hand[cardIndex-1].value.value > pointLimit):
            print('Error: That card cannot be played. Please enter a different number 1-{0}.'.format(len(hand)))
            continue
        else:
            return hand.pop(cardIndex-1)

def cpuPlay(cpuHand, chain, chainPoints):
    # First find playable cards
    playableCardIndexes = []
    pointLimit = 31-chainPoints
    for i, card in enumerate(cpuHand):
        if(card.value.value <= pointLimit):
            playableCardIndexes.append(i)
    # Select a random card for now
    cpuCardPlayed = cpuHand.pop(random.choice(playableCardIndexes))
    chain.append(cpuCardPlayed)
    print('{0:>50s}'.format('CPU plays ' + str(cpuCardPlayed)))
    return min(cpuCardPlayed.value.value, 10)

def playerPlay(playerHand, chain, chainPoints):
    # Auto Play
    if(len(playerHand) == 1):
        playerCardPlayed = playerHand.pop(0)
    else:
        playerCardPlayed = selectCard(playerHand, 31-chainPoints)
    chain.append(playerCardPlayed)
    print('Player plays {0}'.format(playerCardPlayed))
    return min(playerCardPlayed.value.value, 10)

def checkChainForExtraPoints(chain, printAlign = '<'):
    printFormat = '{0:' + printAlign + '50s}'
    # Can't get extra points if nothing is there
    if(chain == []):
        return 0
    extraPoints = 0
    # Check for fifteen
    if(sum(min(card.value.value, 10) for card in chain) == 15):
        extraPoints += 2
        print(printFormat.format('15 for 2'))

    # Check for like cards
    currentCardValue = chain[-1].value
    pairLength = 1
    for card in reversed(chain[:-1]):
        if(card.value == currentCardValue):
            pairLength += 1
        else:
            break
    if(pairLength == 2):
        print(printFormat.format('Pair for 2'))
        extraPoints += 2
    elif(pairLength == 3):
        print(printFormat.format('Royal Pair for 6'))
        extraPoints += 6
    elif(pairLength == 4):
        print(printFormat.format('Double Royal Pair for 12'))
        extraPoints += 12

    # Check for runs
    # Only if the chain is 3 or more cards
    if(len(chain) > 2):
        # Only checking last three cards
        sortedThree = sorted(chain[-3:], reverse=True)
        currentCardValue = sortedThree[0].value
        if(sortedThree[0].value == (sortedThree[1].value.value-1) and sortedThree[0].value == (sortedThree[2].value.value-2)):
            print(printFormat.format('Run for 3'))
            extraPoints += 3

    return extraPoints

def canPlay(hand, chainPoints):
    if(len(hand) > 0):
        for card in hand:
            if(min(card.value.value, 10)+chainPoints <= 31):
                return True
    return False

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
    lastCardValue = -1
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

def calculateScoreForHand(hand, cutCard, printAlign='<'):
    printFormat = '{0:' + printAlign + '50s}'
    # We're going to play with this a lot, so don't want to affect the original
    playerHand = copy.deepcopy(hand)
    playerHand.append(cutCard)
    scoreThisRound = 0
    # Find and print fifteens
    fifteensFound = []
    findFifteens(playerHand, fifteensFound)
    for fifteen in fifteensFound:
        scoreThisRound += 2
        print(printFormat.format('15 for ' + str(scoreThisRound)))
        #print(' '.join(['%s' % c for c in fifteen]))
    # Find and print pairs
    pairsFound = findPairs(playerHand)
    for pair in pairsFound:
        ## I WANT SWITCH STATEMENTS IN PYTHON
        if(len(pair) == 2):
            scoreThisRound += 2
            print(printFormat.format('Pair for ' + str(scoreThisRound)))
        elif(len(pair) == 3):
            scoreThisRound += 6
            print(printFormat.format('Royal Pair for ' + str(scoreThisRound)))
        elif(len(pair) == 4):
            scoreThisRound += 12
            print(printFormat.format('Double Royal Pair for ' + str(scoreThisRound)))
        else:
            print('YOU MADE A BOO BOO')
        #print(' '.join(['%s' % c for c in pair]))
    # Find and print runs
    runFound = findRun(playerHand)
    runLength = len(runFound)
    if(runLength > 2):
        scoreThisRound += runLength
        print(printFormat.format('Run of {0} for {1}'.format(runLength, scoreThisRound)))
        #print(' '.join(['%s' % c for c in runFound]))
    # Find flushes
    flushFound = findFlush(hand, cutCard)
    flushLength = len(flushFound)
    if(flushLength > 3):
        scoreThisRound += flushLength
        print(printFormat.format('Flush of {0} for {1}'.format(flushLength, scoreThisRound)))
        #print(' '.join(['%s' % c for c in runFound]))
    # Find the nob
    hasNob = findNob(hand, cutCard)
    if(hasNob):
        scoreThisRound += 1
        print(printFormat.format('Nobs for ' + str(scoreThisRound)))
    
    return scoreThisRound