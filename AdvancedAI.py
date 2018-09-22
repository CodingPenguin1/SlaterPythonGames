#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#==============================================================================
# Title: Advanced AI
# Author: Ryan J. Slater
# Date: 6/4/2018
#==============================================================================

import random as rand
import numpy as np

class AdvancedAI():
    def __init__(self, board):
        self.board = board
        self.mode = 'search'

    def updateMode(self):
        for row in range(0, 10):
            for col in range(0, 10):
                if self.board[row][col] == 2:
                    self.mode = 'target'
                    return 0
        self.mode = 'search'

    def mapValue(self, value, oldMin, oldMax, newMin, newMax):
        oldRange = oldMax - oldMin
        oldRange = oldRange + 1 if oldRange == 0 else oldRange
        newRange = newMax - newMin
        return (((value-oldMin) * newRange) / oldRange) + newMin

    def placeShips(self, frequencyMap):
        print('Ship offset: ')
        print(frequencyMap)
        probabilityMap = np.array([[10, 15, 19, 21, 22, 22, 21, 19, 15, 10],
                                   [15, 20, 24, 26, 27, 27, 26, 24, 20, 15],
                                   [19, 24, 28, 30, 31, 31, 30, 28, 24, 19],
                                   [21, 26, 30, 32, 33, 33, 32, 30, 26, 21],
                                   [22, 27, 31, 33, 34, 34, 33, 31, 27, 22],
                                   [22, 27, 31, 33, 34, 34, 33, 31, 27, 22],
                                   [21, 26, 30, 32, 33, 33, 32, 30, 26, 21],
                                   [19, 24, 28, 30, 31, 31, 30, 28, 24, 19],
                                   [15, 20, 24, 26, 27, 27, 26, 24, 20, 15],
                                   [10, 15, 19, 21, 22, 22, 21, 19, 15, 10]])
        for row in range(10):
            for col in range(10):
                probabilityMap[row][col] += rand.randint(0, 10)

        print('Probability Map:')
        print(probabilityMap)

        for row in range(10):
            for col in range(10):
                freq = self.mapValue(frequencyMap[row][col], 0, np.max(frequencyMap), 0, 34)
                probabilityMap[row][col] = int(((probabilityMap[row][col])**2 + (freq)**2)**0.5)

        print('Biased Probability Map:')
        print(probabilityMap)

        originalProbabilityMap = np.copy(probabilityMap)

        ships = []
        for length in [5, 4, 3, 3, 2]:
            bestLoc = (0, 0)
            bestDirection = 0
            bestMapValue = 0
            probabilityMap = np.copy(originalProbabilityMap)
            for row in range(10):
                for col in range(10):
                    for direction in range(2):
                        probabilityMap = np.copy(originalProbabilityMap)
                        validLoc = True
                        if probabilityMap[row][col] == -1:
                            validLoc = False
                        if validLoc:
                            if direction == 0:
                                if row+length-1 < 10:
                                    for i in range(length):
                                        if probabilityMap[row+i][col] == -1:
                                            validLoc = False
                                            break
                                    if validLoc:
                                        for i in range(length):
                                            probabilityMap[row+i][col] = -1
                                else:
                                    validLoc = False
                            else:
                                if col+length-1 < 10:
                                    for i in range(length):
                                        if probabilityMap[row][col+i] == -1:
                                            validLoc = False
                                            break
                                    if validLoc:
                                        for i in range(length):
                                            probabilityMap[row][col+i] = -1
                                else:
                                    validLoc = False

                        if np.sum(probabilityMap) > bestMapValue and validLoc:
                            bestMapValue = np.sum(probabilityMap)
                            bestLoc = (row, col)
                            bestDirection = direction

            ships.append((bestLoc[0], bestLoc[1], bestDirection))
            if bestDirection == 0:
                for i in range(length):
                    originalProbabilityMap[bestLoc[0]+i][bestLoc[1]] = -1
            else:
                for i in range(length):
                    originalProbabilityMap[bestLoc[0]][bestLoc[1]+i] = -1
#        ships array (row, col, direction)
        # direction 0 is vertical
        return ships

    def move(self, newBoard, offset, turnCount):
        self.board = newBoard
        probabilityMap = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

        self.updateMode()
        if self.mode == 'search':

            # Method:
            # 0 - Probability map + noise
            # 1 - Random shot
            # 2 - Random corner
            # 3 - Probability map

            method = 3
            randomProb = 25
            if turnCount > 50:
                randomProb = 0
            if rand.randint(1, 100) <= randomProb:
                method = 1
                if rand.randint(1, 100) <= 65:
                    method = 0
            elif rand.randint(1, 100) <= 10:
                method = 2

            # Probability map + noise (add noise then do standard probability map method)
            if method == 0:
                print('Map + Noise')
                shipCount = 0
                if -5 in self.board:
                    shipCount += 1
                if -4 in self.board:
                    shipCount += 1
                if -3 in self.board:
                    shipCount += 1
                if -2 in self.board:
                    shipCount += 1
                if -1 in self.board:
                    shipCount += 1
                for row in range(0, 10):
                    for col in range(0, 10):
                        probabilityMap[row][col] = rand.randint(0, shipCount)
                method = 3

            # Random shot
            if method == 1:
                print('Random')
                while True:
                    shot = (rand.randint(0, 9), rand.randint(0, 9))
                    if self.board[shot[0]][shot[1]] <= 0:
                        return shot

            # Random corner
            if method == 2:
                print('Corner')
                c0 = True if self.board[0][0] <= 0 else False
                c1 = True if self.board[0][9] <= 0 else False
                c2 = True if self.board[9][0] <= 0 else False
                c3 = True if self.board[9][9] <= 0 else False

                shot = (0, 0)
                if c0 or c1 or c2 or c3:
                    while True:
                        corner = rand.randint(0, 3)
                        if corner == 0 and c0:
                            return ((0, 0))
                        elif corner == 1 and c1:
                            return ((0, 9))
                        elif corner == 2 and c2:
                            return ((9, 0))
                        elif corner == 3 and c3:
                            return ((9, 9))
                    return shot
                else:
                    method = 3

            # Probability map
            if method == 3:
                print('Map')
                shipLengths = []
                if -1 in self.board:
                    shipLengths.append(2)
                if -2 in self.board:
                    shipLengths.append(3)
                if -3 in self.board:
                    shipLengths.append(3)
                if -4 in self.board:
                    shipLengths.append(4)
                if -5 in self.board:
                    shipLengths.append(5)
                for row in range(0, 10):
                    for col in range(0, 10):

                        #Destroyer Check
                        if -1 in self.board and self.board[row][col] <= 0:
                            if col-1 >= 0:
                                if self.board[row][col-1] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-1 >= 0:
                                if self.board[row-1][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if col+1 <= 9:
                                if self.board[row][col+1] <= 0:
                                    probabilityMap[row][col] += 1
                            if row+1 <= 9:
                                if self.board[row+1][col] <= 0:
                                    probabilityMap[row][col] += 1

                        #Sub Check
                        if -2 in self.board and self.board[row][col] <= 0:
                            if col-1 >= 0 and col+1 <= 9:
                                if self.board[row][col-1] <= 0 and self.board[row][col+1] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-1 >= 0 and row+1 <= 9:
                                if self.board[row-1][col] <= 0 and self.board[row+1][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if col-2 >= 0:
                                if self.board[row][col-2] <= 0 and self.board[row][col-1] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-2 >= 0:
                                if self.board[row-2][col] <= 0 and self.board[row-1][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if col+2 <= 9:
                                if self.board[row][col+2] <= 0 and self.board[row][col+1] <= 0:
                                    probabilityMap[row][col] += 1
                            if row+2 <= 9:
                                if self.board[row+2][col] <= 0 and self.board[row+1][col] <= 0:
                                    probabilityMap[row][col] += 1

                        #Cruiser Check
                        if -3 in self.board and self.board[row][col] <= 0:
                            if col-1 >= 0 and col+1 <= 9:
                                if self.board[row][col-1] <= 0 and self.board[row][col+1] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-1 >= 0 and row+1 <= 9:
                                if self.board[row-1][col] <= 0 and self.board[row+1][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if col-2 >= 0:
                                if self.board[row][col-2] <= 0 and self.board[row][col-1] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-2 >= 0:
                                if self.board[row-2][col] <= 0 and self.board[row-1][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if col+2 <= 9:
                                if self.board[row][col+2] <= 0 and self.board[row][col+1] <= 0:
                                    probabilityMap[row][col] += 1
                            if row+2 <= 9:
                                if self.board[row+2][col] <= 0 and self.board[row+1][col] <= 0:
                                    probabilityMap[row][col] += 1

                        #Battleship Check
                        if -4 in self.board and self.board[row][col] <= 0:
                            if col-3 >= 0:
                                if self.board[row][col-1] <= 0 and self.board[row][col-2] <= 0 and self.board[row][col-3] <= 0:
                                    probabilityMap[row][col] += 1
                            if col-2 >= 0 and col+1 <= 9:
                                if self.board[row][col-1] <= 0 and self.board[row][col-2] <= 0 and self.board[row][col+1] <= 0:
                                    probabilityMap[row][col] += 1
                            if col-1 >= 0 and col+2 <= 9:
                                if self.board[row][col-1] <= 0 and self.board[row][col+1] <= 0 and self.board[row][col+2] <= 0:
                                    probabilityMap[row][col] += 1
                            if col+3 <= 9:
                                if self.board[row][col+1] <= 0 and self.board[row][col+2] <= 0 and self.board[row][col+3] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-3 >= 0:
                                if self.board[row-1][col] <= 0 and self.board[row-2][col] <= 0 and self.board[row-3][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-2 >= 0 and row+1 <= 9:
                                if self.board[row-1][col] <= 0 and self.board[row-2][col] <= 0 and self.board[row+1][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-1 >= 0 and row+2 <= 9:
                                if self.board[row-1][col] <= 0 and self.board[row+1][col] <= 0 and self.board[row+2][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if row+3 <= 9:
                                if self.board[row+1][col] <= 0 and self.board[row+2][col] <= 0 and self.board[row+3][col] <= 0:
                                    probabilityMap[row][col] += 1

                        #Carrier Check
                        if -5 in self.board and self.board[row][col] <= 0:
                            if col-4 >= 0:
                                if self.board[row][col-1] <= 0 and self.board[row][col-2] <= 0 and self.board[row][col-3] <= 0 and self.board[row][col-4] <= 0:
                                    probabilityMap[row][col] += 1
                            if col-3 >= 0 and col+1 <= 9:
                                if self.board[row][col-1] <= 0 and self.board[row][col-2] <= 0 and self.board[row][col-3] <= 0 and self.board[row][col+1] <= 0:
                                    probabilityMap[row][col] += 1
                            if col-2 >= 0 and col+2 <= 9:
                                if self.board[row][col-1] <= 0 and self.board[row][col-2] <= 0 and self.board[row][col+1] <= 0 and self.board[row][col+2] <= 0:
                                    probabilityMap[row][col] += 1
                            if col-1 >= 0 and col+3 <= 9:
                                if self.board[row][col-1] <= 0 and self.board[row][col+1] <= 0 and self.board[row][col+2] <= 0 and self.board[row][col+3] <= 0:
                                    probabilityMap[row][col] += 1
                            if col+4 <= 9:
                                if self.board[row][col+1] <= 0 and self.board[row][col+2] <= 0 and self.board[row][col+3] <= 0 and self.board[row][col+4] <= 0:
                                    probabilityMap[row][col] += 1

                            if row-4 >= 0:
                                if self.board[row-1][col] <= 0 and self.board[row-2][col] <= 0 and self.board[row-3][col] <= 0 and self.board[row-4][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-3 >= 0 and row+1 <= 9:
                                if self.board[row-1][col] <= 0 and self.board[row-2][col] <= 0 and self.board[row-3][col] <= 0 and self.board[row-1][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-2 >= 0 and row+2 <= 9:
                                if self.board[row-1][col] <= 0 and self.board[row-2][col] <= 0 and self.board[row+1][col] <= 0 and self.board[row+2][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if row-1 >= 0 and row+3 <= 9:
                                if self.board[row-1][col] <= 0 and self.board[row+1][col] <= 0 and self.board[row+2][col] <= 0 and self.board[row+3][col] <= 0:
                                    probabilityMap[row][col] += 1
                            if row+4 <= 9:
                                if self.board[row-1][col] <= 0 and self.board[row+2][col] <= 0 and self.board[row+3][col] <= 0 and self.board[row+4][col] <= 0:
                                    probabilityMap[row][col] += 1

            print('\nBefore Offset:')
            print(probabilityMap)

            oldMin = np.amin(offset)
            oldMax = np.amax(offset)
            newMax = int((np.amax(probabilityMap/2) + turnCount/2) / 6)

            for row in range(10):
                for col in range(10):
                    offset[row][col] = self.mapValue(offset[row][col], oldMin, oldMax, 0, newMax)

            print('\nOffset Mapped(' + str(oldMin) + ', ' + str(oldMax) + ', 0, ' + str(newMax) + '):')
            print(offset)
            includeOffset = True
            gamePercentComplete = (turnCount/50) + 0.5
            if gamePercentComplete > 1:
                gamePercentComplete = 1
            print(gamePercentComplete)
            if includeOffset:
                for row in range(10):
                    for col in range(10):
                        if probabilityMap[row][col] != 0:
#                            probabilityMap[row][col] = ((probabilityMap[row][col] + offset[row][col]) / 2)
                            if gamePercentComplete != 1:
                                probabilityMap[row][col] = int( (gamePercentComplete*probabilityMap[row][col] + (1-gamePercentComplete)*offset[row][col]) / 2 )
            print('\nAfter Offset:')
            print(probabilityMap)
            print('\n\n\n')


            maxVal = 0
            target = []
            for row in range(0, 10):
                for col in range(0, 10):
                    if probabilityMap[row][col] > maxVal:
                        maxVal = probabilityMap[row][col]

            while True:
                target = (rand.randint(0, 9), rand.randint(0, 9))
                if probabilityMap[target[0]][target[1]] == maxVal:
                    return target

        else:
            print('Target')
            shipLengths = []
            if -1 in self.board:
                shipLengths.append(2)
            if -2 in self.board:
                shipLengths.append(3)
            if -3 in self.board:
                shipLengths.append(3)
            if -4 in self.board:
                shipLengths.append(4)
            if -5 in self.board:
                shipLengths.append(5)

            for row in range(0, 10):
                for col in range(0, 10):

                    if self.board[row][col] == 2:
                        if col-1 >= 0 and self.board[row][col-1] <= 0:
                            probabilityMap[row][col-1] += 1
                        if col+1 <= 9 and self.board[row][col+1] <= 0:
                            probabilityMap[row][col+1] += 1
                        if row-1 >= 0 and self.board[row-1][col] <= 0:
                            probabilityMap[row-1][col] += 1
                        if row+1 <= 9 and self.board[row+1][col] <= 0:
                            probabilityMap[row+1][col] += 1

                        if col-1 >= 0 and col+1 <= 9:
                            if self.board[row][col+1] <= 0:
                                probabilityMap[row][col+1] += 1
                            if self.board[row][col-1] == 2:
                                probabilityMap[row][col+1] += 1
                            if self.board[row][col+1] == 1 or self.board[row][col+1] == 2:
                                probabilityMap[row][col+1] = 0

                        if row-1 >= 0 and row+1 <= 9:
                            if self.board[row+1][col] <= 0:
                                probabilityMap[row+1][col] += 1
                            if self.board[row-1][col] == 2:
                                probabilityMap[row+1][col] += 1
                            if self.board[row+1][col] == 1 or self.board[row+1][col] == 2:
                                probabilityMap[row+1][col] = 0

                        if col+1 <= 9 and col-1 >= 0:
                            if self.board[row][col-1] <= 0:
                                probabilityMap[row][col-1] += 1
                            if self.board[row][col+1] == 2:
                                probabilityMap[row][col-1] += 1
                            if self.board[row][col-1] == 1 or self.board[row][col-1] == 2:
                                probabilityMap[row][col-1] = 0

                        if row+1 <= 9 and row-1 >= 0:
                            if self.board[row-1][col] <= 0:
                                probabilityMap[row-1][col] += 1
                            if self.board[row+1][col] == 2:
                                probabilityMap[row-1][col] += 1
                            if self.board[row-1][col] == 1 or self.board[row-1][col] == 2:
                                probabilityMap[row-1][col] = 0

            maxVal = 0
            for row in range(0, 10):
                for col in range(0, 10):
                    if probabilityMap[row][col] > maxVal:
                        maxVal = probabilityMap[row][col]

            for row in range(0, 10):
                for col in range(0, 10):
                    if probabilityMap[row][col] == maxVal:
                        return (row, col)