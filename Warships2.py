#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#==============================================================================
# Title: Warships 2
# Author: Ryan J. Slater
# Date: 5/31/2018
#==============================================================================

import platform
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))
operatingSystem = platform.system()

import Warships2Account as Account
import pygame
import numpy as np
import pygame.locals as pl
import time

class colors():
    '''
    Saves constant tuple (RED, GREEN, BLUE) values for colors
    '''
    BLACK = (0,0,0)
    LIGHTGRAY = (100, 100, 100)
    DARKGRAY = (50, 50, 50)
    WHITE = (255,255,255)
    RED = (200,0,0)
    GREEN = (0,200,0)
    BLUE = (0, 0, 200)
    ORANGE = (255, 100, 0)
    PURPLE = (102, 0, 51)
    PINK = (255, 0, 102)
    BROWN = (139, 69, 19)
    BRIGHTRED = (255,0,0)
    BRIGHTGREEN = (0,255,0)
    BRIGHTBLUE = (0, 0, 255)
    SKY = (135, 206, 250)

def text_objects(text, font, color=colors.BLACK):
    '''
    Takes text, font, and optional color and returns textSurface and textSurface.get_rect(), required for displaying text in pygame
    Usage: textSurf, textRect = text_objects(text, font)

    Parameters
    ----------
    text : String
        The text to be displayed
    font : pygame.font.SysFont
        text = pygame.font.SysFont('FONTNAME', FONTSIZE), FONTNAME : String, FONTSIZE : int
    color : colors.COLOR (OPTIONAL)
        Get a color from the colors class. Default = colors.BLACK (0, 0, 0)

    Returns
    ----------
    textSurface : pygame-rendered text
        font.render(text, True, color)
    rect : textSurface.get_rect()

    Usage
    ----------
    textSurf, textRect = text_objects(text, font)
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)
    '''
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, display, action=None, textSize = 30, textColor=colors.BLACK):
    '''
    Displays a colored button with text

    Parameters
    ----------
    msg : String
        The text to be displayed
    x : int
        x-coordinate in pixels of the top left corner of the button
    y : int
        y-coordinate in pixels of the top left corner of the button
    w : int
        Width of the button in pixels
    h : int
        Height of the button in pixels
    ic : colors.COLOR
        Inactive color of the button
    ac : colors.COLOR
        Active color of the button
    display : pygame.Surface
        Pygame display for the button to be displayed on
    action : function
        Action to be performed by pressing the button
        Default = None
    textSize : int
        Font size
        Default = 30
    '''
    pygame.font.init()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, ac, (x, y, w, h))
        text = pygame.font.SysFont('couriernew', textSize)
        textSurf, textRect = text_objects(msg, text, textColor)
        textRect.center = ((x+(w/2)), (y+(h/2)))
        display.blit(textSurf, textRect)
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(display, ic, (x, y, w, h))
        text = pygame.font.SysFont('couriernew', textSize)
        textSurf, textRect = text_objects(msg, text, textColor)
        textRect.center = ((x+(w/2)), (y+(h/2)))
        display.blit(textSurf, textRect)

def buttonImage(x, y, w, h, ic, ac, display, action=None):
    '''
    Displays a colored button with text

    Parameters
    ----------
    x : int
        x-coordinate in pixels of the top left corner of the button
    y : int
        y-coordinate in pixels of the top left corner of the button
    w : int
        Width of the button in pixels
    h : int
        Height of the button in pixels
    ic : pygame.image.load(FILEPATH)
        Inactive image of the button
    ac : pygame.image.load(FILEPATH)
        Active image of the button
    display : pygame.Surface
        Pygame display for the button to be displayed on
    action : function
        Action to be performed by pressing the button
        Default = None
    '''
    pygame.font.init()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        display.blit(ac, (x, y))
        if click[0] == 1 and action != None:
            action()
    else:
        display.blit(ic, (x, y))

class TextInput:
    """
    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(self, font_family = "",
                        font_size = 35,
                        antialias=True,
                        text_color=(0, 0, 0),
                        cursor_color=(0, 0, 1),
                        repeat_keys_initial_ms=400,
                        repeat_keys_interval_ms=35):
        """
        Args:
            font_family: Name or path of the font that should be used. Default is pygame-font
            font_size: Size of the font in pixels
            antialias: (bool) Determines if antialias is used on fonts or not
            text_color: Color of the text
            repeat_keys_initial_ms: ms until the keydowns get repeated when a key is not released
            repeat_keys_interval_ms: ms between to keydown-repeats if key is not released
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.input_string = "" # Inputted text
        if not os.path.isfile(font_family): font_family = pygame.font.match_font(font_family)
        self.font_object = pygame.font.SysFont('couriernew', font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {} # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size/20+1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = 0 # Inside text
        self.cursor_visible = True # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500 # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True # So the user sees where he writes

                # If none exist, create counter for that key:
                if not event.key in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:
                    self.input_string = self.input_string[:max(self.cursor_position - 1, 0)] + \
                                        self.input_string[self.cursor_position:]

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pl.K_DELETE:
                    self.input_string = self.input_string[:self.cursor_position] + \
                                        self.input_string[self.cursor_position + 1:]

                elif event.key == pl.K_RETURN:
                    return True

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                else:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = self.input_string[:self.cursor_position] + \
                                        event.unicode + \
                                        self.input_string[self.cursor_position:]
                    self.cursor_position += len(event.unicode) # Some are empty, e.g. K_UP

            elif event.type == pl.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters :
            self.keyrepeat_counters[key][0] += self.clock.get_time() # Update clock
            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = self.keyrepeat_intial_interval_ms - \
                                                    self.keyrepeat_interval_ms

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

        # Rerender text surface:
        self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string=""

def firstRunSetup():
    '''
    If first launch, create .account directory and prompt the user to create an account

    Returns
    ----------
    firstTime : boolean
        True if initial setup was performed AND first account was created
    '''
    files = [f for f in os.listdir(os.getcwd())]
    if '.accounts' not in files:
        os.mkdir('.accounts')
        if createNewAccount(True):
            return True
    return False

def getAllAccountNames():
    print('Getting all account names')
    accts = []
    if operatingSystem == 'Windows':
        print('Windows')
        for i in os.listdir('.accounts\\'):
            accts.append(i)
        i = 0
        stop = len(accts)
        while i < stop:
            if accts[i][len(accounts[i])-4:] != '.txt':
                accts.pop(i)
                i -= 1
                stop = len(accts)
            else:
                accts[i] = accts[i][:len(accts[i])-4]
            i += 1
        return accts
    else:
        for i in os.listdir('.accounts/'):
            accts.append(i)
        i = 0
        stop = len(accts)
        while i < stop:
            if accts[i][len(accts[i])-4:] == '.txt':
                accts.pop(i)
                i -= 1
                stop = len(accts)
            i += 1
        return accts

def getAllAccounts():
    print('Getting all accounts')
    accts = []
    accountNames = getAllAccountNames()
    for i in accountNames:
        a = Account.account()
        if operatingSystem == 'Windows':
            a.updateFromFile(i)
        else:
            a.updateFromFile(i)
        accts.append(a)
    return accts

def createNewAccount(isFirstTime=False):
    '''
    Creates account creation window
    '''
    global creatingUsername
    global displayWidth
    global displayHeight
    global gameDisplay
    global accounts

    print('New account creation menu')
    pygame.init()
    displayWidth = 1000
    displayHeight = 600
    creatingAccountWindow = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption('Create New Account')
    textinput = TextInput()
    printErrorMessage = False
    breakWhileLoop = False
    createAccount = False
    accountNames = getAllAccountNames()
    while True:
        creatingAccountWindow.fill(colors.WHITE)
        text = pygame.font.SysFont('couriernew', 35)
        smallText = pygame.font.SysFont('couriernew', 15)
        TextSurf, TextRect = text_objects('Create account username:', text, colors.BLACK)
        TextRect.center = (displayWidth/2, displayHeight/2)
        creatingAccountWindow.blit(TextSurf, TextRect)

        if printErrorMessage:
            TextSurf, TextRect = text_objects('Username cannot contain spaces', text, colors.RED)
            TextRect.center = (displayWidth/2, displayHeight/2+85)
            creatingAccountWindow.blit(TextSurf, TextRect)
            TextSurf, TextRect = text_objects('or be longer than 20 characters', text, colors.RED)
            TextRect.center = (displayWidth/2, displayHeight/2+110)
            creatingAccountWindow.blit(TextSurf, TextRect)
            TextSurf, TextRect = text_objects('or reuse an existing username', text, colors.RED)
            TextRect.center = (displayWidth/2, displayHeight/2+135)
            creatingAccountWindow.blit(TextSurf, TextRect)
        if not isFirstTime:
            button('Cancel', 0, 575, 75, 25, colors.RED, colors.BRIGHTRED, gameDisplay, mainMenu, 15)
        if len(accounts) > 0:
            TextSurf, TextRect = text_objects('ACCOUNTS:', smallText)
            TextRect.center = (displayWidth/10, 12)
            creatingAccountWindow.blit(TextSurf, TextRect)
            for i in range(len(accounts)):
                TextSurf, TextRect = text_objects(accounts[i].username, smallText)
                TextRect.center = (displayWidth/10, 24+12*i)
                creatingAccountWindow.blit(TextSurf, TextRect)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                # In case window is closed
                if isFirstTime:
                    os.rmdir('.accounts')
                    pygame.quit()
                    breakWhileLoop = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    creatingUsername = textinput.get_text()
                    if len(creatingUsername) <= 20 and ' ' not in creatingUsername and creatingUsername not in accountNames:
                        createAccount = True
                        pygame.quit()
                        breakWhileLoop = True
                    else:
                        printErrorMessage = True

        if breakWhileLoop:
            break
        textinput.update(events)
        creatingAccountWindow.blit(textinput.get_surface(), (displayWidth/3, displayHeight/2+35))
        pygame.display.update()
        clock.tick(60)

    if createAccount:
        print('Creating account file: ' + creatingUsername)

        if operatingSystem == 'Windows':
            file = open('.accounts\\' + creatingUsername + '.txt', 'w+')
        else:
            file = open('.accounts/' + creatingUsername, 'w+')
        file.write(creatingUsername)
        for i in range(204):
            file.write('\n' + str(0))
        file.close()

        accounts = getAllAccounts()
        for i in accounts:
            i.updateFromFile(i.username)
            if isFirstTime or loggedIn == None:
                if i.username == creatingUsername:
                    login(i)

    pygame.display.set_caption('Warships 2')
    displayWidth = 1000
    displayHeight = 600
    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))

def login(account=None, playAfterLogin=False):
    '''
    Logs in an account object by setting loggedIn = account

    Parameters
    ----------
    account: Warships2Account.account
        Account to be logged in
    '''
    global loggedIn
    print('Login menu')

    if account != None and loggedIn == None:
        loggedIn = account
        print('\nSuccessfully logged in:\n')
        print(account.username)
        print('\n\n')
        return 0

    if len(accounts) == 0:
        mainMenu()

    # ask for name of account and list accounts
    pygame.display.set_caption('Login')
    displayWidth = 1000
    displayHeight = 600
    loginWindow = pygame.display.set_mode((displayWidth, displayHeight))
    printErrorMessage = False
    breakWhileLoop = False
    textinput = TextInput()

    print('Logged in:', end=' ')
    if loggedIn != None:
        print(loggedIn.username)
    else:
        print('None')

    while True:
        loginWindow.fill(colors.WHITE)
        largeText = pygame.font.SysFont('couriernew', 35)
        smallText = pygame.font.SysFont('couriernew', 15)
        TextSurf, TextRect = text_objects('Enter username to log in:', largeText)
        TextRect.center = (displayWidth/2, displayHeight/2)
        loginWindow.blit(TextSurf, TextRect)

        if loggedIn != None:
            TextSurf, TextRect = text_objects('Logged in: ' + loggedIn.username, smallText)
            TextRect.center = (displayWidth/2, 12)
            loginWindow.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects('ACCOUNTS:', smallText)
        TextRect.center = (displayWidth/10, 12)
        loginWindow.blit(TextSurf, TextRect)
        for i in range(len(accounts)):
            TextSurf, TextRect = text_objects(accounts[i].username, smallText)
            TextRect.center = (displayWidth/10, 24+12*i)
            loginWindow.blit(TextSurf, TextRect)

        if printErrorMessage:
            TextSurf, TextRect = text_objects('Ensure you are not already logged in', largeText, colors.RED)
            TextRect.center = (displayWidth/2, displayHeight/2+85)
            loginWindow.blit(TextSurf, TextRect)
            TextSurf, TextRect = text_objects('and that the spelling is correct', largeText, colors.RED)
            TextRect.center = (displayWidth/2, displayHeight/2+115)
            loginWindow.blit(TextSurf, TextRect)

        button('Cancel', 0, 575, 75, 25, colors.RED, colors.BRIGHTRED, gameDisplay, mainMenu, 15)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                    pygame.quit()
                    breakWhileLoop = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if checkValidUsernameLogin(textinput.get_text()):
                        account = textinput.get_text()
                        breakWhileLoop = True
                    else:
                        printErrorMessage = True

        if breakWhileLoop:
            break
        textinput.update(events)
        loginWindow.blit(textinput.get_surface(), (displayWidth/3, displayHeight/2+35))
        pygame.display.update()
        clock.tick(60)

    for i in accounts:
        if i.username == account:
            account = i
            break
    loggedIn = account
    print('Successfully logged in ' + account.username)
    if playAfterLogin:
        play()
    else:
        mainMenu()

def checkValidUsernameLogin(username):
    global loggedIn
    print('Checking login username validity')

    if username in getAllAccountNames():
        if loggedIn == None or username != loggedIn.username:
            return True
        return False
    return False

def getSecondPlayer():
    global secondPlayer
    global loggedIn
    global gameDisplay
    global accounts
    print('Get second player menu')

    pygame.font.init()
    printErrorMessage = False
    breakWhileLoop = False
    textinput = TextInput()
    account = None

    while True:
        gameDisplay.fill(colors.WHITE)
        largeText = pygame.font.SysFont('couriernew', 35)
        smallText = pygame.font.SysFont('couriernew', 15)
        TextSurf, TextRect = text_objects('Enter the second player\'s username:', largeText)
        TextRect.center = (displayWidth/2, displayHeight/2)
        gameDisplay.blit(TextSurf, TextRect)

        if loggedIn != None:
            TextSurf, TextRect = text_objects('Logged in: ' + loggedIn.username, smallText)
            TextRect.center = (displayWidth/2, 12)
            gameDisplay.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects('ACCOUNTS:', smallText)
        TextRect.center = (displayWidth/10, 12)
        gameDisplay.blit(TextSurf, TextRect)
        for i in range(len(accounts)):
            TextSurf, TextRect = text_objects(accounts[i].username, smallText)
            TextRect.center = (displayWidth/10, 24+12*i)
            gameDisplay.blit(TextSurf, TextRect)

        if printErrorMessage:
            TextSurf, TextRect = text_objects('Ensure you are not already logged in', largeText, colors.RED)
            TextRect.center = (displayWidth/2, displayHeight/2+85)
            gameDisplay.blit(TextSurf, TextRect)
            TextSurf, TextRect = text_objects('and that the spelling is correct', largeText, colors.RED)
            TextRect.center = (displayWidth/2, displayHeight/2+115)
            gameDisplay.blit(TextSurf, TextRect)

        button('Cancel', 0, 575, 75, 25, colors.RED, colors.BRIGHTRED, gameDisplay, mainMenu, 15)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                    pygame.quit()
                    breakWhileLoop = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if checkValidUsernameLogin(textinput.get_text()):
                        account = textinput.get_text()
                        breakWhileLoop = True
                    else:
                        printErrorMessage = True

        if breakWhileLoop:
            break
        textinput.update(events)
        gameDisplay.blit(textinput.get_surface(), (displayWidth/3, displayHeight/2+35))
        pygame.display.update()
        clock.tick(60)
    for i in accounts:
        if i.username == account:
            return i

def editProfile():
    global loggedIn
    global gameDisplay
    print('Edit profile menu')
    pygame.font.init()
    largeText = pygame.font.SysFont('couriernew', 35)
    smallText = pygame.font.SysFont('couriernew', 15)
    while True:
        gameDisplay.fill(colors.WHITE)
        TextSurf, TextRect = text_objects(loggedIn.username, largeText)
        TextRect.center = (displayWidth/2, displayHeight/4)
        gameDisplay.blit(TextSurf, TextRect)

        # Titles
        TextSurf, TextRect = text_objects('ONE-PLAYER', smallText)
        TextRect.center = (3*displayWidth/7, displayHeight/3)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects('TWO-PLAYER', smallText)
        TextRect.center = (4*displayWidth/7, displayHeight/3)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects('TOTAL', smallText)
        TextRect.center = (5*displayWidth/7, displayHeight/3)
        gameDisplay.blit(TextSurf, TextRect)

        # Wins
        TextSurf, TextRect = text_objects('     WINS:', smallText)
        TextRect.center = (2*displayWidth/7, displayHeight/3+20)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.onePlayerWins), smallText)
        TextRect.center = (3*displayWidth/7, displayHeight/3+20)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.twoPlayerWins), smallText)
        TextRect.center = (4*displayWidth/7, displayHeight/3+20)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.totalWins), smallText)
        TextRect.center = (5*displayWidth/7, displayHeight/3+20)
        gameDisplay.blit(TextSurf, TextRect)

        # Losses
        TextSurf, TextRect = text_objects('   LOSSES:', smallText)
        TextRect.center = (2*displayWidth/7, displayHeight/3+40)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.onePlayerLosses), smallText)
        TextRect.center = (3*displayWidth/7, displayHeight/3+40)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.twoPlayerLosses), smallText)
        TextRect.center = (4*displayWidth/7, displayHeight/3+40)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.totalLosses), smallText)
        TextRect.center = (5*displayWidth/7, displayHeight/3+40)
        gameDisplay.blit(TextSurf, TextRect)

        # Games Played
        TextSurf, TextRect = text_objects('    GAMES:', smallText)
        TextRect.center = (2*displayWidth/7, displayHeight/3+60)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.onePlayerGamesPlayed), smallText)
        TextRect.center = (3*displayWidth/7, displayHeight/3+60)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.twoPlayerGamesPlayed), smallText)
        TextRect.center = (4*displayWidth/7, displayHeight/3+60)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.totalGamesPlayed), smallText)
        TextRect.center = (5*displayWidth/7, displayHeight/3+60)
        gameDisplay.blit(TextSurf, TextRect)

        # Win Ratio
        TextSurf, TextRect = text_objects('WIN RATIO:', smallText)
        TextRect.center = (2*displayWidth/7, displayHeight/3+80)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.onePlayerWinRatio) + '%', smallText)
        TextRect.center = (3*displayWidth/7, displayHeight/3+80)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.twoPlayerWinRatio) + '%', smallText)
        TextRect.center = (4*displayWidth/7, displayHeight/3+80)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(loggedIn.totalWinRatio) + '%', smallText)
        TextRect.center = (5*displayWidth/7, displayHeight/3+80)
        gameDisplay.blit(TextSurf, TextRect)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        mainMenu()

        button('Reset Statistics', displayWidth/2-75, displayHeight/3+120, 150, 25, colors.RED, colors.BRIGHTRED, gameDisplay, resetStatistics, 15)
        button('Reset AI Development', displayWidth/2-95, displayHeight/3+150, 190, 25, colors.RED, colors.BRIGHTRED, gameDisplay, resetAI, 15)
        button('Delete Account', displayWidth/2-75, displayHeight/3+180, 150, 25, colors.RED, colors.BRIGHTRED, gameDisplay, deleteAccount, 15)
        button('Back', 0, 575, 50, 25, colors.RED, colors.BRIGHTRED, gameDisplay, mainMenu, 15)
        pygame.display.update()
        clock.tick(60)

def resetStatistics():
    loggedIn.resetStatistics()

def resetAI():
    loggedIn.resetAI()

def deleteAccount():
    global gameDisplay
    global accounts
    global loggedIn
    print('Deleting account menu')

    pygame.init()
    displayWidth = 1000
    displayHeight = 600
    creatingAccountWindow = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption('Delete Account Confirmation')
    textinput = TextInput()
    printErrorMessage = False
    breakWhileLoop = False
    deleteAccount = False
    while True:
        creatingAccountWindow.fill(colors.WHITE)
        largeText = pygame.font.SysFont('couriernew', 35)
        smallText = pygame.font.SysFont('couriernew', 15)
        TextSurf, TextRect = text_objects('Enter username to confirm:', largeText, colors.BLACK)
        TextRect.center = (displayWidth/2, displayHeight/2)
        creatingAccountWindow.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects('Logged in: ' + loggedIn.username, smallText)
        TextRect.center = (displayWidth/2, 12)
        gameDisplay.blit(TextSurf, TextRect)

        if printErrorMessage:
            TextSurf, TextRect = text_objects('Usernames do not match!', largeText, colors.RED)
            TextRect.center = (displayWidth/2, displayHeight/2+85)
            creatingAccountWindow.blit(TextSurf, TextRect)

        button('Cancel', 0, 575, 75, 25, colors.RED, colors.BRIGHTRED, gameDisplay, editProfile, 15)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if loggedIn.username == textinput.get_text():
                        deleteAccount = True
                        breakWhileLoop = True
                    else:
                        printErrorMessage = True

        if breakWhileLoop:
            break
        textinput.update(events)
        gameDisplay.blit(textinput.get_surface(), (displayWidth/3, displayHeight/2+35))
        pygame.display.update()
        clock.tick(60)

    if deleteAccount:
        print('Deleting account file: ' + loggedIn.username)
        if operatingSystem == 'Windows':
            os.remove('.accounts\\' + loggedIn.username + '.txt')
        else:
            os.remove('.accounts/' + loggedIn.username)
        loggedIn = None
    mainMenu()

def quitGame():
    print('Closing game')
    pygame.quit()
    quit()

def settingsMenu():
    global loggedIn
    global gameDisplay
    print('Settings menu')
    pygame.font.init()
    largeText = pygame.font.SysFont('couriernew', 35)
    smallText = pygame.font.SysFont('couriernew', 15)
    pygame.display.set_caption('Settings')
    while True:
        gameDisplay.fill(colors.WHITE)
        TextSurf, TextRect = text_objects('SETTINGS', largeText)
        TextRect.center = (displayWidth/2, displayHeight/4)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects('Created by', smallText)
        TextRect.center = (displayWidth/2, displayHeight/3)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects('Ryan J. Slater', smallText)
        TextRect.center = (displayWidth/2, displayHeight/3+25)
        gameDisplay.blit(TextSurf, TextRect)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainMenu()

        button('Quit Game', displayWidth/2-50, 3*displayHeight/4, 100, 25, colors.RED, colors.BRIGHTRED, gameDisplay, quitGame, 15)
        button('Back', 0, 575, 50, 25, colors.RED, colors.BRIGHTRED, gameDisplay, mainMenu, 15)
        pygame.display.update()
        clock.tick(60)

def play():
    global displayWidth
    global displayHeight
    global gameDisplay
    global accounts
    global pause
    print('Game starting')

    if loggedIn == None:
        login(None, True)

    accounts = getAllAccounts()
    pygame.display.set_caption('Warships 2')

    pygame.font.init()
    textinput = TextInput()
    breakWhileLoop = False
    twoPlayer = False
    while True:
        gameDisplay.fill(colors.WHITE)
        largeText = pygame.font.SysFont('couriernew', 35)
        smallText = pygame.font.SysFont('couriernew', 15)
        TextSurf, TextRect = text_objects('Enter number of players:', largeText)
        TextRect.center = (displayWidth/2, displayHeight/2)
        gameDisplay.blit(TextSurf, TextRect)

        button('Main Menu', 0, 575, 100, 25, colors.RED, colors.BRIGHTRED, gameDisplay, mainMenu, 15)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if textinput.get_text().lower() in ['1', 'one']:
                        breakWhileLoop = True
                    elif textinput.get_text().lower() in ['2', 'two'] and len(accounts) > 1:
                        twoPlayer = True
                        breakWhileLoop = True

        if breakWhileLoop:
            break
        textinput.update(events)
        gameDisplay.blit(textinput.get_surface(), (displayWidth/3, displayHeight/2+35))
        pygame.display.update()
        clock.tick(60)

    p1 = loggedIn.human
    p1acct = loggedIn
    p2 = None
    p2acct = None
    if twoPlayer:
        p2acct = getSecondPlayer()
        p2 = p2acct.human
    else:
        p2 = loggedIn.computer

    # Place ships
    p1.board = placeShips(p1.name, 0)
#    -5 = carrier
#    -4 = battleship
#    -3 = cruiser
#    -2 = submarine
#    -1 = destroyer
#    0 = empty
#    1 = miss
#    2 = hit
#    3 = sunk ship
    p2.board = placeShips(p2.name, 1) if twoPlayer else placeShips(p2.name, 1, True)

    p1BoardCopy = np.copy(p1.board)
    p2BoardCopy = np.copy(p2.board)

    print('\nPlaying:')
    print('Player 1: ' + p1.name)
    print('Player 2: ' + p2.name)

    largeText = pygame.font.SysFont('couriernew', 35)
    smallText = pygame.font.SysFont('couriernew', 15)
    gameOver = False
    turn = -1
    reticleImg = pygame.image.load('icons\\reticle.png') if operatingSystem == 'Windows' else pygame.image.load('icons/reticle.png')
    reticleLoc = (4, 4)
    turnEnded = False
    mouseBoardCoords = np.array([[(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)]], dtype=object)
    for row in range(10):
        for col in range(10):
            mouseBoardCoords[row][col] = (200+60*row, 260+60*row, 60*col, 60+60*col)
    turnCount = 0

    p1Fleet = []
    p2Fleet = []

    while True:
        pygame.mouse.set_visible(False)
        gameDisplay.fill(colors.WHITE)

        # Display Player Names
        # TODO: make colors based on who's turn it is
        p1Col = colors.RED if turn == -1 else colors.BLACK
        p2Col = colors.RED if turn == 1 else colors.BLACK
        TextSurf, TextRect = text_objects(p1.name, smallText, p1Col)
        TextRect.center = (int(10*len(p1.name)/2), 12)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(p2.name, smallText, p2Col)
        TextRect.center = (995-int(10*len(p2.name)/2), 12)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(str(turnCount+1), smallText, colors.BLACK)
        TextRect.center = (int(10*len(p1.name))+15, 12)
        gameDisplay.blit(TextSurf, TextRect)

        # Display Ships
        pygame.draw.rect(gameDisplay, colors.BLACK, (0, 100, 200, 250))
        pygame.draw.rect(gameDisplay, colors.BLACK, (800, 100, 200, 250))
        iconDir = 'icons/'
        if operatingSystem == 'Windows':
            iconDir = 'icons\\'
        if -5 in p1Fleet:
            gameDisplay.blit(pygame.image.load(iconDir + 'carrierOutline.png'), (0, 100))
        if -4 in p1Fleet:
            gameDisplay.blit(pygame.image.load(iconDir + 'battleshipOutline.png'), (0, 150))
        if -3 in p1Fleet:
            gameDisplay.blit(pygame.image.load(iconDir + 'cruiserOutline.png'), (0, 200))
        if -2 in p1Fleet:
            gameDisplay.blit(pygame.image.load(iconDir + 'submarineOutline.png'), (0, 250))
        if -1 in p1Fleet:
            gameDisplay.blit(pygame.image.load(iconDir + 'destroyerOutline.png'), (0, 300))
        if -5 in p2Fleet:
            gameDisplay.blit(pygame.image.load(iconDir + 'carrierOutline.png'), (800, 100))
        if -4 in p2Fleet:
            gameDisplay.blit(pygame.image.load(iconDir + 'battleshipOutline.png'), (800, 150))
        if -3 in p2Fleet:
            gameDisplay.blit(pygame.image.load(iconDir + 'cruiserOutline.png'), (800, 200))
        if -2 in p2Fleet:
            gameDisplay.blit(pygame.image.load(iconDir + 'submarineOutline.png'), (800, 250))
        if -1 in p2Fleet:
            gameDisplay.blit(pygame.image.load(iconDir + 'destroyerOutline.png'), (800, 300))

        # Display Board
        for row in range(10):
            for col in range(10):
                pygame.draw.rect(gameDisplay, colors.BRIGHTBLUE, (200+60*col, 60*row, 60, 60))
                pygame.draw.rect(gameDisplay, colors.BLUE, (201+60*col, 1+60*row, 59, 59))
                if turn == -1:
                    if p2.board[row][col] == 1:
                        pygame.draw.circle(gameDisplay, colors.WHITE, (230+60*col, 30+60*row), 20)
                    if p2.board[row][col] == 2:
                        pygame.draw.rect(gameDisplay, colors.DARKGRAY, (201+60*col, 1+60*row, 59, 59))
                        pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                    if p2.board[row][col] == 3:
                        pygame.draw.rect(gameDisplay, colors.BLACK, (201+60*col, 1+60*row, 59, 59))
                        pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                else:
                    if p1.board[row][col] == 1:
                        pygame.draw.circle(gameDisplay, colors.WHITE, (230+60*col, 30+60*row), 20)
                    if p1.board[row][col] == 2:
                        pygame.draw.rect(gameDisplay, colors.DARKGRAY, (201+60*col, 1+60*row, 59, 59))
                        pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                    if p1.board[row][col] == 3:
                        pygame.draw.rect(gameDisplay, colors.BLACK, (201+60*col, 1+60*row, 59, 59))
                        pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)

        # Reticle
        gameDisplay.blit(reticleImg, (201+60*reticleLoc[1], 1+60*reticleLoc[0]))

        # AI move
        if not twoPlayer and turn == 1:
            reticleLoc = p2.move(p1.board, turnCount)
            if p1.board[reticleLoc[0]][reticleLoc[1]] == 0:
                p1.board[reticleLoc[0]][reticleLoc[1]] = 1
                turnEnded = True
            elif p1.board[reticleLoc[0]][reticleLoc[1]] < 0:
                p1.board[reticleLoc[0]][reticleLoc[1]] = 2
                turnEnded = True
                shipHit = p1BoardCopy[reticleLoc[0]][reticleLoc[1]]
                shipSunk = True
                for row in range(10):
                    for col in range(10):
                        if p1.board[row][col] == shipHit:
                            shipSunk = False
                            break
                    if not shipSunk:
                        break
                if shipSunk:
                    for row in range(10):
                        for col in range(10):
                            if p1BoardCopy[row][col] == shipHit:
                                p1.board[row][col] = 3

        if turnEnded:
            if not twoPlayer and turn == 1:
                turn *= -1
                for row in range(10):
                    for col in range(10):
                        pygame.draw.rect(gameDisplay, colors.BRIGHTBLUE, (200+60*col, 60*row, 60, 60))
                        pygame.draw.rect(gameDisplay, colors.BLUE, (201+60*col, 1+60*row, 59, 59))
                        if p1.board[row][col] == 1:
                            pygame.draw.circle(gameDisplay, colors.WHITE, (230+60*col, 30+60*row), 20)
                        if p1.board[row][col] == 2:
                            pygame.draw.rect(gameDisplay, colors.DARKGRAY, (201+60*col, 1+60*row, 59, 59))
                            pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                        if p1.board[row][col] == 3:
                            pygame.draw.rect(gameDisplay, colors.BLACK, (201+60*col, 1+60*row, 59, 59))
                            pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                pygame.display.update()
                time.sleep(3)
                turnEnded = False
            else:
                for row in range(10):
                    for col in range(10):
                        pygame.draw.rect(gameDisplay, colors.BRIGHTBLUE, (200+60*col, 60*row, 60, 60))
                        pygame.draw.rect(gameDisplay, colors.BLUE, (201+60*col, 1+60*row, 59, 59))
                        if turn == -1:
                            if p2.board[row][col] == 1:
                                pygame.draw.circle(gameDisplay, colors.WHITE, (230+60*col, 30+60*row), 20)
                            if p2.board[row][col] == 2:
                                pygame.draw.rect(gameDisplay, colors.DARKGRAY, (201+60*col, 1+60*row, 59, 59))
                                pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                            if p2.board[row][col] == 3:
                                pygame.draw.rect(gameDisplay, colors.BLACK, (201+60*col, 1+60*row, 59, 59))
                                pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                        else:
                            if p1.board[row][col] == 1:
                                pygame.draw.circle(gameDisplay, colors.WHITE, (230+60*col, 30+60*row), 20)
                            if p1.board[row][col] == 2:
                                pygame.draw.rect(gameDisplay, colors.DARKGRAY, (201+60*col, 1+60*row, 59, 59))
                                pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                            if p1.board[row][col] == 3:
                                pygame.draw.rect(gameDisplay, colors.BLACK, (201+60*col, 1+60*row, 59, 59))
                                pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                pygame.display.update()
                time.sleep(3)
                turn *= -1
                turnEnded = False
            if turn == 1:
                turnCount += 1

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    paused()

        # Reticle control with mouse
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for row in range(10):
            for col in range(10):
                if mouse[0] > mouseBoardCoords[row][col][0] and mouse[0] < mouseBoardCoords[row][col][1] and mouse[1] > mouseBoardCoords[row][col][2] and mouse[1] < mouseBoardCoords[row][col][3]:
                    reticleLoc = (col, row)

                    # Update Display after click-moving reticle
                    for row in range(10):
                        for col in range(10):
                            pygame.draw.rect(gameDisplay, colors.BRIGHTBLUE, (200+60*col, 60*row, 60, 60))
                            pygame.draw.rect(gameDisplay, colors.BLUE, (201+60*col, 1+60*row, 59, 59))
                            if turn == -1:
                                if p2.board[row][col] == 1:
                                    pygame.draw.circle(gameDisplay, colors.WHITE, (230+60*col, 30+60*row), 20)
                                if p2.board[row][col] == 2:
                                    pygame.draw.rect(gameDisplay, colors.DARKGRAY, (201+60*col, 1+60*row, 59, 59))
                                    pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                                if p2.board[row][col] == 3:
                                    pygame.draw.rect(gameDisplay, colors.BLACK, (201+60*col, 1+60*row, 59, 59))
                                    pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                            else:
                                if p1.board[row][col] == 1:
                                    pygame.draw.circle(gameDisplay, colors.WHITE, (230+60*col, 30+60*row), 20)
                                if p1.board[row][col] == 2:
                                    pygame.draw.rect(gameDisplay, colors.DARKGRAY, (201+60*col, 1+60*row, 59, 59))
                                    pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                                if p1.board[row][col] == 3:
                                    pygame.draw.rect(gameDisplay, colors.BLACK, (201+60*col, 1+60*row, 59, 59))
                                    pygame.draw.circle(gameDisplay, colors.RED, (230+60*col, 30+60*row), 20)
                    gameDisplay.blit(reticleImg, (201+60*reticleLoc[1], 1+60*reticleLoc[0]))
                    pygame.display.update()

                    if click[0] == 1 and not turnEnded:
                        if turn == -1:
                            if p2.board[reticleLoc[0]][reticleLoc[1]] == 0:
                                p2.board[reticleLoc[0]][reticleLoc[1]] = 1
                                turnEnded = True
                            elif p2.board[reticleLoc[0]][reticleLoc[1]] < 0:
                                p2.board[reticleLoc[0]][reticleLoc[1]] = 2
                                turnEnded = True
                                shipHit = p2BoardCopy[reticleLoc[0]][reticleLoc[1]]
                                shipSunk = True
                                for row in range(10):
                                    for col in range(10):
                                        if p2.board[row][col] == shipHit:
                                            shipSunk = False
                                            break
                                    if not shipSunk:
                                        break
                                if shipSunk:
                                    for row in range(10):
                                        for col in range(10):
                                            if p2BoardCopy[row][col] == shipHit:
                                                p2.board[row][col] = 3
                            if not twoPlayer:
                                loggedIn.shipOffset[reticleLoc[0]][reticleLoc[1]] += 1
                        else:
                            if p1.board[reticleLoc[0]][reticleLoc[1]] == 0:
                                p1.board[reticleLoc[0]][reticleLoc[1]] = 1
                                turnEnded = True
                            elif p1.board[reticleLoc[0]][reticleLoc[1]] < 0:
                                p1.board[reticleLoc[0]][reticleLoc[1]] = 2
                                turnEnded = True
                                shipHit = p1BoardCopy[reticleLoc[0]][reticleLoc[1]]
                                shipSunk = True
                                for row in range(10):
                                    for col in range(10):
                                        if p1.board[row][col] == shipHit:
                                            shipSunk = False
                                            break
                                    if not shipSunk:
                                        break
                                if shipSunk:
                                    for row in range(10):
                                        for col in range(10):
                                            if p1BoardCopy[row][col] == shipHit:
                                                p1.board[row][col] = 3

        p1Fleet = getShipsLeft(p1.board)
        p2Fleet = getShipsLeft(p2.board)
        if len(p1Fleet) == 0:
            winner = 2
            gameOver = True
        elif len(p2Fleet) == 0:
            winner = 1
            gameOver = True

        if gameOver:
            break
        pygame.display.update()
        clock.tick(60)

    time.sleep(2)
    if winner == 1:
        print(p1.name + ' wins')
        if p2acct == None:
            p1acct.win('c', p1.board)
        else:
            p1acct.win('h', p1.board)
            p2acct.lose('h', p2.board)
    elif winner == 2:
        print(p2.name + ' wins')
        if p2acct == None:
            p1acct.lose('c', p1.board)
        else:
            p1acct.lose('h', p1.board)
            p2acct.win('h', p2.board)

    pygame.mouse.set_visible(True)
    print('Winner screen')
    pygame.font.init()
    largeText = pygame.font.SysFont('couriernew', 35)
    smallText = pygame.font.SysFont('couriernew', 15)
    winnerName = p1.name if winner == 1 else p2.name
    while True:
        gameDisplay.fill(colors.WHITE)
        TextSurf, TextRect = text_objects(winnerName + ' won in ' + str(turnCount+1) + ' turns!', largeText)
        TextRect.center = (displayWidth/2, displayHeight/4)
        gameDisplay.blit(TextSurf, TextRect)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    mainMenu()

        button('Quit Game', displayWidth/2-50, 3*displayHeight/4, 100, 25, colors.RED, colors.BRIGHTRED, gameDisplay, quitGame, 15)
        button('Main Menu', 0, 575, 100, 25, colors.RED, colors.BRIGHTRED, gameDisplay, mainMenu, 15)
        pygame.display.update()
        clock.tick(60)

def getShipsLeft(board):
    shipsLeft = []
    for row in range(10):
        for col in range(10):
            if board[row][col] < 0 and board[row][col] not in shipsLeft:
                shipsLeft.append(board[row][col])
    return shipsLeft

def placeCarrier():
    global currentPlaceShip
    global currentPlaceShipLoc
    if -5 not in Board:
        print('Placing carrier')
        currentPlaceShip = -5
        currentPlaceShipLoc = (-1, -1)
        time.sleep(0.25)

def placeBattleship():
    global currentPlaceShip
    global currentPlaceShipLoc
    if -4 not in Board:
        print('Placing battleship')
        currentPlaceShip = -4
        currentPlaceShipLoc = (-1, -1)
        time.sleep(0.25)

def placeCruiser():
    global currentPlaceShip
    global currentPlaceShipLoc
    if -3 not in Board:
        print('Placing cruiser')
        currentPlaceShip = -3
        currentPlaceShipLoc = (-1, -1)
        time.sleep(0.25)

def placeSubmarine():
    global currentPlaceShip
    global currentPlaceShipLoc
    if -2 not in Board:
        print('Placing submarine')
        currentPlaceShip = -2
        currentPlaceShipLoc = (-1, -1)
        time.sleep(0.25)

def placeDestroyer():
    global currentPlaceShip
    global currentPlaceShipLoc
    if -1 not in Board:
        print('Placing destroyer')
        currentPlaceShip = -1
        currentPlaceShipLoc = (-1, -1)
        time.sleep(0.25)

def getFirstValidShipLoc(board):
    global currentPlaceShip
    print('Finding default ship location')
    length = getShipLengthFromId(currentPlaceShip)
    for row in range(11-length):
        for col in range(10):
            if checkValidShipLocation(board, (row, col)):
                return (row, col)

def checkValidShipLocation(board, loc, direction=-1):
    global currentPlaceShip
    if loc[0] < 0 or loc[0] > 10 or loc[1] < 0 or loc[1] > 10:
        return False
    length = getShipLengthFromId(currentPlaceShip)
    valid = True
    if board[loc[0]][loc[1]] == 0:
        for i in range(length):
            if direction == -1:
                if loc[0]+i > 9:
                    valid = False
                    break
                if board[loc[0]+i][loc[1]] != 0:
                    valid = False
                    break
            else:
                if loc[1]+i > 9:
                    valid = False
                    break
                if board[loc[0]][loc[1]+i] != 0:
                    valid = False
                    break
    else:
        valid = False
    return valid

def getShipLengthFromId(idNum):
    return abs(idNum)+1 if abs(idNum) < 3 else abs(idNum)

def placeShips(player, playerNum, ai=False):
    global pause
    global currentPlaceShip
    global currentPlaceShipLoc
    global Board
    print('Placing ships')
    currentPlaceShipLoc = (-1, -1)
    currentPlaceShipDir = -1 # -1 = vertical, 1 = horizontal
    currentPlaceShip = 0
    largeText = pygame.font.SysFont('couriernew', 35)
    smallText = pygame.font.SysFont('couriernew', 15)
    Board = np.zeros((10, 10))
    shipPlaceCount = 0

    if ai:
        loggedIn.computer = Account.computerPlayer(loggedIn.username, loggedIn.aioffset, loggedIn.shipOffset)
        shipLocs = loggedIn.computer.placeShips(loggedIn.shipOffset)
        shipLengths = [5, 4, 3, 3, 2]
        shipIds = [-5, -4, -3, -2, -1]
        for i in range(5):
            for length in range(shipLengths[i]+1):
                if shipLocs[i][2] == 0:
                    for j in range(length):
                        Board[shipLocs[i][0]+j][shipLocs[i][1]] = shipIds[i]
                else:
                    for j in range(length):
                        Board[shipLocs[i][0]][shipLocs[i][1]+j] = shipIds[i]
        return Board


    mouseBoardCoords = np.array([[(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)],
                                 [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)]], dtype=object)
    for row in range(10):
        for col in range(10):
            mouseBoardCoords[row][col] = (200+60*row, 260+60*row, 60*col, 60+60*col)

    gameDisplay.fill(colors.WHITE)
    # Display Player Names
    TextSurf, TextRect = text_objects(player, smallText)
    TextRect.center = (int(10*len(player)/2), 12)
    if playerNum == 1:
        TextRect.center = (995-int(10*len(player)/2), 12)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.draw.rect(gameDisplay, colors.SKY, (800*playerNum, 100, 200, 250))
    iconDir = 'icons\\' if operatingSystem == 'Windows' else 'icons/'

    shipsPlaced = []

    while True:
        # Display ship selction buttons
        pygame.draw.rect(gameDisplay, colors.BLACK, (800*playerNum, 100, 200, 250))
        if -5 not in shipsPlaced:
            buttonImage(800*playerNum, 100, 200, 50, pygame.image.load(iconDir + 'carrierOutline.png'), pygame.image.load(iconDir + 'carrierOutline.png'), gameDisplay, placeCarrier)
        if -4 not in shipsPlaced:
            buttonImage(800*playerNum, 150, 200, 50, pygame.image.load(iconDir + 'battleshipOutline.png'), pygame.image.load(iconDir + 'battleshipOutline.png'), gameDisplay, placeBattleship)
        if -3 not in shipsPlaced:
            buttonImage(800*playerNum, 200, 200, 50, pygame.image.load(iconDir + 'cruiserOutline.png'), pygame.image.load(iconDir + 'cruiserOutline.png'), gameDisplay, placeCruiser)
        if -2 not in shipsPlaced:
            buttonImage(800*playerNum, 250, 200, 50, pygame.image.load(iconDir + 'submarineOutline.png'), pygame.image.load(iconDir + 'submarineOutline.png'), gameDisplay, placeSubmarine)
        if -1 not in shipsPlaced:
            buttonImage(800*playerNum, 300, 200, 50, pygame.image.load(iconDir + 'destroyerOutline.png'), pygame.image.load(iconDir + 'destroyerOutline.png'), gameDisplay, placeDestroyer)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for row in range(10):
            for col in range(10):
                if mouse[0] > mouseBoardCoords[row][col][0] and mouse[0] < mouseBoardCoords[row][col][1] and mouse[1] > mouseBoardCoords[row][col][2] and mouse[1] < mouseBoardCoords[row][col][3]:

                    # Move Ship
                    if currentPlaceShipDir == -1:
                        if col >= 0 and col+getShipLengthFromId(currentPlaceShip)-1 < 10 and row >= 0 and row < 10:
                            currentPlaceShipLoc = (col, row)
                    else:
                        if col >= 0 and col < 10 and row >= 0 and row+getShipLengthFromId(currentPlaceShip)-1 < 10:
                            currentPlaceShipLoc = (col, row)

                    # Display Board
                    for row in range(10):
                        for col in range(10):
                            pygame.draw.rect(gameDisplay, colors.BRIGHTBLUE, (200+60*col, 60*row, 60, 60))
                            pygame.draw.rect(gameDisplay, colors.BLUE, (201+60*col, 1+60*row, 59, 59))
                            if Board[row][col] < 0:
                                pygame.draw.rect(gameDisplay, colors.BLACK, (201+60*col, 1+60*row, 59, 59))

                    if currentPlaceShip != 0 and currentPlaceShipLoc != (-1, -1):
                        if currentPlaceShipDir == -1:
                            for i in range(getShipLengthFromId(currentPlaceShip)):
                                pygame.draw.rect(gameDisplay, colors.RED, (201+60*currentPlaceShipLoc[1], 1+60*(i+currentPlaceShipLoc[0]), 59, 59))
                        else:
                            for i in range(getShipLengthFromId(currentPlaceShip)):
                                pygame.draw.rect(gameDisplay, colors.RED, (201+60*(i+currentPlaceShipLoc[1]), 1+60*currentPlaceShipLoc[0], 59, 59))
                    pygame.display.update()

        # Rotate Ship
        if click[2] == 1:
            if currentPlaceShipDir == -1:
                if currentPlaceShipLoc[1]+getShipLengthFromId(currentPlaceShip)-1 < 10:
                    currentPlaceShipDir *= -1
                    click = (click[0], click[1], 0)
            elif currentPlaceShipDir == 1:
                if currentPlaceShipLoc[0]+getShipLengthFromId(currentPlaceShip)-1 < 10:
                    currentPlaceShipDir *= -1
                    click = (click[0], click[1], 0)
            time.sleep(0.2)

        # Place Ship
        if click[0] == 1 and currentPlaceShip != 0:
            if checkValidShipLocation(Board, currentPlaceShipLoc, currentPlaceShipDir):
                for i in range(getShipLengthFromId(currentPlaceShip)):
                    if currentPlaceShipDir == -1:
                        Board[currentPlaceShipLoc[0]+i][currentPlaceShipLoc[1]] = currentPlaceShip
                    else:
                        Board[currentPlaceShipLoc[0]][currentPlaceShipLoc[1]+i] = currentPlaceShip
                shipsPlaced.append(currentPlaceShip)
                currentPlaceShip = 0
                currentPlaceShipLoc = (-1, -1)
                currentPlaceShipDir = -1

        # Pause and Quit Game
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    paused()

        if len(shipsPlaced) == 5:
            break
        pygame.display.update()
        clock.tick(15)
    time.sleep(0.2)
    return Board

def paused():
    pygame.mouse.set_visible(True)
    text = pygame.font.SysFont('couriernew', 35)
    TextSurf, TextRect = text_objects('Paused', text)
    TextRect.center = ((displayWidth/2), (displayHeight/4))
    print('Game paused')
    while True:
        if not pause:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    unpause()
        gameDisplay.fill(colors.WHITE)
        gameDisplay.blit(TextSurf, TextRect)
        button('CONTINUE', int(displayWidth/2-(125/640)*displayWidth), int((3/4)*displayHeight), int((12/64)*displayWidth), int((5/48)*displayHeight), colors.GREEN, colors.BRIGHTGREEN, gameDisplay, unpause)
        button('MAIN MENU', int((displayWidth/2)+(5/640)*displayWidth), int((3/4)*displayHeight), int((13/64)*displayWidth), int((5/48)*displayHeight), colors.RED, colors.BRIGHTRED, gameDisplay, mainMenu)
        pygame.display.update()
        clock.tick(60)

def unpause():
    global pause
    print('Game unpaused')
    pause = False

def mainMenu():
    global displayWidth
    global displayHeight
    global gameDisplay
    global accounts
    print('Main menu')

    accounts = getAllAccounts()

    pygame.display.set_caption('Warships 2')
    displayWidth = 1000
    displayHeight = 600
    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))

    while True:
        pygame.display.set_caption('Warships 2')
        gameDisplay.fill(colors.WHITE)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

        if loggedIn != None:
            button(loggedIn.getProfileDisplay(), 0, 0, 35+10*len(loggedIn.username), 25, colors.WHITE, colors.WHITE, gameDisplay, editProfile, 15)
        button('New Account', 750, 0, 125, 25, colors.BLUE, colors.BRIGHTBLUE, gameDisplay, createNewAccount, 15, colors.WHITE)
        button('Login', 875, 0, 100, 25, colors.GREEN, colors.BRIGHTGREEN, gameDisplay, login, 15)
        if operatingSystem == 'Windows':
            buttonImage(975, 0, 25, 25, pygame.image.load('icons\\settingsIconInactive.png'), pygame.image.load('icons\\settingsIconActive.png'), gameDisplay, settingsMenu)
        else:
            buttonImage(975, 0, 25, 25, pygame.image.load('icons/settingsIconInactive.png'), pygame.image.load('icons/settingsIconActive.png'), gameDisplay, settingsMenu)
        button('Play', displayWidth/2-50, displayWidth/2, 100, 25, colors.BLUE, colors.BRIGHTBLUE, gameDisplay, play, 15, colors.WHITE)

        pygame.display.update()
        clock.tick(60)

def Warships2():
    global accounts
    global loggedIn
    global pause
    global creatingUsername
    global clock

    accounts = []
    loggedIn = None
    pause = False
    pygame.display.set_caption('Warships 2')
    pygame.display.set_icon(pygame.image.load('WarshipsIcon.png'))
    creatingUsername = ''
    clock = pygame.time.Clock()
    firstRunSetup()
    accounts = getAllAccounts()
    mainMenu()

if __name__ == '__main__':
    Warships2()