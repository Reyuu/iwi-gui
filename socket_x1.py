import sys, socket, random, string, time
global HOST, PORT, NICK, IDENT, REALNAME, CHAN, TIMEOUTTIME, PING
execfile("configirc.ini")
class Irc:
    def __init__(self):
        self.readbuffer = ""
        self.onChannelMsg = 'PRIVMSG %s :' % (CHAN)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self):
        self.socket.connect((HOST, PORT))
        self.socket.send("NICK %s\r\n" % NICK)
        self.socket.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
        time.sleep(5)
        self.socket.send("JOIN %s\r\n" % (CHAN))
        self.socket.settimeout(TIMEOUTTIME)
    def whileSection(self):
        while True:
            try:
                self.readbuffer = self.socket.recv(1024)
            except:
                self.readbuffer = ""
            self.temp = string.split(self.readbuffer, "\n")
            for self.line in self.temp:
                try:
                    self.line = string.rstrip(self.line)
                    self.line = string.split(self.line)
                    if(self.line[0] == "PING"):
                        self.socket.send("PONG %s\r\n" % self.line[1])
                        if(PING == 1):
                            print "Pinged and ponged"
                        else:
                            pass
                    print ' '.join(self.line)  # putting this at end of try;except clause because it crashes on empty lines
                except:
                    pass

IrcC = Irc()
IrcC.connect()
IrcC.whileSection()


