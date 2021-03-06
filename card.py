from enum import Enum

class CardValue(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class CardSuit(Enum):
    SPADES = 1
    CLUBS = 2
    DIAMONDS = 3
    HEARTS = 4

class Card:
    def __init__(self, value: CardValue, suit: CardSuit):
        self.value = value
        self.suit = suit

    @property
    def valueStr(self):
        return self.value.name

    @property
    def valueInt(self):
        return self.value.value

    @property
    def valuePoints(self):
        return min(self.value.value, 10)

    @property
    def suitStr(self):
        return self.suit.name

    @property
    def suitInt(self):
        return self.suit.value

    def __repr__(self):
        return "Card()"

    def __str__(self):
        if(self.suit == CardSuit.SPADES):
            suitSymbol = '♠'
        elif(self.suit == CardSuit.CLUBS):
            suitSymbol = '♣'
        elif(self.suit == CardSuit.DIAMONDS):
            suitSymbol = '♦'
        elif(self.suit == CardSuit.HEARTS):
            suitSymbol = '♥'
        # IF ACE or TEN, JACK, QUEEN, KING; use the first letter of the name
        if(self.value.value == 1 or self.value.value >= 10):
            return '[{0}{1}]'.format(self.value.name[0], suitSymbol)
        else:
            return '[{0}{1}]'.format(self.value.value, suitSymbol)

    def __eq__(self, other):
        return ((self.value.value == other.value.value) and (self.suit.value == other.suit.value))
        
    def __lt__(self, other):
        return self.value.value < other.value.value

    def __gt__(self, other):
        return self.value.value > other.value.value