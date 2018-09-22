#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#==============================================================================
# Title: 2048
# Author: Ryan J Slater
# Date: 12/25/2017
#==============================================================================

import pygame
import random as rand
import numpy as np

class __colors__():
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (200,0,0)
    GREEN = (0,200,0)
    BLUE = (0, 0, 200)
    BRIGHTRED = (255,0,0)
    BRIGHTGREEN = (0,255,0)
    BRIGHTBLUE = (0, 0, 255)
    BOARD = (187, 173, 160)

    def __getTileColor__(number):
        if number == 0:
            return((248, 238, 228,))
        elif number == 2:
            return((238, 228, 218))
        elif number == 4:
            return((237, 224, 200))
        elif number == 8:
            return((242, 177, 121))
        elif number == 16:
            return((245, 149, 99))
        elif number == 32:
            return((246, 124, 95))
        elif number == 64:
            return((246, 94, 59))
        elif number == 128:
            return((237, 207, 114))
        elif number == 256:
            return((237, 204, 97))
        elif number == 512:
            return((237, 200, 80))
        elif number == 1024:
            return((237, 197, 63))
        elif number == 2048:
            return((237, 194, 46))
        else:
            if number >= 131072:
                return((0, 0, 0))
            val = 4096
            color = 50
            while True:
                if number == val:
                    return((color, color, color))
                else:
                    color -= 10
                    val *= 2

    def __getTileTextColor__(number):
        if number >= 8:
            return((249, 246, 242))
        return((119, 110, 101))

def __text_objects__(text, font):
    textSurface = font.render(text, True, __colors__.BLACK)
    return textSurface, textSurface.get_rect()

def __tileText__(text, font, val):
    textSurface = font.render(text, True, __colors__.__getTileTextColor__(val))
    return textSurface, textSurface.get_rect()

def __button__(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == play:
                play(displayWidth, displayHeight)
            elif action == __optionMenu__:
                __optionMenu__()
            else:
                action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    text = pygame.font.SysFont('comicsansms', __button__TextSize)
    textSurf, textRect = __text_objects__(msg, text)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)

def __unpause__():
    global pause
    pause = False

def __paused__():
    text = pygame.font.SysFont('comicsansms', __titleTextSize__)
    TextSurf, TextRect = __text_objects__('Paused', text)
    TextRect.center = ((displayWidth/2), (displayHeight/2))
    gameDisplay.blit(TextSurf, TextRect)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                __quitGame__()
        __button__('CONTINUE', int(displayWidth/2-(125/640)*displayWidth), int((3/4)*displayHeight), int((12/64)*displayWidth), int((5/48)*displayHeight), __colors__.GREEN, __colors__.BRIGHTGREEN, __unpause__)
        __button__('MAIN MENU', int((displayWidth/2)+(5/640)*displayWidth), int((3/4)*displayHeight), int((13/64)*displayWidth), int((5/48)*displayHeight), __colors__.RED, __colors__.BRIGHTRED, play)
        pygame.display.update()
        clock.tick(60)

def __quitGame__():
    pygame.quit()
    quit()


#==================================================================================================================


def __gameIntro__():
    gameDisplay.fill(__colors__.WHITE)
    largeText = pygame.font.SysFont('comicsansms', __titleTextSize__)
    smallText = pygame.font.SysFont('comicsansms', __button__TextSize)
    TextSurf, TextRect = __text_objects__('2048', largeText)
    TextRect.center = (int(displayWidth/2), int(displayHeight/2))
    gameDisplay.blit(TextSurf, TextRect)
    TextSurf, TextRect = __text_objects__('Ryan J Slater', smallText)
    TextRect.center = ((displayWidth/2), (displayHeight/2)+int((4/48)*displayHeight))
    gameDisplay.blit(TextSurf, TextRect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                __quitGame__()
        __button__('PLAY', int((displayWidth/2)-(165/640)*displayWidth), int((3/4)*displayHeight), int((10/64)*displayWidth), int((5/48)*displayHeight), __colors__.GREEN, __colors__.BRIGHTGREEN, __gameLoop__)
        __button__('OPTIONS', int((displayWidth/2)-(55/640)*displayWidth), int((3/4)*displayHeight), int((11/64)*displayWidth), int((5/48)*displayHeight), __colors__.BLUE, __colors__.BRIGHTBLUE, __optionMenu__)
        __button__('QUIT', int((displayWidth/2)+(65/640)*displayWidth), int((3/4)*displayHeight), int((10/64)*displayWidth), int((5/48)*displayHeight), __colors__.RED, __colors__.BRIGHTRED, __quitGame__)

        pygame.display.update()
        clock.tick(60)

def __changeRes1__():
    global displayWidth
    global displayHeight
    global __button__TextSize
    global __titleTextSize__
    __titleTextSize__ = 77
    __button__TextSize = 20
    displayWidth = 480
    displayHeight = 320
    play(displayWidth, displayHeight)

def __changeRes2__():
    global displayWidth
    global displayHeight
    global __button__TextSize
    global __titleTextSize__
    __titleTextSize__ = 115
    __button__TextSize = 30
    displayWidth = 640
    displayHeight = 480
    play(displayWidth, displayHeight)

def __changeRes3__():
    global displayWidth
    global displayHeight
    global __button__TextSize
    global __titleTextSize__
    __titleTextSize__ = 144
    __button__TextSize = 38
    displayWidth = 1024
    displayHeight = 600
    play(displayWidth, displayHeight)

def __changeRes4__():
    global displayWidth
    global displayHeight
    global __button__TextSize
    global __titleTextSize__
    __titleTextSize__ = 216
    __button__TextSize = 56
    displayWidth = 1200
    displayHeight = 900
    play(displayWidth, displayHeight)

def __changeRes5__():
    global displayWidth
    global displayHeight
    global __button__TextSize
    global __titleTextSize__
    __titleTextSize__ = 259
    __button__TextSize = 68
    displayWidth = 1920
    displayHeight = 1080
    play(displayWidth, displayHeight)

def __optionMenu__():
    # Graphics Options:
        # Color Scheme
        # Display Resolution
    global displayWidth
    global displayHeight
    gameDisplay.fill(__colors__.WHITE)
    text = pygame.font.SysFont('comicsansms', __titleTextSize__)
    TextSurf, TextRect = __text_objects__('Options', text)
    TextRect.center = ((displayWidth/2), int((5/48)*displayHeight))
    gameDisplay.blit(TextSurf, TextRect)

    text = pygame.font.SysFont('comicsansms', __button__TextSize)
    TextSurf, TextRect = __text_objects__('Resolution', text)
    TextRect.center = (int(displayWidth/3), int((11/48)*displayHeight))
    gameDisplay.blit(TextSurf, TextRect)
    TextSurf, TextRect = __text_objects__('Color Scheme', text)
    TextRect.center = (int(2*displayWidth/3), int((11/48)*displayHeight))
    gameDisplay.blit(TextSurf, TextRect)

    text = pygame.font.SysFont('comicsansms', int(__button__TextSize/2))
    TextSurf, TextRect = __text_objects__(str(displayWidth) + 'x' + str(displayHeight), text)
    TextRect.center = (int(displayWidth/3), int((125/480)*displayHeight))
    gameDisplay.blit(TextSurf, TextRect)

    __button__Width = int((11/48)*displayWidth)
    __button__Height =  int((5/48)*displayHeight)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                __quitGame__()
        __button__('BACK', int((1/48)*displayWidth), int((1/48)*displayHeight), __button__Width, __button__Height, __colors__.RED, __colors__.BRIGHTRED, play)
        __button__('480x320', int((displayWidth/3)-(__button__Width/2)), int((135/480)*displayHeight), __button__Width, __button__Height, __colors__.BLUE, __colors__.BRIGHTBLUE, __changeRes1__)
        __button__('640x480', int((displayWidth/3)-(__button__Width/2)), int((195/480)*displayHeight), __button__Width, __button__Height, __colors__.BLUE, __colors__.BRIGHTBLUE, __changeRes2__)
        __button__('1024x600', int((displayWidth/3)-(__button__Width/2)), int((255/480)*displayHeight), __button__Width, __button__Height, __colors__.BLUE, __colors__.BRIGHTBLUE, __changeRes3__)
        __button__('1200x900', int((displayWidth/3)-(__button__Width/2)), int((315/480)*displayHeight), __button__Width, __button__Height, __colors__.BLUE, __colors__.BRIGHTBLUE, __changeRes4__)
        __button__('1920x1080', int((displayWidth/3)-(__button__Width/2)), int((375/480)*displayHeight), __button__Width, __button__Height, __colors__.BLUE, __colors__.BRIGHTBLUE, __changeRes5__)
        pygame.display.update()
        clock.tick(60)

def __getInitialBoard__():
    board = np.zeros((4, 4), dtype=int)
    coord = (rand.randint(0, 3), rand.randint(0, 3))
    if rand.randint(0, 100) > 10:
        board[coord] = 2
    else:
        board[coord] = 4
    while True:
        coord2 = (rand.randint(0, 3), rand.randint(0, 3))
        if coord2 != coord:
            board[coord2] = 2
            if rand.randint(0, 100) < 10 and board[coord] != 4:
                board[coord2] = 4
            return board

def __checkLoss__(board):
    zeros = 0
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                zeros += 1
            else:
                if row > 0:
                    if board[row][col] == board[row-1][col]:
                        return False
                if row < 3:
                    if board[row][col] == board[row+1][col]:
                        return False
                if col > 0:
                    if board[row][col] == board[row][col-1]:
                        return False
                if col < 3:
                    if board[row][col] == board[row][col+1]:
                        return False
    if zeros > 0:
        return False
    return True

def __drawTile__(row, col, w, h, origin, val):
    text = [pygame.font.SysFont('comicsansms', int((3/2)*__button__TextSize)), pygame.font.SysFont('comicsansms', int((7/6)*__button__TextSize)), pygame.font.SysFont('comicsansms', int((5/6)*__button__TextSize))]
    pygame.draw.rect(gameDisplay, __colors__.__getTileColor__(val), (origin[0]+col*(w+10), origin[1]+row*(h+10), w, h))
    if val < 1000:
        text = text[0]
    elif val < 10000:
        text = text[1]
    elif val < 100000:
        text = text[2]
    if val != 0:
        TextSurf, TextRect = __tileText__(str(val), text, val)
        TextRect.center = ((origin[0]+col*(w+10)+int(w/2), origin[1]+row*(h+10)+int(h/2)))
        gameDisplay.blit(TextSurf, TextRect)

def __drawBoard__(board, dw, dh):
    gameDisplay.fill(__colors__.WHITE)
    tileWidth, tileHeight = int(dh/5), int(dh/5)
    if dw < dh:
        tileWidth, tileHeight = int(dw/5), int(dw/5)

    origin = (int(dw/2)-2*tileHeight-15, int(dh/2)-2*tileWidth-15)
    pygame.draw.rect(gameDisplay, __colors__.BOARD, (origin[0]-10, origin[1]-10, 4*tileWidth+50, 4*tileHeight+50))
    for row in range(4):
        for col in range(4):
            __drawTile__(row, col, tileWidth, tileHeight, origin, board[row][col])

def __gameLoss__():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                __quitGame__()
        largeText = pygame.font.SysFont('comicsansms', __titleTextSize__)
        TextSurf, TextRect = __text_objects__('You Lose', largeText)
        TextRect.center = ((displayWidth/2), (displayHeight/2))
        gameDisplay.blit(TextSurf, TextRect)
        gameDisplay.blit(TextSurf, TextRect)
        __button__('PLAY AGAIN', int((displayWidth/2)-(135/640)*displayWidth), int((3/4)*displayHeight), int((13/64)*displayWidth), int((5/48)*displayHeight), __colors__.GREEN, __colors__.BRIGHTGREEN, __gameLoop__)
        __button__('QUIT', int((displayWidth/2)+(5/640)*displayWidth), int((3/4)*displayHeight), int((10/64)*displayWidth), int((5/48)*displayHeight), __colors__.RED, __colors__.BRIGHTRED, __quitGame__)
        pygame.display.update()
        clock.tick(60)

def __moveRow__(row, direction):
    if direction == 'left' or direction == 'up':
        for i in range(len(row)):
            if row[i] != 0:
                if i > 0:
                    moveto = 0
                    for j in range(i-1, -1, -1):
                        if row[j] != 0:
                            moveto = j
                            break
                    if row[moveto] != 0:
                        if row[moveto] != row[i]:
                            moveto += 1
                    if moveto != i:
                        row[moveto] += row[i]
                        row[i] = 0
                else:
                    i += 1
    else:
        for i in range(len(row)-1, -1, -1):
            if row[i] != 0:
                if i < len(row)-1:
                    moveto = len(row)-1
                    for j in range(i+1, len(row)):
                        if row[j] != 0:
                            moveto = j
                            break
                    if row[moveto] != 0:
                        if row[moveto] != row[i]:
                            moveto -= 1
                    if moveto != i:
                        row[moveto] += row[i]
                        row[i] = 0
                else:
                    i -= 1
    return row

def __shift__(board, direction):
    origBoard = np.copy(board)
    if direction == 'left' or direction == 'right':
        for row in range(4):
            tmprow = np.array([0, 0, 0, 0])
            for col in range(4):
                tmprow[col] = board[row][col]
            tmprow = __moveRow__(tmprow, direction)
            for i in range(len(tmprow)):
                board[row][i] = tmprow[i]

    elif direction == 'up' or direction == 'down':
        for col in range(4):
            tmpcol = np.array([0, 0, 0, 0])
            for row in range(4):
                tmpcol[row] = board[row][col]
            tmpcol = __moveRow__(tmpcol, direction)
            for i in range(len(tmpcol)):
                board[i][col] = tmpcol[i]

    if np.array_equal(origBoard, board):
        return(board)

    while True:
        coord = (rand.randint(0, 3), rand.randint(0, 3))
        if board[coord] == 0:
            if rand.randint(0, 100) > 10:
                board[coord] = 2
            else:
                board[coord] = 4
            return(board)

def __gameLoop__():
    global pause
    board = __getInitialBoard__()

    while True:
        if __checkLoss__(board):
            __gameLoss__()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                __quitGame__()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    board = __shift__(board, 'left')
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    board = __shift__(board, 'right')
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    board = __shift__(board, 'down')
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    board = __shift__(board, 'up')
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    pause = True
                    __paused__()
        __drawBoard__(board, displayWidth, displayHeight)
        pygame.display.update()
        clock.tick(60)

def play(dw=640, dh=480):
    global displayWidth
    global displayHeight
    global pause
    global gameDisplay
    global clock
    global options

    pygame.init()
    displayWidth = dw
    displayHeight = dh
    pause = False
    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption('2048')
    clock = pygame.time.Clock()

    __gameIntro__()
    __gameLoop__()
    __quitGame__()

def TwentyFortyEight():
    global __titleTextSize__
    global __button__TextSize
    __titleTextSize__ = 115
    __button__TextSize = 30
    play()

if __name__ == '__main__':
    TwentyFortyEight()