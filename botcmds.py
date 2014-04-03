
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
        for item in (x1, x2, x3, x4, x5, x6, x7, x8, x9):
            self.sendMsg(CHAN, item)
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

    if(commandMsg == "!mode" and username is TrueMaster):
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
        self.sendMsg(CHAN, "Bye")
        import os
        os._exit(1)
    else:
        pass

    if(commandMsg == "!print" and argMsg2 == "MASTERS" and username in MASTERS):
        self.sendMsg(CHAN, str(MASTERS))
    else:
        pass

    if(commandMsg == "!losuj"):
        sayMsg = ' '.join(argMsg)
        y = random.choice(sayMsg.split(', '))
        self.sendMsg(CHAN, y)
    else:
        pass

    if(commandMsg == "!vs"):
        sayMsg = ' '.join(argMsg)
        y = random.choice(sayMsg.split(' vs '))
        yu = y[0].upper()+y[1:]
        self.sendMsg(CHAN, yu+" is better!")
    else:
        pass

    '''if(commandMsg == "!faq"):
        self.send(values_dict[str(argMsg2)])
    else:
        pass'''

    if (commandMsg == "!exec" and username is TrueMaster):
        sayMsg = ' '.join(argMsg)
        exec(sayMsg)
    else:
        pass
