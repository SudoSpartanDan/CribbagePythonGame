from player import Player
from hand import Hand

class Human(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.hand = Hand()

    def discard(self):
        if(self.hand == None or len(self.hand) <= 0):
            raise RuntimeError('No cards to discard')
        print('{0}\'s Hand: {1}'.format(self.name, str(self.hand)))
        handLength = len(self.hand)
        while True:
            try:
                cardIndex = int(input('Choose a card to discard (1-{0}): '.format(handLength))) - 1
            except ValueError:
                print('Error: Please enter a number 1-{0}.'.format(handLength))
                continue
            if(cardIndex < 0 or cardIndex >= handLength):
                print('Error: Please enter a number 1-{0}.'.format(handLength))
                continue
            else:
                return self.hand.pop(cardIndex)

    def play(self, currentPlayPointLimit):
        if(self.playHand == None):
            raise RuntimeError('No play hand was created')
        playHandLength = len(self.playHand)
        # Auto Play
        if(playHandLength <= 0):
            raise RuntimeError('No cards to play')
        elif(playHandLength == 1):
            return self.playHand.pop(0)
        else:
            print('{0}\'s Hand: {1}'.format(self.name, str(self.playHand)))
            while True:
                try:
                    cardIndex = int(input('Choose card (1-{0}): '.format(playHandLength))) - 1
                except ValueError:
                    print('Error: Please enter a number 1-{0}.'.format(playHandLength))
                    continue
                if(cardIndex < 0 or cardIndex >= playHandLength):
                    print('Error: Please enter a number 1-{0}.'.format(playHandLength))
                    continue
                if(self.playHand[cardIndex].valuePoints > currentPlayPointLimit):
                    print('Error: That card cannot be played. Please enter a different number 1-{0}.'.format(playHandLength))
                    continue
                else:
                    return self.playHand.pop(cardIndex)