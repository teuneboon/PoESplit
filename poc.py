import re

import tailer
import os

log_file = 'C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/client.txt'


def put_on_clipboard(text):
    # WARNING, THIS IS THE HACKIEST SHIT EVER, I JUST WANTED TO MAKE IT WORK REAL QUICK, IF YOU HAVE A BETTER WAY PLZ
    # MAKE A PULL REQUEST
    os.system('echo {0} | clip'.format(text))


def parse(line):
    matches = re.match(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) (\d+) ([a-z0-9]+) \[([^]]+)\](.*)', line)
    if matches:
        timestamp = int(matches.group(2))
        info = matches.group(5).strip()
        if info.startswith('Got Instance Details'):
            event = 'LOADSCREEN_START'
        elif info.startswith('Entering area '):
            event = 'LOADSCREEN_STOP'
        else:
            event = None
        return timestamp, event
    else:
        print('WEIRD LINE: {0}'.format(line))
        return None, None


def main():
    total_loadscreen_time = 0
    last_loadscreen_start = None
    for line in tailer.follow(open(log_file, encoding='utf-8')):
        timestamp, event = parse(line)
        if event == 'LOADSCREEN_START':
            last_loadscreen_start = timestamp
        elif event == 'LOADSCREEN_STOP' and last_loadscreen_start is not None:
            total_loadscreen_time += timestamp - last_loadscreen_start
            last_loadscreen_start = None
            put_on_clipboard('My total loadscreen time so far: {0}ms'.format(total_loadscreen_time))
            print('Total loadscreen time: {0}'.format(total_loadscreen_time))

if __name__ == '__main__':
    main()
