#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, socket, random, string, time, logging, threading, ConfigParser, os
from time import gmtime, strftime
global HOST, PORT, NICK, IDENT, REALNAME, CHAN, TIMEOUTTIME, PING, PLUGINFILE, MASTERS, counter, TrueMaster, NOTICEMSGONCHANNELJOIN, NOTICEMSGONCHANNELJOINON, HIGHLIGHT
global SELFCOLOR, PINGCOLOR, NORMALCOLOR, HIGHLIGHTCOLOR, JOINCOLOR, QUITCHANCOLOR, QUITSERVCOLOR, PASSWORD, QUITMSGON, JOINMSGON, USERSLIST, MOTDCOLOR, NOTIFILE, ERRORCOLOR
global OPACTIONSCOLOR, NOTICECOLOR

CHAN = '#polish'
counter = 0
def fetchSettings():
    config = ConfigParser.ConfigParser()
    config.read('configirc.ini')
    try:
        global HOST, PORT, NICK, IDENT, REALNAME, CHAN, TIMEOUTTIME, PING, PLUGINFILE, MASTERS, counter, TrueMaster, NOTICEMSGONCHANNELJOIN, NOTICEMSGONCHANNELJOINON, HIGHLIGHT
        global SELFCOLOR, PINGCOLOR, NORMALCOLOR, HIGHLIGHTCOLOR, JOINCOLOR, QUITCHANCOLOR, QUITSERVCOLOR, PASSWORD, QUITMSGON, JOINMSGON, USERSLIST, MOTDCOLOR, NOTIFILE, ERRORCOLOR
        global OPACTIONSCOLOR, NOTICECOLOR

        HOST = config.get('Server', 'Server')
        PORT = int(config.get('Server', 'Port'))
        CHAN = config.get('Server', 'Channel')

        NICK = config.get('Bot', 'Nick')
        IDENT = config.get('Bot', 'Ident')
        REALNAME = config.get('Bot', 'RealName')

        NOTICEMSGONCHANNELJOIN = config.get('Messages', 'WelcomeMsg')
        NOTICEMSGONCHANNELJOINON = config.get('Messages', 'WelcomeMsgActive')
        PING = config.get('Messages', 'OutputPing')
        HIGHLIGHT = config.get('Messages', 'HighlightPhrases').split(',')

        TIMEOUTTIME = float(config.get('Settings', 'SocketDelay'))
        PLUGINFILE = config.get('Settings', 'PluginFile')
        TrueMaster = config.get('Settings', 'BotOwner')
        MASTERS = config.get('Settings', 'Masters').replace(' ', '').split(',')
        
        SELFCOLOR = config.get('TextColors', 'SelfColor')
        PINGCOLOR = config.get('TextColors', 'PingColor')
        NORMALCOLOR = config.get('TextColors', 'NormalColor')
        HIGHLIGHTCOLOR = config.get('TextColors', 'HighlightColor')
        JOINCOLOR = config.get('TextColors', 'JoinColor')
        QUITCHANCOLOR = config.get('TextColors', 'QuitChannelColor')
        QUITSERVCOLOR = config.get('TextColors', 'QuitServerColor')
        USERSLIST = config.get('TextColors', 'UsersListColor')
        MOTDCOLOR = config.get('TextColors', 'MotdColor')
        ERRORCOLOR = config.get('TextColors', 'ErrorColor')
        NOTICECOLOR = config.get('TextColors', 'NoticeColor')
        OPACTIONSCOLOR = config.get('TextColors', 'OpActionColor')

        QUITMSGON = int(config.get('Visuals', 'QuitMessagesOn'))
        JOINMSGON = int(config.get('Visuals', 'JoinMessagesOn'))
    except:
            print "[!] Error have happened while fetching settings from configirc.ini!"
            sys.exit(1)

    try:
        PASSWORD = config.get('Server', 'Password')
    except:
        PASSWORD = ''
    try:
        NOTIFILE = config.get('Settings', 'NotificationFile')
    except:
        NOTIFILE = ''
has_colours = False
def multi_detect(string, inputArray):
    for item in inputArray:
        if item in string:
            print '\a'
            return 1
    return 0

def print_date(pointer, msg, colour="", postfix=""):
    hour = int(strftime('%H', gmtime()))+2
    seq = strftime("[*] ["+str(hour)+":%M:%S] ", gmtime())
    if postfix:
        seq = seq + postfix
    pointer.pointer(seq, pointer.tex, colour=colour, newline=False)
    pointer.pointer(msg, pointer.tex)

class Irc:
    def __init__(self):
        self.onChannelMsg = 'hi'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lastHL = 'Null'
        self.variables, self.messages = {}, {}
        self.lastMessage = ['rey44', 'elo']
    def send(self, msg):
        self.socket.send(msg + u"\r\n")
    def sendMsg(self, chan, msg):
        paymsg = u'PRIVMSG %s :' % (chan,) + msg + u'\r\n'
        self.socket.send(paymsg.encode('utf-8'))
        print_date(self, msg.encode('utf-8'), colour=SELFCOLOR, postfix='[%s] to <%s>: ' % (NICK, chan))

    def connect(self):
        global CHAN
        #config_fetch()# just couldn't get it to work
        #logging section
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler('socket.log')
        self.formatter = logging.Formatter('[*] [%(asctime)s] %(message)s', datefmt='%H:%M:%S')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr) 
        self.logger.setLevel(logging.INFO)

        self.socket.connect((HOST, PORT))
        if PASSWORD:
            self.send("PASS "+PASSWORD)
        self.send("NICK %s" % NICK)
        self.send("USER %s %s bla :%s" % (IDENT, HOST, REALNAME))
        time.sleep(5)
        self.send("JOIN %s" % (CHAN))
        self.socket.settimeout(TIMEOUTTIME)
        time.sleep(2)
        self.sendMsg(CHAN, NOTICEMSGONCHANNELJOIN)
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
                            print_date(self, "Pinged and ponged.", colour=PINGCOLOR, )
                        else:
                            pass
                    elif line[1] == "PRIVMSG":
                        channel = line[2]
                        message = (' '.join(line[3:]))[1:]
                        username = (line[0].split('!')[0])[1:]
                        hld = multi_detect(message, HIGHLIGHT)
                        if hld:
                            self.lastHL = username
                        if hld or (channel == TrueMaster):
                            if NOTIFILE and os.name is 'nt':
                                import winsound
                                winsound.PlaySound(NOTIFILE, winsound.SND_FILENAME|winsound.SND_ASYNC)
                        colour = {0:NORMALCOLOR, 1:HIGHLIGHTCOLOR}[hld or (channel == TrueMaster)]
                        print_date(self, message, colour=colour, postfix="[%s] to <%s>: " % (username, channel), )
                        execfile(PLUGINFILE)
                    elif line[1] == "JOIN":
                        if JOINMSGON:
                            username = (line[0].split('!')[0])[1:]
                            if NOTICEMSGONCHANNELJOINON == 1:
                                self.send("NOTICE "+username+" :"+NOTICEMSGONCHANNELJOIN)
                            print_date(self, "", colour=JOINCOLOR, postfix="[%s] joined the channel <%s>" % (username, ' '.join(line[1:])[1:]), )
                    elif line[1] == "QUIT":
                        if QUITMSGON:
                            username = (line[0].split('!')[0])[1:]
                            print_date(self, "", colour=QUITSERVCOLOR, postfix="[%s] has quit: %s" % (username, ' '.join(line[2:])[1:]), )
                    elif line[1] == "PART":
                        if QUITMSGON:
                            username = (line[0].split('!')[0])[1:]
                            channel = line[2]
                            print_date(self, "", colour=QUITCHANCOLOR, postfix="[%s] leaves from <%s>" % (username, channel), )
                    elif line[1] == "KICK":
                        username_op = (line[0].split('!')[0])[1:]
                        username_kicked = line[3]
                        channel = line[2]
                        reason = ' '.join(line[4:])[1:]
                        msggg = "["+username_kicked+"] have been kicked from ["+channel+"] by <"+username_op+"> for: "
                        print_date(self, reason, colour=OPACTIONSCOLOR, postfix=msggg)
                    elif line[1] == '353': #list of users
                        channel = line[4]
                        users = ', '.join(line[5:])[1:]
                        print_date(self, "", colour=USERSLIST, postfix="["+channel+"] List of users: "+users)
                    elif line[1] == '332': #motd
                        channel = line[3]
                        motd = ' '.join(line[4:])[1:]
                        print_date(self, motd, colour=MOTDCOLOR, postfix="["+channel+"] Motd: ")
                    elif line[1] == '404': #error
                        reason = ' '.join(line[4:])[1:]
                        print_date(self, '', colour=ERRORCOLOR, postfix="Error: "+reason)
                    elif line[1] == '433': #nickname in use
                        reason = ' '.join(line[4:])[1:]
                        print_date(self, '', colour=ERRORCOLOR, postfix="Error: "+reason)
                    elif line[1] == '451':
                        reason = ' '.join(line[3:])[1:]
                        print_date(self, '', colour=NOTICECOLOR, postfix="Server Notice: "+reason)
                    else:
                        print ' '.join(line)
                except IndexError:
                    pass

fetchSettings()
