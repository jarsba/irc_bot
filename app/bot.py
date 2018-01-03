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
        self.local_port = "NULL"
        self.nick = ''.join([random.choice(string.ascii_letters) for n in range(9)])
        self.print_envs()
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        self.join_server()
        self.add_master_socket()
        self.listen()

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
                cmd_msg = self.local_sock.recv(2048).decode("UTF-8")
                buffer = ircmsg.split("\r\n")
                cmd_buffer = cmd_msg.split("\r\n")
                for line in buffer:
                    print(line)
                    line = line.split(" ")
                    if line[0] == "PING":
                        sock.send(bytes("PONG " + line[1] + "\r\n", "UTF-8"))
                for line in cmd_buffer:
                    print(line)
                    if line[0] == "CMD:":
                        cmd = line[1] + line[2]
                        self.command(cmd)

    def command(self, command):
        self.sock.send(bytes(command + "\n", "UTF-8"))
        resp = self.sock.recv(4096).decode("UTF-8")
        print(" ".join(resp))
        self.master_sock.send(bytes("PRIVMSG " + master_channel + " :" + "[" + self.botnick + "]: " + resp + "\r\n", "UTF-8"))

    def add_master_socket(self):
        host = ""
        while 1:
            port = self.get_port()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.bind((host, port))
                self.local_port = port
                self.local_sock = s
                break;
            except socket.error as msg:
                print("Binding failed.")

        s.listen(5)

        while 1:
            conn, addr = s.accept()
            print('Connected with ' + addr[0] + ':' + str(addr[1]))

    def get_port(self):
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.local_port == "NULL":
            self.local_port = 1023
        # result == 0 equals free port
        result = 1
        while result != 0 and self.local_port < 65535:
            self.local_port = self.local_port + 1
            result = test_sock.connect_ex(("127.0.0.1" , self.local_port))
        print("PORT FOUND: " + str(self.local_port))
        return self.local_port

