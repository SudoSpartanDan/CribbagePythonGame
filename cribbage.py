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
        game.playRound()
        print('------------------- THE SHOW -------------------')
        print('Player Hand: {0} Cut Card: {1}'.format(game.getPlayerHandString(), game.cutCard))
        game.calculatePlayerScore()
        print('CPU Hand:    {0} Cut Card: {1}'.format(game.getCPUHandString(), game.cutCard))
        game.calculateCPUScore()
        print('------------------- THE CRIB -------------------')
        print('Crib Hand:   {0} Cut Card: {1}'.format(game.getCribHandString(), game.cutCard))
        game.calculateCribScore()
        print('------------------- SCORE -------------------')
        print(game.getScoreBoardString())
        game.endRound()
        if(game.isComplete()):
            print('Game Complete')
            break
        game.switchDealer()

main()