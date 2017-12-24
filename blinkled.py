import RPi.GPIO as GPIO
from datetime import datetime
import math

# Use pin numbers, not GPIO numbers
GPIO.setmode(GPIO.BOARD)

#active pins
pins = [7, 11, 13, 15, 16, 18]

#maximum value displayable, for testing
maxValue = math.pow(2, len(pins))

# set up the GPIO channels
for i in xrange(0, len(pins)):
  GPIO.setup(pins[i], GPIO.OUT)
 
#check for keyboardInterrupt
try:
  while True:
    #get the current amount of seconds
    date = datetime.now()
    sec = int(date.strftime("%S"))
    
    #convert seconds to binary display
    for i in xrange(len(pins)-1, -1, -1):
      if sec >= (math.pow(2,i) or 1):
        GPIO.output(pins[i], True)
        sec = sec - math.pow(2, i)
      else:
        GPIO.output(pins[i], False)

except (KeyboardInterrupt):
  #clean and reset all gpio pins and outputs
  GPIO.cleanup()
  print 'Ended Program: keyboard interrupt'
