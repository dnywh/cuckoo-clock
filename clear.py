#!/usr/bin/env python3

import time
import json
import os

from inky.auto import auto
from inky.inky_uc8159 import CLEAN

# State file for tracking last displayed bird
STATE_FILE = "display_state.json"

inky = auto(ask_user=True, verbose=True)

for _ in range(2):
    for y in range(inky.height - 1):
        for x in range(inky.width - 1):
            inky.set_pixel(x, y, CLEAN)

    inky.show()
    time.sleep(1.0)

# Clear the state file to ensure next morning's bird will be displayed
try:
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
        print(f"Cleared state file: {STATE_FILE}")
    else:
        print(f"State file {STATE_FILE} does not exist, nothing to clear")
except Exception as e:
    print(f"Error clearing state file: {e}")
