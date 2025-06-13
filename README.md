# Cuckoo Clock

`clock.py` changes the bird via a CRON schedule. `button.py` plays a sound for the current bird whenever the button is pressed. `clear.py`. nicely wipes the e-ink display before sleep.

See also the [companion site](http://github.com/dnywh/cuckoo-clock-site). [GitHub Actions](https://github.com/dnywh/cuckoo-clock/blob/main/.github/workflows/sync-birds.yml) syncs bird data and imagery between the two repositories.

All of the sound and image files are in the public domain. The companion site’s [Colophon](https://clock.dannywhite.net/colophon) provides more information, including credits.

## Quick start

On your Raspberry Pi:

```bash
# Install Inky library for your Inky Impression display
source ~/.virtualenvs/pimoroni/bin/activate
cd inky
./install.sh

# Activate their venv
source ~/.virtualenvs/pimoroni/bin/activate

# Get the Cuckoo Clock going!
git clone https://github.com/dnywh/cuckoo-clock
cd cuckoo-clock
```

## Features

### Helpers

The [`helpers`](https://github.com/dnywh/cuckoo-clock/blob/main/simulator) directory contains some progressivesly-more involved helper and example files to help you go from your Mac, to just a button press, to button press and sound, to the whole shebang with image rendering on your Inky Impression display.

### Inky library

Follow [Pimoroni’s instructions](https://github.com/pimoroni/inky) for setting up your Inky display. The steps can be boiled down to:

```bash
python3 -m venv --system-site-packages $HOME/.virtualenvs/pimoroni
source ~/.virtualenvs/pimoroni/bin/activate
pip install inky
```

You may also need to manually enable I2C and SPI on your Rapsberry Pi.

Try running their example files before continuing.

### Schedule

You can (and should) set Cuckoo Clock up on a regular schedule via CRON. See the \_[crontab.example](https://github.com/dnywh/cuckoo-clock/blob/main/crontab.example) and [clock_runner.sh](https://github.com/dnywh/cuckoo-clock/blob/main/clock_runner.sh) file for what it might look like. Note that the CRON job(s) I've set up will automatically create logs for debugging.

First, install the Inky library and clone this repo onto your Pi, as described above. Then, create the logs directory (required for CRON logging):

```bash
# Create a logs directory (at the root level as you might use it for other stuff)
mkdir -p /home/pi/logs

# Set permissions for logs directory
chmod 755 /home/pi/logs

# Make the clock runner executable
chmod +x /home/pi/cuckoo-clock/clock_runner.sh

# Set up the CRON schedule
crontab -e
```

Paste in the contents from _crontab.example_ as a starting point.

You can test if the above works by running the following:

```bash
/home/pi/cuckoo-clock/clock_runner.sh >/home/pi/logs/cronlog.log 2>&1
```

You should hopefully see the bird of the hour appear on your Inky!

See my [Pi Frame documentation](https://github.com/dnywh/pi-frame?tab=readme-ov-file#scheduling) for more about scheduling.

#### Display maintenance

To prevent ghosting on the e-ink display, the `clear.py` script runs at the beginning of quiet hours (9pm) every day. This ensures the display gets a fresh refresh cycle before entering its overnight rest period. The script logs its output to `/home/pi/logs/clear.log` for debugging purposes.

Make sure both runner scripts are executable:

```bash
# This one is new and important:
chmod +x /home/pi/cuckoo-clock/clear_runner.sh

# We did this one before, but just in case you missed it:
chmod +x /home/pi/cuckoo-clock/clock_runner.sh
```

### Button controls

The clock supports physical button interaction to play bird sounds. This runs as a separate continuous process, started automatically on boot via CRON.

To set up the button handler:

1. Make the button runner executable, run:

   ```bash
   chmod +x /home/pi/cuckoo-clock/button_runner.sh
   ```

2. Install pygame for sound playback:

   ```bash
   source ~/.virtualenvs/pimoroni/bin/activate
   pip install pygame
   ```

3. Test the button handler:

   ```bash
   /home/pi/cuckoo-clock/button_runner.sh
   ```

Give it a minute to print that it’s ready. Then, after pressing your button, you should hear a bird chirp!

The button handler will automatically start on boot and log to `/home/pi/logs/button.log`. The `button.py` file assumes you have used what’s already set as `BUTTON_GPIO_PIN`, or that you’ve edited that value. If you want to use the built-in Inky button(s), check out the `helpers/inky_buttons.py` file.

### Bird checks

After looking up which bird is currently active, Cuckoo Clock will check to see if that bird happens to already be rendered to the e-ink display. If it is, it’ll skip the update. This helps unnecessary screen re-renders, which is important given the short lifespan of e-ink displays.

I’ve set up `display_state.json` ahead of time to show you how this is structured. It assumes the `red-wattlebird` is currently active. Simply delete this file if you want to start afresh. Otherwise it will quietly be overriden as the clock goes through various birds.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setting up the environment

1. Clone the repository:

   ```
   git clone https://github.com/dnywh/cuckoo-clock.git
   cd cuckoo-clock
   ```

2. Set up your virtual environment and install the required packages

3. Upload the entire repo to your Pi

### Setting up the environment

1. Clone the repository:

   ```
   git clone https://github.com/dnywh/cuckoo-clock.git
   cd cuckoo-clock
   ```

2. Create and activate a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required packages:

   ```
   pip install Pillow pygame
   ```

### Additional setup for Raspberry Pi

If you're setting up on a Raspberry Pi, make sure you have the necessary hardware:

- E-ink display (Pimoroni Inky Impression)
- Standard button

I'm using a Pimoroni Inky Impression. You'll need to adapt the code to match your own e-ink display, if it differs.

The CRON schedule should match the quiet hours for each of the four seasons set out in [schedule.json](schedule.json).

### Running the project

1. Ensure you have the `schedule.json` file in the project directory.

2. Create a `birds` folder in the project directory with subfolders for each bird, containing the images (`.jpg`) and sound files (`.mp3`).

3. Run the script:

   ```
   source ~/.virtualenvs/pimoroni/bin/activate
   python clock.py
   ```

## Colophon

You can find more information about how it all works on the [Colophon](https://clock.dannywhite.net/colophon) page.
