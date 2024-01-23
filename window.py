# IMPORTS
# pygame
from mimetypes import init
from posixpath import dirname
from turtle import width
import pygame
# functions
import functions

# ALL WINDOW SETUP
# monitor setup
MAIN_MONITOR = functions.getPrimaryMonitor()

# config setup
# setting title 
TITLE = 'F1 Racing Game'
pygame.display.set_caption(TITLE)
# setting icon 
FAVIOCON = pygame.image.load(functions.getsCorrectPath('img\\favicon.ico'))
pygame.display.set_icon(FAVIOCON)

# window const
screen = object
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Fonts
DEAFULTFONT = functions.getsCorrectPath('font\\Formula1-Regular_web_0.ttf')


def main(running):
  global screen

  # initialize window 
  pygame.init()
  screen = pygame.display.set_mode((MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT), pygame.RESIZABLE)

  # setting tickrate
  clock = pygame.time.Clock()
  clock.tick(60)

  # imports game file with all stuff
  import game
  # CREATE STARTING MENU
  mainMenu = game.Menu(['Play', 'Options', 'Exit'])

  # starting game
  while running:
    # events control
    for event in pygame.event.get():
      # closing
      if event.type == pygame.QUIT:
        running = False

      # keydown event
      elif event.type == pygame.KEYDOWN:
        # fullscreen
        if event.key == pygame.K_F11:
          pygame.display.toggle_fullscreen()
        # key up or w clicked
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
          if game.inMainMenu:
            mainMenu.activeOptionIndex = len(mainMenu.options) - 1 if mainMenu.activeOptionIndex == 0 else mainMenu.activeOptionIndex - 1
        # key down or s clicked
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
          if game.inMainMenu:
            mainMenu.activeOptionIndex = 0 if mainMenu.activeOptionIndex + 1 == len(mainMenu.options) else mainMenu.activeOptionIndex + 1
        # enter clicked
        elif event.key == pygame.K_RETURN:
          # closing game from main menu
          if game.inMainMenu and mainMenu.activeOptionIndex == len(mainMenu.options) - 1:
            running = False

      # setting min width & height
      elif event.type == pygame.VIDEORESIZE:
        windowWidth = min(MAIN_MONITOR.width, max(MIN_WINDOW_WIDTH, event.w))
        windowHeight = min(MAIN_MONITOR.height, max(MIN_WINDOW_HEIGHT, event.h))

        if (windowWidth, windowHeight) != event.size:
          screen = pygame.display.set_mode((windowWidth, windowHeight), pygame.RESIZABLE)
          pygame.display.update()
        

    # fill the screen with a color to wipe away anything from last frame

    mainMenu.display()

    # RENDER YOUR GAME HERE

    pygame.display.flip()

  pygame.quit()