#!/usr/bin/env python3
import socket
from config import *
import time
import threading
import re
import select
import ssl


class Bot():
    def __init__(self, server, interval=1):

        # Init some variables

        self.interval = interval
        self.stop = False
        self.server = server

        self.botnick = "bot_" + server

        # Servers random string nick, so name collision is not so likely

        self.nick = "".join([random.choice(string.ascii_lowercase) for n in range(9)])

        # Start new thread for bot

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while self.stop == False:
            self.print_envs()
            try:
                self.join_master_server()
            except:
                print("Could not connect to C&C server")
            try:
                self.join_host_server()
            except:
                print("Could not connect to " + self.server)

            self.listen()

    def print_envs(self):

        print("STARTING BOT...")

        print("\n######## BOT CONFIG ########")
        print("BOT SERVER: " + self.server)
        print("BOT NICK: " + self.nick)
        print("############################\n")

    def join_master_server(self):
        self.master_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if SSL:
            self.master_sock = ssl.wrap_socket(self.master_sock)

        try:
            self.master_sock.connect((MASTERSERVER, PORT))

        except:
            print("Connecting to " + MASTERSERVER + " failed, trying again in 5 seconds...")
            time.sleep(5)
            self.join_master_server()

        self.master_sock.send(
            bytes("USER " + self.nick + " " + self.nick + " " + self.nick + " " + self.nick + "\n",
                  "UTF-8"))
        self.master_sock.send(bytes("NICK " + self.nick + "\n", "UTF-8"))
        self.master_sock.send(bytes("JOIN " + MASTERCHANNEL + "\n", "UTF-8"))

    def join_host_server(self):
        self.host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if SSL:
            self.host_sock = ssl.wrap_socket(self.host_sock)

        try:
            self.host_sock.connect((self.server, PORT))
            print("CONNECTED TO " + self.server)

        except:
            print("Connecting to " + self.server + " failed, trying again in 5 seconds...")
            time.sleep(5)
            self.join_host_server()

        self.host_sock.send(
            bytes("USER " + self.nick + " " + self.nick + " " + self.nick + " " + self.nick + "\n", "UTF-8"))
        self.host_sock.send(bytes("NICK " + self.nick + "\n", "UTF-8"))

    # Mainloop where the magic happens

    def listen(self):

        # Listening both host and master servers, need to respond to PING on both servers

        while 1 and self.stop == False:
            msg = ""
            time.sleep(1)

            # Using select-library to manage socket statuses, otherwise answering takes a long time while in wait-loop
            try:
                readables, writables, exceptionals = select.select([self.master_sock], [self.master_sock],[self.master_sock])
            except:
                continue

            if len(readables) == 1:
                try:
                    msg = self.master_sock.recv(2048).decode("UTF-8")
                except:
                    print("Connection failed with C&C server")
                    self.join_master_server()
                    self.listen()

                # If message is empty, then connection could be detached

                if len(msg) > 0:
                    buffer = msg.split("\r\n")
                    for line in buffer:

                        # Uncomment if want to hear sockets
                        # print(line)

                        line = line.split(" ")
                        if line[0] == "PING":
                            self.send(self.master_sock, "PONG " + line[1])

                        if len(line) >= 4:

                            if line[1] == "PRIVMSG":

                                if line[3][1:].lower() == "quit":
                                    self.send(self.master_sock, "PRIVMSG " + MASTERCHANNEL + " :" + "[" + self.botnick + "]: " +  "quitting...")
                                    self.master_sock.close()
                                    self.host_sock.close()
                                    self.stop = True
                                    print(self.botnick +  " killing itself")

                                if line[3][1:].lower() == "cmd":
                                    command = line[4] + " " + line[5]

                                    # Could ask also universal command-function instead of
                                    # writing different functions for every command

                                    if line[4].lower() == "whois":
                                        self.whois(line[5])
                else:
                    print(self.server + " lost connection to C&C, connecting again...")
                    self.join_master_server()
                    self.listen()

            try:
                readables, writables, exceptionals = select.select([self.host_sock], [self.host_sock], [self.host_sock])
            except:
                continue

            if len(readables) == 1:
                try:
                    host_msg = self.host_sock.recv(2048).decode("UTF-8")
                except:
                    print("Connection failed with "+ self.server + " server")
                    self.join_host_server()
                    self.listen()

                # If message is empty, then connection could be detached

                if len(host_msg) > 0:
                    host_msg_buf = host_msg.split("\r\n")
                    for line in host_msg_buf:

                        # Uncomment if want to hear sockets
                        # print(line)

                        line = line.split(" ")
                        if line[0] == "PING":
                            self.send(self.host_sock, "PONG " + line[1])
                else:
                    print(self.server + " lost connection to " + self.server + ", connecting again...")
                    self.join_host_server()
                    self.listen()

    def whois(self, nick):
        msg_success = self.send(self.host_sock, "WHOIS " + nick)
        if msg_success:
            while True:
                resp = self.host_sock.recv(2048).decode("UTF-8")
                buffer = resp.split("\r\n")
                for line in buffer:
                    line = line.split(" ")
                    answer = " ".join(line[3:])
                    self.send(self.master_sock,
                              "PRIVMSG " + MASTERCHANNEL + " :" + "[" + self.botnick + "]: " + answer)
                    if len(line) >= 8:
                        if re.sub("[^a-z]+", "", "".join(line[4:]).lower()) == "endofwhoislist":
                            self.listen()

    def send(self, sock, msg):
        try:
            sock.send(bytes(msg + "\r\n", "UTF-8"))
            return True
        except:
            if sock
            print("Sending to " + str(sock.getsockname()) + " failed")
            return False

    def ping(self, sock):
        try:
            sock.send(bytes("PING" + "\r\n", "UTF-8"))
            return True
        except:
            print("Pingin " + str(sock.getsockname()) + " failed")
            return False

