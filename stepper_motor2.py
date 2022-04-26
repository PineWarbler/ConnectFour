# modified from: https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/experiment-1-digital-input-and-output

# follow wiring according to: https://lastminuteengineers.b-cdn.net/wp-content/uploads/arduino/Wiring-Nema-17-Stepper-Motor-to-A4988-driver-Arduino.png

#def stepServo(dirPin, stepPin, dir, numPulses, pulseGap):
import time
import RPi.GPIO as GPIO

# top to bottom on RHS:
# green, red, yellow, blue

# according to the datasheet, step width should be at least 1 μs (1E-6 s) (page 6 of https://www.pololu.com/file/0J450/a4988_DMOS_microstepping_driver_with_translator.pdf)
pulseGap = 1E-4 # seconds between pulses.

dirPin = 17 # lowest left hand corner of a4988
stepPin = 27 # pin above dirPin
dir="clockwise"
numPulses=1000



# Suppress warnings
GPIO.setwarnings(False)

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

# Set pin states
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(stepPin, GPIO.OUT)


if dir=="clockwise":
    GPIO.output(dirPin, GPIO.HIGH) # set rotation direction; HIGH -> clockwise and LOW -> counterclockwise.
else:
    GPIO.output(dirPin, GPIO.LOW) # set rotation direction; HIGH -> clockwise and LOW -> counterclockwise.   

# now step the motor
for i in range(0, numPulses):
    GPIO.output(stepPin, GPIO.HIGH)
    time.sleep(pulseGap)
    GPIO.output(stepPin, GPIO.LOW)
    time.sleep(pulseGap)

GPIO.cleanup()
