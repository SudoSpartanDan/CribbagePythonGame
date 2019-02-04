from game import Game

def main():
    game = Game()
    print(game.getScoreBoardString(), '\n')
    print('Dealing Cards', '\n')
    game.dealCards()
    print(game.getPlayerHandString(), '\n')
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
        if(firstCard < 1 or firstCard > 5):
            print('Error: Please enter a number 1-5.')
            continue
        else:
            game.crib.append(game.player.hand.pop(firstCard-1))
            break

    print(game.getPlayerHandString(), '\n')
    print(game.getCribHandString(), '\n')

main()