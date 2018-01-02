#!/usr/bin/env python3
from app.command_control import CC
from app.bot import Bot
from config import *
import random
import string
import time
import queue

cmd_q = queue.Queue()
resp_q = queue.Queue()

command_control = CC()
time.sleep(10)

while 1:
    time.sleep(1)