#! /usr/bin/env python3

import time
from datetime import datetime, timedelta
import requests
import sys
from signal import signal, SIGINT, SIGTERM

from blink1.blink1 import Blink1

WARN_PING_DELAY = {'minutes': 3}

b1 = Blink1()

def interrupt_handler(sig, frame):
    b1.fade_to_color(0, 'black')
    b1.close()
    sys.exit(1)

signal(SIGINT, interrupt_handler)
signal(SIGTERM, interrupt_handler)

while True:
    b1.fade_to_color(250, 'white')
    time.sleep(.5)
    b1.fade_to_color(250, 'black')

    try:
        r = requests.get('http://localhost:14002/api/sno')
        #print(r)
        sno = r.json()
        lastPinged = datetime.strptime(sno['lastPinged'][:19], '%Y-%m-%dT%H:%M:%S')
        delay = datetime.utcnow() - lastPinged
        #print(delay)
        if delay > timedelta(**WARN_PING_DELAY):
            b1.fade_to_rgb(150, 255, 153, 0, 0)
        #print(lastPinged)
        #print('Up to date: ' + str(sno['upToDate']))
        #print('Last ping: ' + str(sno['lastPinged']))
        #print('Disk space available: ' + str(sno['diskSpace']['available']))
        #print('Disk space used: ' + str(sno['diskSpace']['used']))
    except requests.exceptions.ConnectionError:
        b1.fade_to_rgb(150, 255, 0, 0, 1)
        b1.fade_to_rgb(150, 255, 153, 0, 2)

    time.sleep(15)

# Low disk space (colored fg)
# Not up to date (blue bg)
# Last pinged too long ago (long colored pulse)
# Unreachable (flashing red/orange)
