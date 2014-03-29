import sys, threading
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
                line = sys.stdin.readline()
            except KeyboardInterrupt:
                break

            if(line == "QUIT"):
                sys.exit()

            elif not line:
                break

            else:
                IrcC.sendMsg(CHAN, line)

thread1 = IrcThread()
thread2 = InputThreadIrc()

thread1.start()
thread2.start()

