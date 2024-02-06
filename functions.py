# os 
import os
# screeninfo
from screeninfo import get_monitors
import pygame
import window
from re import sub
import json

getsCorrectPath = lambda pathToRootDirectory: f'{os.getcwd()}\{pathToRootDirectory}'

def getPrimaryMonitor():
  for monitor in get_monitors():
    if monitor.is_primary:
      return monitor

def transformImage(image, scale):
  return pygame.transform.scale(image, (window.screen.get_width() * scale, window.screen.get_width() * scale / image.get_width() * image.get_height()))

def convertToCammelCase(text):
  text = sub(r"(_|-)+", " ", text).title().replace(" ", "")
  return ''.join([text[0].lower(), text[1:]])

def readConfigJson():
  with open(getsCorrectPath('data\\config.json'), 'r') as file:
   data = json.loads(file.read())
  return data

def saveConfigJson(data):
  with open(getsCorrectPath('data\\config.json'), 'w') as file:
    file.write(json.dumps(data, indent=2))
