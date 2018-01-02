#!/usr/bin/env python3
import random
import string
import select
import socket


MASTERSERVER=["chat.freenode.net"]
MASTERCHANNEL="#" + ''.join([random.choice(string.ascii_letters) for n in range(9)])
MASTERNICK=''.join([random.choice(string.ascii_letters) for n in range(9)])
PWD=''.join([random.choice(string.ascii_letters) for n in range(9)])

BOTSERVERS=["irc.inet.fi"]
#BOTSERVERS=["irc.inet.fi" , "irc.cc.tut.fi."]