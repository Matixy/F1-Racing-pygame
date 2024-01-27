# IMPORTS
import pygame
import functions
import json

# setting data from config.json
jsonConfigData = dict()
with open(functions.getsCorrectPath('data\\config.json'), 'r') as file:
  jsonConfigData = json.loads(file.read())


TITLE = 'F1 Racing Game'
FAVIOCON = pygame.image.load(functions.getsCorrectPath('img\\favicon.ico'))
DEAFULTFONT = functions.getsCorrectPath('font\\Formula1-Regular_web_0.ttf')

LOGO = pygame.image.load(functions.getsCorrectPath('img\\f1_banner.png'))
ARROW_RIGHT = pygame.image.load(functions.getsCorrectPath('img\\angle-right-solid.svg'))
ARROW_LEFT =pygame.image.load(functions.getsCorrectPath('img\\angle-left-solid.svg'))

MAIN_MONITOR = functions.getPrimaryMonitor()
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

DISPLAY_MODE_NUMBERS = {
  'Resizable': 16,
  'Fullscreen': -2147483648
}

MAIN_MENU_OPTIONS = {
  "Play": [],
  "Options": [],
  "Exit": [] 
}

OPTIONS_MENU_OPTIONS = {
  "Resolution": jsonConfigData['resolutionOptions']['options'],
  "Display Mode": jsonConfigData['displayMode']['options'],
  "Back": [] 
}