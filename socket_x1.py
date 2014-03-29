#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, socket, random, string, time, logging, threading
from time import gmtime, strftime
execfile("configirc.ini")
global HOST, PORT, NICK, IDENT, REALNAME, CHAN, TIMEOUTTIME, PING, PLUGINFILE, MASTERS, counter, TrueMaster, NoticeMsgOnChannelJoin, NoticeMsgOnChannelJoinOn, HighLight

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
counter = 0
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)

def multi_detect(string, inputArray):
    for item in inputArray:
        if item in string:
            return 1
    return 0

def print_date(msg, colour=YELLOW):
    if has_colours:
        seq = "\x1b[1;%dm" % (30+colour) + strftime("[*] [%H:%M:%S] ",gmtime()) + "\x1b[0m"
        print seq+msg
    else:
        print strftime("[*] [%H:%M:%S] "+msg, gmtime()) 

class Irc:
    def __init__(self):
        self.onChannelMsg = 'Sup cunts.'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def send(self, msg):
        self.socket.send(msg + "\r\n")
    def sendMsg(self, chan, msg):
        self.socket.send('PRIVMSG '+chan+' :'+msg+'\r\n')
        print_date('[%s] to <%s>: %s' % (NICK, chan, msg), colour=GREEN)      
    def connect(self):
        #config_fetch()# just couldn't get it to work
        #logging section
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler('socket.log')
        self.formatter = logging.Formatter('[*] [%(asctime)s] %(message)s', datefmt='%H:%M:%S')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr) 
        self.logger.setLevel(logging.INFO)

        self.socket.connect((HOST, PORT))
        self.send("NICK %s" % NICK)
        self.send("USER %s %s bla :%s" % (IDENT, HOST, REALNAME))
        time.sleep(5)
        self.send("JOIN %s" % (CHAN))
        self.socket.settimeout(TIMEOUTTIME)
        time.sleep(2)
        self.send("PRIVMSG #polish :Joined. Hi.")
    def whileSection(self):
        while True:
            try:
                readbuffer = self.socket.recv(1024)
            except:
                readbuffer = ""
            temp = string.split(readbuffer, "\n")
            for line in temp:
                try:
                    if not line:
                        break
                    line = string.rstrip(line)
                    self.logger.info(str(line))
                    line = string.split(line)
                    if line[0] == "PING":
                        self.send("PONG %s" % line[1])
                        if PING:
                            print_date("Pinged and ponged.")
                        else:
                            pass
                    elif line[1] == "PRIVMSG":
                        channel = line[2]
                        message = (' '.join(line[3:]))[1:]
                        username = (line[0].split('!')[0])[1:]
                        hld = multi_detect(message, HighLight)
                        colour = {0:YELLOW, 1:RED}[(hld == True) or (channel == TrueMaster)]
                        print_date("[%s] to <%s>: %s" % (username, channel, message), colour=colour)
                        execfile(PLUGINFILE)
                    elif line[1] == "JOIN" and NoticeMsgOnChannelJoinOn == 1:
                        username = (line[0].split('!')[0])[1:]
                        self.send("NOTICE "+username+" :"+NoticeMsgOnChannelJoin)
                    else:
                        print ' '.join(line)
                except IndexError:
                    pass
