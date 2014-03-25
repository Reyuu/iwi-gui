import sys, socket, random, string, time
import classesx1
execfile("configirc.ini")

readbuffer = ""
stateTrueLoop = True

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((HOST, PORT))
irc.send("NICK %s\r\n" % NICK)
irc.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
time.sleep(5)
irc.send("JOIN %s\r\n" % (JOIN))

while stateTrueLoop == True:
    try:
        irc.settimeout(TIMEOUTTIME)
        readbuffer = readbuffer + irc.recv(1024)
    except socket.timeout:
        print('Timeouted!')
        break
    except readbuffer == "":
        print('Where\'s data!')
        break
    except:
        print('I donno what happen')
        break

        
    if 'PING' in readbuffer:
        print("[*] [%H:%M:%S] Pinged and ponged", time.gmtime())
    temp = string.split(readbuffer, "\n")
    print(temp)
    for line in temp:
        try:
            line = string.rstrip(line)
            line = string.split(line)
            if(line[0] == "PING"):
                irc.send("PONG %s\r\n" % line[1])
        except:
            pass


