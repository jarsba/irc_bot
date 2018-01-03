## PyBot

A small python3 program to listen C&C-servers commands and return commands output from host servers. Every bot is started on a new thread and every bot attaches itself to C&C server and host server.

### Running:

As default PyBot uses chat.freenode.net as masterserver, as slaveservers irc.inet.fi , irc.​quakenet.​org and irc.​as.​rizon.​net and connections without SSL

> cd ~/path/to/program/folder

> python3 run.py --master <masterserver> --servers <serverlist> --ssl

PyBot prints you C&C-server's servername and C&C-channel where you can join and start giving commands.

### Arguments:

--masterserver

--servers , takes serverlist as text-file, one server per row

### Quitting:

Just say "QUIT" on C&C-channel and bots kill themselfs.