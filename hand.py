import copy
from calculator import Calculator

class Hand():
    def __init__(self):
        self._start = 0
        self._cards = []

    def __len__(self):
        return len(self._cards)

    def __delitem__(self, index):
        self._cards.__delitem__(index)

    def insert(self, index, value):
        self._cards.insert(index, value)

    def __setitem__(self, index, value):
        self._cards.__setitem__(index, value)

    def __getitem__(self, index):
        return self._cards.__getitem__(index)

    def append(self, value):
        self._cards.append(value)

    def pop(self, index):
        return self._cards.pop(index)

    def __iter__(self):
        return (card for card in self._cards)

    def __repr__(self):
        return "Hand()"

    def __str__(self):
        return ' '.join(['%s' % card for card in self._cards])

    def clear(self):
        self._cards = []

    def getPoints(self, cutCard):
        calculator = Calculator()
        # We're going to play with this a lot, so don't want to affect the original
        cardsWithCutCard = copy.deepcopy(self._cards)
        cardsWithCutCard.append(cutCard)
        points = 0
        # Find and print fifteens
        fifteensFound = []
        calculator.findFifteens(cardsWithCutCard, fifteensFound)
        for fifteen in fifteensFound:
            points += 2
            print('15 for {0}'.format(points))
        # Find and print pairs
        pairsFound = calculator.findPairs(cardsWithCutCard)
        for pair in pairsFound:
            points += (len(pair) * (len(pair)-1))
            ## I WANT SWITCH STATEMENTS IN PYTHON
            if(len(pair) == 2):
                print('Pair for {0}'.format(points))
            elif(len(pair) == 3):
                print('Royal Pair {0}'.format(points))
            elif(len(pair) == 4):
                print('Double Royal Pair for {0}'.format(points))
            else:
                print('YOU MADE A BOO BOO')
        # Find and print runs
        runPoints = calculator.getRunPoints(cardsWithCutCard)
        if(runPoints):
            points += runPoints
            print('Run of {0} for {1}'.format(runPoints, points))
        # Find flushes
        flushPoints = calculator.getFlushPoints(self._cards, cutCard)
        if(flushPoints > 3):
            points += flushPoints
            print('Flush of {0} for {1}'.format(flushPoints, points))
        # Find the nob
        hasNob = calculator.hasNob(self._cards, cutCard)
        if(hasNob):
            points += 1
            print('Nobs for {0}'.format(points))
        
        return points