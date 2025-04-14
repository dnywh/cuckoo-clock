#!/bin/bash

# Activate the Pimoroni virtual environment
source /home/pi/.virtualenvs/pimoroni/bin/activate

# Navigate to the script directory
cd /home/pi/cuckoo-clock/

# Run the script (no sudo needed)
# I'm using a Raspberry Pi Model B+ v1.2 which needs to be prefaced with a revision number
RPI_LGPIO_REVISION="900032" python button.py
# You can probably just run:
# python button.py

# Deactivate the virtual environment (good practice)
deactivate 
