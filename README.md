# binaryclock

The code for a clock that displays the time in binairy.

The code is designed to run on a Raspberry Pi Zero. It gives outputs using the GPIO header.

## Installation
1. install RPi-GPIO

sudo apt-get install python-dev python-rpi.gpio

2. install git (if not installed)

sudo apt-get install git

3. clone repos

sudo git clone https://github.com/MAH313/binaryclock

## Configuration
A few settings and modules can be set in the config.ini file

1. brightness

the brightness settings control the brightness of the leds

  * default: int between 0 and 20; 0 = off, 20 = brightest; the default brightness. Is overwritten by any of the modules when they are active.

2. lightSensor

The settings for the optional lightsensor module. This overrides the default brightness

  * enabled: 'yes' or 'no'; if the light sensor module is enabled
  * pin1: int; the pin used for the first input
  * pin2: int; the pin used for the second input
  * level0: int between 0 and 20; 0 = off, 20 = brightest; the brightness for the lowest light level, active when none of the pins are active.
  * level1: int between 0 and 20; 0 = off, 20 = brightest; the brightness for mid light level, active when the first pin is active.
  * level2: int between 0 and 20; 0 = off, 20 = brightest; the brightness for highest light level, active when both pins are active.