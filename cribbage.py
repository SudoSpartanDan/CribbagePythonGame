import random
from game import Game

def pegPhase(game: Game):
    currentChain = []
    playerHand = game.player.hand
    cpuHand = game.cpu.hand


def discardPhase(game: Game):
    while True:
        try:
            firstCard = int(input('Choose first card to give to crib (1-6): '))
        except ValueError:
            print('Error: Please enter a number 1-6.')
            continue
        if(firstCard < 1 or firstCard > 6):
            print('Error: Please enter a number 1-6.')
            continue
        else:
            game.crib.append(game.player.hand.pop(firstCard-1))
            break
    print(game.getPlayerHandString(), '\n')

    while True:
        try:
            secondCard = int(input('Choose second card to give to crib (1-5): '))
        except ValueError:
            print('Error: Please enter a number 1-5.')
            continue
        if(secondCard < 1 or secondCard > 5):
            print('Error: Please enter a number 1-5.')
            continue
        else:
            game.crib.append(game.player.hand.pop(secondCard-1))
            break

    # CPU Discard
    # First
    game.crib.append(game.cpu.hand.pop(random.randrange(6)))
    # Second
    game.crib.append(game.cpu.hand.pop(random.randrange(5)))

def main():
    game = Game()
    # Start the game
    game.determineDealer()
    while True:
        print('Dealing Cards', '\n')
        game.dealCards()
        print(game.getPlayerHandString(), '\n')
        discardPhase(game)
        pegPhase(game)
        print('Player Hand: {0} Cut Card: {1}'.format(game.getPlayerHandString(), game.cutCard))
        game.calculatePlayerScore()
        print()
        print('CPU Hand:    {0} Cut Card: {1}'.format(game.getCPUHandString(), game.cutCard))
        game.calculateCPUScore()
        print()
        print('Crib Hand:   {0} Cut Card: {1}'.format(game.getCribHandString(), game.cutCard))
        game.calculateCribScore()
        print()
        print(game.getScoreBoardString(), '\n')
        game.endRound()
        if(game.isComplete()):
            print('Game Complete')
            break
        game.switchDealer()

main()