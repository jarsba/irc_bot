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

        self.cmd_status = 0

        # Servers random string nick, so name collision is not so likely

        self.nick = "".join([random.choice(string.ascii_lowercase) for n in range(9)])

        # Start new thread for bot

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()


    def run(self):
        self.print_envs()
        try:
            self.join_master_server()
        except:
            print("Could not connect to master server")
        try:
            self.join_host_server()
        except:
            print("Could not connect to master server")
        self.listen()

    def print_envs(self):
        print("\n######## BOT CONFIG ########")
        print("BOT SERVER: " + self.server)
        print("BOT NICK: " + self.nick)
        print("############################\n")

    def join_master_server(self):
        self.master_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if SSL:
            self.master_sock = ssl.wrap_socket(self.master_sock)
        self.master_sock.connect((MASTERSERVER[0], PORT))
        self.master_sock.send(
            bytes("USER " + self.nick + " " + self.nick + " " + self.nick + " " + self.nick + "\n",
                  "UTF-8"))
        self.master_sock.send(bytes("NICK " + self.nick + "\n", "UTF-8"))
        self.master_sock.send(bytes("JOIN " + MASTERCHANNEL + "\n", "UTF-8"))

    def join_host_server(self):
        self.host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if SSL:
            self.host_sock = ssl.wrap_socket(self.host_sock)
        self.host_sock.connect((self.server, PORT))
        self.host_sock.send(
            bytes("USER " + self.nick + " " + self.nick + " " + self.nick + " " + self.nick + "\n", "UTF-8"))
        self.host_sock.send(bytes("NICK " + self.nick + "\n", "UTF-8"))


    def listen(self):

        # Listening both host and master servers, need to respond to PING on both servers

        while 1:
            msg = ""
            while msg.find("QUIT") == -1:
                time.sleep(0.2)

                # Using select-library to manage socket statuses, otherwise answering takes a long time while in wait-loop

                readables, writables, exceptionals = select.select([self.master_sock], [self.master_sock], [self.master_sock])
                if len(readables) == 1:
                    msg = self.master_sock.recv(2048).decode("UTF-8")
                    if len(msg) > 0:
                        buffer = msg.split("\r\n")
                        for line in buffer:
                            print(line)
                            line = line.split(" ")
                            if line[0] == "PING":
                                self.send(self.master_sock, "PONG " + line[1])

                            if len(line) >= 4:
                                if line[1] == "PRIVMSG":
                                    if line[3][1:].lower() == "cmd":
                                        print(self.botnick + " GOT COMMAND")
                                        command = line[4] + " " + line[5]

                                        # Could ask also universal command-function instead of
                                        # writing different functions for every command

                                        if line[4].lower() == "whois":
                                            self.whois(line[5])

                readables, writables, exceptionals = select.select([self.host_sock], [self.host_sock],
                                                                   [self.host_sock])
                if len(readables) == 1:
                    host_msg = self.host_sock.recv(2048).decode("UTF-8")
                    if len(host_msg) > 0:
                        host_msg_buf = host_msg.split("\r\n")
                        for line in host_msg_buf:
                            print(line)
                            line = line.split(" ")
                            if line[0] == "PING":
                                self.send(self.host_sock, "PONG " + line[1])

            self.stop = True

    def whois(self, nick):
        msg_success = self.send(self.host_sock, "WHOIS " + nick)
        if msg_success:
            answer = ""
            while True:
                resp = self.host_sock.recv(2048).decode("UTF-8")
                buffer = resp.split("\r\n")
                for line in buffer:
                    answer = answer + line + "\r\n"
                    line = line.split(" ")
                    if len(line) >= 8:
                        if re.sub("[^a-z]+","","".join(line[4:]).lower()) == "endofwhoislist":
                            self.master_sock.send(
                                bytes("PRIVMSG " + MASTERCHANNEL + " :" + "[" + self.botnick + "]: " + resp + "\r\n",
                                      "UTF-8"))
                            self.listen()

    def send(self, sock, msg):
        try:
            self.host_sock.send(bytes(msg + "\r\n", "UTF-8"))
            return True
        except:
            print("Sending to " + sock.gethostname() + " failed")
            return False

    def ping(self, sock):
        try:
            sock.send(bytes("PING" + "\r\n", "UTF-8"))
        except:
            print("")