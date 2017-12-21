## Design and implement an IRC based solution that fulfills the following requirements.


It is an IRC bot (or horde of bots) that consists of:

* Something listening for commands on an IRC server/channel specified in the configuration

* Is connected to n+1 IRC networks (specified in the configuration)


The idea is that you can perform the following task:

1) Use an IRC client to connect to the Command and Control channel

2) Issue a simple /whois <nick> query

3) Bots connected to the C&C channel will issue the whois query in their respective IRC network and return the answer

It could look something like this after the connection to the C&C channel:


> /whois nick

> [bot1@efnet]: No such nick.
> [bot2@ircnet]: No such nick.
> [bot3@quakenet]: No such nick.