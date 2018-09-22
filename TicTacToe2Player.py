# =============================================================================
# Title: 2 Player Tic-Tac-Toe
# Author: Ryan Slater
# Date: July 2017
# =============================================================================


def __printBoard__(board):
    '''
    Prints the board

    Parameters
    ----------
    board : list
        List of pieces at their locations
    '''
    print(board[0] + ' | ' + board[1] + ' | ' + board[2])
    print('--+---+--')
    print(board[3] + ' | ' + board[4] + ' | ' + board[5])
    print('--+---+--')
    print(board[6] + ' | ' + board[7] + ' | ' + board[8])

def __findWinner__(board):
    '''
    Parameters
    ----------
    board : list
        List of pieces at their locations
    Returns
    ----------
    winner : string
        'X', 'O', or 'No winner'
    '''
    winner = ''
    if (board[0] == board[3] and board[3] == board[6]):
        winner = board[0]
    elif (board[1] == board[4] and board[4] == board[7]):
        winner = board[1]
    elif (board[2] == board[5] and board[5] == board[8]):
        winner = board[2]
    elif (board[0] == board[1] and board[1] == board[2]):
        winner = board[0]
    elif (board[3] == board[4] and board[4] == board[5]):
        winner = board[3]
    elif (board[6] == board[7] and board[7] == board[8]):
        winner = board[6]
    elif (board[0] == board[4] and board[4] == board[8]):
        winner = board[0]
    elif (board[2] == board[4] and board[4] == board[6]):
        winner = board[2]
    else:
        winner = 'No winner'
    return(winner)

def TicTacToe2Player():
    board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    __printBoard__(board)

    for turnNumber in range(1, 10):
        legitSpace = False
        if turnNumber%2 != 0:
            print('X turn')
        else:
            print('O turn')
        while legitSpace == False:
                x = input()
                try:
                    x = int(x)
                except ValueError:
                    print('', end='')
                if isinstance(x, int) == True and x < 10 and x > 0:
                    if board[x-1] != 'X' and board[x-1] != 'O':
                        if turnNumber%2 != 0:
                            board[x-1] = 'X'
                        else:
                            board[x-1] = 'O'
                        break
                    else:
                        print('Can\'t go there!')
                else:
                    print('Enter an integer 1-9!')

        turnNumber += 1
        print(100*'\n')
        __printBoard__(board)
        if __findWinner__(board) != 'No winner':
            break
    winner = __findWinner__(board)
    if winner == 'No winner':
        print(winner)
    else:
        print(winner + ' Wins!')

if __name__ == '__main__':
    TicTacToe2Player()