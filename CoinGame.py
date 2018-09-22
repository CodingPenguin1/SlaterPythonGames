#==============================================================================
# Title: Coin Game
# Author: Ryan Slater
# Date: 9/31/2017
#==============================================================================

import random as rand

def __getCoin__():
    validInput = False
    while validInput == False:
        print('Penny, Nickel, Dime, or Quarter?')
        coin = input().lower()
        if coin in ['penny', 'nickel', 'dime', 'quarter', 'quit', 'p', 'n', 'd', 'q']:
            validInput = True
    if coin == 'p':
        coin = 'penny'
    elif coin == 'n':
        coin = 'nickel'
    elif coin == 'd':
        coin = 'dime'
    elif coin == 'q':
        coin = 'quarter'
    return(coin)

def __flipCoin__(coin):
    score = 0
    headsOrTails = rand.randint(0, 1)
    if headsOrTails == 0:
        headsOrTails = -1
    if coin == 'penny':
        score = headsOrTails
    elif coin == 'nickel':
        score = 5*headsOrTails
    elif coin == 'dime':
        score = 10*headsOrTails
    elif coin == 'quarter':
        score = 25*headsOrTails
    return(score)

def __getWinner__(s1, s2):
    if s1 == 100:
        return('s1')
    elif s2 == 100:
        return('s2')
    else:
        return('none')

def CoinGame():
    gameOver, player = False, 0
    p0Score, p1Score = 0, 0
    print('Player 1, what is your name?')
    p0Name = input()
    print('Player 2, what is your name?')
    p1Name = input()
    while gameOver == False:
        t1s = p0Score/100
        t2s = p1Score/100
        print(100*'\n' + p0Name + ': $%.2f'%t1s)
        print(p1Name + ': $%.2f'%t2s)
        if player == 0:
            print('\n' + p0Name + '\'s turn')
        else:
            print('\n' + p1Name + '\'s turn')
        coin = __getCoin__()
        if coin == 'quit':
            break

        scoreMod = __flipCoin__(coin)
        if scoreMod == -1:
            print('Tails')
        else:
            print('Heads')

        if player == 0:
            p0Score += scoreMod
            if p0Score < 0:
                p0Score = 0
            if p0Score > 100:
                p0Score -= scoreMod
        elif player == 1:
            p1Score += scoreMod
            if p1Score < 0:
                p1Score = 0
            if p1Score > 100:
                p1Score -= scoreMod

        if __getWinner__(p0Score, p1Score) != 'none':
            break

        if player == 0:
            player = 1
        else:
            player = 0

    winner = __getWinner__(p0Score, p1Score)
    if winner == 's1':
        winner = p0Name
    else:
        winner = p1Name

    t1s = p0Score/100
    t2s = p1Score/100
    print(100*'\n' + winner + ' wins!')
    print(p0Name + ': $%.2f'%t1s)
    print(p1Name + ': $%.2f'%t2s)

if __name__ == '__main__':
    CoinGame()