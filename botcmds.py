if counter == 0:
    self.sendMsg(CHAN, "Loaded "+PLUGINFILE)
    counter += 1
else:
    pass

if message[0] == '!':
    commandMsg = (message.split(' ')[0])
    argMsg = (message.split(' ')[1:])
    argMsg2 = (message.split(' ')[1])

    if(commandMsg == "!help" and argMsg2 == "all" and username in MASTERS):
        x1 = "|----------------Actuall commands:--------------------|"
        x2 = "|!roll big - rolls a big integer----------------------|"
        x3 = "|!roll small - rolls small integer--------------------|"
        x4 = "|!kick <nick> - kicks <nick>--------------------------|"
        x5 = "|!mode <mode> <nick> - gives <mode> to nick (only op)-|"
        x6 = "|!say <something> - bot says <something>--------------|"
        x7 = "|!losuj <1stitem>, <2nditem>... - returns random item-|"
        x8 = "|!quit now - shutdown bot-----------------------------|"
        x9 = "If command has only one word, remember to add \"null\" at the end!"
        self.sendMsg(CHAN, x1)
        self.sendMsg(CHAN, x2)
        self.sendMsg(CHAN, x3)
        self.sendMsg(CHAN, x4)
        self.sendMsg(CHAN, x5)
        self.sendMsg(CHAN, x6)
        self.sendMsg(CHAN, x7)
        self.sendMsg(CHAN, x8)
        self.sendMsg(CHAN, x9)
    else:
        pass

    if(commandMsg == "!roll" and argMsg2 == "big"):
        x1 = int(strftime("%S", gmtime()))
        x2 = int(strftime("%Y", gmtime()))
        x = random.randint(1, x1*x2)
        self.sendMsg(CHAN, username+" rolled "+str(x))
    else:
        pass

    if(commandMsg == "!roll" and argMsg2 == "small"):
        x1 = int(strftime("%S", gmtime()))
        x = random.randint(1, x1)
        self.sendMsg(CHAN, username+" rolled "+str(x))
    else:
        pass

    if(commandMsg == "!kick" or commandMsg == "!kill" and username in MASTERS):
        sayMsg = ' '.join(argMsg)
        self.send("KICK "+CHAN+" "+sayMsg)
    else:
        pass

    if(commandMsg == "!mode" and username == TrueMaster):
        sayMsg = ' '.join(argMsg)
        self.send("MODE "+CHAN+" "+sayMsg)
    else:
        pass

    if(commandMsg == "!say" and username in MASTERS):
        sayMsg = ' '.join(argMsg)
        self.sendMsg(CHAN, sayMsg)
    else:
        pass

    if(commandMsg == "!quit" and argMsg2 == "now" and username in MASTERS):
        sys.exit()
    else:
        pass

    if(commandMsg == "!print" and argMsg2 == "MASTERS" and username in MASTERS):
        self.sendMsg(CHAN, str(MASTERS))
    else:
        pass

    if(commandMsg == "!losuj"):
        sayMsg = ' '.join(argMsg)
        y = random.choice(sayMsg.split(','))
        self.sendMsg(CHAN, y)
    else:
        pass

    '''if(commandMsg == "!faq"):
        self.send(values_dict[str(argMsg2)])
    else:
        pass'''

    if(commandMsg == "!exec" and username == TrueMaster):
        sayMsg = ' '.join(argMsg)
        if sayMsg == "sys.exit()":
            self.sendMsg(CHAN, "Bye")
            pass
        else:
            pass
        exec(sayMsg)
    else:
        pass
