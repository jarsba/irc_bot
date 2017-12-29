#!/usr/bin/env python3
import socket
from app.bot import Bot
from config import *
import time
import threading

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = MASTERSERVER[0]
channel = MASTERCHANNEL
masternick = MASTERNICK
bots = []

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
            self.listen()

    def print_envs(self):
        print("##### C&C CONFIG #####")
        print("C&C SERVER: " + server)
        print("C&C CHANNEL: " + channel)
        print("C&C MASTERNICK: " + masternick)
        print("######################")

    def create_bots(self):
        for server in BOTSERVERS:
            bot = Bot(server, ''.join([random.choice(string.ascii_letters) for n in range(9)]))
            bots.append(bot)
            time.sleep(10)

    def join_server(self):
        ircsock.connect((server, 6667))
        ircsock.send(bytes("USER " + masternick + " " + masternick + " " + masternick + " " + masternick + "\n","UTF-8"))
        ircsock.send(bytes("NICK " + masternick + "\n", "UTF-8"))
        print("CONNECTED TO SERVER " + server + " WITH MASTERNICK " + masternick)
        time.sleep(3)

    def create_channel(self):
        ircsock.send(bytes("JOIN "+ channel +"\n", "UTF-8"))
        print("CREATED C&C CHANNEL " + channel)
        time.sleep(3)

    def command(msg, target = channel):
        ircsock.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))

    def listen(self):
        while 1:
            time.sleep(1)
            ircmsg = ""
            while ircmsg.find("QUIT") == -1:
                ircmsg = ircsock.recv(2048).decode("UTF-8")
                print(ircmsg)
                if(ircmsg.find("WHOIS") != -1):
                    print("WHOIS-QUERY MADE")
                    who = ircmsg.split(":")[2].split(" ")[1]
                    for bot in bots:
                        resp = bot.whois(who)
                        ircsock.send(bytes("PRIVMSG "+ channel +" :"+ bot.botnick + " says: " + resp + "\n", "UTF-8"))