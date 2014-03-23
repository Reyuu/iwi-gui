import socket, sys, random, string
from configirc import *

readbuffer = ""

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((HOST, PORT))
irc.send("NICK %s\r\n" % NICK)
irc.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
irc.send("JOIN %s\r\n" % (JOIN)

while True:
    readbuffer = readbuffer + irc.recv(1024)
    readbuffer = temp.pop( )
    for line in temp:
        line = string.rstrip(line)
        line = string.split(line)
        if(line[0] == "PING"):
            irc.send("PONG %s\r\n" % line[1])

