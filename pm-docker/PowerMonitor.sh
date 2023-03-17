#!/bin/bash

# cd /code/python/myapp
python3 /PowerMonitor.py >> /Data/logs/PowerMonitor-`date '+%Y%m%d'`.log 2>&1
