"""code for the binary clock"""

__version__ = 0.1
__author__ = "Mark Hongerkamp <mark313@live.nl>"

from datetime import datetime
import math
import RPi.GPIO as GPIO

# Use pin numbers, not GPIO numbers
GPIO.setmode(GPIO.BOARD)

#active pins
pins = [7, 11, 13, 15, 16, 18]

#maximum value displayable, for testing
maxValue = math.pow(2, len(pins))

# set up the GPIO channels
for i in xrange(0, len(pins)):
  GPIO.setup(pins[i], GPIO.OUT)

def displayBinary(pinArray, value):
  """convert number value"""
  for i in xrange(len(pinArray)-1, -1, -1):
    if value >= (math.pow(2, i) or 1):
      GPIO.output(pinArray[i], True)
      value = value - math.pow(2, i)
    else:
      GPIO.output(pinArray[i], False)

#check for keyboardInterrupt
try:
  while True:
    #get the current amount of seconds
    date = datetime.now()
    seconds = int(date.strftime("%S"))
    minutes = int(date.strftime("%M"))
    hours = int(date.strftime("%H"))

    #convert seconds to binary display
    displayBinary(pins, seconds)

except KeyboardInterrupt:
  #clean and reset all gpio pins and outputs
  GPIO.cleanup()
  print 'Ended Program: keyboard interrupt'
