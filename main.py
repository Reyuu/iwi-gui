# -*- coding: utf-8 -*-
import sys
import os
import threading
import socket_x1
from socket_x1 import *
import Tkinter as tk
import tkFont

global IrcC, count
count = 0
IrcC = socket_x1.Irc()

def cbc(idd, tex):
    return lambda : callback(idd, tex)

def callback(text, tex, colour='', newline=True):
    tex.insert(tk.END, str(text)+{0:'',1:'\n'}[newline])
    tex.see(tk.END) # Scroll if necessary
    if colour:
        highlight(tex, colour)

def highlight(tex, colour):
    global count
    idx = str(int(tex.index('end').split('.')[0]) - 1)+'.0'
    idx2 = str(int(tex.index('end').split('.')[0]) - 1)+'.end'
    tag = '__'+str(count)
    count += 1
    tex.tag_add(tag, idx, idx2)
    tex.tag_config(tag, foreground=colour)

def click(key):
    try:
        if ord(key.char) == 13: # enter
            text = E1.get()
            E1.delete(0, tk.END)
            execute, specialChan = True, socket_x1.CHAN
            IrcC.variables['hl'] = IrcC.lastHL
            IrcC.variables['lm'] = IrcC.lastMessage[1]
            if text[0] == ':':
                inputArray = text.replace('\n', '').split(' ')
                command = inputArray[0]
                command = command[1:]
                if command == 'q': # quit
                    os._exit(1)
                    return 0
                elif command == 'l': # last message, eventual append
                    text = IrcC.lastMessage[1]
                    specialChan = IrcC.lastMessage[0]
                    if len(inputArray) > 1:
                        text = text + ' ' + ' '.join(inputArray[1:])
                        text = text.replace('\n', '')
                elif command == 'p': # private message to specified user/chan
                    specialChan = inputArray[1]
                    text = ' '.join(inputArray[2:])
                elif command == 'r': # raw input to server
                    execute = False
                    IrcC.send(' '.join(inputArray[1:]))
                elif command == 'j': # join to a channel
                    execute = False
                    IrcC.send('JOIN '+inputArray[1])
                elif command == 'ch': # changes channel
                    socket_x1.socket_x1.CHAN = inputArray[1]
                    socket_x1.CHAN = inputArray[1]
                    execute = False
                elif command == 'ms': # sets a message to reuse
                    IrcC.messages[inputArray[1]] = ' '.join(inputArray[2:])
                    execute = False
                elif command == 'md': # displays a message
                    if inputArray[1] in IrcC.messages:
                        text = IrcC.messages[inputArray[1]]
                    else:
                        execute = False
                elif command == 'vs': # sets a variable
                    IrcC.variables[inputArray[1]] = ' '.join(inputArray[2:])
                    execute = False
                elif command == 'v': # sends a message with variables
                    words = inputArray[1:]
                    new_msg = ''
                    for word in words:
                        if word[0] == '$':
                            wording = word[1:].replace(',', '')
                            wording = wording.replace(':', '')
                            if wording in IrcC.variables:
                                new_msg += IrcC.variables[wording]
                            if word[-1] == ',':
                                new_msg += ','
                            elif word[-1] == ':':
                                new_msg += ':'
                        else:
                            new_msg += word
                        new_msg += ' '
                    text = new_msg
            if execute:
                IrcC.logger.info(" ["+NICK+"] "+text+" to "+specialChan+":")
                IrcC.sendMsg(specialChan, text)
                IrcC.lastMessage[1] = text
                IrcC.lastMessage[0] = specialChan
    except TypeError:
        pass


class IrcThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        IrcC.connect()
        IrcC.whileSection()

config = ConfigParser.ConfigParser()
config.read('configirc.ini')
bgtex = config.get('TextColors', 'LogsBackground')
fgtex = config.get('TextColors', 'LogsForeground')

e1bg = config.get('TextColors', 'InputBackground')
e1fg = config.get('TextColors', 'InputForeground')

title = config.get('Settings', 'TitleWindow')
arial = ("Arial", "10")

top = tk.Tk()
top.wm_title(title)
tex = tk.Text(master=top, width=80, height=23, font=arial, bg=bgtex, fg=fgtex)
tex.pack(side=tk.TOP)
bop = tk.Frame()
bop.pack(side=tk.BOTTOM)
E1 = tk.Entry(bop, bd=3, width=80, font=arial, bg=e1bg, fg=e1fg)
E1.bind("<Key>", click)
E1.pack()

IrcC.pointer = callback
IrcC.tex = tex

thread1 = IrcThread()
thread1.daemon = True
thread1.start()
arial = ("Arial", "10")

top.mainloop()

