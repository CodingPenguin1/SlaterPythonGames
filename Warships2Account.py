#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#==============================================================================
# Title: Warships 2 Accounts
# Author: Ryan J. Slater
# Date: 5/31/2018
#==============================================================================

import platform
operatingSystem = platform.system()

import numpy as np
import AdvancedAI

class account():
    def __init__(self):
        self.username = ''

        self.onePlayerWins = 0
        self.onePlayerLosses = 0
        self.onePlayerGamesPlayed = 0
        self.onePlayerWinRatio = 0

        self.twoPlayerWins = 0
        self.twoPlayerLosses = 0
        self.twoPlayerGamesPlayed = 0
        self.twoPlayerWinRatio = 0

        self.totalWins = 0
        self.totalLosses = 0
        self.totalGamesPlayed = 0
        self.totalWinRatio = 0

        self.aioffset = np.zeros((10, 10))
        self.shipOffset = np.zeros((10, 10))

        self.human = humanPlayer(self.username)
        self.computer = computerPlayer(self.username, self.aioffset, self.shipOffset)

    def updateFromFile(self, accountName):
        '''
        Account file format:
        name
        onePlayerWins
        onePlayerLosses
        twoPlayerWins
        twoPlayerLosses
        '''
        if operatingSystem == 'Windows':
            file = open('.accounts\\' + accountName + '.txt', 'r')
        else:
            file = open('.accounts/' + accountName, 'r')
        name = file.readline()
        self.username = name[:len(name)-1]

        self.onePlayerWins = int(file.readline())
        self.onePlayerLosses = int(file.readline())
        self.onePlayerGamesPlayed = self.onePlayerWins + self.onePlayerLosses
        self.onePlayerWinRatio = 0
        if self.onePlayerGamesPlayed > 0:
            self.onePlayerWinRatio = int(100*self.onePlayerWins/self.onePlayerGamesPlayed)

        self.twoPlayerWins = int(file.readline())
        self.twoPlayerLosses = int(file.readline())
        self.twoPlayerGamesPlayed = self.twoPlayerWins + self.twoPlayerLosses
        self.twoPlayerWinRatio = 0
        if self.twoPlayerGamesPlayed > 0:
            self.twoPlayerWinRatio = int(100*self.twoPlayerWins/self.twoPlayerGamesPlayed)

        self.totalWins = self.onePlayerWins + self.twoPlayerWins
        self.totalLosses = self.onePlayerLosses + self.twoPlayerLosses
        self.totalGamesPlayed = self.onePlayerGamesPlayed + self.twoPlayerGamesPlayed
        self.totalWinRatio = 0
        if self.totalGamesPlayed > 0:
            self.totalWinRatio = int(100*(self.totalWins/self.totalGamesPlayed))

        for row in range(10):
            for col in range(10):
                self.aioffset[row][col] = int(float(file.readline()))
        for row in range(10):
            for col in range(10):
                self.shipOffset[row][col] = int(float(file.readline()))

        file.close()

        self.human = humanPlayer(self.username)
        self.computer = computerPlayer(self.username, self.aioffset, self.shipOffset)

    def updateOffset(self, board):
        for row in range(10):
            for col in range(10):
                if board[row][col] < 0 or board[row][col] > 1:
                    self.aioffset[row][col] += 1

    def toString(self):
        return ('Username: ' + self.username + '\n' +
        'One Player Wins: ' + str(self.onePlayerWins) + '\n' +
        'One Player Losses: ' + str(self.onePlayerLosses) + '\n' +
        'One Player Games Played: ' + str(self.onePlayerGamesPlayed) + '\n' +
        'One Player Win Ratio: ' + str(self.onePlayerWinRatio) + '\n' +

        'Two Player Wins: ' + str(self.twoPlayerWins) + '\n' +
        'Two Player Losses: ' + str(self.twoPlayerLosses) + '\n' +
        'Two Player Games Played: ' + str(self.twoPlayerGamesPlayed) + '\n' +
        'Two Player Win Ratio: ' + str(self.twoPlayerWinRatio) + '\n' +

        'Total Wins: ' + str(self.totalWins) + '\n' +
        'Total Losses: ' + str(self.totalLosses) + '\n' +
        'Total Games Played: ' + str(self.totalGamesPlayed) + '\n' +
        'Total Win Ratio: ' + str(self.totalWinRatio))

    def getProfileDisplay(self):
        return self.username + ' ' + str(self.totalWinRatio) + '%'

    def resetStatistics(self):
        f = open('.accounts\\' + self.username + '.txt', 'r') if operatingSystem == 'Windows' else open('.accounts/' + self.username, 'r')
        lines = f.readlines()
        f.close()
        for i in range(1, 5):
            lines[i] = str(0) + '\n'
        f = open('.accounts\\' + self.username + '.txt', 'w') if operatingSystem == 'Windows' else open('.accounts/' + self.username, 'w')
        f.writelines(lines)
        f.close()
        self.updateFromFile(self.username)

    def resetAI(self):
        f = open('.accounts\\' + self.username + '.txt', 'r') if operatingSystem == 'Windows' else open('.accounts/' + self.username, 'r')
        lines = f.readlines()
        f.close()
        print(len(lines))
        for i in range(5, 205):
            lines[i] = str(0) + '\n'
        f = open('.accounts\\' + self.username + '.txt', 'w') if operatingSystem == 'Windows' else open('.accounts/' + self.username, 'w')
        f.writelines(lines)
        f.close()
        self.updateFromFile(self.username)

    def win(self, opponent, shipBoard):
        self.updateOffset(shipBoard)
        print(self.aioffset)
        f = open('.accounts\\' + self.username + '.txt', 'r') if operatingSystem == 'Windows' else open('.accounts/' + self.username, 'r')
        lines = f.readlines()
        f.close()
        if opponent == 'c':
            lines[2-1] = str(self.onePlayerWins+1) + '\n'
        else:
            lines[4-1] = str(self.twoPlayerWins+1) + '\n'
        count = 0
        for row in range(10):
            for col in range(10):
                lines[5+count] = str(self.aioffset[row][col]) + '\n'
                count += 1
        for row in range(10):
            for col in range(10):
                lines[5+count] = str(self.shipOffset[row][col]) + '\n'
                count += 1
        f = open('.accounts\\' + self.username + '.txt', 'w') if operatingSystem == 'Windows' else open('.accounts/' + self.username, 'w')
        f.writelines(lines)
        f.close()
        self.updateFromFile(self.username)

    def lose(self, opponent, shipBoard):
        self.updateOffset(shipBoard)
        print(self.aioffset)
        f = open('.accounts\\' + self.username + '.txt', 'r') if operatingSystem == 'Windows' else open('.accounts/' + self.username, 'r')
        lines = f.readlines()
        if opponent == 'c':
            lines[3-1] = str(self.onePlayerLosses+1) + '\n'
        else:
            lines[5-1] = str(self.onePlayerLosses+1) + '\n'
        count = 0
        for row in range(10):
            for col in range(10):
                lines[5+count] = str(self.aioffset[row][col]) + '\n'
                count += 1
        for row in range(10):
            for col in range(10):
                lines[5+count] = str(self.shipOffset[row][col]) + '\n'
                count += 1
        f = open('.accounts\\' + self.username + '.txt', 'w') if operatingSystem == 'Windows' else open('.accounts/' + self.username, 'w')
        f.writelines(lines)
        f.close()
        self.updateFromFile(self.username)

class player():
    def __init__(self, name):
        self.name = name
        self.board = np.zeros((10, 10))

class humanPlayer():
    def __init__(self, username):
        player.__init__(self, username)

class computerPlayer():
    def __init__(self, username, aioffset, shipOffset):
        player.__init__(self, username + ' AI')
        self.offsetArray = aioffset
        self.AI = AdvancedAI.AdvancedAI(aioffset)
        self.shipOffset = shipOffset

    def move(self, board, turnCount):
        return self.AI.move(board, self.offsetArray, turnCount)

    def placeShips(self, board):
        return self.AI.placeShips(self.shipOffset)

