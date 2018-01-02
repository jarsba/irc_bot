#!/usr/bin/env python3
import socket
from config import *
import time
import threading
import select
import queue

master_server = MASTERSERVER[0]
master_channel = MASTERCHANNEL

class Bot():

    def __init__(self, server, master_sock, interval=1):
        self.interval = interval
        self.stop = False
        self.server = server
        self.botnick = "bot_" + server
        self.master_sock = master_sock
        self.nick = ''.join([random.choice(string.ascii_letters) for n in range(9)])
        self.print_envs()
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        self.join_server()
        # listen_thread = threading.Thread(target=self.listen, args=(self.sock,))
        # listen_thread.start()

    def print_envs(self):
        print("\n######## BOT CONFIG ########")
        print("BOT SERVER: " + self.server)
        print("BOT NICK: " + self.nick)
        print("############################\n")

    def join_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server, 6667))
        self.sock.send(bytes("USER " + self.nick + " " + self.nick + " " + self.nick + " " + self.nick + "\n","UTF-8"))
        self.sock.send(bytes("NICK " + self.nick + "\n", "UTF-8"))

    def listen(self, sock):
        while 1:
            time.sleep(0.2)
            ircmsg = ""
            while ircmsg.find("QUIT") == -1:
                ircmsg = sock.recv(2048).decode("UTF-8")
                buffer = ircmsg.split("\r\n")
                for line in buffer:
                    print(line)
                    line = line.split(" ")
                    if line[0] == "PING":
                        sock.send(bytes("PONG " + line[1] + "\r\n", "UTF-8"))

    def command(self, command):
        self.sock.send(bytes(command + "\n", "UTF-8"))
        resp = self.sock.recv(4096).decode("UTF-8")
        print(" ".join(resp))
        self.master_sock.send(bytes("PRIVMSG " + master_channel + " :" + "[" + self.botnick + "]: " + resp + "\r\n", "UTF-8"))

