# IMPORTS
from window import *
import functions
from constants import *

# Menu
class Menu:
  def __init__(self, menuOptions, active, fontSize = int(MAIN_MONITOR.width * 0.04)):
    self.options = [str(i) for i in menuOptions.keys()]
    self.propertiesOfOption = menuOptions
    self.active = active
    self.fontSize = fontSize
    self.font = pygame.font.Font(DEAFULTFONT, fontSize)

  defaultColor = 'red'
  hoverColor = 'white'
  margin = screen.get_width() * 0.02
  activeOptionIndex = 0

  def displayOptionsToText(self, optionName):
    print(functions.convertToCammelCase(optionName))

  def displayLogo(self):
    transformedLogo = functions.transformImage(LOGO, 0.5)
    screen.blit(transformedLogo, (int(screen.get_width() / 2 - transformedLogo.get_width() / 2), int(screen.get_height() / 2 - self.fontSize - transformedLogo.get_height())))

  def displayText(self, textContent, index):
    color = self.hoverColor if index == self.activeOptionIndex else self.defaultColor
    text = self.font.render(textContent, True, color)
    text_rect = text.get_rect(center = (int(screen.get_width() / 2), int(screen.get_height() / 2 + (self.fontSize + self.margin) * index)))
    
    if len(self.propertiesOfOption[textContent]) > 0:
      optionTextContent = str(jsonConfigData[functions.convertToCammelCase(textContent)]['active'][0]) + 'x ' + str(jsonConfigData[functions.convertToCammelCase(textContent)]['active'][1]) if textContent == 'Resolution' else jsonConfigData[functions.convertToCammelCase(textContent)]['active']
      
      transformedArrowLeft = functions.transformImage(ARROW_LEFT, 0.01)
      transformedArrowRight = functions.transformImage(ARROW_RIGHT, 0.01)
      
      transformedArrowLeft_rect = transformedArrowLeft.get_rect(center = (int(text_rect.x + text_rect.width + self.margin), int(text_rect.y + text.get_height() / 2)))
      
      optionText = self.font.render(optionTextContent, True, color)
      optionText_rect = optionText.get_rect(center = (int(transformedArrowLeft_rect.x + optionText.get_width() / 2 + self.margin + transformedArrowLeft.get_width()), int((screen.get_height() / 2 + (self.fontSize + self.margin) * index))))
      
      transformedArrowRight_rect = transformedArrowRight.get_rect(center = (int(optionText_rect.x + optionText_rect.width + self.margin), int(text_rect.y + text.get_height() / 2)))
     
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