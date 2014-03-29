import sys
import os
import threading
import socket_x1
from socket_x1 import *
global IrcC, CHAN
IrcC = socket_x1.Irc()

class IrcThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        IrcC.connect()
        IrcC.whileSection()


class InputThreadIrc (threading.Thread):
    def __init__(self):
        global CHAN
        threading.Thread.__init__(self)
        socket_x1.fetchSettings()
        self.lastMessage = [CHAN, '']
        self.messages = {}
        self.variables = {}

    def run(self):
        global CHAN
        while 1:
            try:
                self.line2 = sys.stdin.readline()
            except KeyboardInterrupt:
                break
            execute, specialChan = True, CHAN
            if self.line2[0] == ':':
                inputArray = self.line2.replace('\n', '').split(' ')
                command = inputArray[0]
                command = command[1:]
                if command == 'q': # quit
                    os._exit(1)
                    break
                elif command == 'l': # last message, eventual append
                    self.line2 = self.lastMessage[1]
                    specialChan = self.lastMessage[0]
                    if len(inputArray) > 1:
                        self.line2 = self.line2 + ' ' + ' '.join(inputArray[1:])
                        self.line2 = self.line2.replace('\n', '')
                elif command == 'p': # private message to specified user/chan
                    specialChan = inputArray[1]
                    self.line2 = ' '.join(inputArray[2:])
                elif command == 'r': # raw input to server
                    execute = False
                    IrcC.send(' '.join(inputArray[1:]))
                elif command == 'j': # join to a channel
                    execute = False
                    IrcC.send('JOIN '+inputArray[1])
                elif command == 'ch': # changes channel
                    socket_x1.CHAN = inputArray[1]
                    CHAN = inputArray[1]
                    execute = False
                elif command == 'ms': # sets a message to reuse
                    self.messages[inputArray[1]] = ' '.join(inputArray[2:])
                    execute = False
                elif command == 'md': # displays a message
                    if inputArray[1] in self.messages:
                        self.line2 = self.messages[inputArray[1]]
                    else:
                        execute = False
                elif command == 'vs': # sets a variable
                    self.variables[inputArray[1]] = ' '.join(inputArray[2:])
                    execute = False
                elif command == 'v': # sends a message with variables
                    words = inputArray[1:]
                    new_msg = ''
                    for word in words:
                        if word[0] == '$':
                            if word[1:] in self.variables:
                                new_msg += self.variables[word[1:]]
                        else:
                            new_msg += word
                        new_msg += ' '
                    self.line2 = new_msg
            if execute:
                IrcC.logger.info(" ["+NICK+"] "+self.line2+" to "+specialChan+":")
                IrcC.sendMsg(specialChan, self.line2)
                self.lastMessage[1] = self.line2
                self.lastMessage[0] = specialChan

thread1 = IrcThread()
thread2 = InputThreadIrc()
thread2.daemon = 1

thread1.start()
thread2.start()

