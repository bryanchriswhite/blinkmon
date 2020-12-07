#! /usr/bin/env python3

import time
from datetime import datetime, timedelta
import requests
import sys
import semver
from signal import signal, SIGINT, SIGTERM

from blink1.blink1 import Blink1

WARN_PING_DELAY = {'minutes': 3}
DEFAULT_FADE_DURATION = 250  # ms
FAST_FADE_DURATION = 150  # ms

b1 = Blink1()


def interrupt_handler(sig, frame):
    b1.fade_to_color(0, 'black')
    b1.close()
    sys.exit(1)


signal(SIGINT, interrupt_handler)
signal(SIGTERM, interrupt_handler)


def get_sno_stats():
    return requests.get('http://localhost:14002/api/sno').json()


# TODO: refactor
def updateRequired(currentVer):
    r = requests.get('https://version.storj.io')
    storagenode = r.json()['processes']['storagenode']
    minVer = semver.parse(storagenode['minimum']['version'])
    return semver.compare(currentVer, minVer) < 0


# TODO: refactor
def updateAvailable(current_ver):
    r = requests.get('https://version.storj.io')
    storagenode = r.json()['processes']['storagenode']
    suggested_ver = semver.parse(storagenode['suggested']['version'])
    return semver.compare(current_ver, suggested_ver) < 0


def blink_color(color, duration=DEFAULT_FADE_DURATION):
    b1.fade_to_color(duration, color)
    time.sleep(.5)
    b1.fade_to_color(duration, 'black')


def check_delay(last_pinged):
    delay = datetime.utcnow() - last_pinged
    if delay > timedelta(**WARN_PING_DELAY):
        b1.fade_to_rgb(FAST_FADE_DURATION, 255, 153, 0, 0)
        time.sleep(3)


def get_last_pinged(stats):
    return datetime.strptime(stats['lastPinged'][:19], '%Y-%m-%dT%H:%M:%S')


def check_version(currentVerStr):
    try:
        if updateRequired(currentVerStr):
            b1.fade_to_color(DEFAULT_FADE_DURATION, 'yellow')
        else:
            if updateAvailable(currentVerStr):
                blink_color('green')

    except requests.exceptions.ConnectionError:
        pass


def get_version_str(stats):
    return stats['version']


if __name__ == '__main__':
    while True:
        # Idle indicator
        blink_color('white')

        try:
            stats = get_sno_stats()

            # Ping delay indicator
            check_delay(get_last_pinged(stats))

            # Update available / required indicator
            check_version(get_version_str(stats))

        except requests.exceptions.ConnectionError:
            b1.fade_to_rgb(FAST_FADE_DURATION, 255, 0, 0, 1)
            b1.fade_to_rgb(FAST_FADE_DURATION, 255, 153, 0, 2)

        time.sleep(15)

# Low disk space (colored fg)
# Not up to date (blue bg)
# Last pinged too long ago (long colored pulse)
# Unreachable (flashing red/orange)
