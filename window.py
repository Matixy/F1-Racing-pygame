# IMPORTS
from mimetypes import init
from posixpath import dirname
from turtle import width
import pygame
import functions
from constants import *

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
  clock.tick(60)

  # window states
  inMainMenu = True
  inPauseMenu = False
  inOptionsMenu = False
  inGame = False

  # imports game file with all stuff
  import game
  # CREATE MENU'S OBJECTS
  mainMenu = game.Menu(MAIN_MENU_OPTIONS, inMainMenu, int(MAIN_MONITOR.width * 0.04))
  pauseMenu = game.Menu(PAUSE_MENU_OPTIONS, inPauseMenu)
  optionsMenu = game.Menu(OPTIONS_MENU_OPTIONS, inOptionsMenu)
  previousMenu = ''

  # create user's car
  userCar = game.Car()

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
        # key up or w clicked
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
          if inMainMenu:
            mainMenu.activeOptionIndex = len(mainMenu.options) - 1 if mainMenu.activeOptionIndex == 0 else mainMenu.activeOptionIndex - 1
          elif inOptionsMenu:
            optionsMenu.activeOptionIndex = len(optionsMenu.options) - 1 if optionsMenu.activeOptionIndex == 0 else optionsMenu.activeOptionIndex - 1
          elif inPauseMenu:
            pauseMenu.activeOptionIndex = len(pauseMenu.options) - 1 if pauseMenu.activeOptionIndex == 0 else pauseMenu.activeOptionIndex - 1
          elif inGame:
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
            userCar.movingBackward = True
        # key right or d clicked
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          if inOptionsMenu and len(optionsMenu.propertiesOfOption[optionsMenu.options[optionsMenu.activeOptionIndex]]):
            optionsMenu.changeOptionToPrevious(optionsMenu.options[optionsMenu.activeOptionIndex])     
            screen = pygame.display.set_mode((jsonConfigData["resolution"]["active"][0], jsonConfigData["resolution"]["active"][1]), DISPLAY_MODE_NUMBERS[jsonConfigData['displayMode']['active']])

            pygame.display.update()
            optionsMenu.updateFontAndMargin(int(screen.get_width() * 0.04))
            pauseMenu.updateFontAndMargin(int(screen.get_width() * 0.04))
          elif inGame:
            userCar.movingRight = True
        # key left or a clicked
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
          if inOptionsMenu and len(optionsMenu.propertiesOfOption[optionsMenu.options[optionsMenu.activeOptionIndex]]):
            optionsMenu.changeOptionToNext(optionsMenu.options[optionsMenu.activeOptionIndex])
            screen = pygame.display.set_mode((jsonConfigData["resolution"]["active"][0], jsonConfigData["resolution"]["active"][1]), DISPLAY_MODE_NUMBERS[jsonConfigData['displayMode']['active']])

            pygame.display.update()
            optionsMenu.updateFontAndMargin(int(screen.get_width() * 0.04))
            pauseMenu.updateFontAndMargin(int(screen.get_width() * 0.04))
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
        
    # fill the screen with a color to wipe away anything from last frame
    if inMainMenu:
      mainMenu.display()
    elif inOptionsMenu:
      optionsMenu.display()
    elif inPauseMenu:
      pauseMenu.display()
    elif inGame:
      game.Grid.generateMap()
      userCar.moveCar()
      userCar.displayCar()
    # RENDER YOUR GAME HERE
    
    pygame.display.flip()

  pygame.quit()
  
  functions.saveConfigJson(jsonConfigData)