import pylab as P
from scipy import *


def freq_resp(w, H, \
              xlabel='$\\omega$ (rad./sec.)', \
              maglabel='Mag. Ratio.', \
              phaselabel='Phase (deg.)', \
              fignum=1, clear=True, \
              grid=False, deg=True, dB=False, \
              freqlim=None, **plot_kwargs):
    P.figure(fignum)
    if clear:
        P.clf()
    mag = abs(H)
    if dB:
        mag = 20*log10(mag)
    P.subplot(211)
    P.plot(w, mag, **plot_kwargs)
    P.grid(1)
    P.ylabel(maglabel)
    if freqlim is not None:
        P.xlim(freqlim)
    P.grid(bool(grid))
        
    if deg:
        phase = angle(H,1)
    else:
        phase = angle(H)

    P.subplot(212)
    P.plot(w, phase, **plot_kwargs)
    P.xlabel(xlabel)
    P.ylabel(phaselabel)
    
    if freqlim is not None:
        P.xlim(freqlim)
    P.grid(bool(grid))


#!/usr/bin/env python3

import os
import shutil
import time
from datetime import datetime, time as dt_time
from pathlib import Path

# Configuration
WATCH_FOLDER = "/path/to/master/folder"  # Update this path
DESTINATION_BASE = "/users/master"       # Update this path
EXPECTED_FOLDERS = ["folder1", "folder2", "folder3"]  # Update with your folder names
START_TIME = dt_time(3, 0)  # 3:00 AM
END_TIME = dt_time(12, 0)   # 12:00 PM (noon)
CHECK_INTERVAL = 300  # 5 minutes

def all_folders_present():
    """Check if all expected folders exist in the watch directory"""
    for folder_name in EXPECTED_FOLDERS:
        folder_path = os.path.join(WATCH_FOLDER, folder_name)
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return False
    return True

def copy_folders():
    """Copy all folders to destination with today's date"""
    today_date = datetime.now().strftime("%Y-%m-%d")
    destination = os.path.join(DESTINATION_BASE, today_date)
    
    # Create destination directory
    Path(destination).mkdir(parents=True, exist_ok=True)
    
    for folder_name in EXPECTED_FOLDERS:
        source = os.path.join(WATCH_FOLDER, folder_name)
        dest = os.path.join(destination, folder_name)
        
        print(f"Copying {folder_name}...")
        shutil.copytree(source, dest, dirs_exist_ok=True)
        print(f"Successfully copied {folder_name}")
    
    print(f"All folders copied to {destination}")

def main():
    """Main function to watch and copy folders"""
    print("Folder watcher started...")
    
    while True:
        current_time = datetime.now().time()
        
        # Check if we're within the active time window
        if START_TIME <= current_time <= END_TIME:
            print(f"Checking for folders at {datetime.now().strftime('%H:%M:%S')}...")
            
            if all_folders_present():
                print("All folders detected!")
                copy_folders()
                print("Script completed successfully. Exiting...")
                break
            else:
                missing = [f for f in EXPECTED_FOLDERS if not os.path.exists(os.path.join(WATCH_FOLDER, f))]
                print(f"Still waiting for folders: {missing}")
        else:
            print(f"Outside active hours ({START_TIME} - {END_TIME}). Current time: {current_time}")
        
        time.sleep(CHECK_INTERVAL)
