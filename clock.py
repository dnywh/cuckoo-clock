from PIL import Image
from inky.auto import auto

import json
from datetime import datetime, time


# Load the shared bird data
with open("bird-data.json", "r") as f:
    bird_data = json.load(f)


def parse_time(time_str):
    """Convert time string (HH:MM) to datetime.time object for comparison"""
    return datetime.strptime(time_str, "%H:%M").time()


def get_current_bird(current_datetime):
    current_month = current_datetime.month
    current_time = current_datetime.strftime("%H:%M")
    current_time_obj = parse_time(current_time)

    print(f"Current time: {current_time}")
    print(f"Current month: {current_month}")

    # Check if it's quiet hours
    quiet_hours = bird_data["quietHours"]
    quiet_start = parse_time(quiet_hours["start"])
    quiet_end = parse_time(quiet_hours["end"])

    # Handle quiet hours that span midnight (e.g., 20:00 to 05:00)
    if quiet_start > quiet_end:
        if current_time_obj >= quiet_start or current_time_obj < quiet_end:
            print("It's quiet hours!")
            return "quiet-hours", current_time
    else:
        if quiet_start <= current_time_obj < quiet_end:
            print("It's quiet hours!")
            return "quiet-hours", current_time

    # Get the birds for the current month
    month_birds = bird_data["months"][str(current_month)]

    # Find the bird whose time matches or is closest to the current time
    current_bird = None
    for bird_info in month_birds:
        bird_time = parse_time(bird_info["time"])
        if bird_time <= current_time_obj:
            current_bird = bird_info["bird"]
            print(f"Found bird for time {bird_info['time']}: {current_bird}")

    # If no bird found (current time is before first bird's time), use the last bird of the day
    if not current_bird:
        current_bird = month_birds[-1]["bird"]
        print(f"Using last bird of the day: {current_bird}")

    return current_bird


inky = auto(ask_user=True, verbose=True)


def prepare_image(image_path, target_width, target_height):
    # TODO: Clear display before wiping first?
    # Open the image
    image = Image.open(image_path)

    # Rotate image 90° anticlockwise for portrait orientation
    image = image.rotate(90, expand=True)

    # Calculate aspect ratios
    img_ratio = image.width / image.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        # Image is wider than the target ratio
        new_width = target_width
        new_height = int(target_width / img_ratio)
    else:
        # Image is taller than the target ratio
        new_height = target_height
        new_width = int(target_height * img_ratio)

    # Resize image maintaining aspect ratio
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a new white background image of target size
    final = Image.new("RGB", (target_width, target_height), "white")

    # Calculate position to paste resized image (centering it)
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2

    # Paste the resized image onto the white background
    final.paste(resized, (paste_x, paste_y))

    return final


# Get the display dimensions
display_width, display_height = inky.resolution

# Prepare the image
saturation = 0.5


# Run
if __name__ == "__main__":
    try:
        current_datetime = datetime.now()
        result = get_current_bird(current_datetime)
        print(f"Final result: {result}")

        # TODO: if the result bird is the same as what's currently rendered, don't update

        full_image_url = f"birds/{result}/{result}.jpg"
        processed_image = prepare_image(full_image_url, display_width, display_height)
        print(f"Displaying {result} on e-ink display")

        inky.set_image(processed_image, saturation=saturation)
    # TODO: Do we need this? See what Inky does on their example files
    # except TypeError:
    #     inky.set_image(processed_image)
    except Exception as e:
        print(f"Error: {e}")
    inky.show()
