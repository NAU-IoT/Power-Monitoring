#!/bin/bash

# Find the process ID (PID) of the running PowerMonitor script
pid=$(pgrep -f PowerMonitor.py)

# Kill the process if it is running
if [ -n "$pid" ]; then
  kill "$pid"
fi

python3 /PowerMonitor.py >> /Data/logs/PowerMonitor-`date '+%Y%m%d'`.log 2>&1
