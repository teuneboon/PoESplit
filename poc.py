import re

import tailer

log_file = 'C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/client.txt'


def parse(line):
    matches = re.match(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) (\d+) ([a-z0-9]+) \[([^]]+)\](.*)', line)
    if matches:
        print(matches.groups())
    else:
        print(line)


def main():
    for line in tailer.follow(open(log_file, encoding='utf-8')):
        parse(line)

if __name__ == '__main__':
    main()
