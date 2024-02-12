# IMPORTS
import pygame
import functions

# setting data from config.json
jsonConfigData = functions.readJson(functions.getsCorrectPath('data\\config.json'))
jsonScoreData = functions.readJson(functions.getsCorrectPath('data\\scores.json'))

# text
TITLE = 'F1 Racing Game'
FAVIOCON = pygame.image.load(functions.getsCorrectPath('img\\favicon.ico'))

DEFAULT_FONT = functions.getsCorrectPath('font\\Formula1-Regular_web_0.ttf')
DEFAULT_FONT_COLOR = 'white'
DEFAULT_FONT_SIZE_RATIO = 0.01
DEFAULT_MIN_MARGIN = 6.4
DEFAULT_MAX_MARGIN = 10.2
DEFAULT_MARGIN_RATIO = 0.005

MENU_FONT_COLOR = 'red'
MENU_FONT_SIZE_RATIO = 0.03
MENU_MIN_MARGIN = 12.8
MENU_MAX_MARGIN = 21.6
MENU_MARGIN_RATIO = 0.01
MAIN_MENU_FONT_SIZE_RATIO = 0.05

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
CAR_ROTATE_SPEED_RATIO = 0.015
CAR_MAX_SPEED_RATIO = 0.005
CAR_ACCELERATION_RATIO = CAR_MAX_SPEED_RATIO / 5