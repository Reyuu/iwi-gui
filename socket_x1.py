import sys, socket, random, string, time, ConfigPraser
from time import gmtime, strftime
global HOST, PORT, NICK, IDENT, REALNAME, CHAN, TIMEOUTTIME, PING, PLUGINFILE, MASTERS, counter, TrueMaster
execfile("configirc.ini")
counter = 0
def print_date(msg):
    print strftime("[*] [%H:%M:%S] "+msg, gmtime())
class Irc:
    def __init__(self):
        self.onChannelMsg = 'Sup cunts.'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def send(self, msg):
        self.socket.send(msg + "\r\n")
    def sendMsg(self, chan, msg):
        self.socket.send('PRIVMSG '+chan+' :'+msg+'\r\n')
        print_date('[%s] to <%s>: %s' % (NICK, chan, msg))      
    def connect(self):
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
                        print_date("[%s] to <%s>: %s" % (username, channel, message))
                        execfile(PLUGINFILE)
                    else:
                        print ' '.join(line)
                except IndexError:
                    pass

IrcC = Irc()
IrcC.connect()
IrcC.whileSection()
sys.exit()
