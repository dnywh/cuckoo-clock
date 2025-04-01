# Cuckoo Clock Project

See also the [companion site](http://github.com/dnywh/cuckoo-clock-site). A [GitHub Action](https://github.com/dnywh/cuckoo-clock/blob/main/.github/workflows/sync-birds.yml) syncs bird data and imagery between the two repositories.

## Features

### Bird checks

After looking up which bird is currently active, Cuckoo Clock will check to see if that bird happens to already be rendered to the e-ink display. If it is, it'll skip the update. This helps unnecessary screen re-renders, which is especially important here given the short lifespan of e-ink displays.

I've set up `display_state.json` ahead of time to show you how this is structured. It assumes the `red-wattlebird` is currently active. Simply delete this file if you want to start afresh. Otherwise it will quietly be overriden as the clock goes through various birds.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setting up the environment

1. Clone the repository:

   ```
   git clone https://github.com/your-username/cuckoo-clock.git
   cd cuckoo-clock
   ```

2. (Optional) Create and activate a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required packages:

   ```
   pip install Pillow pygame
   ```

### Additional Setup for Raspberry Pi

If you're setting up on a Raspberry Pi, make sure you have the necessary hardware:

- E-ink display (Pimoroni Inky Impression)

I'm using a Pimoroni Inky Impression. You'll need to adapt the code to match your own e-ink display, if it differs.

The CRON schedule should match the quiet hours for each of the four seasons set out in [birds.json](birds.json).

### Running the Project

1. Ensure you have the `birds_data.json` file in the project directory.

2. Create a `birds` folder in the project directory with subfolders for each bird, containing the images (`.jpg`) and sound files (`.mp3`).

3. Run the script:

   ```
   python clock.py
   ```
