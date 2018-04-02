"""code for the binary clock"""

__version__ = 1.2
__author__ = "Mark Hongerkamp <mark313@live.nl>"

from datetime import datetime
import time
import math
import json
import ConfigParser
import RPi.GPIO as GPIO

#load the config
config = ConfigParser.ConfigParser()
config.read('/home/pi/binaryclock/config.ini')

# load all config settings
brightness = {
    'default': int(config.get('brightness', 'default'))
}
lightSensor = {
    'enabled': True if config.get('lightSensor', 'enabled') == 'yes' else False,
    'pin1': int(config.get('lightSensor', 'pin1')),
    'pin2': int(config.get('lightSensor', 'pin2')),
    'level0': int(config.get('lightSensor', 'level0')),
    'level1': int(config.get('lightSensor', 'level1')),
    'level2': int(config.get('lightSensor', 'level2'))
}


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

#button initialisation
GPIO.setup(modePin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(setPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
modeDown = False
setDown = False
mode = "none"

#lightsensor init
if lightSensor['enabled']:
  GPIO.setup(lightSensor['pin1'], GPIO.IN)
  GPIO.setup(lightSensor['pin2'], GPIO.IN)

#save file name
SaveFile = "saveFile"

#time offsets
Offset = [0, 0]

try:
  with open(SaveFile, 'r') as F:
    Offset = json.load(F)
except IOError:
  pass

def wait(ms):
  """wait for ms microseconds"""
  thatdate = datetime.now()
  while ms > 0:
    thisdate = datetime.now()
    ms = ms - ((thisdate - thatdate).microseconds/1000.0)
    thatdate = thisdate


def displayBinary(pinArray, value):
  """convert number value to the display"""
  for x in xrange(len(pinArray)-1, -1, -1):
    if value >= (math.pow(2, x) or 1):
      GPIO.output(pinArray[x], True)
      value = value - math.pow(2, x)
    else:
      GPIO.output(pinArray[x], False)

def displayOff(pinArray):
  """turns all pins in pinArray off"""
  for x in xrange(len(pinArray)-1, -1, -1):
    GPIO.output(pinArray[x], False)

#check for keyboardInterrupt
try:
  #startup check
  date = datetime.now()
  print "start time is %s:%s:%s" % (int(date.strftime("%H"))+Offset[0]%24,
                                    int(date.strftime("%M"))+Offset[1]%60,
                                    date.strftime("%S"))

  for i in xrange(0, len(pins)):
    for j in xrange(0, len(pins[i])):
      GPIO.output(pins[i][j], True)

  time.sleep(1)

  #start displaying time
  while True:
    #get the current amount of seconds, minutes and hours
    date = datetime.now()
    seconds = int(date.strftime("%S"))
    minutes = int(date.strftime("%M"))+Offset[1]
    hours = int(date.strftime("%H"))+Offset[0]

    if lightSensor['enabled']:
      if not GPIO.input(lightSensor['pin1']) and not GPIO.input(lightSensor['pin2']):
        PWMOnTime = lightSensor['level2']
      elif not GPIO.input(lightSensor['pin1']):
        PWMOnTime = lightSensor['level1']
      else:
        PWMOnTime = lightSensor['level0']
    else:
      PWMOnTime = brightness['default']

    if seconds > 59:
      minutes += 1
      seconds = seconds % 60
    if minutes > 59:
      hours += 1
      minutes = minutes % 60
    hours = hours % 24

    wait(20-PWMOnTime)

    if PWMOnTime > 0:
      # on
      displayBinary(pins[0], seconds)

      if mode != "minute" or not seconds%2:
        displayBinary(pins[1], minutes)
      elif seconds%2:
        displayOff(pins[1])

      if mode != "hour" or not seconds%2:
        displayBinary(pins[2], hours)
      elif seconds%2:
        displayOff(pins[2])

      wait(PWMOnTime)

    #off
    displayOff(pins[0])
    displayOff(pins[1])
    displayOff(pins[2])

    #setting functionality

    if GPIO.input(setPin) and GPIO.input(modePin):
      # ofset reset
      Offset = [0, 0]
      with open(SaveFile, 'w') as F:
          json.dump(Offset, F)
      print "offset reset"
    else:
      if GPIO.input(setPin) and not setDown:
        # ofset adding
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
        # mode switch
        modeDown = True
        if mode == "hour":
          mode = "minute"
        elif mode == "minute":
          mode = "none"
        else:
          mode = "hour"
      elif not GPIO.input(modePin):
        modeDown = False


except KeyboardInterrupt:
  #clean and reset all gpio pins
  GPIO.cleanup()
  print 'Ended Program: keyboard interrupt'
