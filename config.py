#!/usr/bin/env python3
import random
import string

MASTERSERVER=["chat.freenode.net"]
MASTERCHANNEL="#" + ''.join([random.choice(string.ascii_letters) for n in range(9)])
PORT=6667
SSL = False
BOTSERVERS=["irc.inet.fi" , "irc.​quakenet.​org", "irc.​as.​rizon.​net"]