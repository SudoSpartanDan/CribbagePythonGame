import unittest
from play import Play
from card import Card, CardSuit, CardValue

class GameTest(unittest.TestCase):
    def setUp(self):
        self.play = Play()

    def test_init(self):
        self.assertEqual(self.play.cards, [])

    def test_append(self):
        # Setup
        card = Card(CardValue.TEN, CardSuit.HEARTS)

        # Run
        self.play.append(card)

        # Assert
        self.assertEqual(card, self.play.cards[0])

    def test_calculateExtraPoints_runOfThree(self):
        # Setup
        self.play.append(Card(CardValue.TEN, CardSuit.HEARTS))
        self.play.append(Card(CardValue.NINE, CardSuit.HEARTS))
        self.play.append(Card(CardValue.EIGHT, CardSuit.HEARTS))

        # Run
        extraPoints = self.play.calculateExtraPoints()

        # Assert
        self.assertEqual(extraPoints, 3)

if __name__ == '__main__':
    unittest.main()