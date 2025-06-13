#!/usr/bin/env python3
# Use this to clean up GPIO pins, if you end up switching between then throughout development
import RPi.GPIO as GPIO

print("Cleaning up all GPIO pins...")
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
print("Done.")
