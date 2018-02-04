"""code for the binary clock"""

__version__ = 1.2
__author__ = "Mark Hongerkamp <mark313@live.nl>"

from datetime import datetime
import time
import math
import json
import RPi.GPIO as GPIO

# Use board numbers, not GPIO numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#led pins
pins = [[8, 12, 18, 24, 29, 36],  #seconds
        [10, 16, 22, 26, 32, 38],  #minutes
        [3, 5, 7, 11, 13]]  #hours

# set up the GPIO channels
for i in xrange(0, len(pins)):
  for j in xrange(0, len(pins[i])):
    GPIO.setup(pins[i][j], GPIO.OUT)

#button pins
modePin = 19
setPin = 21

GPIO.setup(modePin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(setPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
modeDown = False
setDown = False
mode = "none"

SaveFile = "saveFile"

#time offsets
Offset = [0, 0]

try:
  with open(SaveFile, 'r') as F:
    Offset = json.load(F)
except IOError:
  pass

def displayBinary(pinArray, value):
  """convert number value"""
  for x in xrange(len(pinArray)-1, -1, -1):
    if value >= (math.pow(2, x) or 1):
      GPIO.output(pinArray[x], True)
      value = value - math.pow(2, x)
    else:
      GPIO.output(pinArray[x], False)

#check for keyboardInterrupt
try:
  #startup check
  date = datetime.now()
  print "start time is %s:%s:%s" % (int(date.strftime("%H"))+Offset[0], int(date.strftime("%M"))+Offset[1], date.strftime("%S"))

  for i in xrange(0, len(pins)):
    for j in xrange(0, len(pins[i])):
      GPIO.output(pins[i][j], True)

  time.sleep(1)

  #start displaying time
  while True:
    #get the current amount of seconds
    date = datetime.now()
    seconds = int(date.strftime("%S"))
    minutes = int(date.strftime("%M"))+Offset[1]
    hours = int(date.strftime("%H"))+Offset[0]

    if seconds > 59:
      minutes += 1
      seconds = seconds % 60
    if minutes > 59:
      hours += 1
      minutes = minutes % 60
    hours = hours % 24

    #convert seconds to binary display
    displayBinary(pins[0], seconds)
    displayBinary(pins[1], minutes)
    displayBinary(pins[2], hours)

    if GPIO.input(setPin) and not setDown:
      setDown = True
      if mode == "hour":
        Offset[0] = (Offset[0]+1)%24
      elif mode == "minute":
        Offset[1] = (Offset[1]+1)%60

      with open(SaveFile, 'w') as F:
        json.dump(Offset, F)
    elif not GPIO.input(setPin):
      setDown = False

    if GPIO.input(modePin) and not modeDown:
      modeDown = True
      if mode == "hour":
        mode = "minute"
      elif mode == "minute":
        mode = "none"
      else:
        mode = "hour"
      print "setting %s" % mode
    elif not GPIO.input(modePin):
      modeDown = False


except KeyboardInterrupt:
  #clean and reset all gpio pins
  GPIO.cleanup()
  print 'Ended Program: keyboard interrupt'
