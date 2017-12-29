#!/usr/bin/env python3
import random
import string

MASTERSERVER=["chat.freenode.net"]
MASTERCHANNEL="#" + ''.join([random.choice(string.ascii_letters) for n in range(9)])
MASTERNICK=''.join([random.choice(string.ascii_letters) for n in range(9)])
PWD=''.join([random.choice(string.ascii_letters) for n in range(9)])

BOTSERVERS=["efnet.port80.se", "port80a.se.quakenet.org"]

