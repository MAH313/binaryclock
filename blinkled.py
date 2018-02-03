"""code for the binary clock"""

__version__ = 0.2
__author__ = "Mark Hongerkamp <mark313@live.nl>"

from datetime import datetime
import math
import RPi.GPIO as GPIO

# Use board numbers, not GPIO numbers
GPIO.setmode(GPIO.BOARD)

#active pins
pins = [[8, 12, 18, 24, 29, 36],  #seconds
        [10, 16, 22, 26, 32, 38],  #minutes
        [3, 5, 7, 11, 13]]  #hours

#time offsets
secondOffset = 0
minuteOffset = 50
hourOffset = 0

# set up the GPIO channels
for i in xrange(0, len(pins)):
  for j in xrange(0, len(pins[i])):
    GPIO.setup(pins[i][j], GPIO.OUT)

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
  while True:
    #get the current amount of seconds
    date = datetime.now()
    seconds = int(date.strftime("%S"))+secondOffset
    minutes = int(date.strftime("%M"))+minuteOffset
    hours = int(date.strftime("%H"))+hourOffset

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

except KeyboardInterrupt:
  #clean and reset all gpio pins
  GPIO.cleanup()
  print 'Ended Program: keyboard interrupt'
