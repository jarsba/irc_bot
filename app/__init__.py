#!/usr/bin/env python3
from app.bot import Bot
from config import *
import time
import sys

usage = "Usage: python3 run.py --master <masterserver> --servers <serverlist> --ssl \nGive commands with first word as 'cmd'\nExample: cmd whois jack"

print(usage)
# print(sys.argv)

if len(sys.argv) <= 6:
    for i, arg in enumerate(sys.argv):
        if arg.lower() == '--master':
            MASTERSERVER = sys.argv[i+1]
        elif arg.lower() == '--servers':
            BOTSERVERS = []
            with open(sys.argv[i+1]) as file:
                for line in file:
                    print(line)
                    BOTSERVERS.append(line.rstrip('\n'))
        elif arg.lower() == '--ssl':
            PORT = 6697
            SSL = True
else:
    print(usage)


def print_cc_info():
    print("\n######## C&C CONFIG ########")
    print("C&C SERVER: " + MASTERSERVER)
    print("C&C CHANNEL: " + MASTERCHANNEL)
    print("##############################\n")

# print(str(PORT) + " " + str(SSL))

def print_botservers():
    print("######## BOTSERVERS ########")
    for server in BOTSERVERS:
        print(server)
    print("##############################\n")

print_cc_info()
print_botservers()

for server in BOTSERVERS:
    bot = Bot(server)

while 1:
    time.sleep(1)

