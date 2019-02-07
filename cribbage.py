import random
import copy
from game import Game

def main():
    game = Game()
    # Start the game
    game.determineDealer()
    while True:
        print('------------------- THE DEAL -------------------')
        game.dealCards()
        print('Player Hand: {0}'.format(game.getPlayerHandString()))
        game.discard()
        print('------------------- THE PLAY -------------------')
        game.play()
        print('------------------- THE SHOW -------------------')
        print('{0:^50s}'.format('Cut Card: {0}'.format(game.cutCard)))
        print('Player Hand : {0}'.format(game.getPlayerHandString()))
        game.calculatePlayerScore()
        print('{0:>50s}'.format('{0} : CPU Hand'.format(game.getCPUHandString())))
        game.calculateCPUScore()
        print('------------------- THE CRIB -------------------')
        print('{0:^50s}'.format('Crib Hand: {0}'.format(game.getCribHandString())))
        game.calculateCribScore()
        print('------------------- SCORE -------------------')
        print(game.getScoreBoardString())
        game.endRound()
        if(game.isComplete()):
            print('Game Complete')
            break
        game.switchDealer()

main()