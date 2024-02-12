# IMPORTS
import math
import time
from window import *
import functions
from constants import *
import math

prevScreenSize = []

class Text:
  def __init__(self, minMargin, maxMargin, marginRatio, color, fontSizeRatio = DEFAULT_FONT_SIZE_RATIO):
    self.defaultColor = color
    self.fontSizeRatio = fontSizeRatio
    self.fontSize = self.calculateFont()
    self.font = pygame.font.Font(DEFAULT_FONT, self.fontSize)
    self.minMargin = minMargin
    self.maxMargin = maxMargin
    self.marginRatio = marginRatio
    self.margin = self.calculateMargin()

  def calculateMargin(self):
    return max(self.minMargin, min(round(screen.get_width() * self.marginRatio, 2), self.maxMargin))
  
  def calculateFont(self):
    return int(screen.get_width() * self.fontSizeRatio)
  
  def updateFontAndMargin(self):
    self.fontSize = self.calculateFont()
    self.margin = self.calculateMargin()

  def renderText (self, textContent, color): return self.font.render(textContent, True, color)

  def displayText(self, renderedText, textContent, color, pos, containsOptions = False):
    # display text
    text_rect = renderedText.get_rect(topleft = pos)
    
    # display options if text is in option menu
    if containsOptions:
      self.displayOptions(textContent, renderedText, text_rect, color)
      
    screen.blit(renderedText, text_rect) 
  
# stats
class Stats(Text):
  def __init__(self):
    super().__init__(DEFAULT_MIN_MARGIN, DEFAULT_MAX_MARGIN, DEFAULT_MARGIN_RATIO, DEFAULT_FONT_COLOR, DEFAULT_FONT_SIZE_RATIO)
    self.times = {
      "Best Lap Time": jsonScoreData['bestLapTime'],
      "Current Lap": 0.00,
      "Best Lap on Current Session": 0.00
    }
    self.startLapTimestamp = None
    self.freezeTimestamp = None

  def startCountLapTime(self):
    self.startLapTimestamp = round(time.time(), 2)

  def freezeTime(self):
    self.startLapTimestamp = round(time.time() - self.times["Current Lap"], 2)

  def countLapTime(self):
    if self.freezeTimestamp != None: self.freezeTimestamp = None
    self.times["Current Lap"] = round(time.time() - self.startLapTimestamp , 2)

  def updateStats(self):
    if self.times["Current Lap"] <= self.times["Best Lap on Current Session"] or self.times["Best Lap on Current Session"] == 0:
      self.times["Best Lap on Current Session"] = self.times["Current Lap"]
    if self.times["Best Lap on Current Session"] <= self.times["Best Lap Time"] or self.times["Best Lap Time"] == 0:
      self.times["Best Lap Time"] = self.times["Best Lap on Current Session"]
      jsonScoreData['bestLapTime'] = self.times["Best Lap on Current Session"]
  
  def display(self):
    for timeParameter in self.times:
      index = list(self.times).index(timeParameter)
      # set time always to 00:00 format
      textContent = str(self.times[timeParameter]).replace('.',':')
      if textContent[1] == ':': textContent = '0' + textContent
      if textContent[-2] == ':': textContent += '0'
      textContent = f'{timeParameter}: {textContent}'
      # display
      renderedText = self.renderText(textContent, self.defaultColor)
      pos = ((self.margin/2), (self.margin * index + renderedText.get_height() * index + self.margin/2))
      self.displayText(renderedText, textContent, self.defaultColor, pos)

# Menu
class Menu(Text):
  def __init__(self, menuOptions, active, fontSizeRatio = MENU_FONT_SIZE_RATIO):
    super().__init__(MENU_MIN_MARGIN, MENU_MAX_MARGIN, MENU_MARGIN_RATIO, MENU_FONT_COLOR, fontSizeRatio)
    self.options = [str(i) for i in menuOptions.keys()]
    self.propertiesOfOption = menuOptions
    self.active = active

  hoverColor = DEFAULT_FONT_COLOR
  activeOptionIndex = 0

  def displayLogo(self):
    transformedLogo = functions.transformImage(LOGO, 0.5)
    screen.blit(transformedLogo, (int(screen.get_width() / 2 - transformedLogo.get_width() / 2), int(screen.get_height() / 2 - self.fontSize - transformedLogo.get_height())))
  
  def displayOptions(self, textContent, text, text_rect, color):
    optionTextContent = str(jsonConfigData[functions.convertToCammelCase(textContent)]['active'][0]) + ' x ' + str(jsonConfigData[functions.convertToCammelCase(textContent)]['active'][1]) if textContent == 'Resolution' else jsonConfigData[functions.convertToCammelCase(textContent)]['active']
    
    transformedArrowLeft = functions.transformImage(ARROW_LEFT, 0.01)
    transformedArrowRight = functions.transformImage(ARROW_RIGHT, 0.01)
    
    transformedArrowLeft_rect = transformedArrowLeft.get_rect(center = (int(text_rect.x + text_rect.width + self.margin * 2), int(text_rect.y + text.get_height() / 2)))
    
    optionText = self.renderText(optionTextContent, color)
    optionText_rect = optionText.get_rect(center = (int(transformedArrowLeft_rect.x + optionText.get_width() / 2 + self.margin * 0.5 + transformedArrowLeft.get_width()), text_rect.y + text_rect.height / 2))
    
    transformedArrowRight_rect = transformedArrowRight.get_rect(center = (int(optionText_rect.x + self.margin * 0.5 + optionText.get_width() + transformedArrowLeft_rect.width), int(text_rect.y + text.get_height() / 2)))
    
    screen.blit(transformedArrowLeft, transformedArrowLeft_rect)      
    screen.blit(optionText, optionText_rect)
    screen.blit(transformedArrowRight, transformedArrowRight_rect)

  def changeOptionToNext(self, option):
    cammelTextOption = functions.convertToCammelCase(option)

    jsonConfigData[cammelTextOption]['active'] = self.propertiesOfOption[option][0] if self.propertiesOfOption[option].index(jsonConfigData[cammelTextOption]['active']) == len(self.propertiesOfOption[option]) - 1 else self.propertiesOfOption[option][self.propertiesOfOption[option].index(jsonConfigData[cammelTextOption]['active']) + 1]
    
  def changeOptionToPrevious(self, option):
    cammelTextOption = functions.convertToCammelCase(option)

    jsonConfigData[cammelTextOption]['active'] = self.propertiesOfOption[option][len(self.propertiesOfOption[option]) - 1] if self.propertiesOfOption[option].index(jsonConfigData[cammelTextOption]['active']) == 0 else self.propertiesOfOption[option][self.propertiesOfOption[option].index(jsonConfigData[cammelTextOption]['active']) - 1]

  def display(self):
    screen.fill('black')
    self.displayLogo()
    for index in range(len(self.options)):
      color = self.hoverColor if index == self.activeOptionIndex else self.defaultColor
      containsOptions = True if len(self.propertiesOfOption[self.options[index]]) > 0 else False
      renderedText = self.renderText(self.options[index], color)
      pos = (int(screen.get_width() / 2 - renderedText.get_width() / 2), int(screen.get_height() / 2 + self.margin * index + renderedText.get_height() * index - renderedText.get_height() / 2))
      
      self.displayText(renderedText, self.options[index], color, pos, containsOptions)

class Grid:
  def __init__(self):
    self.transformedMap = functions.transformImage(MAP, 1)
    self.borderMap = functions.transformImage(MAP_BORDER, 1)
    self.borderMask = pygame.mask.from_surface(self.borderMap)
    self.finishLine = functions.transformImage(FINISH_LINE, FINISH_LINE_SCALE)
    self.finishLinePosition = (int(screen.get_width() / 1.21), int(screen.get_height()/ 1.86))
    self.finishLineMask = pygame.mask.from_surface(self.finishLine)

  def updateMap(self):
    self.transformedMap = functions.transformImage(MAP, 1)
    self.borderMap = functions.transformImage(MAP_BORDER, 1)
    self.borderMask = pygame.mask.from_surface(self.borderMap)
    self.finishLine = functions.transformImage(FINISH_LINE, FINISH_LINE_SCALE)
    self.finishLinePosition = (int(screen.get_width() / 1.21), int(screen.get_height()/ 1.86))
    self.finishLineMask = pygame.mask.from_surface(self.finishLine)

  def generateMap(self):
    screen.blit(self.transformedMap, (0,0))
    screen.blit(self.finishLine, self.finishLinePosition)

class Car:
  def __init__(self):
    self.carImg = functions.transformImage(CAR, CAR_SCALE)
    self.movingFoward = False
    self.movingRight = False
    self.movingBackward = False
    self.movingLeft = False
    self.angle = 0
    self.speed = 0
    self.acceleration = screen.get_width() * CAR_ACCELERATION_RATIO
    self.maxSpeed = screen.get_width() * CAR_MAX_SPEED_RATIO
    self.rotateSpeed = CAR_ROTATE_SPEED_RATIO * 360
    self.carCurrentImg = pygame.transform.rotate(self.carImg, self.angle)
    self.wrongDirection = False
    self.position = [screen.get_width()/2 + screen.get_width() * 0.355, screen.get_height()/2 + self.carCurrentImg.get_height()]

  def updateParameters(self, prevScreenSize):
    self.acceleration = screen.get_width() * CAR_ACCELERATION_RATIO
    self.maxSpeed = screen.get_width() * CAR_MAX_SPEED_RATIO
    self.rotateSpeed = CAR_ROTATE_SPEED_RATIO * 360
    self.carImg = functions.transformImage(CAR, CAR_SCALE)
    self.position = [screen.get_width() / prevScreenSize[0] * self.position[0], screen.get_height() / prevScreenSize[1] * self.position[1]]

  def move(self):
    radians = math.radians(self.angle)
    speedX = math.sin(radians) * self.speed
    speedY = math.cos(radians) * self.speed

    self.position[0] += speedX
    self.position[1] += speedY

  def rotateCar(self, option):
    if option == 'left':
      self.angle += self.rotateSpeed
    elif option == 'right':
      self.angle -= self.rotateSpeed

    if self.angle > 360:
      self.angle -= 360
    elif self.angle < 0:
      self.angle = 360 + self.angle

  def reduceSpeed(self):
    self.speed = max(self.speed - self.acceleration / 1.2 , min(self.speed + self.acceleration / 1.2 ,0))

  def moveCar(self):
    if self.movingFoward: self.speed = min(self.speed + self.acceleration, self.maxSpeed)
    elif self.movingBackward: self.speed = max(self.speed - self.acceleration, -self.maxSpeed / 2)
    else:
      self.reduceSpeed()

    if self.movingLeft: self.rotateCar('left')
    if self.movingRight: self.rotateCar('right')

    self.move()

  def blitCarCenter(self):
    rotated_image = pygame.transform.rotate(self.carImg, self.angle)
    new_rect = rotated_image.get_rect(
        center=self.carImg.get_rect(topleft=self.position).center)
    self.carCurrentImg = rotated_image
    screen.blit(rotated_image, new_rect.topleft)

  def colide(self, gridMask, x = 0, y = 0):
    carMask = pygame.mask.from_surface(self.carCurrentImg)
    offset = (int(self.position[0] - x), int(self.position[1] - y))
    pos = gridMask.overlap(carMask, offset)
    return pos
  
  def bounce(self):
    if self.movingLeft:
      self.movingLeft = False
      self.angle -= self.rotateSpeed * 3
    if self.movingRight:
      self.movingRight = False
      self.angle += self.rotateSpeed * 3
    self.speed = -self.speed
    self.move()

  def displayCar(self):
    self.blitCarCenter()