#!/usr/bin/env python3
import os
import random
import json
import signal
import RPi.GPIO as GPIO
import pygame as pg
import time

print("button.py - Plays a sound when button is pressed.")

# Setup
BUTTON_GPIO_PIN = 5
GPIO.setmode(GPIO.BCM)  # Use GPIO numbers (not pin numbers)
GPIO.setup(
    BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP
)  # Enable pull-up on GPIO 5

# Fade settings
FADE_DURATION = 500  # 0.5 seconds for both fade in and out
FADE_STEPS = 50  # Number of steps for fade in
MAX_VOLUME = 0.5  # Maximum volume level (0.0 to 1.0)

# Track last played sound to avoid repeats
last_played = None

# Run a few attempts as a way to wait for the sound system to be ready
max_attempts = 20
for attempt in range(max_attempts):
    try:
        # Initialize with the same settings as button_sound.py
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 2048  # number of samples
        pg.mixer.init(freq, bitsize, channels, buffer)
        pg.mixer.music.set_volume(0)
        print("Successfully initialized audio")
        break
    except Exception as e:
        if attempt < max_attempts - 1:
            print(f"Audio init attempt {attempt + 1} failed, waiting 1 second...")
            time.sleep(1)
        else:
            print(f"Failed to initialize audio after {max_attempts} attempts: {e}")
            # Continue running for button detection, even if sound fails
            pass


def get_current_bird():
    try:
        with open("display_state.json", "r") as f:
            state = json.load(f)
            return state.get("last_bird")
    except Exception as e:
        print(f"Error reading current bird: {e}")
        return None


def fade_in():
    """Gradually increase volume from 0 to MAX_VOLUME"""
    for i in range(FADE_STEPS + 1):
        volume = (i / FADE_STEPS) * MAX_VOLUME
        pg.mixer.music.set_volume(volume)
        time.sleep(FADE_DURATION / (FADE_STEPS * 1000))  # Convert ms to seconds


def play_bird_sound(bird_name):
    print(f"Getting sound for {bird_name}")
    try:
        bird_dir = f"birds/{bird_name}"
        sound_files = [f for f in os.listdir(bird_dir) if f.endswith(".mp3")]
        if not sound_files:
            print(f"No sound files found for {bird_name}")
            return False

        sound_path = os.path.join(bird_dir, random.choice(sound_files))
        print(f"Playing sound: {sound_path}")

        # Start with volume at 0
        pg.mixer.music.load(sound_path)
        pg.mixer.music.set_volume(0)
        pg.mixer.music.play()
        fade_in()

        # Wait for sound to finish
        while pg.mixer.music.get_busy():
            if (
                GPIO.input(BUTTON_GPIO_PIN) == GPIO.LOW
            ):  # Button pressed while sound is playing
                print("Skipping current sound...")
                pg.mixer.music.fadeout(FADE_DURATION)
                time.sleep(0.3)  # Debounce delay
                return True  # Return True to indicate we should play a new sound
            time.sleep(0.1)

        return False
    except Exception as e:
        print(f"Error playing sound: {e}")
        return False


def handle_button(pin):
    if pin == BUTTON_GPIO_PIN:
        current_bird = get_current_bird()
        if current_bird:
            print(f"Button pressed at: {time.strftime('%H:%M:%S')}")
            should_play_new = play_bird_sound(current_bird)

            # If the sound was skipped, immediately play a new one
            while should_play_new:
                should_play_new = play_bird_sound(current_bird)

            time.sleep(0.3)  # Simple debounce delay
        else:
            print("No bird is currently active")


# Attach the button handler
GPIO.add_event_detect(BUTTON_GPIO_PIN, GPIO.FALLING, handle_button, bouncetime=250)

# Keep the script running
signal.pause()
