from player import Player
from card import Card, CardSuit, CardValue
from deck import Deck

class Game:
    def __init__(self):
        self.player_one = Player('Player One')
        self.player_two = Player('Player Two')
        self.dealer = None
        self.deck = Deck()
        print('Game Created')