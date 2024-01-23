# IMPORTS
from window import *
import functions

# Menu
class Menu:
  def __init__(self, menuOptions, active):
    self.options = menuOptions

  fontSize = int(screen.get_width() * 0.08)
  defaultColor = 'red'
  hoverColor = 'white'
  font = pygame.font.Font(DEAFULTFONT, fontSize)
  logo = pygame.image.load(functions.getsCorrectPath('img\\f1_banner.png'))
  margin = screen.get_width() * 0.02
  options = []
  activeOptionIndex = 0

  def displayLogo(self):
    transformedLogo = pygame.transform.scale(self.logo, (screen.get_width() * 0.5, screen.get_width() * 0.5 / self.logo.get_width() * self.logo.get_height()))
    screen.blit(transformedLogo, (int(screen.get_width() / 2 - transformedLogo.get_width() / 2), int(screen.get_height() / 2 - self.fontSize - transformedLogo.get_height())))

  def displayText(self, text, index):
    color = self.hoverColor if index == self.activeOptionIndex else self.defaultColor

    text = self.font.render(text, True, color)
    text_rect = text.get_rect(center = (int(screen.get_width() / 2), int(screen.get_height() / 2 + (self.fontSize + self.margin) * index)))
    screen.blit(text, text_rect)

  def display(self):
    screen.fill('black')
    self.displayLogo()
    for i in range(len(self.options)):
      self.displayText(self.options[i], i)
