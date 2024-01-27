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
  screen = pygame.display.set_mode((jsonConfigData["resolutionOptions"]["active"][0], jsonConfigData["resolutionOptions"]["active"][1]), DISPLAY_MODE_NUMBERS[jsonConfigData['displayMode']['active']])

  # setting tickrate
  clock = pygame.time.Clock()
  clock.tick(60)

  # window states
  inMainMenu = True
  inPauseMenu = False
  inOptionsMenu = False

  # imports game file with all stuff
  import game
  # CREATE MENU'S OBJECTS
  mainMenu = game.Menu(MAIN_MENU_OPTIONS, inMainMenu)
  optionsMenu = game.Menu(OPTIONS_MENU_OPTIONS, inOptionsMenu)

  # starting game
  while running:
    # events control
    for event in pygame.event.get():
      # closing
      if event.type == pygame.QUIT:
        running = False

      # keydown events
      elif event.type == pygame.KEYDOWN:
        # fullscreen
        if event.key == pygame.K_F11:
          if (screen.get_flags() & pygame.FULLSCREEN) == 0:
            screen = pygame.display.set_mode((MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT), pygame.RESIZABLE)
          pygame.display.toggle_fullscreen()
        # key up or w clicked
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
          if inMainMenu:
            mainMenu.activeOptionIndex = len(mainMenu.options) - 1 if mainMenu.activeOptionIndex == 0 else mainMenu.activeOptionIndex - 1
          elif inOptionsMenu:
            optionsMenu.activeOptionIndex = len(optionsMenu.options) - 1 if optionsMenu.activeOptionIndex == 0 else optionsMenu.activeOptionIndex - 1
        # key down or s clicked
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
          if inMainMenu:
            mainMenu.activeOptionIndex = 0 if mainMenu.activeOptionIndex + 1 == len(mainMenu.options) else mainMenu.activeOptionIndex + 1
          elif inOptionsMenu:
            optionsMenu.activeOptionIndex = 0 if optionsMenu.activeOptionIndex + 1 == len(optionsMenu.options) else optionsMenu.activeOptionIndex + 1
        # enter clicked
        elif event.key == pygame.K_RETURN:
          # closing game from main menu
          if inMainMenu and mainMenu.activeOptionIndex == len(mainMenu.options) - 1:
            running = False
          # enter to options menu from main menu
          if inMainMenu and mainMenu.options[mainMenu.activeOptionIndex] == 'Options':
            inMainMenu = False
            inOptionsMenu = True
          # enter to main menu from options menu
          if inOptionsMenu and optionsMenu.activeOptionIndex == len(optionsMenu.options) - 1:
            inMainMenu = True
            inOptionsMenu = False
            optionsMenu.activeOptionIndex = 0

      # resize event
      elif event.type == pygame.VIDEORESIZE:
        windowWidth = min(MAIN_MONITOR.width, max(MIN_WINDOW_WIDTH, event.w))
        windowHeight = min(MAIN_MONITOR.height, max(MIN_WINDOW_HEIGHT, event.h))
        if (windowWidth, windowHeight) != event.size:
          screen = pygame.display.set_mode((windowWidth, windowHeight), pygame.RESIZABLE)
          pygame.display.update()
        
    # fill the screen with a color to wipe away anything from last frame
    if inMainMenu:
      mainMenu.display()
    elif inOptionsMenu:
      optionsMenu.display()

    # RENDER YOUR GAME HERE

    pygame.display.flip()

  pygame.quit()