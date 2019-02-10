import sys
import os
import platform
import random
import copy
from game import Game

def main():
    if(platform.system() == 'Windows'):
        clearString = 'cls'
    else:
        clearString = 'clear'
    game = Game()
    # Start the game
    game.determineDealer()
    while True:
        os.system(clearString)
        print('------------------- THE DEAL -------------------')
        game.dealCards()
        game.discard()
        os.system(clearString)
        print('------------------- THE PLAY -------------------')
        print('Cut Card: {0}'.format(game.cutCard))
        game.playRound()
        print('------------------- THE SHOW -------------------')
        game.show()
        print('------------------- SCORE -------------------')
        print(game.getScoreBoardString())
        game.endRound()
        if(game.isComplete()):
            print('Game Complete')
            break
        input('Press enter to play the next round...')
        game.switchDealer()

main()