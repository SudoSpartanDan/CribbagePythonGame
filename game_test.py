import unittest
from game import Game
from deck import Deck
from player import Player
from card import Card, CardSuit, CardValue

class GameTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_init(self):
        self.assertIsInstance(self.game.player, Player)
        self.assertIsInstance(self.game.cpu, Player)
        self.assertIsInstance(self.game.deck, Deck)
        self.assertEqual(self.game.crib, [])
        self.assertIsNone(self.game.cutCard)
        self.assertIsNone(self.game.currentDealer)

    def test_determineDealer(self):
        self.game.determineDealer()
        self.assertIsInstance(self.game.currentDealer, Player)

    def test_switchDealer(self):
        self.game.determineDealer()
        dealerName = self.game.currentDealer.name
        self.game.switchDealer()
        self.assertNotEqual(self.game.currentDealer.name, dealerName)

    def test_dealCards(self):
        self.game.determineDealer()
        self.game.dealCards()
        self.assertEqual(len(self.game.player.hand), 6)
        self.assertEqual(len(self.game.cpu.hand), 6)
        self.assertIsInstance(self.game.cutCard, Card)

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()