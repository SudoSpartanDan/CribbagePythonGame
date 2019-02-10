import random
import copy
from human import Human
from cpu import CPU
from card import Card, CardSuit, CardValue
from hand import Hand
from deck import Deck
from play import Play

class Game:
    def __init__(self):
        self.players = [Human('Player'), CPU('CPU')]
        self.dealToCrib = False
        if(len(self.players) == 2):
            self.dealCardNumber = 6
        elif(len(self.players) == 3 or len(self.players) == 4):
            self.dealCardNumber = 5
            self.dealToCrib = True
        else:
            raise ValueError('Number of players not supported')
        self.gameWinningScore = 121
        self.cutCard = None
        self.currentDealer = None
        self.deck = Deck()
        self.crib = Hand()

    def determineDealer(self):
        randomIndex = random.randrange(len(self.players))
        self.currentDealer = self.players[randomIndex]

    def switchDealer(self):
        dealerIndex = self.players.index(self.currentDealer)
        if(dealerIndex < 0 or dealerIndex >= len(self.players)):
            self.determineDealer()
        elif((dealerIndex + 1) % len(self.players) == 0):
            self.currentDealer = self.players[0]
        else:
            self.currentDealer = self.players[dealerIndex + 1]

    def dealCards(self):
        self.deck.shuffle()
        for i in range(self.dealCardNumber):
            for player in self.players:
                player.hand.append(self.deck.deal())
        if(self.dealToCrib):
            self.crib.append(self.deck.deal())
        self.cutCard = self.deck.cut()

    def discard(self):
        # Player discard
        # First
        for player in self.players:
            self.crib.append(player.discard())
            self.crib.append(player.discard())

    def playRound(self):
        currentPlay = Play()
        currentPlayerIndex = self.players.index(self.currentDealer)
        currentPlayer = self.players[currentPlayerIndex]
        for player in self.players:
            player.createPlayHand()
        lastPlayerToPlay = None
        while True:
            # Determine is anyone has cards left
            someoneHasCards = False
            for player in self.players:
                if(len(player.playHand) > 0):
                    someoneHasCards = True
            if(not someoneHasCards):
                break

            # Get the next player
            if((currentPlayerIndex + 1) % len(self.players) == 0):
                currentPlayerIndex = 0
                currentPlayer = self.players[0]
            else:
                currentPlayerIndex += 1
            currentPlayer = self.players[currentPlayerIndex]

            # If player can play, play
            if(currentPlayer.canPlay(currentPlay.pointLimit)):
                cardPlayed = currentPlayer.play(currentPlay.pointLimit)
                currentPlay.append(cardPlayed)
                print('{0} plays {1}'.format(currentPlayer.name, cardPlayed))
                currentPlayer.score += currentPlay.calculateExtraPoints()
                lastPlayerToPlay = currentPlayer
                print(currentPlay.points)
            else:
                if(currentPlayer == lastPlayerToPlay):
                    currentPlayer.score += 1
                    print('{0}: One for last'.format(currentPlayer.name))
                    currentPlay.reset()
                else:
                    print('{0} GO'.format(currentPlayer.name))
        currentPlayer.score += 1
        print('{0}: One for last'.format(currentPlayer.name))
        currentPlay.reset()

    def show(self):
        print('Cut Card: {0}'.format(self.cutCard))
        for player in self.players:
            print(player.name, player.hand)
            player.show(self.cutCard)
        print('The Crib: {0}'.format(self.crib))
        self.currentDealer.score += self.crib.getPoints(self.cutCard)

    def endRound(self):
        self.crib.clear()
        self.cutCard = None
        for player in self.players:
            player.hand.clear()

    def isComplete(self):
        for player in self.players:
            if(player.score >= self.gameWinningScore):
                return True
        return False

    def getScoreBoardString(self):
        scoreBoardString = ''
        for player in self.players:
            scoreBoardString += '{0:16s}: {1:3d}\n'.format(player.name, player.score)
        return scoreBoardString