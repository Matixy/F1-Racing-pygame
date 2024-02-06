# IMPORTS
import pygame
import functions

# setting data from config.json
jsonConfigData = functions.readConfigJson()

# text
TITLE = 'F1 Racing Game'
FAVIOCON = pygame.image.load(functions.getsCorrectPath('img\\favicon.ico'))
DEAFULTFONT = functions.getsCorrectPath('font\\Formula1-Regular_web_0.ttf')

# images
LOGO = pygame.image.load(functions.getsCorrectPath('img\\f1_banner.png'))
ARROW_RIGHT = pygame.image.load(functions.getsCorrectPath('img\\angle-right-solid.png'))
ARROW_LEFT = pygame.image.load(functions.getsCorrectPath('img\\angle-left-solid.png'))
MAP = pygame.image.load(functions.getsCorrectPath('img\\map.png'))
MAP_BORDER = pygame.image.load(functions.getsCorrectPath('img\\map-border.png'))
FINISH_LINE = pygame.image.load(functions.getsCorrectPath('img\\finish_line.png'))
CAR = pygame.image.load(functions.getsCorrectPath('img\\car.png'))

# monitor's options
MAIN_MONITOR = functions.getPrimaryMonitor()
MIN_WINDOW_WIDTH = jsonConfigData['resolution']['options'][len(jsonConfigData['resolution']['options']) - 1][0]
MIN_WINDOW_HEIGHT = jsonConfigData['resolution']['options'][len(jsonConfigData['resolution']['options']) - 1][1]

DISPLAY_MODE_NUMBERS = {
  'Windowed': 0,
  'Fullscreen': -2147483648
}

# menu's options
MAIN_MENU_OPTIONS = {
  "Play": [],
  "Options": [],
  "Exit": [] 
}

PAUSE_MENU_OPTIONS = {
  "Resume": [],
  "Options": [],
  "Save & exit to main menu": [] 
}

OPTIONS_MENU_OPTIONS = {
  "Resolution": jsonConfigData['resolution']['options'],
  "Display Mode": jsonConfigData['displayMode']['options'],
  "Back": [] 
}

# Finish line settings
FINISH_LINE_SCALE = 0.1

# car's settings
CAR_SCALE = 0.04
CAR_ROTATE_SPEED_RATIO = 0.0005
# CAR_MAX_SPEED_RATIO = 1 * 
# CAR_ACCELERATION = 0.01