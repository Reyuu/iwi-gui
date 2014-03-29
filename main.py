import sys
import threading
from socket_x1 import *
global IrcC
IrcC = Irc()

class IrcThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        IrcC.connect()
        IrcC.whileSection()


class InputThreadIrc (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            try:
                self.line2 = sys.stdin.readline()
            except KeyboardInterrupt:
                break

            if(self.line2 == "QUIT"):
                sys.exit()

            elif not self.line2:
                break

            else:
                IrcC.logger.info(" ["+NICK+"] "+self.line2+" to "+CHAN+":")
                IrcC.sendMsg(CHAN, self.line2)

thread1 = IrcThread()
thread2 = InputThreadIrc()
thread2.daemon = 1

thread1.start()
thread2.start()

