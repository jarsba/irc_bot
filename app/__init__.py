#!/usr/bin/env python3
from app.command_control import CC
from app.bot import Bot
from config import *
import random
import string
import time
import queue

command_control = CC()
while 1:
    time.sleep(1)