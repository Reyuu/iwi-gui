#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, socket, random, string, time, logging, threading, ConfigParser
from time import gmtime, strftime
global HOST, PORT, NICK, IDENT, REALNAME, CHAN, TIMEOUTTIME, PING, PLUGINFILE, MASTERS, counter, TrueMaster, NoticeMsgOnChannelJoin, NoticeMsgOnChannelJoinOn, HighLight
global BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
global SELFCOLOR, PINGCOLOR, NORMALCOLOR, HIGHLIGHTCOLOR, JOINCOLOR, QUITCHANCOLOR, QUITSERVCOLOR

CHAN = '#polish'
counter = 0
def fetchSettings():
    config = ConfigParser.ConfigParser()
    config.read('configirc.ini')
    try:
        global HOST, PORT, NICK, IDENT, REALNAME, CHAN, TIMEOUTTIME, PING, PLUGINFILE, MASTERS, counter, TrueMaster, NoticeMsgOnChannelJoin, NoticeMsgOnChannelJoinOn, HighLight
        global BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, COLORS
        global SELFCOLOR, PINGCOLOR, NORMALCOLOR, HIGHLIGHTCOLOR, JOINCOLOR, QUITCHANCOLOR, QUITSERVCOLOR

        HOST = config.get('Server', 'Server')
        PORT = int(config.get('Server', 'Port'))
        CHAN = config.get('Server', 'Channel')

        NICK = config.get('Bot', 'Nick')
        IDENT = config.get('Bot', 'Ident')
        REALNAME = config.get('Bot', 'RealName')

        NoticeMsgOnChannelJoin = config.get('Messages', 'WelcomeMsg')
        NoticeMsgOnChannelJoinOn = config.get('Messages', 'WelcomeMsgActive')
        PING = config.get('Messages', 'OutputPing')
        HighLight = config.get('Messages', 'HighlightPhrases').split(',')

        TIMEOUTTIME = float(config.get('Settings', 'SocketDelay'))
        PLUGINFILE = config.get('Settings', 'PluginFile')
        TrueMaster = config.get('Settings', 'BotOwner')
        MASTERS = config.get('Settings', 'Masters').replace(' ', '').split(',')

        BLACK = config.get('Colors', 'Black')
        RED = config.get('Colors', 'Red')
        GREEN = config.get('Colors', 'Green')
        YELLOW = config.get('Colors', 'Yellow')
        BLUE = config.get('Colors', 'Blue')
        MAGENTA = config.get('Colors', 'Magenta')
        CYAN = config.get('Colors', 'Cyan')
        WHITE = config.get('Colors', 'White')
        COLORS = {'black':BLACK, 'red':RED, 'green':GREEN,
        'yellow':YELLOW, 'blue':BLUE, 'magenta': MAGENTA,
        'cyan':CYAN, 'white':WHITE}

        SELFCOLOR = config.get('TextColors', 'SelfColor')
        PINGCOLOR = config.get('TextColors', 'PingColor')
        NORMALCOLOR = config.get('TextColors', 'NormalColor')
        HIGHLIGHTCOLOR = config.get('TextColors', 'HighlightColor')
        JOINCOLOR = config.get('TextColors', 'JoinColor')
        QUITCHANCOLOR = config.get('TextColors', 'QuitChannelColor')
        QUITSERVCOLOR = config.get('TextColors', 'QuitServerColor')

    except:
            print "[!] Error have happened while fetching settings from configirc.ini!"
            sys.exit(1)

has_colours = False
def multi_detect(string, inputArray):
    for item in inputArray:
        if item in string:
            print '\a'
            return 1
    return 0

def print_date(pointer, msg, colour="", postfix="", colors={}):
    seq = strftime("[*] [%H:%M:%S] ", gmtime())
    if postfix:
        seq = seq + postfix
    pointer.pointer(seq, pointer.tex, colour=colour, newline=False, colors=colors)
    pointer.pointer(msg, pointer.tex, colors=colors)

class Irc:
    def __init__(self):
        self.onChannelMsg = 'hi'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lastHL = 'Null'
        self.variables, self.messages = {}, {}
        self.lastMessage = ['rey44', 'elo']
    def send(self, msg):
        self.socket.send(msg + "\r\n")
    def sendMsg(self, chan, msg):
        try:
            self.socket.send('PRIVMSG '+chan+' :'+unicode(msg)+'\r\n')
            print_date(self, msg, colour=SELFCOLOR, colors=COLORS, postfix='[%s] to <%s>: ' % (NICK, chan))
        except UnicodeEncodeError:
            a = u""
            for char in msg:
                try:
                    a += char.decode('ascii')
                except UnicodeEncodeError:
                    a += "?"
            self.socket.send('PRIVMSG '+chan+' :'+unicode(a)+'\r\n')
            print_date(self, a, colour=SELFCOLOR, colors=COLORS, postfix='[%s] to <%s>: ' % (NICK, chan))

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
                            print_date(self, "Pinged and ponged.", colour=PINGCOLOR, colors=COLORS)
                        else:
                            pass
                    if line[1] == "PRIVMSG":
                        channel = line[2]
                        message = (' '.join(line[3:]))[1:]
                        username = (line[0].split('!')[0])[1:]
                        hld = multi_detect(message, HighLight)
                        if hld:
                            self.lastHL = username
                        colour = {0:NORMALCOLOR, 1:HIGHLIGHTCOLOR}[(hld == True) or (channel == TrueMaster)]
                        print_date(self, message, colour=colour, postfix="[%s] to <%s>: " % (username, channel), colors=COLORS)
                        execfile(PLUGINFILE)
                    elif line[1] == "JOIN":
                        username = (line[0].split('!')[0])[1:]
                        if NoticeMsgOnChannelJoinOn == 1:
                            self.send("NOTICE "+username+" :"+NoticeMsgOnChannelJoin)
                        print_date(self, "", colour=JOINCOLOR, postfix="[%s] joined the channel <%s>" % (username, ' '.join(line[2:])[1:]), colors=COLORS)
                    elif line[1] == "QUIT":
                        username = (line[0].split('!')[0])[1:]
                        print_date(self, "", colour=QUITSERVCOLOR, postfix="[%s] has quit: %s" % (username, ' '.join(line[2:])[1:]), colors=COLORS)
                    elif line[1] == "PART":
                        username = (line[0].split('!')[0])[1:]
                        channel = line[2]
                        print_date(self, "", colour=QUITCHANCOLOR, postfix="[%s] leaves from <%s>" % (username, channel), colors=COLORS)
                    else:
                        print ' '.join(line)
                except IndexError:
                    pass

fetchSettings()


