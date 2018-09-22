'''
1 Player Tic-Tac-Toe
By Ryan Slater
July 2017
'''
import random as rand

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
        'You', 'Computer', or 'No winner'
    '''
    winner = ''
    if board[0] == board[3] and board[3] == board[6]:
        winner = board[0]
    elif board[1] == board[4] and board[4] == board[7]:
        winner = board[1]
    elif board[2] == board[5] and board[5] == board[8]:
        winner = board[2]
    elif board[0] == board[1] and board[1] == board[2]:
        winner = board[0]
    elif board[3] == board[4] and board[4] == board[5]:
        winner = board[3]
    elif board[6] == board[7] and board[7] == board[8]:
        winner = board[6]
    elif board[0] == board[4] and board[4] == board[8]:
        winner = board[0]
    elif board[2] == board[4] and board[4] == board[6]:
        winner = board[2]
    else:
        winner = 'No winner'
    if winner == 'X': winner = 'You'
    else: winner == 'Computer'
    return(winner)

def __computerTurn__(difficulty):
    '''
    Modifies global list 'board' to take a turn

    ParametersprintNoose(num):
    ----------
    difficulty : string
        'easy', 'normal', or 'hard'
    '''
    move, validMove = 0, False
    if difficulty == 'easy':
        while validMove == False:
            move = rand.randint(0, 8)
            if board[move] != 'X' and board[move] != 'O':
                    board[move] = 'O'
                    validMove = True

    elif difficulty == 'normal':
        #Check for win possibility horizontally
        if board[0] == 'O' and board[1] == 'O' and board[2] == '3':
            board[2] = 'O'
        elif board[1] == 'O' and board[2] == 'O' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'O' and board[2] == 'O' and board[1] == '2':
            board[1] = 'O'
        elif board[3] == 'O' and board[4] == 'O' and board[5] == '6':
            board[5] = 'O'
        elif board[4] == 'O' and board[5] == 'O' and board[3] == '4':
            board[3] = 'O'
        elif board[3] == 'O' and board[5] == 'O' and board[4] == '5':
            board[4] = 'O'
        elif board[6] == 'O' and board[7] == 'O' and board[8] == '9':
            board[8] = 'O'
        elif board[7] == 'O' and board[8] == 'O' and board[6] == '7':
            board[6] = 'O'
        elif board[6] == 'O' and board[8] == 'O' and board[7] == '8':
            board[7] = 'O'

        #Check for win possibility vertically
        elif board[0] == 'O' and board[3] == 'O' and board[6] == '7':
            board[6] = 'O'
        elif board[3] == 'O' and board[6] == 'O' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'O' and board[6] == 'O' and board[3] == '4':
            board[3] = 'O'
        elif board[1] == 'O' and board[4] == 'O' and board[7] == '8':
            board[7] = 'O'
        elif board[4] == 'O' and board[7] == 'O' and board[1] == '2':
            board[1] = 'O'
        elif board[1] == 'O' and board[7] == 'O' and board[4] == '5':
            board[4] = 'O'
        elif board[2] == 'O' and board[5] == 'O' and board[8] == '9':
            board[8] = 'O'
        elif board[5] == 'O' and board[8] == 'O' and board[2] == '3':
            board[2] = 'O'
        elif board[2] == 'O' and board[8] == 'O' and board[5] == '6':
            board[5] = 'O'

        #Check for win possibility diagonally
        elif board[0] == 'O' and board[4] == 'O' and board[8] == '9':
            board[8] = 'O'
        elif board[4] == 'O' and board[8] == 'O' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'O' and board[8] == 'O' and board[4] == '5':
            board[4] = 'O'
        elif board[2] == 'O' and board[4] == 'O' and board[6] == '7':
            board[6] = 'O'
        elif board[4] == 'O' and board[6] == 'O' and board[2] == '3':
            board[2] = 'O'
        elif board[2] == 'O' and board[6] == 'O' and board[4] == '5':
            board[5] = 'O'

        #Check to block 2 in a row horizontally
        elif board[0] == 'X' and board[1] == 'X' and board[2] == '3':
            board[2] = 'O'
        elif board[1] == 'X' and board[2] == 'X' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'X' and board[2] == 'X' and board[1] == '2':
            board[1] = 'O'
        elif board[3] == 'X' and board[4] == 'X' and board[5] == '6':
            board[5] = 'O'
        elif board[4] == 'X' and board[5] == 'X' and board[3] == '4':
            board[3] = 'O'
        elif board[3] == 'X' and board[5] == 'X' and board[4] == '5':
            board[4] = 'O'
        elif board[6] == 'X' and board[7] == 'X' and board[8] == '9':
            board[8] = 'O'
        elif board[7] == 'X' and board[8] == 'X' and board[6] == '7':
            board[6] = 'O'
        elif board[6] == 'X' and board[8] == 'X' and board[7] == '7':
            board[7] = 'O'

        #Check to block 2 in a row vertically
        elif board[0] == 'X' and board[3] == 'X' and board[6] == '7':
            board[6] = 'O'
        elif board[3] == 'X' and board[6] == 'X' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'X' and board[6] == 'X' and board[3] == '4':
            board[3] = 'O'
        elif board[1] == 'X' and board[4] == 'X' and board[7] == '8':
            board[7] = 'O'
        elif board[4] == 'X' and board[7] == 'X' and board[1] == '2':
            board[1] = 'O'
        elif board[1] == 'X' and board[7] == 'X' and board[4] == '5':
            board[4] = 'O'
        elif board[2] == 'X' and board[5] == 'X' and board[8] == '9':
            board[8] = 'O'
        elif board[5] == 'X' and board[8] == 'X' and board[2] == '3':
            board[2] = 'O'
        elif board[2] == 'X' and board[8] == 'X' and board[5] == '6':
            board[5] = 'O'

        #Check to block 2 in a row diagonally
        elif board[0] == 'X' and board[4] == 'X' and board[8] == '9':
            board[8] = 'O'
        elif board[4] == 'X' and board[8] == 'X' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'X' and board[8] == 'X' and board[4] == '5':
            board[4] = 'O'
        elif board[2] == 'X' and board[4] == 'X' and board[6] == '7':
            board[6] = 'O'
        elif board[4] == 'X' and board[6] == 'X' and board[2] == '3':
            board[2] = 'O'
        elif board[2] == 'X' and board[6] == 'X' and board[4] == '5':
            board[4] = 'O'

        else:
            while validMove == False:
                move = rand.randint(0, 8)
                if board[move] != 'X' and board[move] != 'O':
                        board[move] = 'O'
                        validMove = True
    else:
        #Check for win possibility horizontally
        if board[0] == 'O' and board[1] == 'O' and board[2] == '3':
            board[2] = 'O'
        elif board[1] == 'O' and board[2] == 'O' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'O' and board[2] == 'O' and board[1] == '2':
            board[1] = 'O'
        elif board[3] == 'O' and board[4] == 'O' and board[5] == '6':
            board[5] = 'O'
        elif board[4] == 'O' and board[5] == 'O' and board[3] == '4':
            board[3] = 'O'
        elif board[3] == 'O' and board[5] == 'O' and board[4] == '5':
            board[4] = 'O'
        elif board[6] == 'O' and board[7] == 'O' and board[8] == '9':
            board[8] = 'O'
        elif board[7] == 'O' and board[8] == 'O' and board[6] == '7':
            board[6] = 'O'
        elif board[6] == 'O' and board[8] == 'O' and board[7] == '8':
            board[7] = 'O'

        #Check for win possibility vertically
        elif board[0] == 'O' and board[3] == 'O' and board[6] == '7':
            board[6] = 'O'
        elif board[3] == 'O' and board[6] == 'O' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'O' and board[6] == 'O' and board[3] == '4':
            board[3] = 'O'
        elif board[1] == 'O' and board[4] == 'O' and board[7] == '8':
            board[7] = 'O'
        elif board[4] == 'O' and board[7] == 'O' and board[1] == '2':
            board[1] = 'O'
        elif board[1] == 'O' and board[7] == 'O' and board[4] == '5':
            board[4] = 'O'
        elif board[2] == 'O' and board[5] == 'O' and board[8] == '9':
            board[8] = 'O'
        elif board[5] == 'O' and board[8] == 'O' and board[2] == '3':
            board[2] = 'O'
        elif board[2] == 'O' and board[8] == 'O' and board[5] == '6':
            board[5] = 'O'

        #Check for win possibility diagonally
        elif board[0] == 'O' and board[4] == 'O' and board[8] == '9':
            board[8] = 'O'
        elif board[4] == 'O' and board[8] == 'O' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'O' and board[8] == 'O' and board[4] == '5':
            board[4] = 'O'
        elif board[2] == 'O' and board[4] == 'O' and board[6] == '7':
            board[6] = 'O'
        elif board[4] == 'O' and board[6] == 'O' and board[2] == '3':
            board[2] = 'O'
        elif board[2] == 'O' and board[6] == 'O' and board[4] == '5':
            board[5] = 'O'

        #Check to block 2 in a row horizontally
        elif board[0] == 'X' and board[1] == 'X' and board[2] == '3':
            board[2] = 'O'
        elif board[1] == 'X' and board[2] == 'X' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'X' and board[2] == 'X' and board[1] == '2':
            board[1] = 'O'
        elif board[3] == 'X' and board[4] == 'X' and board[5] == '6':
            board[5] = 'O'
        elif board[4] == 'X' and board[5] == 'X' and board[3] == '4':
            board[3] = 'O'
        elif board[3] == 'X' and board[5] == 'X' and board[4] == '5':
            board[4] = 'O'
        elif board[6] == 'X' and board[7] == 'X' and board[8] == '9':
            board[8] = 'O'
        elif board[7] == 'X' and board[8] == 'X' and board[6] == '7':
            board[6] = 'O'
        elif board[6] == 'X' and board[8] == 'X' and board[7] == '8':
            board[7] = 'O'

        #Check to block 2 in a row vertically
        elif board[0] == 'X' and board[3] == 'X' and board[6] == '7':
            board[6] = 'O'
        elif board[3] == 'X' and board[6] == 'X' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'X' and board[6] == 'X' and board[3] == '4':
            board[3] = 'O'
        elif board[1] == 'X' and board[4] == 'X' and board[7] == '8':
            board[7] = 'O'
        elif board[4] == 'X' and board[7] == 'X' and board[1] == '2':
            board[1] = 'O'
        elif board[1] == 'X' and board[7] == 'X' and board[4] == '5':
            board[4] = 'O'
        elif board[2] == 'X' and board[5] == 'X' and board[8] == '9':
            board[8] = 'O'
        elif board[5] == 'X' and board[8] == 'X' and board[2] == '3':
            board[2] = 'O'
        elif board[2] == 'X' and board[8] == 'X' and board[5] == '6':
            board[5] = 'O'

        #Check to block 2 in a row diagonally
        elif board[0] == 'X' and board[4] == 'X' and board[8] == '9':
            board[8] = 'O'
        elif board[4] == 'X' and board[8] == 'X' and board[0] == '1':
            board[0] = 'O'
        elif board[0] == 'X' and board[8] == 'X' and board[4] == '5':
            board[4] = 'O'
        elif board[2] == 'X' and board[4] == 'X' and board[6] == '7':
            board[6] = 'O'
        elif board[4] == 'X' and board[6] == 'X' and board[2] == '3':
            board[2] = 'O'
        elif board[2] == 'X' and board[6] == 'X' and board[4] == '5':
            board[4] = 'O'

        else:
            if board[4] == '5':
                board[4] = 'O'
            elif board[0] == '1' or board[2] == '3' or board[6] == '7' or board[8] == '9':
                while validMove == False:
                    move = rand.randint(0, 3)
                    if move == 1: move = 2
                    elif move == 2: move = 6
                    elif move == 3: move = 8
                    if board[move] != 'X' and board[move] != 'O':
                        board[move] = 'O'
                        break
            else:
                while validMove == False:
                    move = rand.randint(0, 3)
                    if move == 0: move = 1
                    elif move == 1: move = 3
                    elif move == 2: move = 5
                    elif move == 3: move = 7
                    if board[move] != 'X' and board[move] != 'O':
                        board[move] = 'O'
                        break

def TicTacToe1Player():
    global board
    board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    legitSpace = False

    print('Enter difficulty:\nEasy Normal Hard')
    while legitSpace == False:
        difficulty = input()
        difficulty = difficulty.lower()
        if difficulty == 'easy' or difficulty == 'normal' or difficulty == 'hard':
            break
        else:
            print('Please enter \'Easy\', \'Normal\', \'Hard\'')

    __printBoard__(board)
    for turnNumber in range(1, 10):

        if turnNumber%2 != 0:
            while legitSpace == False:
                print('X turn')
                x = input()
                try:
                    x = int(x)
                except ValueError:
                    print('', end='')
                if isinstance(x, int) == True and x < 10 and x > 0:
                    if board[x-1] != 'X' and board[x-1] != 'O':
                        board[x-1] = 'X'
                        break
                    else:
                        print('Can\'t go there!')
                else:
                    print('Enter an integer 1-9!')

        elif turnNumber%2 == 0:
            __computerTurn__(difficulty)

        turnNumber += 1
        print(100*'\n')
        __printBoard__(board)
        if __findWinner__(board) != 'No winner':
            break
    winner = __findWinner__(board)
    if winner == 'No winner':
        print(winner)
    else:
        print(winner + ' Won!')

if __name__ == '__main__':
    TicTacToe1Player()