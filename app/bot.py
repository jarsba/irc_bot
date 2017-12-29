#!/usr/bin/env python3
import socket
from config import *
import time
import threading

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
master_server = MASTERSERVER[0]
master_channel = MASTERCHANNEL

class Bot():

    def __init__(self, server, nick, interval=1):
        self.interval = interval
        self.stop = False
        self.server = server
        self.botnick = "bot_" + server
        self.nick = nick
        self.print_envs()
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while not self.stop:
            #self.join_server()
            time.sleep(10)

    def print_envs(self):
        print("##### BOT CONFIG #####")
        print("BOT SERVER: " + self.server)
        print("BOT NICK: " + self.nick)
        print("######################")

    def join_server(self):
        server_sock.connect((self.server, 6667))
        server_sock.send(bytes("USER " + self.nick + " " + self.nick + " " + self.nick + " " + self.nick + "\n","UTF-8"))
        server_sock.send(bytes("NICK " + self.nick + "\n", "UTF-8"))
        print("BOT CONNECTED TO SERVER " + self.server + " WITH NICK " + self.nick )
        time.sleep(3)

    def whois(self, who):
        #server_sock.send(bytes("WHOIS" + who + "\n", "UTF-8"))
        #resp = server_sock.recv(2048).decode("UTF-8")
        return "not yet"

