from player import Player
from card import Card, CardSuit, CardValue
from deck import Deck

class Game:
    def __init__(self):
        self.player = Player('Player')
        self.cpu = Player('CPU')
        self.cutCard = None
        self.deck = Deck()
        self.crib = []

    def getScoreBoardString(self):
        playerScore = '{0:16s}: {1:3d}'.format(self.player.name, self.player.score)
        cpuScore = '{0:16s}: {1:3d}'.format(self.cpu.name, self.cpu.score)
        return '{0}\n{1}'.format(playerScore, cpuScore)

    def dealCards(self):
        self.deck.shuffle()
        for i in range(6):
            self.player.hand.append(self.deck.deal())
            self.cpu.hand.append(self.deck.deal())
        self.cutCard = self.deck.cut()

    def getPlayerHandString(self):
        return ' '.join(['%s' % c for c in self.player.hand])
    
    def getCribHandString(self):
        return ' '.join(['%s' % c for c in self.crib])