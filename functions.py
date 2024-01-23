# os 
import os
# screeninfo
from screeninfo import get_monitors

getsCorrectPath = lambda pathToRootDirectory: f'{os.getcwd()}\{pathToRootDirectory}'

def getPrimaryMonitor():
  for monitor in get_monitors():
    if monitor.is_primary:
      return monitor
