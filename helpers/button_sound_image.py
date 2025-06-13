import sys
import pygame as pg
import os
import RPi.GPIO as GPIO
import time
import random
from PIL import Image, ImageDraw
from inky.auto import auto  # The Inky Impression driver


# Setup
# Display
inky_display = auto(
    ask_user=True, verbose=True
)  # Not sure if I need this, I could just hardcode the display

# Buttons
BUTTON_GPIO_PIN = 5
GPIO.setmode(GPIO.BCM)  # Use GPIO numbers (not pin numbers)
GPIO.setup(
    BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP
)  # Enable pull-up on GPIO 5

print("Welcome! Press the button to play a random bird sound, or CTRL+C to quit")

# Sounds
# Define the sound directory and file extension
SOUND_DIR = "sounds"  # Directory containing your sound files
SOUND_EXT = ".mp3"  # File extension for your sound files

# Fade settings
FADE_DURATION = 500  # 0.5 seconds for both fade in and out
FADE_STEPS = 50  # Number of steps for fade in
MAX_VOLUME = 0.5  # Maximum volume level (0.0 to 1.0)

# Track last played sound to avoid repeats
last_played = None


# Create new PIL image with a white background
image = Image.new("P", (inky_display.width, inky_display.height), inky_display.WHITE)
draw = ImageDraw.Draw(image)
# draw some shapes
draw.rectangle((50, 50, 200, 200), fill=inky_display.RED)  # Rectangle
draw.ellipse((150, 150, 300, 300), fill=inky_display.YELLOW)  # Circle (ellipse)
draw.line((0, 0, 400, 400), fill=inky_display.BLUE, width=10)  # Diagonal line
# Render to screen!
inky_display.set_image(image)
inky_display.show()


def get_sound_path(filename):
    """Get the full path to a sound file"""
    return os.path.join(SOUND_DIR, filename + SOUND_EXT)


def verify_sound_files():
    """Verify that all sound files exist and are accessible"""
    missing_files = []
    for sound_file in sound_files:
        full_path = get_sound_path(sound_file)
        if not os.path.exists(full_path):
            missing_files.append(full_path)

    if missing_files:
        print("Warning: The following sound files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    return True


def fade_in():
    """Gradually increase volume from 0 to MAX_VOLUME"""
    for i in range(FADE_STEPS + 1):
        volume = (i / FADE_STEPS) * MAX_VOLUME
        pg.mixer.music.set_volume(volume)
        time.sleep(FADE_DURATION / (FADE_STEPS * 1000))  # Convert ms to seconds


def play_music(music_file):
    """Play a sound file with fade in/out"""
    clock = pg.time.Clock()
    full_path = get_sound_path(music_file)

    try:
        pg.mixer.music.load(full_path)
        print("Music file {} loaded!".format(full_path))
    except pygame.error:
        print("File {} not found! {}".format(full_path, pg.get_error()))
        return False

    # Start with volume at 0
    pg.mixer.music.set_volume(0)
    pg.mixer.music.play()
    fade_in()

    # Check for button presses while sound is playing
    while pg.mixer.music.get_busy():
        if (
            GPIO.input(BUTTON_GPIO_PIN) == GPIO.LOW
        ):  # Button pressed while sound is playing
            print("Skipping current sound...")
            pg.mixer.music.fadeout(FADE_DURATION)
            time.sleep(0.3)  # Debounce delay
            return True  # Return True to indicate we should play a new sound
        clock.tick(30)

    return False  # Return False if sound played completely


# Initialize audio
freq = 44100  # audio CD quality
bitsize = -16  # unsigned 16 bit
channels = 2  # 1 is mono, 2 is stereo
buffer = 2048  # number of samples
pg.mixer.init(freq, bitsize, channels, buffer)
pg.mixer.music.set_volume(0)

# List of sound files
sound_files = ["XC171970", "XC269691", "XC287327", "XC375294", "XC716894", "XC717137"]

# Verify sound files before starting
if not verify_sound_files():
    print(
        "Please ensure all sound files are present in the '{}' directory".format(
            SOUND_DIR
        )
    )
    sys.exit(1)


def get_random_sound():
    """Get a random sound that's different from the last one played"""
    global last_played
    available_sounds = [s for s in sound_files if s != last_played]
    selected = random.choice(available_sounds)
    last_played = selected
    return selected


try:
    while True:
        if GPIO.input(BUTTON_GPIO_PIN) == GPIO.LOW:  # Button pressed (LOW = grounded)
            print("Pressed at:", time.strftime("%H:%M:%S"))
            selected_sound = get_random_sound()
            print(f"Selected sound: {selected_sound}")

            # Play the sound and check if it was skipped
            should_play_new = play_music(selected_sound)

            # If the sound was skipped, immediately play a new one
            while should_play_new:
                selected_sound = get_random_sound()
                print(f"Selected new sound: {selected_sound}")
                should_play_new = play_music(selected_sound)

            time.sleep(0.3)  # Simple debounce delay
except KeyboardInterrupt:
    GPIO.cleanup()
    pg.mixer.music.fadeout(FADE_DURATION)
    pg.mixer.music.stop()
    raise SystemExit
