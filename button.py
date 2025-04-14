#!/usr/bin/env python3
import os
import random
import json
import signal
import RPi.GPIO as GPIO
from pygame import mixer  # For sound playback


print(
    """button.py - Plays a sound when button 0 (A) is pressed.
"""
)


# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ["A", "B", "C", "D"]

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialise pygame mixer
mixer.init()


# TODO: This seems quite repetitive of clock.py, should
# we extract and share the logic between the two?
def get_current_bird():
    try:
        with open("display_state.json", "r") as f:
            state = json.load(f)
            return state.get("last_bird")
    except Exception as e:
        print(f"Error reading current bird: {e}")
        return None


def play_bird_sound(bird_name):
    print(f"Getting sound for {bird_name}")
    try:
        bird_dir = f"birds/{bird_name}"
        sound_files = [f for f in os.listdir(bird_dir) if f.endswith(".mp3")]
        sound_path = os.path.join(bird_dir, random.choice(sound_files))
        print(f"Playing random sound for {bird_name}")
        sound = mixer.Sound(sound_path)
        sound.play()
    except Exception as e:
        print(f"Error playing sound: {e}")


# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
# def handle_button(pin):
#     label = LABELS[BUTTONS.index(pin)]
#     print("Button press detected on pin: {} label: {}".format(pin, label))


def handle_button(pin):
    # Just allow the first button to be pressed for now
    if pin == BUTTONS[0]:
        current_bird = get_current_bird()
        if current_bird:
            play_bird_sound(current_bird)
        else:
            print("No bird is currently active")


# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

# Set up the button handler
# GPIO.add_event_detect(BUTTONS[0], GPIO.FALLING, handle_button, bouncetime=250)

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
# Keep the script running
signal.pause()
