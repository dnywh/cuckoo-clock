import json
import random
import time
import os
from datetime import datetime, timedelta
from PIL import Image  # Images, at least on macOS
import pygame  # Audio playback

# Conditional imports and setup
try:
    import RPi.GPIO as GPIO

    ON_RASPBERRY_PI = True
    # GPIO setup for buttons (only on Raspberry Pi)
    GPIO.setmode(GPIO.BCM)
    NEXT_BUTTON = 17
    PREV_BUTTON = 27
    SOUND_BUTTON = 22
    GPIO.setup(NEXT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PREV_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SOUND_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
except ImportError:
    ON_RASPBERRY_PI = False
    print("Running in development mode (not on Raspberry Pi)")

# Initialize pygame mixer for audio
pygame.mixer.init()

# Load the shared bird data
with open("bird_data.json", "r") as f:
    bird_data = json.load(f)

# Base path for the birds folder
BIRDS_FOLDER = "birds"


def load_image(bird_key):
    slug = bird_data["birds"][bird_key]["slug"]
    image_path = os.path.join(BIRDS_FOLDER, slug, f"{slug}.jpg")
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        print(f"Image not found for {bird_data['birds'][bird_key]['name']}")
        return None


def play_random_sound(bird_key):
    slug = bird_data["birds"][bird_key]["slug"]
    sound_folder = os.path.join(BIRDS_FOLDER, slug)
    sound_files = [f for f in os.listdir(sound_folder) if f.endswith(".mp3")]
    if sound_files:
        chosen_sound = random.choice(sound_files)
        sound_path = os.path.join(sound_folder, chosen_sound)
        try:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            print(f"Playing {chosen_sound} for {bird_data['birds'][bird_key]['name']}")
        except pygame.error as e:
            print(
                f"Error playing sound for {bird_data['birds'][bird_key]['name']}: {e}"
            )
    else:
        print(f"No sound files found for {bird_data['birds'][bird_key]['name']}")


def display_image(bird_key):
    image = load_image(bird_key)
    if image:
        if ON_RASPBERRY_PI:
            # Here you would send the image to your e-ink display
            # For example: display_eink(image)
            print(
                f"Displaying image for {bird_data['birds'][bird_key]['name']} on e-ink display"
            )
        else:
            # For development on Mac, just show the image using PIL
            image.show()
        print(f"Displaying image for {bird_data['birds'][bird_key]['name']}")
    else:
        print(f"Failed to display image for {bird_data['birds'][bird_key]['name']}")


def get_current_bird(current_datetime):
    current_month = current_datetime.month
    current_time = current_datetime.strftime("%H:%M")

    # Determine current season
    current_season = next(
        season
        for season, data in bird_data["seasons"].items()
        if current_month in data["months"]
    )

    # Check if it's quiet hours
    quiet_hours = bird_data["quietHours"][current_season]
    if quiet_hours["start"] <= current_time or current_time < quiet_hours["end"]:
        return "quiet-hours", current_season

    # Find the most recent bird for the current time
    scheduled_birds = {
        time: bird
        for bird, info in bird_data["birds"].items()
        for time in info["seasons"].get(current_season, [])
    }
    if not scheduled_birds:
        return "no-birds-scheduled", current_season

    most_recent_time = max(
        [time for time in scheduled_birds.keys() if time <= current_time]
    )
    current_bird = scheduled_birds[most_recent_time]

    return current_bird, current_season


def main():
    print("Bird Sound and Display Clock")
    if ON_RASPBERRY_PI:
        print("Press the 'Next' button to manually change to the next hour")
        print("Press the 'Prev' button to manually change to the previous hour")
        print("Press the 'Sound' button to play the current bird's sound")
    else:
        print("Press 'n' to manually change to the next hour")
        print("Press 'p' to manually change to the previous hour")
        print("Press 's' to play the current bird's sound")
        print("Press 'q' to quit")

    simulated_datetime = datetime.now()
    current_bird, current_season = get_current_bird(simulated_datetime)
    if current_bird != "quiet-hours" and current_bird != "no-birds-scheduled":
        display_image(current_bird)
    print(f"Current time: {simulated_datetime.strftime('%H:%M')} in {current_season}")
    print(
        f"Current bird: {bird_data['birds'][current_bird]['name'] if current_bird in bird_data['birds'] else current_bird}"
    )

    def handle_input(input_key):
        nonlocal simulated_datetime, current_bird, current_season
        if input_key in ["n", "next"]:
            simulated_datetime += timedelta(hours=1)
        elif input_key in ["p", "prev"]:
            simulated_datetime -= timedelta(hours=1)

        new_bird, new_season = get_current_bird(simulated_datetime)
        if new_bird != current_bird or new_season != current_season:
            current_bird = new_bird
            current_season = new_season
            if current_bird != "quiet-hours" and current_bird != "no-birds-scheduled":
                display_image(current_bird)
            print(
                f"Current time: {simulated_datetime.strftime('%H:%M')} - {current_season}"
            )
            print(
                f"Current bird: {bird_data['birds'][current_bird]['name'] if current_bird in bird_data['birds'] else current_bird}"
            )

        if input_key in ["s", "sound"]:
            if current_bird != "quiet-hours" and current_bird != "no-birds-scheduled":
                play_random_sound(current_bird)

    if ON_RASPBERRY_PI:

        def button_callback(channel):
            if channel == NEXT_BUTTON:
                handle_input("next")
            elif channel == PREV_BUTTON:
                handle_input("prev")
            elif channel == SOUND_BUTTON:
                handle_input("sound")

        GPIO.add_event_detect(
            NEXT_BUTTON, GPIO.FALLING, callback=button_callback, bouncetime=300
        )
        GPIO.add_event_detect(
            PREV_BUTTON, GPIO.FALLING, callback=button_callback, bouncetime=300
        )
        GPIO.add_event_detect(
            SOUND_BUTTON, GPIO.FALLING, callback=button_callback, bouncetime=300
        )

    try:
        while True:
            if not ON_RASPBERRY_PI:
                user_input = input("Enter command (n/p/s/q): ").lower()
                if user_input == "q":
                    break
                handle_input(user_input)

            if ON_RASPBERRY_PI:
                # On Raspberry Pi, we update the simulated time to match the real time
                simulated_datetime = datetime.now()
                new_bird, new_season = get_current_bird(simulated_datetime)
                if new_bird != current_bird or new_season != current_season:
                    current_bird = new_bird
                    current_season = new_season
                    if (
                        current_bird != "quiet-hours"
                        and current_bird != "no-birds-scheduled"
                    ):
                        display_image(current_bird)
                    print(
                        f"Current time: {simulated_datetime.strftime('%H:%M')} - {current_season}"
                    )
                    print(
                        f"Current bird: {bird_data['birds'][current_bird]['name'] if current_bird in bird_data['birds'] else current_bird}"
                    )
                time.sleep(30)  # Check every 30 seconds on Raspberry Pi
            else:
                time.sleep(1)  # Check every second in development mode
    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        if ON_RASPBERRY_PI:
            GPIO.cleanup()  # Clean up GPIO on program exit


if __name__ == "__main__":
    main()
