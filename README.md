## PyBot

A small python3 program to listen C&C-servers commands and return commands output from host servers. Every bot is started on a new thread and every bot attaches itself to C&C server and host server.

### Running:

As default PyBot uses chat.freenode.net as masterserver, as hostservers irc.inet.fi and irc.​as.​rizon.​net and connections without SSL

> cd ~/path/to/program/folder

> python3 run.py --master <masterserver> --servers <serverlist> --ssl

PyBot prints you C&C-server's servername and C&C-channel where you can join and start giving commands.

You can give commands by starting the message with 'cmd' <command>

Example: cmd whois jack

PyBot supports only WHOIS-command at the moment

### Arguments:

--masterserver , optional

--servers , takes serverlist as text-file, one server per row, optional

--ssl , default without, optional

### Quitting:

Just say "QUIT" on C&C-channel and bots kill themselfs.