#!/usr/bin/env python3
import socket
from app.bot import Bot
from config import *
import time
import threading
import select
import ssl

#ircsock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
server = MASTERSERVER[0]
channel = MASTERCHANNEL
masternick = MASTERNICK
bots = []
bot_socks = []


class CC():

    def __init__(self, interval=1):
        self.interval = interval
        self.stop = False
        print("STARTING C&C BOT")
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while not (self.stop):
            self.print_envs()
            self.join_server()
            self.create_channel()
            self.create_bots()
            time.sleep(15)
            self.connect_bot_sockets()
            self.listen()

    def print_envs(self):
        print("\n######### C&C CONFIG #########")
        print("C&C SERVER: " + server)
        print("C&C CHANNEL: " + channel)
        print("C&C MASTERNICK: " + masternick)
        print("##############################\n")

    def join_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server, 6667))
        self.sock.send(bytes("USER " + masternick + " " + masternick + " " + masternick + " " + masternick + "\n","UTF-8"))
        self.sock.send(bytes("NICK " + masternick + "\n", "UTF-8"))

    def create_channel(self):
        self.sock.send(bytes("JOIN "+ channel +"\n", "UTF-8"))

    def create_bots(self):
        for i, server in enumerate(BOTSERVERS):
            bot = Bot(server, self.sock)
            bots.append(bot)

    def listen(self):
        while 1:
            time.sleep(1)
            ircmsg = ""
            while ircmsg.find("QUIT") == -1:

                ircmsg = self.sock.recv(2048).decode("UTF-8")
                buffer = ircmsg.split("\r\n")
                if len(ircmsg) == 0:
                    print(masternick + " GOT TIMEOUT")
                for line in buffer:
                    print(line)
                    line = line.split(" ")
                    if line[0] == "PING":
                        self.sock.send(bytes("PONG " + line[1] + "\r\n", "UTF-8"))

                    if line[0] == "RESP:":
                        print("")

                    if line[0] == "CMD:":
                        print("")

                    if len(line) >= 4:
                        if line[1] == "PRIVMSG":
                            command = line[3][1:] + " " + line[4]
                            for bot in bots:
                                self.command(command)

    def connect_bot_sockets(self):
        for bot in bots:
            bot_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bot_sock.connect(("127.0.0.1", bot.local_port))
            bot_socks.append(bot_sock)

    def command(self, cmd):
        for bot_sock in bot_socks:
            print(cmd)
            bot_sock.send(bytes("CMD: " + cmd + "\n", "UTF-8"))
        self.listen()