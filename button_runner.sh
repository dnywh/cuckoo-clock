#!/bin/bash

# Log start date and time of script
echo "$(date): Starting button_runner.sh" >> /home/pi/logs/button.log

# Wait 2–20 seconds for the audio device to be ready
sleep 10

# Activate the Pimoroni virtual environment
source /home/pi/.virtualenvs/pimoroni/bin/activate

# Navigate to the script directory
cd /home/pi/cuckoo-clock/



# Run the script in the background with nohup to prevent it from
# terminating when the terminal closes
nohup python button.py >> /home/pi/logs/button.log 2>&1 &

# If you're debugging (not ready to run on a schedule), try running the script
# That will give you logs
# I'm using a Raspberry Pi Model B+ v1.2 which needs to be prefaced with a revision number, like this:
# RPI_LGPIO_REVISION="900032" python button.py
# You can probably just run:
# python button.py

# Log the script execution
echo "$(date): Button handler started" >> /home/pi/logs/button.log

# Deactivate the virtual environment (good practice)
deactivate 
