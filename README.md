# Cuckoo Clock Project

See also the [companion site](http://github.com/dnywh/cuckoo-clock-site). A [GitHub Action](https://github.com/dnywh/cuckoo-clock/blob/main/.github/workflows/sync-birds.yml) syncs bird data and imagery between the two repositories.

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

   Note: If you're setting up on a Raspberry Pi, you'll also need to install RPi.GPIO:

   ```
   pip install RPi.GPIO
   ```

### Additional Setup for Raspberry Pi

If you're setting up on a Raspberry Pi, make sure you have the necessary hardware:

- E-ink display (specifics depend on your chosen model)
- Buttons connected to GPIO pins (as specified in the script)

You may need to install additional libraries specific to your e-ink display. Refer to the display manufacturer's documentation for details.

The CRON schedule should match the quiet hours for each of the four seasons set out in [birds.json](birds.json).

### Running the Project

1. Ensure you have the `birds_data.json` file in the project directory.

2. Create a `birds` folder in the project directory with subfolders for each bird, containing the images (`.jpg`) and sound files (`.mp3`).

3. Run the script:

   ```
   python clock.py
   ```

   - On Mac or non-Raspberry Pi systems, you can interact with the program using keyboard inputs:

     - 'n': Move to the next hour
     - 'p': Move to the previous hour
     - 's': Play the current bird's sound
     - 'q': Quit the program

   - On Raspberry Pi, the script will use GPIO buttons for interaction (once hardware is set up).

Note: The script automatically detects whether it's running on a Raspberry Pi or another system and adjusts its behavior accordingly.
