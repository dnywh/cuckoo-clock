#!/bin/bash

# Activate the Pimoroni virtual environment
source /home/pi/.virtualenvs/pimoroni/bin/activate

# Navigate to the script directory
cd /home/pi/cuckoo-clock/

# Run the script (no sudo needed)
python clear.py

# Deactivate the virtual environment (good practice)
deactivate 
