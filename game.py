# IMPORTS
import math
from turtle import position
from window import *
import functions
from constants import *

curentRaceData = {
  "Best Time": "00:00",
  "Best All Time": "00:00",
  "Lap time": "00:00"
}

prevScreenSize = []

# Menu
class Menu:
  def __init__(self, menuOptions, active, fontSize = int(screen.get_width() * 0.03)):
    self.options = [str(i) for i in menuOptions.keys()]
    self.propertiesOfOption = menuOptions
    self.active = active
    self.fontSize = fontSize
    self.margin = 21.6
    self.font = pygame.font.Font(DEAFULTFONT, fontSize)

  defaultColor = 'red'
  hoverColor = 'white'
  activeOptionIndex = 0

  def updateFontAndMargin(self, fontSize):
    self.fontSize = fontSize
    self.margin = 21.6

  def displayLogo(self):
    transformedLogo = functions.transformImage(LOGO, 0.5)
    screen.blit(transformedLogo, (int(screen.get_width() / 2 - transformedLogo.get_width() / 2), int(screen.get_height() / 2 - self.fontSize - transformedLogo.get_height())))
    

  def displayText(self, textContent, index):
    # display text
    color = self.hoverColor if index == self.activeOptionIndex else self.defaultColor
    text = self.font.render(textContent, True, color)
    text_rect = text.get_rect(center = (int(screen.get_width() / 2), int(screen.get_height() / 2 + (self.fontSize + self.margin * 0.4) * index)))
    
    # display options if text is in option menu
    if len(self.propertiesOfOption[textContent]) > 0:
      optionTextContent = str(jsonConfigData[functions.convertToCammelCase(textContent)]['active'][0]) + ' x ' + str(jsonConfigData[functions.convertToCammelCase(textContent)]['active'][1]) if textContent == 'Resolution' else jsonConfigData[functions.convertToCammelCase(textContent)]['active']
      
      transformedArrowLeft = functions.transformImage(ARROW_LEFT, 0.01)
      transformedArrowRight = functions.transformImage(ARROW_RIGHT, 0.01)
      
      transformedArrowLeft_rect = transformedArrowLeft.get_rect(center = (int(text_rect.x + text_rect.width + self.margin), int(text_rect.y + text.get_height() / 2)))
      
      optionText = self.font.render(optionTextContent, True, color)
      optionText_rect = optionText.get_rect(center = (int(transformedArrowLeft_rect.x + optionText.get_width() / 2 + self.margin * 0.5 + transformedArrowLeft.get_width()), text_rect.y + text_rect.height / 2))
      
      transformedArrowRight_rect = transformedArrowRight.get_rect(center = (int(optionText_rect.x + self.margin * 0.5 + optionText.get_width() + transformedArrowLeft_rect.width), int(text_rect.y + text.get_height() / 2)))
     
      screen.blit(transformedArrowLeft, transformedArrowLeft_rect)      
      screen.blit(optionText, optionText_rect)
      screen.blit(transformedArrowRight, transformedArrowRight_rect)
      
    screen.blit(text, text_rect) 
  
  def changeOptionToNext(self, option):
    cammelTextOption = functions.convertToCammelCase(option)

    jsonConfigData[cammelTextOption]['active'] = self.propertiesOfOption[option][0] if self.propertiesOfOption[option].index(jsonConfigData[cammelTextOption]['active']) == len(self.propertiesOfOption[option]) - 1 else self.propertiesOfOption[option][self.propertiesOfOption[option].index(jsonConfigData[cammelTextOption]['active']) + 1]
    
  def changeOptionToPrevious(self, option):
    cammelTextOption = functions.convertToCammelCase(option)

    jsonConfigData[cammelTextOption]['active'] = self.propertiesOfOption[option][len(self.propertiesOfOption[option]) - 1] if self.propertiesOfOption[option].index(jsonConfigData[cammelTextOption]['active']) == 0 else self.propertiesOfOption[option][self.propertiesOfOption[option].index(jsonConfigData[cammelTextOption]['active']) - 1]

  def display(self):
    screen.fill('black')
    self.displayLogo()
    for i in range(len(self.options)):
      self.displayText(self.options[i], i)

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
    self.acceleration = screen.get_width() / 1280 * 0.01
    self.maxSpeed = screen.get_width() / 1280 * 0.5
    self.carCurrentImg = pygame.transform.rotate(self.carImg, self.angle)
    self.wrongDirection = False
    self.position = [screen.get_width()/2 + screen.get_width() * 0.355, screen.get_height()/2 + self.carCurrentImg.get_height()]

  def updateParameters(self, prevScreenSize):
    self.acceleration = screen.get_width() / 1280 * 0.01
    self.maxSpeed = screen.get_width() / 1280 * 0.5
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
      self.angle += CAR_ROTATE_SPEED_RATIO * screen.get_width()
    elif option == 'right':
      self.angle -= CAR_ROTATE_SPEED_RATIO * screen.get_width()

    if self.angle > 360:
      self.angle -= 360
    elif self.angle < 0:
      self.angle = 360 + self.angle

  def reduceSpeed(self):
    self.speed = max(self.speed - self.acceleration / 1.2 , min(self.speed + self.acceleration / 1.2 ,0))

  def moveCar(self):
    if self.movingFoward and self.speed < self.maxSpeed:
      self.speed += self.acceleration
    elif self.movingBackward and self.speed > self.maxSpeed * -1:
      self.speed -= self.acceleration
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
    self.speed = -self.speed
    if self.movingLeft: 
      self.movingLeft = False
      self.angle -= CAR_ROTATE_SPEED_RATIO * screen.get_width() * 3
    elif self.movingRight: 
      self.movingRight = False
      self.angle += CAR_ROTATE_SPEED_RATIO * screen.get_width() * 3

    self.move()

  def displayCar(self):
    self.blitCarCenter()