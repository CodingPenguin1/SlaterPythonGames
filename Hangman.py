#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Title: Hangman
# Author: Ryan J. Slater
# Date: Tue Aug 21 15:25:11 2018
# =============================================================================

import urllib.request
import requests
import random as rand

wordList = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain").content.splitlines()

for i in range(len(wordList)):
    wordList[i] = str(wordList[i])
    wordList[i] = wordList[i][2:len(wordList[i])-1]
    wordList[i] = wordList[i].lower()

i, stop = 0, len(wordList)
while i < stop:
    for j in range(len(wordList[i])):
        if wordList[i][j] not in 'abcdefghijklmnopqrstuvwxyz':
            wordList.pop(i)
            i -= 1
            stop = len(wordList)
            break
    i += 1

def getRandomWord(numPlayers, minWordLength, maxWordLength):
    while True:
        word = wordList[rand.randint(0, len(wordList))]
        if len(word) >= minWordLength and len(word) <= maxWordLength:
            return word

def printNoose(num):
    if num == 0:
        print('          ')
        print('          ')
        print('          ')
        print('          ')
        print('          ')
        print('          ')
        print('          ')
        print('          ')
        print('       _____')
    elif num == 1:
        print('          ')
        print('          ')
        print('          ')
        print('          ')
        print('          ')
        print('          ')
        print('          ')
        print('          ')
        print('       _/|\_')
    elif num == 2:
        print('          ')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('       _/|\_')
    elif num == 3:
        print('     ____')
        print('        \|')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('       _/|\_')
    elif num == 4:
        print('     ____')
        print('     |  \|')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('       _/|\_')
    elif num == 5:
        print('     ____')
        print('     |  \|')
        print('     O   |')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('       _/|\_')
    elif num == 6:
        print('     ____')
        print('     |  \|')
        print('     O   |')
        print('     |   |')
        print('         |')
        print('         |')
        print('         |')
        print('         |')
        print('       _/|\_')
    elif num == 7:
        print('     ____')
        print('     |  \|')
        print('     O   |')
        print('     |   |')
        print('     |   |')
        print('         |')
        print('         |')
        print('         |')
        print('       _/|\_')
    elif num == 8:
        print('     ____')
        print('     |  \|')
        print('     O   |')
        print('    /|   |')
        print('     |   |')
        print('         |')
        print('         |')
        print('         |')
        print('       _/|\_')
    elif num == 9:
        print('     ____')
        print('     |  \|')
        print('     O   |')
        print('    /|\  |')
        print('     |   |')
        print('         |')
        print('         |')
        print('         |')
        print('       _/|\_')
    elif num == 10:
        print('     ____')
        print('     |  \|')
        print('     O   |')
        print('    /|\  |')
        print('     |   |')
        print('    /    |')
        print('         |')
        print('         |')
        print('       _/|\_')
    elif num >= 11:
        print('     ____')
        print('     |  \|')
        print('     O   |')
        print('    /|\  |')
        print('     |   |')
        print('    / \  |')
        print('         |')
        print('         |')
        print('       _/|\_')


def checkWin(guesses, word):
    win = True
    for i in word:
        if i not in guesses:
            win = False
            break
    if win:
        return 'w'
    incorrectGuessCount = 0
    for i in guesses:
        if i not in word:
            incorrectGuessCount += 1
            if incorrectGuessCount == 11:
                return 'l'
    return ''

def printGuessedLetters(guesses, word):
    incorrectGuesses = []
    for letter in guesses:
        if letter not in word:
            incorrectGuesses.append(letter)
    incorrectGuesses.sort()

    print('Guessed letters: ', end='')
    if len(incorrectGuesses) > 0:
        for i in range(len(incorrectGuesses)):
            print(incorrectGuesses[i], end='')
            if i + 1 < len(incorrectGuesses):
                print(', ', end='')
    print('\n')

def define(search):
    definition = ''
    with urllib.request.urlopen('http://dictionary.reference.com/browse/' + str(search) + '?s=t') as response:
        html = response.read()
        html = str(html)
        for i in range(len(html)):
            if html[i:i+7] == 'content':
                for j in range(i, i+10000000):
                    if html[j] == '"':
                        for k in range(j+14+len(search), j+1000000):
                            if html[k] == '.':
                                break
                            if k == j+1:
                               definition = definition + html[k].upper()
                            else:
                                definition = definition + html[k]
                        break
                break
    return definition

def Hangman():
    print(500*'\n')
    numPlayers = input('How many players? ').lower()
    while True:
        if numPlayers in ['one', 'two', '1', '2']:
            break
        else:
            numPlayers = input('How many players? ').lower()
    if numPlayers == 'one' or numPlayers == '1':
        numPlayers = 1
    else:
        numPlayers = 2

    minWordLength, maxWordLength = 4, 8

    changeLengths = input('Change min and max word lengths? (current: 4, 8) [y/N] ').lower()
    if 'y' in changeLengths:
        changeLengths = True
    else:
        changeLengths = False

    if changeLengths:
        while True:
            minWordLength = input('Min word length (0 < x < 11): ')
            try:
                minWordLength = int(float(minWordLength))
                if minWordLength > 0 and minWordLength < 11:
                    break
                else:
                    print('Enter an integer between 1 and 10')
            except:
                print('Enter an integer between 1 and 10')

        while True:
            maxWordLength = input('Max word length (x > ' + str(minWordLength) + '): ')
            try:
                maxWordLength = int(float(maxWordLength))
                if maxWordLength > minWordLength:
                    break
                else:
                    print('Enter an integer > ' + str(minWordLength))
            except:
                print('Enter an integer > ' + str(minWordLength))

    word = ''
    if numPlayers == 1:
        word = getRandomWord(numPlayers, minWordLength, maxWordLength)
    else:
        pass

    guesses = []
    incorrectGuessCount = 0
    while incorrectGuessCount < 11:
        print(500*'\n')
        printNoose(incorrectGuessCount)

        printGuessedLetters(guesses, word)

        for i in word:
            if i in guesses:
                print(i, end=' ')
            else:
                print('', end='_ ')
        print()

        while True:
            guess = input('Guess a letter: ').lower()
            if guess in 'abcdefghijklmnopqrstuvwxyz' and guess not in guesses and len(guess) == 1:
                guesses.append(guess)
                guesses.sort()
                break
            else:
                if guess not in 'abcdefghijklmnopqrstuvwxyz' or len(guess) > 1:
                    print('Enter a letter')
                elif guess in guesses:
                    print('You\'ve already guessed that letter!')
        if guess not in word:
            incorrectGuessCount += 1

        if checkWin(guesses, word) == 'w':
            print('\nYou win')
            break
        elif checkWin(guesses, word) == 'l':
            print('\nYou lose')
            break

    print(500*'\n')
    printNoose(11)
    print('The word was: ' + word)
    try:
        print('Definition: ' + define(word))
    except:
        print('Unable to find definition')




if __name__ == '__main__':
    Hangman()
