import sys, socket, random, string, time
from configirc import *

readbuffer = ""
stateTrueLoop = True

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((HOST, PORT))
irc.send("NICK %s\r\n" % NICK)
irc.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
time.sleep(5)
irc.send("JOIN %s\r\n" % (JOIN))

while stateTrueLoop == True:
    irc.settimeout(TIMEOUTTIME)
    readbuffer = readbuffer + irc.recv(1024)
    if 'PING' in readbuffer:
        print strftime("[*] [%H:%M:%S] Pinged and ponged", gmtime())
    temp = string.split(readbuffer, "\n")

    for line in temp:
        line = string.rstrip(line)
        line = string.split(line)
        if(line[0] == "PING"):
            irc.send("PONG %s\r\n" % line[1])


