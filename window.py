# IMPORTS
import pygame
import functions
from constants import *
import math

# ALL WINDOW SETUP
# setting title
pygame.display.set_caption(TITLE)
# setting icon
pygame.display.set_icon(FAVIOCON)

# window const
screen = object

def main(running):
  global screen
  # initialize window 
  pygame.init()
  screen = pygame.display.set_mode((jsonConfigData["resolution"]["active"][0], jsonConfigData["resolution"]["active"][1]), DISPLAY_MODE_NUMBERS[jsonConfigData['displayMode']['active']])

  # setting tickrate
  clock = pygame.time.Clock()

  # window states
  inMainMenu = True
  inPauseMenu = False
  inOptionsMenu = False
  inGame = False

  # imports game file with all stuff
  import game
  # CREATE MENU'S OBJECTS
  mainMenu = game.Menu(MAIN_MENU_OPTIONS, inMainMenu, MAIN_MENU_FONT_SIZE_RATIO)
  pauseMenu = game.Menu(PAUSE_MENU_OPTIONS, inPauseMenu)
  optionsMenu = game.Menu(OPTIONS_MENU_OPTIONS, inOptionsMenu)
  previousMenu = ''
  
  # generate user's car
  userCar = game.Car()
  # generate stats object 
  stats = game.Stats()
  # generate grid
  grid = game.Grid()
  finishColisionPos = None

  # starting game
  while running:
    # events control
    for event in pygame.event.get():
      # quit event - closing
      if event.type == pygame.QUIT:
        running = False

      # keydown events
      elif event.type == pygame.KEYDOWN:
        # f11 clicked- fullscreen
        if event.key == pygame.K_F11:
          if (screen.get_flags() & pygame.FULLSCREEN) == 0:
            jsonConfigData['displayMode']['active'] = "Fullscreen"
          else:
            jsonConfigData['displayMode']['active'] = "Windowed"

          pygame.display.toggle_fullscreen()
          pygame.display.update()
          
        # key up or w clicked
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
          if inMainMenu:
            mainMenu.activeOptionIndex = len(mainMenu.options) - 1 if mainMenu.activeOptionIndex == 0 else mainMenu.activeOptionIndex - 1
          elif inOptionsMenu:
            optionsMenu.activeOptionIndex = len(optionsMenu.options) - 1 if optionsMenu.activeOptionIndex == 0 else optionsMenu.activeOptionIndex - 1
          elif inPauseMenu:
            pauseMenu.activeOptionIndex = len(pauseMenu.options) - 1 if pauseMenu.activeOptionIndex == 0 else pauseMenu.activeOptionIndex - 1
          elif inGame:
            if stats.startLapTimestamp == None: stats.startCountLapTime()
            userCar.movingFoward = True
        # key down or s clicked
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
          if inMainMenu:
            mainMenu.activeOptionIndex = 0 if mainMenu.activeOptionIndex + 1 == len(mainMenu.options) else mainMenu.activeOptionIndex + 1
          elif inOptionsMenu:
            optionsMenu.activeOptionIndex = 0 if optionsMenu.activeOptionIndex + 1 == len(optionsMenu.options) else optionsMenu.activeOptionIndex + 1
          elif inPauseMenu:
            pauseMenu.activeOptionIndex = 0 if pauseMenu.activeOptionIndex + 1 == len(pauseMenu.options) else pauseMenu.activeOptionIndex + 1
          elif inGame:
            if stats.startLapTimestamp == None: stats.startCountLapTime()
            userCar.movingBackward = True
        # key right or d clicked
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          if inOptionsMenu and len(optionsMenu.propertiesOfOption[optionsMenu.options[optionsMenu.activeOptionIndex]]):
            prevScreenSize = screen.get_size()
            optionsMenu.changeOptionToPrevious(optionsMenu.options[optionsMenu.activeOptionIndex])     
            screen = pygame.display.set_mode((jsonConfigData["resolution"]["active"][0], jsonConfigData["resolution"]["active"][1]), DISPLAY_MODE_NUMBERS[jsonConfigData['displayMode']['active']])

            # update game params
            grid.updateMap()
            userCar.updateParameters(prevScreenSize)  
            # update margin & font
            optionsMenu.updateFontAndMargin()
            pauseMenu.updateFontAndMargin()
            mainMenu.updateFontAndMargin()
            stats.updateFontAndMargin()

            pygame.display.update()
          elif inGame:
            userCar.movingRight = True
        # key left or a clicked
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
          if inOptionsMenu and len(optionsMenu.propertiesOfOption[optionsMenu.options[optionsMenu.activeOptionIndex]]):
            # SET SETTINGS
            prevScreenSize = screen.get_size()
            optionsMenu.changeOptionToNext(optionsMenu.options[optionsMenu.activeOptionIndex])
            screen = pygame.display.set_mode((jsonConfigData["resolution"]["active"][0], jsonConfigData["resolution"]["active"][1]), DISPLAY_MODE_NUMBERS[jsonConfigData['displayMode']['active']])

            # update game params
            grid.updateMap()
            userCar.updateParameters(prevScreenSize)  
            # update margin & font
            optionsMenu.updateFontAndMargin()
            pauseMenu.updateFontAndMargin()
            mainMenu.updateFontAndMargin()
            stats.updateFontAndMargin()

            pygame.display.update()
          elif inGame:
            userCar.movingLeft = True
        # escape clicked
        elif event.key == pygame.K_ESCAPE:
          if inGame:
            inGame = False
            inPauseMenu = True
          elif inOptionsMenu:
            inOptionsMenu = False
            if previousMenu == 'main':
              inMainMenu = True
            elif previousMenu == 'pause':
              inPauseMenu = True
            optionsMenu.activeOptionIndex = 0
          elif inPauseMenu:
            inPauseMenu = False
            inGame = True
            pauseMenu.activeOptionIndex = 0
        # enter clicked
        elif event.key == pygame.K_RETURN:
          # entering into game
          if inMainMenu and mainMenu.activeOptionIndex == 0:
            inMainMenu = False
            inGame = True
          # closing game from main menu
          elif inMainMenu and mainMenu.activeOptionIndex == len(mainMenu.options) - 1:
            running = False
          # enter to options menu from main menu
          elif inMainMenu and mainMenu.options[mainMenu.activeOptionIndex] == 'Options':
            inMainMenu = False
            inOptionsMenu = True
            previousMenu = 'main'
          # enter to menu's from options menu
          elif inOptionsMenu and optionsMenu.activeOptionIndex == len(optionsMenu.options) - 1:
            inOptionsMenu = False
            if previousMenu == 'main':
              inMainMenu = True
            elif previousMenu == 'pause':
              inPauseMenu = True
            optionsMenu.activeOptionIndex = 0
          # enter to game from pause menu
          elif inPauseMenu and pauseMenu.activeOptionIndex == 0:
            inPauseMenu = False
            inGame = True
          # enter to options from pause menu
          elif inPauseMenu and pauseMenu.options[pauseMenu.activeOptionIndex] == 'Options':
            inPauseMenu = False
            inOptionsMenu = True
            previousMenu = 'pause'
          # emter to main menu from pause menu
          elif inPauseMenu and pauseMenu.activeOptionIndex == len(pauseMenu.options) - 1:
            inPauseMenu = False
            inMainMenu = True
            previousMenu = 'pause'
            pauseMenu.activeOptionIndex = 0
      
      # key up events
      elif event.type == pygame.KEYUP:
        # key up or w clicked
        if event.key == pygame.K_UP or event.key == pygame.K_w:
          if inGame:
            userCar.movingFoward = False
        # key down or s clicked
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
          if inGame:
            userCar.movingBackward = False
        # key left or a clicked
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
          if inGame:
            userCar.movingLeft = False
        # key right or d clicked
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          if inGame:
            userCar.movingRight = False

    if inMainMenu:
      if previousMenu == 'pause':
        userCar = game.Car()
        stats = game.Stats()
      mainMenu.display()
    elif inOptionsMenu:
      optionsMenu.display()
    elif inPauseMenu:
      pauseMenu.display()
      if stats.startLapTimestamp != None: stats.freezeTime()
    elif inGame:
      grid.generateMap()

      stats.display()
      if stats.startLapTimestamp != None: stats.countLapTime()

      userCar.displayCar()
      userCar.moveCar()

      # bounce from borders
      if userCar.colide(grid.borderMask): userCar.bounce()

      # prevent wrong way driving
      if userCar.colide(grid.finishLineMask, *grid.finishLinePosition) == None and finishColisionPos != None:
        if finishColisionPos[1] == 0: 
          userCar.wrongDirection = True
      elif userCar.colide(grid.finishLineMask, *grid.finishLinePosition) != None and finishColisionPos == None:
        newFinishColisionPos = userCar.colide(grid.finishLineMask, *grid.finishLinePosition)
        if userCar.wrongDirection and newFinishColisionPos[1] == 0:
          userCar.wrongDirection = False
        elif newFinishColisionPos[1] == 0 and userCar.wrongDirection == False:
          stats.updateStats()
          stats.startCountLapTime()
      finishColisionPos = userCar.colide(grid.finishLineMask, *grid.finishLinePosition)


    clock.tick(60)
    pygame.display.flip()

  pygame.quit()
  
  functions.saveJson(jsonConfigData, functions.getsCorrectPath('data\\config.json'))
  functions.saveJson({"bestLapTime":stats.times['Best Lap Time']}, functions.getsCorrectPath('data\\scores.json'))