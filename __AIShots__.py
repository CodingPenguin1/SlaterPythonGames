# =============================================================================
# Battleship AI generate shots
# =============================================================================

# import matplotlib.pyplot as plt
import random as rand
import numpy as np

AIBoard = np.array([[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])

def updateMode():
    """
    Updates the AI mode

    Returns
    -------------------

    mode: str
        "target" or "search"
    """
    for row in range(0, 10):
        for col in range(0, 10):
            if AIBoard[row][col] == 'X':
                return "target"
    return "search"

def updateAIBoardSinking(shipCoords):
    """
    Call once a ship is sunk. Replaces the 'X's on the AI board with 'S's to denote a sunk ship
    """
    for i in range(0, len(shipCoords)):
        row = shipCoords[i][0]
        col = shipCoords[i][1]
        AIBoard[row][col] = 'S'

def updateAIBoard(guess, value):
    """
    Mutator function for AIBoard

    Parameters
    -------------------

    guess: Tuple (int, int)
        Coordinates of guess (row, column)
    value: str
        Use 'O' or 'X'
    """
    AIBoard[guess[0]][guess[1]] = value

def checkValidShotLocation(guess):
    """
    Checks if a shot location is valid

    Parameters
    -------------------

    guess: Tuple (int, int)
        Coordinates of guess (row, column)

    Returns
    -------------------

    Boolean, true if valid location, false if not
    """
    if str(guess[0]) in "0123456789" and str(guess[1]) in "0123456789":
        if AIBoard[guess[0]][guess[1]] == 'O' or AIBoard[guess[0]][guess[1]] == 'X' or AIBoard[guess[0]][guess[1]] == 'S':
            return False
        return True
    return False

def __saveHeatMap__(ships, mode, diff, turn, directory, name):
    if mode == "search":
        search(diff, ships, AIBoard, turn)
    else:
        target(ships)
    a = AIBoardHeatMap
#     plt.imshow(a, cmap='binary')
#     plt.title(name + ' ' + str(turn))
#     plt.savefig(directory + '/' + str(turn) + '.png')

def search(diff, ships, p2board, turnCount):
    global AIBoardHeatMap
    AIBoardHeatMap = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    method = 3
    randomProb = 25
    if turnCount > 50:
        randomProb = 0
    if rand.randint(1, 100) <= randomProb:
        #random
        method = 1
        if rand.randint(1, 100) <= 65:
            #noisemap
            method = 0
    elif rand.randint(1, 100) <= 10:
        #corner
        method = 2

    #NOISEMAP
    if method == 0:
        shipCount = 0
        if ships[0] == False:
            shipCount += 1
        if ships[1] == False:
            shipCount += 1
        if ships[2] == False:
            shipCount += 1
        if ships[3] == False:
            shipCount += 1
        if ships[4] == False:
            shipCount += 1
        for row in range(0, 10):
            for col in range(0, 10):
                AIBoardHeatMap[row][col] = rand.randint(0, shipCount)
        method = 3

    #RANDOM SHOT
    if method == 1:
        while True:
            shot = (rand.randint(0, 9), rand.randint(0, 9))
            if AIBoard[shot[0]][shot[1]] == ' ':
                return shot

    #RANDOM CORNER
    if method == 2:
        c0, c1, c2, c3 = False, False, False, False
        if AIBoard[0][0] == ' ':
            c0 = True
        if AIBoard[0][9] == ' ':
            c1 = True
        if AIBoard[9][0] == ' ':
            c2 = True
        if AIBoard[9][9] == ' ':
            c3 = True

        shot = (0, 0)
        if c0 or c1 or c2 or c3:
            while True:
                corner = rand.randint(0, 3)
                if corner == 0:
                    if c0 == True:
                        shot = (0, 0)
                        break
                elif corner == 1:
                    if c1 == True:
                        shot = (0, 9)
                        break
                elif corner == 2:
                    if c2 == True:
                        shot = (9, 0)
                        break
                elif corner == 3:
                    if c3 == True:
                        shot = (9, 9)
                        break
            return shot

        else:
            method = 3

    #HEATMAP
    if method == 3:
        #For each space
        for row in range(0, 10):
            for col in range(0, 10):

                #Destroyer Check
                if ships[4] == False and p2board[row][col] == ' ':
                    if col-1 >= 0:
                        if AIBoard[row][col-1] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-1 >= 0:
                        if AIBoard[row-1][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col+1 <= 9:
                        if AIBoard[row][col+1] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row+1 <= 9:
                        if AIBoard[row+1][col] == ' ':
                            AIBoardHeatMap[row][col] += 1

                #Sub Check
                if ships[3] == False and p2board[row][col] == ' ' and diff >= 2:
                    if col-1 >= 0 and col+1 <= 9:
                        if AIBoard[row][col-1] == ' ' and AIBoard[row][col+1] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-1 >= 0 and row+1 <= 9:
                        if AIBoard[row-1][col] == ' ' and AIBoard[row+1][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col-2 >= 0:
                        if AIBoard[row][col-2] == ' ' and AIBoard[row][col-1] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-2 >= 0:
                        if AIBoard[row-2][col] == ' ' and AIBoard[row-1][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col+2 <= 9:
                        if AIBoard[row][col+2] == ' ' and AIBoard[row][col+1] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row+2 <= 9:
                        if AIBoard[row+2][col] == ' ' and AIBoard[row+1][col] == ' ':
                            AIBoardHeatMap[row][col] += 1

                #Cruiser Check
                if ships[2] == False and p2board[row][col] == ' ' and diff >= 2:
                    if col-1 >= 0 and col+1 <= 9:
                        if AIBoard[row][col-1] == ' ' and AIBoard[row][col+1] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-1 >= 0 and row+1 <= 9:
                        if AIBoard[row-1][col] == ' ' and AIBoard[row+1][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col-2 >= 0:
                        if AIBoard[row][col-2] == ' ' and AIBoard[row][col-1] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-2 >= 0:
                        if AIBoard[row-2][col] == ' ' and AIBoard[row-1][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col+2 <= 9:
                        if AIBoard[row][col+2] == ' ' and AIBoard[row][col+1] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row+2 <= 9:
                        if AIBoard[row+2][col] == ' ' and AIBoard[row+1][col] == ' ':
                            AIBoardHeatMap[row][col] += 1

                #Battleship Check
                if ships[1] == False and p2board[row][col] == ' ' and diff == 3:
                    if col-3 >= 0:
                        if AIBoard[row][col-1] == ' ' and AIBoard[row][col-2] == ' ' and AIBoard[row][col-3] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col-2 >= 0 and col+1 <= 9:
                        if AIBoard[row][col-1] == ' ' and AIBoard[row][col-2] == ' ' and AIBoard[row][col+1] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col-1 >= 0 and col+2 <= 9:
                        if AIBoard[row][col-1] == ' ' and AIBoard[row][col+1] == ' ' and AIBoard[row][col+2] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col+3 <= 9:
                        if AIBoard[row][col+1] == ' ' and AIBoard[row][col+2] == ' ' and AIBoard[row][col+3] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-3 >= 0:
                        if AIBoard[row-1][col] == ' ' and AIBoard[row-2][col] == ' ' and AIBoard[row-3][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-2 >= 0 and row+1 <= 9:
                        if AIBoard[row-1][col] == ' ' and AIBoard[row-2][col] == ' ' and AIBoard[row+1][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-1 >= 0 and row+2 <= 9:
                        if AIBoard[row-1][col] == ' ' and AIBoard[row+1][col] == ' ' and AIBoard[row+2][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row+3 <= 9:
                        if AIBoard[row+1][col] == ' ' and AIBoard[row+2][col] == ' ' and AIBoard[row+3][col] == ' ':
                            AIBoardHeatMap[row][col] += 1

                #Carrier Check
                if ships[0] == False and p2board[row][col] == ' ' and diff == 3:
                    if col-4 >= 0:
                        if AIBoard[row][col-1] == ' ' and AIBoard[row][col-2] == ' ' and AIBoard[row][col-3] == ' ' and AIBoard[row][col-4] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col-3 >= 0 and col+1 <= 9:
                        if AIBoard[row][col-1] == ' ' and AIBoard[row][col-2] == ' ' and AIBoard[row][col-3] == ' ' and AIBoard[row][col+1] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col-2 >= 0 and col+2 <= 9:
                        if AIBoard[row][col-1] == ' ' and AIBoard[row][col-2] == ' ' and AIBoard[row][col+1] == ' ' and AIBoard[row][col+2] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col-1 >= 0 and col+3 <= 9:
                        if AIBoard[row][col-1] == ' ' and AIBoard[row][col+1] == ' ' and AIBoard[row][col+2] == ' ' and AIBoard[row][col+3] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if col+4 <= 9:
                        if AIBoard[row][col+1] == ' ' and AIBoard[row][col+2] == ' ' and AIBoard[row][col+3] == ' ' and AIBoard[row][col+4] == ' ':
                            AIBoardHeatMap[row][col] += 1

                    if row-4 >= 0:
                        if AIBoard[row-1][col] == ' ' and AIBoard[row-2][col] == ' ' and AIBoard[row-3][col] == ' ' and AIBoard[row-4][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-3 >= 0 and row+1 <= 9:
                        if AIBoard[row-1][col] == ' ' and AIBoard[row-2][col] == ' ' and AIBoard[row-3][col] == ' ' and AIBoard[row-1][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-2 >= 0 and row+2 <= 9:
                        if AIBoard[row-1][col] == ' ' and AIBoard[row-2][col] == ' ' and AIBoard[row+1][col] == ' ' and AIBoard[row+2][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row-1 >= 0 and row+3 <= 9:
                        if AIBoard[row-1][col] == ' ' and AIBoard[row+1][col] == ' ' and AIBoard[row+2][col] == ' ' and AIBoard[row+3][col] == ' ':
                            AIBoardHeatMap[row][col] += 1
                    if row+4 <= 9:
                        if AIBoard[row-1][col] == ' ' and AIBoard[row+2][col] == ' ' and AIBoard[row+3][col] == ' ' and AIBoard[row+4][col] == ' ':
                            AIBoardHeatMap[row][col] += 1

        maxVal = 0
        target = []
        for row in range(0, 10):
            for col in range(0, 10):
                if AIBoardHeatMap[row][col] > maxVal:
                    maxVal = AIBoardHeatMap[row][col]

        while True:
            target = (rand.randint(0, 9), rand.randint(0, 9))
            if AIBoardHeatMap[target[0]][target[1]] == maxVal:
                return target









def target(ships):
    global AIBoardHeatMap
    AIBoardHeatMap = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    #For each space
    for row in range(0, 10):
        for col in range(0, 10):

            if AIBoard[row][col] == 'X':
                if col-1 >= 0 and AIBoard[row][col-1] == ' ':
                    AIBoardHeatMap[row][col-1] += 1
                if col+1 <= 9 and AIBoard[row][col+1] == ' ':
                    AIBoardHeatMap[row][col+1] += 1
                if row-1 >= 0 and AIBoard[row-1][col] == ' ':
                    AIBoardHeatMap[row-1][col] += 1
                if row+1 <= 9 and AIBoard[row+1][col] == ' ':
                    AIBoardHeatMap[row+1][col] += 1

                if col-1 >= 0 and col+1 <= 9:
                    if AIBoard[row][col+1] == ' ':
                        AIBoardHeatMap[row][col+1] += 1
                    if AIBoard[row][col-1] == 'X':
                        AIBoardHeatMap[row][col+1] += 1
                    if AIBoard[row][col+1] == 'O' or AIBoard[row][col+1] == 'X':
                        AIBoardHeatMap[row][col+1] = 0

                if row-1 >= 0 and row+1 <= 9:
                    if AIBoard[row+1][col] == ' ':
                        AIBoardHeatMap[row+1][col] += 1
                    if AIBoard[row-1][col] == 'X':
                        AIBoardHeatMap[row+1][col] += 1
                    if AIBoard[row+1][col] == 'O' or AIBoard[row+1][col] == 'X':
                        AIBoardHeatMap[row+1][col] = 0

                if col+1 <= 9 and col-1 >= 0:
                    if AIBoard[row][col-1] == ' ':
                        AIBoardHeatMap[row][col-1] += 1
                    if AIBoard[row][col+1] == 'X':
                        AIBoardHeatMap[row][col-1] += 1
                    if AIBoard[row][col-1] == 'O' or AIBoard[row][col-1] == 'X':
                        AIBoardHeatMap[row][col-1] = 0

                if row+1 <= 9 and row-1 >= 0:
                    if AIBoard[row-1][col] == ' ':
                        AIBoardHeatMap[row-1][col] += 1
                    if AIBoard[row+1][col] == 'X':
                        AIBoardHeatMap[row-1][col] += 1
                    if AIBoard[row-1][col] == 'O' or AIBoard[row-1][col] == 'X':
                        AIBoardHeatMap[row-1][col] = 0

    maxVal = 0
    for row in range(0, 10):
        for col in range(0, 10):
            if AIBoardHeatMap[row][col] > maxVal:
                maxVal = AIBoardHeatMap[row][col]

    for row in range(0, 10):
        for col in range(0, 10):
            if AIBoardHeatMap[row][col] == maxVal:
                return (row, col)
