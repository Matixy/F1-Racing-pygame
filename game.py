# IMPORTS
from window import *
import functions
from constants import *

# Menu
class Menu:
  def __init__(self, menuOptions, active, fontSize = int(screen.get_width() * 0.08)):
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
    print('ds')
    # print(self.propertiesOfOption[optionName]) it works :)


  def displayLogo(self):
    transformedLogo = pygame.transform.scale(LOGO, (screen.get_width() * 0.5, screen.get_width() * 0.5 / LOGO.get_width() * LOGO.get_height()))
    screen.blit(transformedLogo, (int(screen.get_width() / 2 - transformedLogo.get_width() / 2), int(screen.get_height() / 2 - self.fontSize - transformedLogo.get_height())))

  def displayText(self, textContent, index):
    color = self.hoverColor if index == self.activeOptionIndex else self.defaultColor
    text = self.font.render(textContent, True, color)
    options = self.displayOptionsToText(textContent)
    text_rect = text.get_rect(center = (int(screen.get_width() / 2), int(screen.get_height() / 2 + (self.fontSize + self.margin) * index)))
    screen.blit(text, text_rect)

  def display(self):
    screen.fill('black')
    self.displayLogo()
    for i in range(len(self.options)):
      self.displayText(self.options[i], i)
